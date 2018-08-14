FROM ubuntu:trusty
MAINTAINER manuel.peuster@uni-paderborn.de

# define interface names (should be the same as in VNFD)
ENV IFIN input
ENV IFOUT output

RUN apt-get update && apt-get install -y \
	iptables \
	arptables \
	ebtables \
	ethtool \
	bridge-utils \
	build-essential \
	libpcap-dev \
	libpcre3-dev \
	libdumbnet-dev \
	bison \
	flex \
	hwloc \
	libhwloc-dev \
	libluajit-5.1 \
	libluajit-5.1-dev \
	pkg-config \
	cmake \
	openssl \
	libssl-dev \
	python \
	python-pandas \
	python-yaml \
	nano \
	tcpdump \
	net-tools

ADD ./snort/ /snort

ADD snort/src/snort-3.0.0-a4 /snort3
ADD snort/src/daq-2.0.6 /daq

WORKDIR /daq
RUN ./configure
RUN make
RUN make install

WORKDIR /snort3
ENV snort_path=/snort3
ENV LUA_PATH=/snort3/include/snort/lua/\?.lua\;\;
ENV SNORT_LUA_PATH=/snort3/etc/snort/

RUN ./configure_cmake.sh --prefix=/snort3
WORKDIR /snort3/build
RUN make -j 8
RUN make install
RUN ln -s /snort3/conf /snort3/etc
RUN ldconfig

WORKDIR /snort3/build/src
ENV PATH /snort3/build/src:$PATH

ADD snort/start.sh start.sh
RUN chmod +x start.sh
ADD snort/stop.sh stop.sh
RUN chmod +x stop.sh
ADD snort/restart_snort.sh restart_snort.sh
RUN chmod +x restart_snort.sh
ADD snort/processresults.py processresults.py
RUN chmod +x processresults.py
ADD snort/snort.lua snort.lua
ADD snort/log_intf_statistics.py log_intf_statistics.py

CMD /bin/bash
