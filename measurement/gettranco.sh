#!/bin/bash

mkdir -p old_lists
mv tranco_* old_lists
wget https://tranco-list.eu/top-1m.csv.zip
unzip top-1m.csv.zip
rm top-1m.csv.zip
id=$(curl --silent https://tranco-list.eu/top-1m-id)
mv top-1m.csv tranco_$id.csv
