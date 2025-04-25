FROM ubuntu
SHELL ["/bin/bash", "-c"]

RUN apt update && apt upgrade -y && apt install -y \
    tor vim netcat-traditional net-tools \
    software-properties-common \
    stubby proxychains4 \
    ldnsutils # for srill
RUN add-apt-repository ppa:deadsnakes/ppa -y && apt update
RUN apt install -y python3.11 python3.11-venv python3.11-dev
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
RUN apt install -y python3-pip
RUN apt remove -y python3-cryptography
RUN pip install carml --break-system-packages
RUN pip install stem --break-system-packages
RUN rm -rf /var/lib/apt/lists/*


ENV ENTRY_NODES=
ENV MIDDLE_NODES=
ENV EXIT_NODES=
ENV EXCLUDE_NODES=
ENV HOPS=

WORKDIR /etc/stubby/
COPY stubby.yml /etc/stubby/stubby.yml
COPY proxychains4.conf /etc/proxychains4.conf
COPY torrc_template /etc/tor/torrc
COPY relays.py .
COPY bootup.sh .

#HEALTHCHECK --interval=120s --timeout=30s --start-period=10s CMD drill @127.0.0.1 -p 8053 getdnsapi.net || exit 1

CMD ["./bootup.sh"]
