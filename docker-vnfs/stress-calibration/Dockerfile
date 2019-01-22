FROM ubuntu:xenial
LABEL maintainer="manuel.peuster@uni-paderborn.de"

RUN	apt-get update && apt-get install -y \
	net-tools \
	iproute \
	inetutils-ping \
	curl \
	stress

ADD ./stress /stress
WORKDIR /stress

RUN chmod +x start.sh
RUN chmod +x stop.sh

RUN mkdir /tngbench_share
CMD /bin/bash