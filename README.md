# DoHoT - DNS over HTTPS over Tor

## Overview
This repository contains resources and experiments related to improving the performance of DNS
queries over Tor to DoH (DNS over HTTPS) servers, an approach known as DoHoT.
This method aims to achieve anonymity between the client and the resolver
without requiring additional infrastructure beyond the existing Tor network.

## Background
Alec Muffet has been testing the feasibility of using Tor to send DNS queries
to DoH servers [[github](https://github.com/alecmuffett/dohot)].
This approach differs from other anonymity-preserving DNS
methods, such as Oblivious DNS (ODNS) and Oblivious DoH (ODoH), which rely on
additional infrastructure operated by non-colluding parties. Instead, DoHoT
leverages the existing Tor network to provide anonymity without further
dependencies.

## Challenges of DoHoT
One of the main challenges of using Tor for DNS is latency. Tor routes traffic
through multiple relays across the globe and builds circuits repeatedly,
leading to increased query times compared to traditional DNS resolution
methods.

## Potential Improvements
Muffet's current testing utilizes Tor with its default configuration, which
consists of three relays (Entry, Middle, Exit) with no geographic restrictions.
However, there are potential optimizations that could improve DoHoT's performance:
- Reducing Circuit Length: Configuring Tor to use only two relays instead of three.
- Geographical Relay Selection: Restricting the relays to a specific geographic
  region to reduce network latency.

Investigating these parameters could provide insights into optimizing DoHoT
while maintaining a balance between anonymity and performance.

## Threat Model Discussion
An important aspect to discuss is the threat model when using encrypted DNS
transport (DoT, DoH, DoQ) and anonymous query techniques (ODNS, ODoH, DoHoT).
The security and privacy benefits of these methods depend on the considered
adversary. For instance, if your primary adversary is your Internet Service
Provider (ISP) and you use a third-party DoH resolver to conceal your DNS
queries, your ISP can still see subsequent connections to that obtained IP.
This raises questions about the effectiveness of different encrypted DNS
solutions depending on the adversary's capabilities and the information they
can infer from your traffic patterns. Exploring these scenarios is important to
understand the trade-offs between anonymity, encryption, and performance in DNS
resolution.

## This Repository
This repository is intended for DNS hackathon participants to:
- Obtain docker containers for 
    - DoHoT
    - DNSperf
- Add measurement ideas
- Run small measurements for some initial results
- Discuss thread models in DNS Privacy

