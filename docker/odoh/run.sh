#!/bin/bash

docker rm odoh-container
docker build -t odoh-image .
docker run --rm --name odoh-container \
    -p 127.0.0.1:1337:53/udp \
    -p 127.0.0.1:1337:53/tcp \
    odoh-image
