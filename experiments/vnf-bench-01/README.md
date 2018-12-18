# Experimental Analysis of VNF-BD Information Model with Gym

This folder contains the files utilized in an exercise of the, ongoing work, VNF-BR information model with Gym. 

vnf-bd-001.yaml -- Contains the structure of the VNF Benchmarking Descriptor to be used by the Gym-Player component to extract the VNF Performance Profile of a VNF. The VNF-BD file details: the topology of the Gym components needed to perform the VNF-PP extraction; the settings required by each Agent-prober and Monitor-listener to respectively trigger a tcpreplay stimulus while monitoring the VNF docker container. 


layout-001.json -- Contains the parameters that will fulfill the VNF-BD fields, when parsed by the Gym-Player component. Notice this layout can contain any range of values for each field (e.g., lists).

vnf-br-001.json -- Contains both VNF-BD loaded according to the layout-001.json info, and the extracted VNF-PP detailing in each of its reports the inputs used to obtain its measurements. 

vnfpp_001_001.csv -- Contains all the VNF-PP extracted metrics according to the input parameters for the purposes of structured analysis.

vnfpp_001_001_500/501_series_listener_17.csv -- Contains the series of measurements that took place by the Monitor-listeners during each experimental test (e.g., in the layout defined, the docker container running the Suricata VNF was monitored by a listener in the cases of smallFlows.pcap and bigFlows.pcap stimulus).


## Tests Exercised with VNF-BD-001.yaml

The tests were performed with a tcpreplay prober playing two pcap files (small_flows.pcap and big_flows.pcap - available at https://tcpreplay.appneta.com/wiki/captures.html). 
The tests target the Suricata VNF running different configurations ("small_ruleset", "big_ruleset", "empty"), i.e., these parameters define the start.sh script setup that starts Suricata with small/big rules or does not start it (i.e., the empty case as a reference ground truth test).

Added fields to the VNF-BD info model: node "entrypoint", and scenario "deployment". The first defines the script/program called in the node when it is started, and the second defines the fields orchestration (if true or false, needed or not), the plugin name to be used to interface the orchestrator component (e.g., containernet, OSM, ONAP), and entrypoint sets the interface (e.g., ip/http address) to reach the orchestrator.

Possibly, the node that defines the VNF Suricata also contains the field "configuration", which realizes the configuration it will load on startup. OBS: We need to review this field, because currently I used it to parse the entrypoint field (i.e., in the layout-002.yaml file check the field "vm_entrypoint", it receives a configuration parameter).

In the layout-001.json the network_type field named "E-Flow" defines a direct path from (agent 1 -> SUT (VNF) -> agent 2) via two switches, programmed with simple flowentries (in_port -> out_port).

In addition, I also defined the node vnf_id as type ["sut", "monitor"], because I am using this field to identify the role of each node in the topology scenario. In this case, there is the VNF SUT and also a monitor process inside the VNF to listen to the Suricata process logs/metrics. 


