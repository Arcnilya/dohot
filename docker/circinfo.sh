#!/bin/bash

docker exec dohot-container bash getinfo.sh > circuits.txt

while read line; do
    ip=$(echo $line | awk '{print $3}')
    cc=$(whois $ip | grep -i 'country:' | awk '{print $2}')
    echo "$line ($(echo $cc))"
done < circuits.txt
