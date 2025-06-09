# DNS over HTTPS over Tor

Measuring performance of DoHoT configurations

## Overview
This repository contains resources and experiments related to improving the
performance of DNS queries over Tor to DoH (DNS over HTTPS) servers, an
approach known as DoHoT. This method aims to achieve anonymity between the
client and the resolver without requiring additional infrastructure beyond the
existing Tor network.

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

