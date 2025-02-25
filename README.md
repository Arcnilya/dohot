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

## Configuration
- [x] Proximity constrains on relays (region)
    1. [Sweden](docker/torrc/sweden)
    2. [Nordics](docker/torrc/nordics)
    3. [Europe](docker/torrc/europe)
    - Verify `docker $ ./circinfo.sh`

- [ ] Single-hop using custom Tor binary + [carml](https://github.com/meejah/carml)
    - [container](single-hop-tor) WIP
    - We are stopped by TORPROTOCOL, very sad

- [ ] Two-hop (entry/exit) using only carml+stem
    No need for a custom binary or separate container
    - [x] Copy changes to [other container](docker)
    - [x] Automate selection of relays [script](docker/relays.py)
    - [x] Swap circinfo.sh to carml+stem
    - [ ] Make two-hop a toggle (similar to region), parse torrc?

- [ ] DoH list
    - Change stuff in [dnscrypt-proxy.toml](docker/dnscrypt-proxy.toml)

### Picking relay pairs
Groups:
1. Same country
2. Same continent
3. Diff continent

Combinations:
- Same country entry: (1,1) (1,2) (1,3)
- Same continent entry: (2,1) (2,2) (2,3)
- Diff continent entry: (3,1) (3,2) (3,3)

## Integration
- [ ] Learn to program in Rust
- [ ] Modify a DoH stub in Rust to use arti

## Reflect on threat model and attacker capabilities
Client -- Attacker/Observer -- Resolver
