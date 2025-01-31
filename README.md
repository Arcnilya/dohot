# DNS over HTTPS over Tor

Measuring performance of anonymized DNS queries using Tor.

## Set up Muffet's DoHoT
- Measure performance (baseline) 
- https://github.com/alecmuffett/dohot

## Ideas to test
- Fewer relays
- Geographical constrains on relays
- Maintaining circuits over multiple queries

## Integration
- Learn to program in Rust
- Implement/modify a DoH stub in Rust to use arti (a rust tor implementation)

## Reflect on threat model and attacker capabilities
Client -- Attacker -- Resolver
