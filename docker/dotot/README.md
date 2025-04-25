# DoToT container
 

## Running container
```sh
./run.sh

./run.sh --entry se --exit se

./run.sh --entry se --exit no,fi,dk,is
```

## Send DNS query
```sh
dig @localhost -p 8053 example.com
```

## Fetch circuit and relay info
```sh
# List current built circuits
docker exec dotot-container python3 relays.py --circ

# Get a random relay from location
docker exec dotot-container python3 relays.py --cc se

# Get a random relay from location with role (entry/exit)
docker exec dotot-container python3 relays.py --cc de --role exit
```



## links
- https://github.com/MatthewVance/stubby-docker/tree/master
- https://dnsprivacy.org/dns_privacy_daemon_-_stubby/configuring_stubby/
- https://github.com/DNSCrypt/dnscrypt-proxy/issues/1124
- https://dnscrypt.info/faq/
- https://dnsprivacy.org/dns_privacy_daemon_-_stubby/configuring_stubby/
- https://github.com/getdnsapi/stubby/issues/131
- https://dnsprivacy.org/public_resolvers/#dns-over-tls-dot
- https://github.com/rofl0r/proxychains-ng
- https://medium.com/@redfanatic7/how-to-use-proxychains-8420dd4ef88c

 
