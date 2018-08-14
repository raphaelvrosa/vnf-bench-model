#!/usr/bin/python
from mininet.net import Containernet
from mininet.node import Controller, Docker, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Link
from mininet import clean

import os
import yaml
import shutil
import logging
import coloredlogs
import time
LOG = logging.getLogger(os.path.basename(__file__))
# experiment logs
coloredlogs.install(level="DEBUG")
# mininet logs
setLogLevel('info')
# others
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("docker").setLevel(logging.WARNING)


# wait between start scripts are triggered
TRIGGER_DELAY = 5


class Experiment:
    def __init__(self, run_id, name, parameter, cli_mode=False):
        self.run_id = run_id
        self.name = name
        self.scenario = parameter
        self.cli_mode = cli_mode
        self.net = None
        self.nodes = {}
        self.switches = {}
        self.containers = []
        # give status
        # LOG.info("Switch mode: %s" % str(self.switch_mode))
        LOG.debug("Scenario: %r" % self.scenario)
        self.topo_parsed = {}

    def __repr__(self):
        return "run_%s_%06d" % (str(self.name), self.run_id)

    def start(self):
        # split down experiments in small steps that can be overwritten subclasses
        self._create_network()
        self._add_containers()
        self._add_switches()
        self._add_links()
        self._start_network()
        self._trigger_container_scripts(cmd="./start.sh")
        if self.cli_mode:  # interactive mode vs. experiment mode
            CLI(self.net)
        LOG.info("Experiment %s running." % (self.run_id))
            # else:
        #     self._wait_experiment()

    def stop(self):
        # time.sleep(3)
        self._trigger_container_scripts(cmd="./stop.sh")
        self._stop_network()
        self.mn_cleanup()

    def mn_cleanup(self):
        # mininet cleanup
        clean.cleanup()

    def _create_network(self):
        self.net = Containernet(controller=Controller)
        self.net.addController('c0')
        LOG.info("Created network: %r" % self.net)

    def _add_containers(self):
        nodes = self.topo_parsed.get("nodes")
        self.add_nodes(nodes)

    def _add_switches(self):
        switches = self.topo_parsed.get("switches")
        self.add_switches(switches)

    def _add_links(self):
        links = self.topo_parsed.get("links")
        self.add_links(links)

    def _start_network(self):
        if self.net:
            self.net.start()
            LOG.info("Started network: %r" % self.net)

    def _trigger_container_scripts(self, cmd="./start.sh"):
        time.sleep(TRIGGER_DELAY)
        for c in self.containers:
            c.cmd(cmd)
            LOG.debug("Triggered %r in container %r" % (cmd, c))
            time.sleep(TRIGGER_DELAY)

    def _stop_network(self):
        if self.net:
            self.net.stop()
            LOG.info("Stopped network: %r" % self.net)

    def wait_experiment(self, wait_time):
        LOG.info("Experiment %s running. Waiting for %d seconds." % (self.run_id , wait_time))
        time.sleep(wait_time)
        LOG.info("Experiment done.")

    def _new_container(self, name, ip, image, cpu_cores=None, cpu_bw=None, mem=None, environment=None):
        """
        Helper method to create and configure a single container.
        """
        def calculate_cpu_cfs_values(cpu_bw):
            cpu_bw_p = 100000
            cpu_bw_q = int(cpu_bw_p*cpu_bw)
            return cpu_bw_p, cpu_bw_q

        # translate cpu_bw to period and quota
        cpu_bw_p, cpu_bw_q = calculate_cpu_cfs_values(cpu_bw)
        # create container
        c = self.net.addDocker(name,
           ip=ip,
           dimage=image,
           # volumes=[os.path.join(os.getcwd(), self.out_path) + "share_" + name + ":/mnt/share:rw"],
           cpu_period=cpu_bw_p,
           cpu_quota=cpu_bw_q,
           cpuset_cpus=cpu_cores,
           mem_limit=str(mem) + "m",
           environment=environment)
        # bookkeeping
        self.containers.append(c)
        LOG.debug("Started container: %r" % str(c))
        return c

    def _parse_topo(self, topo):
        topo_parsed = {}

        nodes = topo.get("nodes")
        links = topo.get("links")

        topo_parsed["nodes"] = {}
        for node in nodes:
            node_id = node.get("id")
            node_image = node.get("image")
            topo_parsed["nodes"][node_id] = {
                "image": node_image,
                "interfaces": {},
            }
            interfaces = node.get("connection_points")
            faces = {}
            for intf in interfaces:
                intf_id = intf.get("id")
                faces[intf_id] = intf
            topo_parsed["nodes"][node_id]["interfaces"] = faces

        topo_parsed["links"] = {}
        topo_parsed["switches"] = []

        for link in links:
            link_id = link.get("id")
            link_type = link.get("type")

            if link_type == "E-LAN":
                link_network = link.get("network")
                if link_network not in topo_parsed["switches"]:
                    topo_parsed["switches"].append(link_network)

                adjacencies = link.get("connection_points")

                link_id_num = 0
                for adj in adjacencies:
                    dst, dst_intf = adj.split(":")

                    params_dst = {}
                    if dst_intf in topo_parsed["nodes"][dst]["interfaces"]:
                        face = topo_parsed["nodes"][dst]["interfaces"].get(dst_intf)
                        params_dst["ip"] = face.get("address", "")

                        link_id_parsed = link_id + str(link_id_num)
                        topo_parsed["links"][link_id_parsed] = {
                        'type': link_type,
                        'src': link_network,
                        'dst': dst,
                        'intf_dst': dst_intf,
                        'params_dst': params_dst,
                    }
                    link_id_num += 1

            elif link_type == "E-Line":
                adjacencies = link.get("connection_points")
                src, src_inft = adjacencies[0].split(":")
                dst, dst_intf = adjacencies[1].split(":")

                params_dst = {}
                if dst_intf in topo_parsed["nodes"][dst]["interfaces"]:
                    face = topo_parsed["nodes"][dst]["interfaces"].get(dst_intf)
                    params_dst["ip"] = face.get("address", "")

                params_src = {}
                if src_inft in topo_parsed["nodes"][src]["interfaces"]:
                    face = topo_parsed["nodes"][src]["interfaces"].get(src_inft)
                    params_src["ip"] = face.get("address", "")

                topo_parsed["links"][link_id] = {
                    'type': link_type,
                    'src': src,
                    'intf_src': src_inft,
                    'dst': dst,
                    'intf_dst': dst_intf,
                    'params_src': params_src,
                    'params_dst': params_dst,
                }
            else:
                LOG.debug("unknown link type")

        return topo_parsed

    def _parse_requirements(self, topo, reqs):
        for req in reqs:
            req_id = req.get("id")
            req_res = req.get("resources")
            if req_id in topo["nodes"]:
                vcpus = req_res["cpu"]["vcpus"]
                mem = req_res["memory"]["size"]
                node_res = {
                    "cpu_bw": vcpus,
                    "mem": mem,
                }
                topo["nodes"][req_id].update(node_res)

    def build(self):
        topo = self.scenario.get("topology")
        topo_parsed = self._parse_topo(topo)
        reqs = self.scenario.get("requirements")
        self._parse_requirements(topo_parsed, reqs)
        self.topo_parsed = topo_parsed

    def add_nodes(self, nodes):
        for node_id, node in nodes.items():
            added_node = self._new_container(
                node_id,
                node.get("addr_input", None),
                node.get("image"),
                cpu_cores=node.get("cpu_cores", ''),
                cpu_bw=node.get("cpu_bw"),
                mem=node.get("mem"),
                environment=node.get("environment", None)
            )
            self.nodes[node_id] = added_node

    def add_switches(self, switches):
        for sw_name in switches:
            s = self.net.addSwitch(sw_name)
            self.switches[sw_name] = s

    def add_links(self, links):
        for link_id, link in links.items():
            link_type = link.get("type")
            if link_type == "E-LAN":
                src = link.get("src")
                dst = link.get("dst")
                intf_dst = link.get("intf_dst")
                params_dst = link.get("params_dst", {})
                src_node = self.switches.get(src)
                dst_node = self.nodes.get(dst)
                self.add_link_sw(src_node, dst_node, intf_dst, params_dst)

            if link_type == "E-Line":
                src = link.get("src")
                dst = link.get("dst")
                intf_src = link.get("intf_src")
                intf_dst = link.get("intf_dst")
                params_src = link.get("params_src", None)
                params_dst = link.get("params_dst", None)
                src_node = self. nodes.get(src)
                dst_node = self.nodes.get(dst)
                self.add_link_direct(src_node, dst_node, intf_src, intf_dst, params_src, params_dst)

    def add_link_sw(self, sw, dst, intf_dst, params_dst):
        LOG.info("adding link dst %s, intf_dst %s, params_dst %s", dst, intf_dst, params_dst)
        self.net.addLink(sw, dst,
                         intfName2=intf_dst, params2=params_dst)

    def add_link_direct(self, src, dst, intf_src, intf_dst, params_src, params_dst):
        self.net.addLink(src, dst,
                         intfName1=intf_src, intfName2=intf_dst,
                         params1=params_src, params2=params_dst)
