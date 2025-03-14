FROM ubuntu
SHELL ["/bin/bash", "-c"]

RUN apt update && apt upgrade -y
RUN apt install -y tor vim netcat-traditional net-tools dnscrypt-proxy
RUN apt install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa -y && apt update
RUN apt install -y python3.11 python3.11-venv python3.11-dev
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
RUN apt install -y python3-pip
RUN apt remove -y python3-cryptography
RUN pip install carml --break-system-packages
RUN pip install stem --break-system-packages
RUN rm -rf /var/lib/apt/lists/*

ENV ENTRY_NODES=
ENV EXIT_NODES=
ENV EXCLUDE_NODES=
ENV HOPS=3
WORKDIR /etc/dnscrypt-proxy
COPY dnscrypt-proxy.toml .
COPY torrc_template /etc/tor/torrc
COPY relays.py .
COPY bootup.sh .
CMD ["./bootup.sh"]
