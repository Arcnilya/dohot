FROM ubuntu
#SHELL ["bin/bash", "-c"]

RUN apt update && apt upgrade -y
RUN apt install -y net-tools vim netcat-traditional curl build-essential pkg-config dnsutils

RUN mkdir /opt/odoh
ADD https://github.com/cloudflare/odoh-client-rs.git /opt/odoh
WORKDIR /opt/odoh
RUN sed -i '/^\[dependencies\]/a openssl = { version = "0.10", features = ["vendored"] }' Cargo.toml
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
ENV OPENSSL_NO_VENDOR=0
RUN cargo build --release
#RUN cargo run -- example.com AAAA

RUN rm -rf /var/lib/apt/lists/*
CMD ["sleep", "infinity"]
