FROM ubuntu:latest
#SHELL ["/bin/bash", "-c"]

RUN apt update && apt upgrade -y
RUN apt install -y tor vim netcat-traditional net-tools #dnscrypt-proxy
RUN apt install -y software-properties-common

# Install python 3.11 for carl and stem
RUN add-apt-repository ppa:deadsnakes/ppa -y && apt update
RUN apt install -y python3.11 python3.11-venv python3.11-dev
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
RUN apt install -y python3-pip
RUN apt remove -y python3-cryptography
RUN pip install carml --break-system-packages
RUN pip install stem --break-system-packages
RUN apt install -y lsof

RUN apt install -y git golang
RUN rm -rf /var/lib/apt/lists/*

# Install dnscrypt-proxy from source
RUN mkdir -p /etc/dnscrypt-proxy-src
WORKDIR /etc/dnscrypt-proxy-src
RUN git clone --depth=1 https://github.com/DNSCrypt/dnscrypt-proxy src
ENV GOOS=linux
ENV GOARCH=amd64
RUN cd src/dnscrypt-proxy && go build -ldflags="-s -w" -mod vendor && cp /etc/dnscrypt-proxy-src/src/dnscrypt-proxy/dnscrypt-proxy /usr/local/bin/
RUN mkdir -p /var/log/dnscrypt-proxy/

ENV ENTRY_NODES=
ENV MIDDLE_NODES=
ENV EXIT_NODES=
ENV EXCLUDE_NODES=
ENV HOPS=
ENV METHOD=
WORKDIR /etc/dnscrypt-proxy
COPY dnscrypt-proxy.toml .
COPY torrc_template /etc/tor/torrc
COPY relays.py .
COPY circuit_tracker.py .
COPY bootup.sh .
CMD ["./bootup.sh"]
