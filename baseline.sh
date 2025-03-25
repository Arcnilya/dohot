#!/bin/bash

domains=${1:-"lists/mini.txt"}
starttime=$(date +"%Y-%m-%dT%H:%M")

echo "$(date +"%Y-%m-%dT%H:%M:%S"): Stopping DoHoT if already running"
docker stop dohot-container

echo "$(date +"%Y-%m-%dT%H:%M:%S"): Starting DoHoT"
docker run --rm -d -p 1337:53/tcp -p 1337:53/udp --name dohot-container dohot-image > /dev/null
sleep 120 # Let dnscrypt-proxy find a nearby DoH server

echo "$(date +"%Y-%m-%dT%H:%M:%S"): Warmup DoHoT"
dig @localhost -p 1337 kauotic.se +noall

echo "$(date +"%Y-%m-%dT%H:%M:%S"): Running dnsperf: $domains"
docker run --rm -v $(pwd)/${domains}:/tmp/domains.txt \
	dnsperf -d /tmp/domains.txt -s 172.17.0.1 -p 1337 -v -Q 100 -t 10 > dnsperf.log

echo "$(date +"%Y-%m-%dT%H:%M:%S"): Parsing log"
grep "^>" dnsperf.log | \
   	sed 's/T /TIMEOUT /' | \
   	sed "s/^> /$starttime /" | \
   	sed 's/ /,/g' >> data.csv

echo "$(date +"%Y-%m-%dT%H:%M:%S"): Stopping DoHoT"
docker stop dohot-container
