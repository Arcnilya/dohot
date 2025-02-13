#!/bin/bash

while read line; do
    ip=$(echo $line | awk '{print $3}')
    cc=$(whois $ip | grep -m 1 -i 'country' | head -1 | awk '{print $2}')
    echo $line $cc
done < $1
