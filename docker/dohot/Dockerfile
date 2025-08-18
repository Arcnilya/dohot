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
      tor tor-geoipdb vim netcat-traditional net-tools lsof \
      software-properties-common ca-certificates curl git \
    && rm -rf /var/lib/apt/lists/*

# Python 3.11 (deadsnakes)
RUN add-apt-repository ppa:deadsnakes/ppa -y && apt-get update && \
    apt-get install -y --no-install-recommends python3.11 python3.11-venv python3.11-dev python3-pip && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 && \
    apt-get remove -y python3-cryptography || true && \
    rm -rf /var/lib/apt/lists/*

# Create and use a dedicated venv
RUN python3.11 -m venv /opt/venv
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apt-get update && apt-get install -y python3.11-distutils
RUN python -m pip install --upgrade pip setuptools wheel

RUN pip install --no-cache-dir stem carml

# Copy compiled dnscrypt-proxy from builder
COPY --from=builder /usr/local/bin/dnscrypt-proxy /usr/local/bin/
RUN mkdir -p /var/log/dnscrypt-proxy/

WORKDIR /etc/dnscrypt-proxy-src
COPY dnscrypt-proxy.toml .
COPY torrc_template /etc/tor/torrc
COPY relays.py .
COPY circuit_tracker.py .
COPY bootup.sh .

ENV ENTRY_NODES=
ENV MIDDLE_NODES=
ENV EXIT_NODES=
ENV EXCLUDE_NODES=
ENV HOPS=
ENV METHOD=

CMD ["./bootup.sh"]
