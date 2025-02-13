# Analysis

## Circuits
After changing the torrc I need a way of confirming the selection of relays.
Run the dohot-container locally, then run:
```sh
docker exec dohot-container bash getinfo.sh > circuits.txt
```
I have made a simple script for using whois:
```sh
./cc.sh circuits.txt
```
