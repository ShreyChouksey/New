# MAPAE Host-a-Shard Pilot Status

**Status date:** 29 August 2026  
**Canonical registration queue:** https://github.com/ShreyChouksey/New/issues/20

## Current state

| Measure | Count |
|---|---:|
| Previously exposed addresses excluded | 1,100 |
| Remaining addresses partitioned | 998,900 |
| Deterministic shards prepared | 9,989 |
| Addresses per shard | 100 |
| Pilot shards listed in public manifest | 100 |
| Pilot address capacity | 10,000 |
| Operator-controlled reference shards public | 1 |
| Previously unexposed addresses in reference shard | 100 |
| Verified independent hosts | 0 |
| Verified independent host placements | 0 |

## Reference shard

- **Shard ID:** `MAPAE-HAS-00001`
- **Address count:** `100`
- **SHA-256:** `f6c97c6efc2145bd6db56e783e4efb8c6b624cb5cd88407fcc0cdd7bb16e8f50`
- **Public TXT:** https://raw.githubusercontent.com/ShreyChouksey/New/claude/babel-image-archive-generator-mf9Gy/MAPAE/host-a-shard/reference-host/MAPAE-HAS-00001.txt
- **Registry classification:** `REFERENCE_PUBLIC_NONINDEPENDENT`

This reference publication proves the assignment, hosting, retrieval and exact-byte verification workflow. Because the destination is controlled by the MAPAE operator, it does not count as an independent external host.

## Next acceptance gate

The next milestone is achieved only when one independently administered website or public repository:

1. voluntarily registers in issue #20;
2. proves control or publishing authority;
3. receives a reserved, previously unassigned shard;
4. stores the exact shard at a public URL without login;
5. passes address-count, format, final-LF and SHA-256 verification; and
6. is entered in `HOST_REGISTRY.csv` as `VERIFIED_PUBLIC`.

## Counting rule

A manifest entry is not itself an address exposure. An address counts as independently scattered only after an authorized external host publishes the actual shard and that copy passes verification.

No private keys, WIFs, seeds, mnemonics, entropy source, recovery material, xprvs or signing credentials are included in this program.
