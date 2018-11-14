FROM ubuntu:xenial

RUN apt-get update
RUN apt-get install build-essential -y
RUN apt-get install libpcre3 libpcre3-dbg libpcre3-dev build-essential libpcap-dev   \
                     libnet1-dev libyaml-0-2 libyaml-dev pkg-config zlib1g zlib1g-dev \
                     libcap-ng-dev libcap-ng0 make libmagic-dev libjansson-dev        \
                     libnss3-dev libgeoip-dev liblua5.1-dev libhiredis-dev -y
RUN apt-get install libnetfilter-queue-dev libnetfilter-queue1  \
                     libnetfilter-log-dev libnetfilter-log1      \
                     libnfnetlink-dev libnfnetlink0 -y
RUN apt-get install git autoconf ethtool tcpdump bridge-utils net-tools nano python python-yaml -y

RUN mkdir /suricata
ADD ./suricata/ /suricata

WORKDIR /suricata
RUN tar xvfz suricata-4.0.0.tar.gz

WORKDIR /suricata/suricata-4.0.0

RUN ./configure && make && ldconfig && make install-full && make clean && ldconfig

RUN cp /suricata/config/suricata-ids.yaml /usr/local/etc/suricata/

WORKDIR /suricata/config
RUN tar xvfz emerging.rules.tar.gz
RUN cp rules/* /usr/local/etc/suricata/rules/
RUN rm -rf rules

WORKDIR /suricata
RUN chmod +x start.sh

ENV IFIN input
ENV IFOUT output
ENV SON_EMU_CMD ./start.sh
# ENV SON_EMU_CMD_STOP ./my_stop_command

CMD /bin/bash

