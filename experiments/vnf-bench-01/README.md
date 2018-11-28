# Experimental Analysis of VNF-BD Informatio Model

The file "vnf-bd-002.yaml" defines the vnf-bd to perform the benchmarking tests with Suricata VNF defined as a docker container in docker-vnfs.

The tests were performed with tcpreplay playing two pcap files (small_flows.pcap and big_flows.pcap - available at https://tcpreplay.appneta.com/wiki/captures.html). 
The tests target the Suricata VNF running different configurations ("small_ruleset", "big_ruleset", "empty"), i.e., these parameters define the start.sh script setup that starts Suricata with small/big rules or does not start it (i.e., the empty case), as a reference ground truth test.

Added fields to the VNF-BD info model: node "entrypoint", and scenario "deployment". The first defines the script/program called in the node when it is started, and the second defines the fields orchestration (if true or false, needed or not), the plugin name to be used to interface the orchestrator component (e.g., containernet, OSM, ONAP), and entrypoint sets the interface (e.g., ip/http address) to reach the orchestrator.

Possibly, the node that defines the VNF Suricata also contains the field "configuration", which realizes the configuration it will load on startup. OBS: We need to review this field, because currently I used it to parse the entrypoint field (i.e., in the layout-002.yaml file check the field "vm_entrypoint", it receives a configuration parameter).

I also called another network_type named "E-Flow", it defines a direct path from (agent 1 -> SUT (VNF) -> agent 2) via two switches, programmed with simple flowentries (in_port -> out_port). This type of network can be used for back to back evaluations too (e.g., agent 1 -> SUT (VNF) -> agent 1).

In addition, I also defined the node vnf_id as type ["sut", "monitor"], because I am using this field to identify the role of each node in the topology scenario. In this case, there is the VNF SUT and also a monitor process inside the VNF to listen to the Suricata process logs/metrics. 


