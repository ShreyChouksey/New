# MAPAE Host-a-Shard Network

**Status:** Pilot opened  
**Pilot capacity:** 100 shards × 100 addresses = 10,000 previously unexposed public Bitcoin addresses  
**Full planned capacity:** 9,989 shards × 100 addresses = 998,900 addresses  
**Canonical one-million-address corpus SHA-256:** `5bb9320bc93f07e3129cb6ef5aee4da2c245e0ca11279d4963244bead79a90df`

The Host-a-Shard Network is the permission-based distribution layer of the
Million-Address Perpetual Adversarial Exposure Experiment (MAPAE).

Its purpose is to place exact, verifiable copies of small public-address shards
on independently administered websites that voluntarily opt in. It is not an
automated posting campaign and does not authorize unsolicited submissions,
fake accounts, platform-rule circumvention, or use of unrelated forms.

## What a host receives

Each host is assigned one or more immutable files named:

```text
MAPAE-HAS-00001.txt
MAPAE-HAS-00002.txt
...
```

Each file contains exactly 100 lowercase Bitcoin mainnet native-SegWit
`bc1q...` public addresses, one per LF-terminated line. Every shard has its own
SHA-256 value.

The first 100 assignable shards are listed in `PILOT_MANIFEST_100.csv`.

## Host eligibility

A proposed host qualifies when all of the following are true:

1. The applicant controls, administers, or has explicit publishing authority
   for the destination.
2. The destination knowingly agrees to host a MAPAE research shard.
3. The shard is publicly retrievable without login.
4. The host stores an actual copy rather than an iframe or hotlink to the
   canonical repository.
5. The exact shard bytes match the assigned SHA-256.
6. The page or adjacent documentation identifies the material as a public
   research artifact and does not imply that funding is requested.
7. The host does not modify, reorder, add, or remove addresses.
8. No private key, seed, mnemonic, WIF, entropy source, recovery secret, xprv,
   or signing credential is published.

## Registration

Apply in the public **MAPAE Host-a-Shard registration issue**. Provide:

```text
Host name:
Domain or public repository:
Proposed public URL/path:
Number of shards requested:
Verification method: DNS TXT or /.well-known/ file
Contact GitHub account:
Consent statement: I control or am authorized to publish at this destination,
and I voluntarily agree to host the assigned MAPAE shard(s) for lawful research.
```

## Domain-control verification

The registrar will issue a unique token. Publish it by either method:

### DNS TXT

```text
_mapae.<your-domain> TXT "mapae-verification=<token>"
```

### Well-known file

```text
https://<your-domain>/.well-known/mapae-host-verification.txt
```

with exact content:

```text
mapae-verification=<token>
```

Public Git repositories under the applicant's authenticated account may be
verified through repository ownership instead.

## Assignment and publication

After verification:

1. An unassigned shard is reserved in the registry.
2. The applicant receives the TXT shard, its SHA-256, and an optional HTML
   wrapper.
3. The host publishes the exact TXT file.
4. MAPAE verifies HTTP availability, line count, address format, and SHA-256.
5. Only then is the placement marked `VERIFIED_PUBLIC`.
6. The URL and timestamps are written to the public registry.

## Canonical hashing rule

The shard hash is calculated over the exact ASCII bytes:

```text
address-1\n
address-2\n
...
address-100\n
```

There is one final LF after the 100th address.

## Permission granted to participating hosts

Shrey Chouksey grants each verified participating host a non-exclusive,
revocable permission to reproduce and publicly display the exact assigned
MAPAE shard for research, verification, indexing, citation, and archival
purposes, with attribution to MAPAE and Shrey Chouksey.

This permission covers only the public-address shard and associated MAPAE
metadata. It conveys no private-key material, spending authority, fund
ownership, warranty, endorsement, or permission to misrepresent the data.

## Removal and reassignment

A host may withdraw. Historical exposure remains recorded, and an unavailable
shard may be reassigned to another consenting host. Reassignment does not erase
the earlier publication record.

## Pilot discipline

The pilot begins with 100 shards. It will expand only after the registration,
verification, assignment, and recheck workflow has been proven on real hosts.

**Maximum exposure. Maximum longevity. Maximum independent scrutiny.  
Zero private-key disclosure. Zero unauthorized activity. Zero spam.  
Zero deception. Zero circumvention.**
