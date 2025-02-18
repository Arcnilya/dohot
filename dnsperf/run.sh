#!/bin/bash

docker build -t dnsperf .

echo "Warmup Tor and DoH (kauotic.se)"
resp=$(dig @localhost -p 1337 kauotic.se)
echo $resp | grep -oE "status: [A-Z]+"
echo $resp | grep -oE "[0-9]+ msec"

# $1 = a list of domains
# -t = timeout 
# -Q = queries per second
docker run --rm \
    -v $(pwd)/$1:/tmp/domains.txt \
    dnsperf -d /tmp/domains.txt -s 172.17.0.1 -p 1337 -v -Q 100 -t 10

