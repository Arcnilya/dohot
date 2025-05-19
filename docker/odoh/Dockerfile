FROM ubuntu
SHELL ["/bin/bash", "-c"]

RUN apt update && apt upgrade -y
RUN apt install -y vim netcat-traditional net-tools dnscrypt-proxy ca-certificates
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /etc/dnscrypt-proxy
COPY dnscrypt-proxy.toml .
COPY bootup.sh .
CMD ["./bootup.sh"]
