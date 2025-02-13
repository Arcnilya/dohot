FROM ubuntu

RUN apt update && apt upgrade -y && apt install -y \
    vim \
    netcat-traditional \
    net-tools \
    tor \
    dnscrypt-proxy \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /etc/dnscrypt-proxy
COPY dnscrypt-proxy.toml .
COPY torrc/nordics /etc/tor/torrc
COPY getinfo.sh .
COPY bootup.sh .
CMD ["./bootup.sh"]
