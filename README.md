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
- [ ] Establish a baseline (default config/torrc)
    - [ ] Setup VM with containers
    - [ ] Run Tranco 1M

## Configuration
- [x] Proximity constrains on relays (region)
    1. [Sweden](docker/torrc/sweden)
    2. [Nordics](docker/torrc/nordics)
    3. [Europe](docker/torrc/europe)
    - Verify `docker $ ./circinfo.sh` 

- [ ] Fewer relays (hops) using custom Tor binary + [carml](https://github.com/meejah/carml)
    - [container](single-hop-tor) WIP

- [ ] DoH list
    - Change stuff in [dnscrypt-proxy.toml](docker/dnscrypt-proxy.toml)

## Integration
- [ ] Learn to program in Rust
- [ ] Modify a DoH stub in Rust to use arti

## Reflect on threat model and attacker capabilities
Client -- Attacker/Observer -- Resolver
