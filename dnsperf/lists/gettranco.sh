#!/bin/bash

# Cleanup
mkdir -p old
mv tranco_* old

# Fetch Tranco
wget https://tranco-list.eu/top-1m.csv.zip
unzip top-1m.csv.zip
rm top-1m.csv.zip
id=$(curl --silent https://tranco-list.eu/top-1m-id)
mv top-1m.csv tranco_$id.csv

# Parse a list for dnsperf
cut -d, -f2 tranco_$id.csv | sed 's/\r//' | sed 's/$/ A/' > tranco_$id.txt
