# DoHoT container
- https://github.com/alecmuffett/dohot/blob/master/INSTALL.md  
- https://github.com/dnscrypt/dnscrypt-proxy/wiki/Installation-on-Debian-and-Ubuntu

## Running container
```sh
./run.sh

./run.sh --entry se --exit se

./run.sh --entry se --exit no,fi,dk,is
```

## Send DNS query
```sh
dig @localhost -p 1337 example.com
```

## Fetch circuit and relay info
```sh
# List current built circuits
docker exec dohot-container python3 relays.py --circ

# Get a random relay from location
docker exec dohot-container python3 relays.py --cc se

# Get a random relay from location with role (entry/exit)
docker exec dohot-container python3 relays.py --cc de --role exit
```

## links
- https://forum.torproject.org/t/re-tor-relays-disable-conflux-on-exit-relay/12275
- https://gitlab.torproject.org/tpo/core/tor/-/issues/17359
- https://blog.torproject.org/exploring-tor-carml/
- https://github.com/meejah/carml
