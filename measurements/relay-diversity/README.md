# dohot-appendix

Supporting material for analysing the anonymity cost of **country-constrained,
2-hop Tor relay selection**.

`relay_diversity.py` approximates, per country, how many relays are available and
how *diverse* their operators are. This directly addresses a reviewer concern
about Section VI-C (see [Relevance to the review](#relevance-to-the-review)).

## Quick start

```bash
python3 relay_diversity.py            # default: us de fr nl se ru (+ eu, us)
python3 relay_diversity.py de fr ch   # custom country list (+ eu, us always added)
python3 relay_diversity.py --timeout 60 it es
```

No third-party dependencies — Python 3 standard library only. The script fetches
live data over HTTPS, so it needs network access.

Example output:

```
group  relays  families  ASes  /24s  contacts  no-contact
---------------------------------------------------------
us       2775      1348   234  1073       675         251
de       1768      1052   137  1026       786         179
fr        443       235    41   253       182          83
nl       1118       351    99   308       224         102
se        505       129    39    86        83          26
ru         39        25    12    20        21           4
eu       5622      2796   546  2543      1808         718
```

(Numbers vary with each consensus; the above is a single snapshot.)

## What the columns mean

For each group (a single country, or the `eu`/`us` meta aggregate):

| Column       | Meaning |
|--------------|---------|
| `relays`     | Running relays located in the group. |
| `families`   | Distinct **operators**, approximated as the number of connected components in the relay *family* graph (see below). A relay in no family counts as its own component. |
| `ASes`       | Distinct autonomous systems (AS numbers) hosting the relays. |
| `/24s`       | Distinct IPv4 `/24` subnets across the relays' first IPv4 OR address. |
| `contacts`   | Distinct, normalised (lowercased/trimmed) non-empty `ContactInfo` strings. |
| `no-contact` | Relays in the group that publish no `ContactInfo`. |

`families`, `ASes`, `/24s`, and `contacts` are all **operator-diversity proxies**:
the closer they are to `relays`, the more independent operators a country has, and
the lower the chance that one entity controls both relays in a 2-hop circuit.

## Meta groups

- **`eu`** — the union of all relays located in the **European Economic Area plus
  Switzerland** — i.e. the EU-27 plus Iceland, Liechtenstein, Norway (the non-EU
  EEA members) and Switzerland:
  `at be bg hr cy cz dk ee fi fr de gr hu ie it lv lt lu mt nl pl pt ro sk si es se is li no ch`.
- **`us`** — all relays in the United States (identical to the plain `us` country
  row; included explicitly as a meta row for symmetry with `eu`).

Both meta rows are always printed, even if not passed on the command line.

## Data source

The script does **not** parse the raw Tor consensus. The raw network-status
consensus contains neither:

- **country codes** — these require a GeoIP lookup on each relay's IP address, nor
- **family information** — `MyFamily` is published in the relays' *server
  descriptors*, not in the consensus.

Instead it queries the Tor Project's **Onionoo** service, which already joins the
consensus, server descriptors, and GeoIP data and exposes the result as JSON:

```
GET https://onionoo.torproject.org/details
      ?type=relay
      &running=true
      &fields=fingerprint,country,as,as_name,contact,effective_family,or_addresses
```

The response is a JSON object with a top-level `relays` array; each element
describes one relay. The fields the script uses:

| Onionoo field      | Type            | Used for |
|--------------------|-----------------|----------|
| `fingerprint`      | hex string      | Identity / graph node id. |
| `country`          | ISO 3166-1 a2   | Assigning a relay to a country group (GeoIP-derived by Onionoo). |
| `as`               | string (`ASnnn`)| AS-diversity count. |
| `as_name`          | string          | Requested for readability/extensibility (not currently aggregated). |
| `contact`          | string          | Contact-diversity count. |
| `effective_family` | list of hex     | Building the family graph (see below). |
| `or_addresses`     | list of strings | Extracting the first IPv4 → `/24` subnet. |

Requesting only the needed `fields` keeps the download small (a few MB); the
script also sends `Accept-Encoding: gzip` and decompresses if needed.

`effective_family` is Onionoo's **mutually agreed** family: relay A is in relay
B's effective family only if *both* list each other. It is more conservative (and
more correct) than raw `MyFamily`, which a single operator can set unilaterally.

## How `families` is computed

The script builds an undirected graph whose nodes are the relays in a group and
adds an edge between two relays when each lists the other in `effective_family`
(restricted to relays *within the group*). It then counts connected components
with a union-find. Each component is treated as one operator; a relay with no
in-group family member is a component of size one.

This is an **approximation of the number of independent operators**. It is the
metric most directly relevant to the "single entity controls both hops" concern:
the family graph is exactly what Tor itself uses to avoid placing two related
relays in the same circuit.

## Relevance to the review

The reviewer noted (paraphrased) that 2-hop circuits already narrow anonymity
versus the standard 3-hop design, and that **country-specific** selection shrinks
the candidate pool further, raising the probability that a single entity controls
both relays. They asked for an analysis of relay distribution and diversity per
country, using descriptor metadata (contact, naming conventions, AS numbers,
shared `/24` subnets).

This script provides exactly that evidence in one table. Reading the snapshot
above:

- **Sweden** has 505 relays but only **129 families**, **39 ASes** and **86
  `/24`s** — a strong concentration signal (many relays per operator/subnet).
- **France** has fewer relays (443) but **235 families** and **41 ASes** — far
  better diversity *per relay*.

So the table lets a reader judge, per country, whether the latency gains of
2-hop country-constrained selection come at an acceptable anonymity cost, and
which countries (few and poorly diversified relays) should be avoided.

### Caveats / approximations

- Family edges are restricted to **in-group** relays, so a family spanning
  several countries is counted once per country. This matches "diversity *within*
  a country" but means the per-country `families` figures are lower bounds on
  global operator concentration.
- Counts are **uniform over relays**. Tor's path selection is *bandwidth
  weighted*, so a small number of high-bandwidth relays can dominate selection
  probability even where the relay *count* looks diverse. A bandwidth-weighted
  concentration measure (e.g. a Herfindahl–Hirschman index over families or ASes
  using consensus weights) would tighten the argument; it is not yet implemented.
- `effective_family` only captures *declared and mutually agreed* relationships;
  a deliberate adversary running undeclared relays is not detected by any
  descriptor-metadata method, including this one.

## Suggested appendix wording

> To assess whether country-constrained relay selection meaningfully erodes
> anonymity, we measured relay availability and operator diversity per country
> using the Tor Project's Onionoo service, which augments the consensus with
> GeoIP and server-descriptor data. For each country we counted the running
> relays and four diversity proxies: the number of distinct relay *families*
> (connected components of the mutually-agreed `effective_family` graph,
> approximating independent operators), distinct autonomous systems, distinct
> IPv4 `/24` subnets, and distinct `ContactInfo` strings. Table~\ref{tab:diversity}
> reports these figures. Several countries combine a moderate relay count with
> markedly lower family, AS and subnet diversity (e.g. Sweden: 505 relays but
> only 129 families across 39 ASes), indicating that a single operator or
> subnet hosts many relays. In a 2-hop circuit, this raises the probability that
> both hops are controlled by the same entity. We therefore recommend restricting
> the optimisation to countries whose diversity proxies remain close to their
> relay count, and avoiding countries with few, poorly diversified relays. We note
> that these counts are uniform over relays; because Tor weights path selection by
> bandwidth, a bandwidth-weighted concentration index would yield a stricter bound.

(Adjust the concrete numbers to the consensus snapshot used in the final
analysis.)

---

*The `relay_diversity.py` script and this README were created with
[Claude Code](https://claude.com/claude-code).*
