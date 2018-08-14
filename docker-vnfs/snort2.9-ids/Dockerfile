FROM ubuntu:xenial

RUN apt-get update
RUN apt-get -y install build-essential libpcap-dev libpcre3-dev libdumbnet-dev bison flex ethtool
RUN apt-get install git tcpdump net-tools nano python python-yaml bridge-utils -y
RUN apt-get install -y zlib1g-dev liblzma-dev openssl libssl-dev autoconf libtool pkg-config

RUN mkdir /snort
ADD ./snort/ /snort

WORKDIR /snort/snort_src

RUN tar xvfz daq-2.0.6.tar.gz
WORKDIR /snort/snort_src/daq-2.0.6
RUN ./configure
RUN make
RUN make install

WORKDIR /snort/snort_src
RUN rm -rf daq-2.0.6
RUN tar xvfz nghttp2-1.17.0.tar.gz
WORKDIR /snort/snort_src/nghttp2-1.17.0
RUN autoreconf -i --force
RUN automake
RUN autoconf
RUN ./configure --enable-lib-only
RUN make
RUN make install

WORKDIR /snort/snort_src
RUN rm -rf nghttp2-1.17.0
RUN tar xvfz snort-2.9.9.0.tar.gz
WORKDIR /snort/snort_src/snort-2.9.9.0
RUN ./configure --enable-sourcefire --enable-perfprofiling --enable-ppm
RUN make
RUN make install
RUN ldconfig

RUN groupadd snort
RUN	useradd snort -r -s /sbin/nologin -c SNORT_IDS -g snort

RUN rm -rf /usr/sbin/snort
RUN ln -s /usr/local/bin/snort /usr/sbin/snort

RUN rm -rf /etc/snort
RUN mkdir /etc/snort
RUN mkdir /etc/snort/rules
RUN mkdir /etc/snort/rules/iplists
RUN mkdir /etc/snort/preproc_rules
RUN mkdir /etc/snort/so_rules

RUN rm -rf /usr/local/lib/snort_dynamicrules
RUN mkdir /usr/local/lib/snort_dynamicrules

RUN touch /etc/snort/rules/iplists/black_list.rules
RUN touch /etc/snort/rules/iplists/white_list.rules
RUN touch /etc/snort/rules/local.rules
RUN touch /etc/snort/sid-msg.map

RUN rm -rf /var/log/snort
RUN mkdir /var/log/snort
RUN mkdir /var/log/snort/archived_logs

RUN chmod -R 5775 /etc/snort
RUN chmod -R 5775 /var/log/snort
RUN chmod -R 5775 /var/log/snort/archived_logs
RUN chmod -R 5775 /etc/snort/so_rules
RUN chmod -R 5775 /usr/local/lib/snort_dynamicrules

RUN chown -R snort:snort /etc/snort
RUN chown -R snort:snort /var/log/snort
RUN chown -R snort:snort /usr/local/lib/snort_dynamicrules

WORKDIR /snort/etc
RUN cp *.conf* /etc/snort

# RUN cp *.map /etc/snort
# RUN cp *.dtd /etc/snort

WORKDIR /snort/snort_src/snort-2.9.9.0/src/dynamic-preprocessors/build/usr/local/lib/snort_dynamicpreprocessor
RUN cp * /usr/local/lib/snort_dynamicpreprocessor

WORKDIR /snort/snort_src
RUN rm -rf snort-2.9.9.0
RUN tar xvfz snortrules-snapshot-2990.tar.gz
RUN cp -r preproc_rules/* /etc/snort/preproc_rules/
RUN cp -r rules/* /etc/snort/rules/
RUN cp -r so_rules/* /etc/snort/so_rules/
RUN cp -r etc/* /etc/snort/
RUN rm -rf preproc_rules rules so_rules etc

WORKDIR /snort/etc
RUN cp /etc/snort/snort.conf /etc/snort/snort.conf.bak
RUN cp snort.conf /etc/snort/snort.conf

WORKDIR /snort

ENV IFIN input
ENV IFOUT output

CMD /bin/bash
