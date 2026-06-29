#!/usr/bin/env python3
"""Approximate Tor relay count and operator diversity per country.

Motivation
----------
For a 2-hop, country-constrained relay selection, the candidate pool shrinks and
the risk that a single entity controls both relays of a circuit grows. This
script reports, per country (and for the meta groups ``eu`` and ``us``), the
number of running relays and several operator-diversity proxies: distinct
families, distinct autonomous systems (AS), distinct IPv4 /24 subnets, and
distinct contacts.

Data source
-----------
The raw Tor consensus contains neither country codes (which need a GeoIP lookup)
nor family data (``MyFamily`` lives in server descriptors). The Tor Project's
Onionoo ``details`` API already computes and exposes per-relay ``country``,
``as``, ``contact``, ``effective_family`` and ``or_addresses``, so we fetch that
instead. See https://onionoo.torproject.org/.

Dependencies: Python standard library only.

Caveats / approximations
------------------------
- Family edges are restricted to in-group relays, so a family that spans several
  countries is counted per-country. This matches "diversity *within* a country".
- ``effective_family`` is Onionoo's mutually-agreed family; ``MyFamily``
  misconfigurations are not corrected here. A relay in no family counts as its
  own component (i.e. a distinct operator).
- IPv6-only relays contribute no /24. Relays without ``country``/``as``/
  ``contact`` are excluded from the respective distinct counts.
"""

from __future__ import annotations

import argparse
import gzip
import ipaddress
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict

ONIONOO_URL = "https://onionoo.torproject.org/details"
ONIONOO_FIELDS = "fingerprint,country,as,as_name,contact,effective_family,or_addresses"

# The `eu` meta = the European Economic Area (EU-27 + Iceland, Liechtenstein,
# Norway) plus Switzerland (ISO 3166-1 alpha-2, lowercase). `is`/`li`/`no` are the
# non-EU EEA members; `ch` is Switzerland.
EUROPE_COUNTRIES = frozenset(
    {
        # EU-27
        "at", "be", "bg", "hr", "cy", "cz", "dk", "ee", "fi", "fr", "de", "gr",
        "hu", "ie", "it", "lv", "lt", "lu", "mt", "nl", "pl", "pt", "ro", "sk",
        "si", "es", "se",
        # rest of EEA + Switzerland
        "is", "li", "no", "ch",
    }
)

DEFAULT_COUNTRIES = ["us", "de", "fr", "nl", "se", "ru"]


def fetch_details(timeout: float) -> list[dict]:
    """Fetch the Onionoo details document and return its list of relays."""
    url = (
        f"{ONIONOO_URL}?type=relay&running=true"
        f"&fields={urllib.parse.quote(ONIONOO_FIELDS)}"
    )
    req = urllib.request.Request(
        url,
        headers={
            "Accept-Encoding": "gzip",
            "User-Agent": "relay_diversity.py (Tor relay diversity analysis)",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            if resp.headers.get("Content-Encoding", "").lower() == "gzip":
                raw = gzip.decompress(raw)
    except (urllib.error.URLError, OSError) as exc:
        sys.exit(f"error: failed to fetch Onionoo details: {exc}")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        sys.exit(f"error: failed to parse Onionoo JSON: {exc}")

    relays = data.get("relays")
    if not isinstance(relays, list):
        sys.exit("error: unexpected Onionoo response (no 'relays' list)")
    return relays


def first_ipv4_24(or_addresses: list[str]) -> str | None:
    """Return the /24 network (as text) of the first IPv4 OR address, or None."""
    for addr in or_addresses or []:
        # or_addresses entries look like "1.2.3.4:9001" or "[2001:db8::1]:9001".
        if addr.startswith("["):
            continue
        host = addr.rsplit(":", 1)[0]
        try:
            ip = ipaddress.IPv4Address(host)
        except ipaddress.AddressValueError:
            continue
        return str(ipaddress.ip_network(f"{ip}/24", strict=False).network_address)
    return None


def normalize(relays: list[dict]) -> list[dict]:
    """Reduce each Onionoo relay to the fields we care about."""
    records = []
    for r in relays:
        fp = (r.get("fingerprint") or "").lower()
        if not fp:
            continue
        contact = (r.get("contact") or "").strip().lower()
        records.append(
            {
                "fp": fp,
                "country": (r.get("country") or "").lower(),
                "as": r.get("as") or None,
                "contact": contact or None,
                "subnet24": first_ipv4_24(r.get("or_addresses", [])),
                "family": [f.lower() for f in (r.get("effective_family") or [])],
            }
        )
    return records


def count_families(subset: list[dict]) -> int:
    """Count connected components in the effective_family graph over `subset`.

    A relay listed in no family (or whose family members are all outside the
    subset) forms its own component, i.e. counts as one distinct operator.
    """
    in_subset = {rec["fp"] for rec in subset}
    parent: dict[str, str] = {fp: fp for fp in in_subset}

    def find(x: str) -> str:
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:  # path compression
            parent[x], x = root, parent[x]
        return root

    def union(a: str, b: str) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for rec in subset:
        for other in rec["family"]:
            if other in in_subset:
                union(rec["fp"], other)

    return len({find(fp) for fp in in_subset})


def summarize(records: list[dict], member_countries: frozenset[str]) -> dict:
    """Compute metrics for the relays whose country is in `member_countries`."""
    subset = [r for r in records if r["country"] in member_countries]
    ases = {r["as"] for r in subset if r["as"]}
    subnets = {r["subnet24"] for r in subset if r["subnet24"]}
    contacts = {r["contact"] for r in subset if r["contact"]}
    no_contact = sum(1 for r in subset if not r["contact"])
    return {
        "relays": len(subset),
        "families": count_families(subset),
        "ases": len(ases),
        "subnets": len(subnets),
        "contacts": len(contacts),
        "no_contact": no_contact,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Approximate Tor relay count and operator diversity per country, "
            "using the Onionoo details API. The meta groups 'eu' (EEA + Switzerland) "
            "and 'us' are always included."
        )
    )
    parser.add_argument(
        "countries",
        nargs="*",
        default=DEFAULT_COUNTRIES,
        metavar="CC",
        help=(
            "ISO 3166-1 alpha-2 country codes to report (e.g. de fr ch). "
            f"Default: {' '.join(DEFAULT_COUNTRIES)}. "
            "'eu' and 'us' meta rows are always added."
        ),
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=120.0,
        help="HTTP timeout in seconds (default: 120).",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> None:
    args = parse_args(argv)

    print(f"Fetching {ONIONOO_URL} ...", file=sys.stderr)
    records = normalize(fetch_details(args.timeout))
    print(f"Fetched {len(records)} running relays.\n", file=sys.stderr)

    # Build the ordered list of (label, member_countries) groups. Per-country
    # rows first (deduplicated, order preserved), then the meta rows.
    groups: list[tuple[str, frozenset[str]]] = []
    seen = set()
    for cc in args.countries:
        cc = cc.lower()
        if cc in seen:
            continue
        seen.add(cc)
        members = EUROPE_COUNTRIES if cc == "eu" else frozenset({cc})
        groups.append((cc, members))
    for meta, members in (("eu", EUROPE_COUNTRIES), ("us", frozenset({"us"}))):
        if meta not in seen:
            seen.add(meta)
            groups.append((meta, members))

    column_help = [
        ("group", "country code, or a meta group (eu = EEA + Switzerland, us)"),
        ("relays", "running relays located in the group"),
        ("families", "distinct operators (connected components of the "
                     "effective_family graph); a relay in no family counts as one"),
        ("ASes", "distinct autonomous systems (AS numbers) hosting the relays"),
        ("/24s", "distinct IPv4 /24 subnets of the relays' first IPv4 address"),
        ("contacts", "distinct non-empty, normalised ContactInfo strings"),
        ("no-contact", "relays in the group publishing no ContactInfo"),
    ]
    label_w = max(len(name) for name, _ in column_help)
    print("Columns:")
    for name, desc in column_help:
        print(f"  - {name.ljust(label_w)}  {desc}")
    print()

    header = ["group", "relays", "families", "ASes", "/24s", "contacts", "no-contact"]
    rows = [header]
    for label, members in groups:
        m = summarize(records, members)
        rows.append(
            [
                label,
                str(m["relays"]),
                str(m["families"]),
                str(m["ases"]),
                str(m["subnets"]),
                str(m["contacts"]),
                str(m["no_contact"]),
            ]
        )

    widths = [max(len(row[i]) for row in rows) for i in range(len(header))]
    for i, row in enumerate(rows):
        line = "  ".join(
            cell.ljust(widths[j]) if j == 0 else cell.rjust(widths[j])
            for j, cell in enumerate(row)
        )
        print(line)
        if i == 0:
            print("-" * len(line))


if __name__ == "__main__":
    main(sys.argv[1:])
