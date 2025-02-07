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
- [ ] Figure out what measurements to run
- [ ] Establish a baseline (default config)

## Configuration
- [ ] Proximity constrains on relays
    - In torrc: EntryNodes {se} MiddleNodes {se} ExitNodes {se} StrictNodes 1
    - Verify: ControlPort \> GETINFO \> circuit-status \> GETINFO \> ns/id/FINGERPRINT
- [ ] Fewer relays (hops)
    - In torrc:
        - AllowSingleHopCircuits 1?
        - UseEntryGuards 0?
        - ReducedExitPolicy 1?

## Integration
- [ ] Learn to program in Rust
- [ ] Modify a DoH stub in Rust to use arti

## Reflect on threat model and attacker capabilities
Client -- Attacker/Observer -- Resolver
