FROM ubuntu:xenial
MAINTAINER manuel.peuster@uni-paderborn.de

RUN	apt-get update && apt-get install -y \
        git \
        build-essential \
        python-dev \
        python-pip \
	net-tools \
	iproute \
	inetutils-ping \
	curl \
	iperf3 \
	iperf \
	tcpreplay \
	bmon \
	nmap \
	python \
	python-yaml \
	siege \
	httperf \
        gettext \
        #httping \
	apache2-utils \
        hping3 \
	polygraph


RUN git clone https://github.com/flok99/httping.git
WORKDIR /httping/
RUN make install


WORKDIR /

ADD start.sh start.sh
RUN chmod +x start.sh

ADD stop.sh stop.sh
RUN chmod +x stop.sh

ADD process_iperf3_results.py process_iperf3_results.py
RUN chmod +x process_iperf3_results.py

ADD process_ab_results.py process_ab_results.py
RUN chmod +x process_ab_results.py

ADD process_boom_results.py process_boom_results.py
RUN chmod +x process_boom_results.py

ADD process_httping_results.py process_httping_results.py
RUN chmod +x process_httping_results.py

ADD log_intf_statistics.py log_intf_statistics.py

WORKDIR /

RUN git clone https://github.com/mpeuster/boom.git
WORKDIR /boom/
RUN pip install virtualenv
RUN python setup.py install

WORKDIR /

CMD /bin/bash

