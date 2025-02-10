#!/bin/bash
head -n 100 $1 | cut -d, -f2 | while read line; do
    domain=$(echo $line | xargs | tr -d '\r')
    response=$(dig @localhost -p 1337 +tries=1 $domain)
    msec=$(echo $response | grep -oE "[0-9]+ msec" | awk '{print $1}')
    echo "$msec $domain"
done
