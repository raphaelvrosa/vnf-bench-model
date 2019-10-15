.DEFAULT_GOAL := all

DOC_DIR := "doc"
PYBINDPLUGIN := $(shell python3 -c 'import pyangbind; import os; print("{}/plugin".format(os.path.dirname(pyangbind.__file__)))')

validate:
	# generate doc
	pyang vnf-pp.yang -f tree -o "$(DOC_DIR)/vnf-pp.tree"
	pyang vnf-pp.yang -f jstree -o "$(DOC_DIR)/vnf-pp.html"
	pyang vnf-pp.yang -f uml -o "$(DOC_DIR)/vnf-pp.uml"
	pyang vnf-pp.yang --ietf

build:
	# generate / compile python model
	pyang --plugindir $(PYBINDPLUGIN) -f pybind -o vnf_pp.py vnf-pp.yang

test:
	# test the example ped files against the model
	python3 -m pytest -s -v

all: validate build test

clean:
	rm doc/*