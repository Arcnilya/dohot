#!/bin/bash

# TODO: paralellize?

resolver=localhost
port=1337
docker rm -f dohot-container 2>/dev/null
echo "query,time" > log.csv

prot="DOHOT"
setting="DEFAULT"

# DoHoT default
for i in $(seq 0 9);
do
    while : # loop infinitely
    do
        echo "$(date +"%Y-%m-%dT%H:%M:%S"): Starting resolver"
        docker run -d -p $port:53/tcp -p $port:53/udp --name dohot-container dohot-image > /dev/null
        dig @$resolver -p $port kau.se +tries=5 +noall # wait for resolver to run
        dname="$prot-$setting-$i-$(mktemp -u XXXXXXXX).net"
        echo "$(date +"%Y-%m-%dT%H:%M:%S"): Sending query ($dname)"
        qtime=$(dig @$resolver -p $port $dname +tries=2 | grep "Query time" | awk '{print $(NF-1)}')
        echo "$(date +"%Y-%m-%dT%H:%M:%S"): Stopping resolver"
        docker stop dohot-container > /dev/null
        docker rm dohot-container > /dev/null

        if [ "$qtime" ]; then
            echo "$dname,$qtime" >> log.csv
            break
        fi
    done
done

# DoHoT two-hops
setting="TWOHOPS"
for i in $(seq 0 9);
do
    while : # loop infinitely
    do
        echo "$(date +"%Y-%m-%dT%H:%M:%S"): Starting resolver"
        docker run -d -p $port:53/tcp -p $port:53/udp --name dohot-container -e HOPS="2" dohot-image > /dev/null
        dig @$resolver -p $port kau.se +tries=5 +noall # wait for resolver to run
        dname="$prot-$setting-$i-$(mktemp -u XXXXXXXX).net"
        echo "$(date +"%Y-%m-%dT%H:%M:%S"): Sending query ($dname)"
        qtime=$(dig @$resolver -p $port $dname +tries=2 | grep "Query time" | awk '{print $(NF-1)}')
        echo "$(date +"%Y-%m-%dT%H:%M:%S"): Stopping resolver"
        docker stop dohot-container > /dev/null
        docker rm dohot-container > /dev/null

        if [ "$qtime" ]; then
            echo "$dname,$qtime" >> log.csv
            break
        fi
    done
done

# DoHoT Sweden
setting="SWEDEN"
for i in $(seq 0 9);
do
    while : # loop infinitely
    do
        echo "$(date +"%Y-%m-%dT%H:%M:%S"): Starting resolver"
        docker run -d -p $port:53/tcp -p $port:53/udp --name dohot-container \
            -e ENTRY_NODES="se" \
            -e EXIT_NODES="se" \
            -e HOPS="2" \
            dohot-image > /dev/null
        dig @$resolver -p $port kau.se +tries=5 +noall # wait for resolver to run
        dname="$prot-$setting-$i-$(mktemp -u XXXXXXXX).net"
        echo "$(date +"%Y-%m-%dT%H:%M:%S"): Sending query ($dname)"
        qtime=$(dig @$resolver -p $port $dname +tries=2 | grep "Query time" | awk '{print $(NF-1)}')
        echo "$(date +"%Y-%m-%dT%H:%M:%S"): Stopping resolver"
        docker stop dohot-container > /dev/null
        docker rm dohot-container > /dev/null

        if [ "$qtime" ]; then
            echo "$dname,$qtime" >> log.csv
            break
        fi
    done
done

#echo "$(date +"%Y-%m-%dT%H:%M:%S"): Starting resolver"
#docker run -d -p $port:53/tcp -p $port:53/udp --name dohot-container \
#    -e ENTRY_NODES="se" \
#    -e EXIT_NODES="se" \
#    -e HOPS="2" \
#    dohot-image > /dev/null


