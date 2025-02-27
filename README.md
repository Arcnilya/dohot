# DNS over HTTPS over Tor

Measuring performance of DoHoT configurations

## Title ideas
- Tor Circuit Tuning for Anonymized DNS Queries
- The Cost of Private Resulution: Performance Impacts of DoHoT Configurations
- DoHoT or Not? Tuning Tor Circuits for Anonymous DNS
- Fast, Private, or Both? The DNS-over-HTTPS-over-Tor Dilemma

## Set up Muffet's DoHoT
https://github.com/alecmuffett/dohot
- [x] Put everything in a container
- [x] Figure out how to run measurements
- [x] Establish step-by-step
    1. Get Tranco 1M list `dnsperf/lists $ ./gettranco.sh`
    2. Run DoHoT container `docker $ ./run.sh`
    3. wait for latency check
    4. Run dnsperf container `dnsperf $ ./run.sh lists/tranco*.txt`
    5. Shut down container (clearing cache)
- [x] Establish a baseline (default config/torrc)
    - [x] Setup VM with containers
    - [x] Write a [script](baseline.sh) for deployment+measurement
    - [x] Run Tranco 1M a few times WIP

### Analyze Baseline
I have 13 x 1M Tranco:
- AVG latency (overall and for each iteration)
- Popularity impact?
- Circuit/DoH timeout patterns?


## Configuring Circuits
- [x] Proximity constrains on relays (region)
    - `./run.sh --entry se --exit no,dk`

- [x] Two-hop (entry/exit) using only carml+stem
    No need for a custom binary or separate container
    - [x] Copy changes to [other container](docker)
    - [x] Automate selection of relays [script](docker/relays.py)
    - [x] Swap circinfo.sh to carml+stem
    - [x] Make two-hop a toggle (similar to region)
    - `./run.sh --hops 2`
    - `./run.sh --hops 2 --entry se --exit se`

- [ ] DoH list
    - Change stuff in [dnscrypt-proxy.toml](docker/dnscrypt-proxy.toml)

### Picking Relay-pairs
Groups:
1. Same country
2. Same continent
3. Diff continent

Combinations:
- Same country entry: (1,1) (1,2) (1,3)
- Same continent entry: (2,1) (2,2) (2,3)
- Diff continent entry: (3,1) (3,2) (3,3)

### Analyze Configurations
TODO

## Integration
- [ ] Learn to program in Rust
- [ ] Modify a DoH stub in Rust to use arti

## Reflect on threat model and attacker capabilities
Client -- Attacker/Observer -- Resolver
