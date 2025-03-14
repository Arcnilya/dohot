FROM ubuntu
RUN apt update && apt upgrade -y && apt install -y \
    vim netcat-traditional net-tools \
    git build-essential gcc make autoconf automake libtool \
    libssl-dev libldns-dev libck-dev libnghttp2-dev \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/DNS-OARC/dnsperf.git /opt/dnsperf
WORKDIR /opt/dnsperf
RUN ./autogen.sh
RUN ./configure
RUN make
RUN make install

ENTRYPOINT ["dnsperf"]
