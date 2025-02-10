# Modify Tor for Single-Hop Circuits

The only thing missing from below is to pick a target system for the container,
installing build dependencies (run ./configure, follow instructions on fail
works fine), and replacing the final destination for the modified tor binary.

```
apt install make automake gcc libevent-dev libssl-dev zlib1g zlib1g-dev asciidoc
git clone https://gitlab.torproject.org/tpo/core/tor.git
cd tor/
./autogen.sh
./configure
git apply allow-single-hop-circuit.patch
make
cp src/app/tor /some/dst/
```

For controlling tor, warmly recommend [carml](https://github.com/meejah/carml):

```
pip install carml
```

