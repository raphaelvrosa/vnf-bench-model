.DEFAULT_GOAL := all

DOC_DIR := "doc"
PYBINDPLUGIN := $(shell python3 -c 'import pyangbind; import os; print("{}/plugin".format(os.path.dirname(pyangbind.__file__)))')

validate:
	# generate doc
	pyang vnf-bd.yang -f tree -o "$(DOC_DIR)/vnf-bd.tree"
	pyang vnf-bd.yang -f jstree -o "$(DOC_DIR)/vnf-bd.html"
	pyang vnf-bd.yang -f uml -o "$(DOC_DIR)/vnf-bd.uml"
	# finally validate - Not ready yet
	# pyang vnf-bd.yang --ietf

build:
	# generate / compile python model
	pyang --plugindir $(PYBINDPLUGIN) -f pybind -o vnf_bd.py vnf-bd.yang

test:
	# test the example ped files against the model
	python3 -m pytest -s -v

all: validate build test

clean:
	rm doc/*