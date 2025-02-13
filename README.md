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
- [ ] Establish step-by-step
    1. Get Tranco 1M list
    2. Run DoHoT container, wait for latency check
    3. Send non-Tranco domain to warm-up connection (kauotic.se)
    4. Send Tranco 1M in order (top to bottom), store response time (msec)
    5. Shut down container (clearing cache)
    6. Goto step 2
- [ ] Establish a baseline (default config/torrc)

## Configuration
- [ ] Proximity constrains on relays
    1. [Sweden](docker/torrc/sweden)
    2. [Nordics](docker/torrc/nordics)
    3. [Europe](docker/torrc/europe)
    - Verify using ControlPort
        1. GETINFO \> circuit-status
        2. GETINFO \> ns/id/FINGERPRINT
        3. whois IP
    - Find additional tools for ControlPort

- [ ] Fewer relays (hops)
    1. In torrc:
        - AllowSingleHopCircuits 1?
        - UseEntryGuards 0?
        - ReducedExitPolicy 1?
        - Verify using ControlPort
    2. Custom Tor binary (Pulls)

- [ ] DoH list
    - Change stuff in [dnscrypt-proxy.toml](docker/dnscrypt-proxy.toml)

## Integration
- [ ] Learn to program in Rust
- [ ] Modify a DoH stub in Rust to use arti

## Reflect on threat model and attacker capabilities
Client -- Attacker/Observer -- Resolver
