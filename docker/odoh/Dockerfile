# --- builder stage ---
FROM golang:1.24 AS builder
WORKDIR /work
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates \
  && rm -rf /var/lib/apt/lists/*
RUN git clone --depth=1 https://github.com/DNSCrypt/dnscrypt-proxy dnscrypt

WORKDIR /work/dnscrypt/dnscrypt-proxy
ENV CGO_ENABLED=0 GOOS=linux GOARCH=amd64
RUN go version \
 && go build -ldflags="-s -w" -mod=vendor -o /usr/local/bin/dnscrypt-proxy

# ---------- runtime: Ubuntu ----------
FROM ubuntu:latest

# Base packages
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
      tor vim netcat-traditional net-tools lsof \
      software-properties-common ca-certificates curl git \
    && rm -rf /var/lib/apt/lists/*

# Copy compiled dnscrypt-proxy from builder
COPY --from=builder /usr/local/bin/dnscrypt-proxy /usr/local/bin/
RUN mkdir -p /var/log/dnscrypt-proxy/

WORKDIR /etc/dnscrypt-proxy-src
COPY dnscrypt-proxy.toml .
COPY bootup.sh .

CMD ["./bootup.sh"]
