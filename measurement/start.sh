#!/bin/bash

echo "Warmup DoH and Tor (kauotic.se)"
foo=$(dig @localhost -p 1337 +tries=1 kauotic.se)
echo $foo | grep -oE "status: [A-Z]+"
echo $foo | grep -oE "[0-9]+ msec"

top=100
echo "Running $1 top $top"
head -n $top $1 | cut -d, -f2 | while read line; do
    domain=$(echo $line | xargs | tr -d '\r')
    response=$(dig @localhost -p 1337 +tries=1 $domain)
    msec=$(echo $response | grep -oE "[0-9]+ msec" | awk '{print $1}')
    echo "$msec $domain"
done
