# DoHoT container
https://github.com/alecmuffett/dohot/blob/master/INSTALL.md
https://github.com/dnscrypt/dnscrypt-proxy/wiki/Installation-on-Debian-and-Ubuntu

## Running container
```sh
docker compose {build,up,down}
# or
./run.sh
```

## Send DNS query
```sh
dig @localhost -p 1337 example.com
```

## Fetch circuit info
```sh
docker exec -it dohot-container bash
./getinfo.sh
```

