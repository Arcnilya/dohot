FROM ubuntu:latest
#SHELL ["/bin/bash", "-c"]

RUN apt update && apt upgrade -y
RUN apt install -y vim net-tools git golang 
#RUN apt install -y software-properties-common

RUN mkdir -p /etc/dnscrypt-proxy-src
WORKDIR /etc/dnscrypt-proxy-src
RUN git clone --depth=1 https://github.com/DNSCrypt/dnscrypt-proxy src
ENV GOOS=linux
ENV GOARCH=amd64
RUN cd src/dnscrypt-proxy && go build -ldflags="-s -w" -mod vendor && cp /etc/dnscrypt-proxy-src/src/dnscrypt-proxy/dnscrypt-proxy /usr/local/bin/
RUN mkdir -p /var/log/dnscrypt-proxy/
#RUN echo "alias dnscrypt-proxy=/etc/dnscrypt-proxy-src/src/dnscrypt-proxy" >> $BASH_ENV 
WORKDIR /etc/dnscrypt-proxy
#COPY /etc/dnscrypt-proxy-src/src/dnscrypt-proxy/dnscrypt-proxy /usr/local/bin/
COPY dnscrypt-proxy.toml .
COPY bootup.sh .
CMD ["./bootup.sh"]
