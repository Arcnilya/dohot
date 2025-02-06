#!/bin/bash

getip() {
        echo -e "AUTHENTICATE\nGETINFO ns/id/$1\nQUIT" | nc 127.0.0.1 9051 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+'
}

echo -e "AUTHENTICATE\nGETINFO circuit-status\nQUIT" | nc 127.0.0.1 9051 | sed 's/\r/\n/g' | grep BUILT > circuits.txt

while read -r line; do
        id=$(echo "$line" | awk '{print $1}')
        relays=$(echo "$line" | awk '{print $3}' | sed 's/\$//g')
        echo "$relays" | sed 's/,/\n/g' | while read -r relay; do
                fingerprint=$(echo $relay | cut -d '~' -f1)
                name=$(echo $relay | cut -d '~' -f2)
                echo $id $fingerprint $(getip "$fingerprint") $name
        done
done < circuits.txt
