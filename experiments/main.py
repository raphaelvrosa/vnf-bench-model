import logging
import gevent
import json

from gevent.queue import Empty, Queue


logger = logging.getLogger(__name__)

from topo import Experiment
from rest.server import WebServer
from rest.client import WebClient


class Playground:
    def __init__(self):
        self.exp_topo = None
        self.running = False
        self.clear()

    def start(self, run_id, msg):
        scenario = msg.get("scenario")
        instance = msg.get("instance")
        logger.info("received scenario %s", scenario)
        self.exp_topo = Experiment(instance, scenario)
        self.exp_topo.build()
        hosts_info = self.exp_topo.start()
        self.running = True
        logger.info("expo_topo running %s", self.running)
        logger.info("hosts info %s", hosts_info)
        ack = {
            'running': self.running,
            'instance': instance,
            'deploy': hosts_info,
        }
        return ack

    def stop(self):
        self.exp_topo.stop()
        self.running = False
        logger.info("expo_topo running %s", self.running)
        ack = {'running': self.running}
        return ack

    def alive(self):
        return self.running

    def clear(self):
        exp = Experiment(0, None)
        exp.mn_cleanup()
        logger.info("Experiments cleanup OK")


class Scenario:
    def __init__(self, url):
        self.handlers = {
            'post':self.post_handler,
            'put': self.put_handler,
            'delete': self.delete_handler,
        }
        self.server = WebServer(url, self.handlers)
        self.playground = Playground()
        self._ids = 0
        self.in_q = Queue()
        self.client = WebClient()

    def put_handler(self, msg):
        address, prefix, request, data = msg
        logger.info("put_handler - address %s, prefix %s, request %s",
                    address, prefix, request)
        self.in_q.put(data)
        return True, 'Ack'

    def delete_handler(self, msg):
        return False, 'Nack'

    def post_handler(self, msg):
        address, prefix, request, data = msg
        logger.info("post_handler - address %s, prefix %s, request %s",
                    address, prefix, request)
        self.in_q.put(data)
        return True, 'Ack'

    def handle(self, data):
        cmd = data.get("request")
        continuous = data.get("continuous")
        callback = data.get("callback")
        outputs = []
        built = Built()
        built.to(callback)
        logger.info("received msg: request %s, continuous %s, callback %s")
        if continuous:
            if self.playground.alive():
                self.playground.stop()
        if cmd == "start":
            start_info = self.playground.start(self._ids, data)
            built.set("ack", start_info)
            self._ids += 1
            outputs.append(built)
        elif cmd == "stop":
            if self.playground.alive():
                stop_info = self.playground.stop()
                built.set("ack", stop_info)
                outputs.append(built)
        else:
            logger.info("Handle no cmd in request data")
        return outputs

    def serve(self):
        _jobs = self._create_jobs()
        gevent.joinall(_jobs)

    def _create_jobs(self):
        web_server_thread = gevent.spawn(self.server.init)
        msgs_loop = gevent.spawn(self._process_msgs)
        jobs = [web_server_thread, msgs_loop]
        return jobs

    def send(self, url, data, method='post'):
        logger.info("sending msg to %s - data %s", url, data)
        answer = self.client.send_msg(method, url, data)
        return answer

    def exit(self, outputs):
        if outputs:
            for output in outputs:
                url = output.get_to()
                output_json = output.to_json()
                if url:
                    exit_reply = self.send(url, output_json)
                    logger.info("exit_reply %s", exit_reply)
                else:
                    logger.info("No callback provided for %s", output_json)
        else:
            logger.info("nothing to output")

    def _process_msgs(self):
        while True:
            try:
                data = self.in_q.get()
            except Empty:
                continue
            else:
                msg = json.loads(data)
                if msg:
                    outputs = self.handle(msg)
                    self.exit(outputs)
                else:
                    logger.info("could not parse data %s", data)


if __name__ == "__main__":
    url = "http://0.0.0.0:7878"
    sc = Scenario(url)
    sc.serve()
