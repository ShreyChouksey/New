# Million-Address Perpetual Adversarial Exposure Experiment (MAPAE)

**Version:** 1.0.0  
**Canonical date:** 2026-08-28  
**Operator:** Shrey Chouksey

MAPAE is a lawful, open research experiment concerning a fixed corpus of **1,000,000 Bitcoin mainnet native-SegWit (`bc1q...`) public addresses**. Its objective is **adversarial exposure rather than privacy**.

## Critical notice

This publication contains **public Bitcoin addresses only**. It contains no private keys, WIFs, seeds, mnemonics, entropy source, recovery material, extended private keys, signing secrets, or equivalent confidential material.

Do not send funds to an address merely because it appears here. Funding is a separate phase and is not implied by publication.

## Canonical corpus commitment

The normalized Version-1 corpus contains exactly **1,000,000 records**, one address per LF-terminated line.

```text
SHA-256: 5bb9320bc93f07e3129cb6ef5aee4da2c245e0ca11279d4963244bead79a90df
Size: 43,000,000 bytes
Records: 1,000,000
```

The originally uploaded byte stream omitted only the final LF:

```text
SHA-256: b1bd11238815f4f86aa3ba3cee7a5daaa52a6f7578531b805be2a5272bd73abd
Size: 42,999,999 bytes
```

## What is public in this branch now

- `tier-omega-100.txt` — 100 deterministic flagship challenge addresses.
- `verification-summary.json` — machine-readable address-layer validation summary.
- `CHALLENGE_RULES.md` — permitted and prohibited activity.
- `PROJECT_CHARTER.md` — governing research objective.

This branch is the first public beacon. The complete million-address package is being prepared for bulk-capable public archives and dataset hosts; this README does **not** falsely claim that the entire corpus is already present in this Git branch.

## Completed address-layer checks

- Valid addresses: **1,000,000**
- Invalid addresses: **0**
- Unique address strings: **1,000,000**
- Exact duplicate extra rows: **0**
- Unique decoded 20-byte witness programs: **1,000,000**
- Duplicate witness-program extra rows: **0**

These checks concern address syntax, checksum, witness-program decoding, uniqueness, and basic output-distribution measurements. They are not a claim of exhaustive historical blockchain-status verification.

## Open research invitation

Researchers, cryptographers, developers, automated scanners, and future systems are invited to examine the published material for:

- duplicate or malformed addresses;
- encoding or checksum defects;
- statistical or structural anomalies;
- correlations or derivation patterns;
- predictable adjacent or future outputs;
- prior public use or unexpected reuse;
- weaknesses traceable to the generation process;
- or a demonstrable ability to authorize a spend without being supplied the corresponding private key.

## Governing rule

**Maximum exposure. Maximum longevity. Maximum independent scrutiny. Zero private-key disclosure. Zero unauthorized activity. Zero spam. Zero deception. Zero circumvention.**

## Reporting

Open a GitHub issue with reproducible evidence, exact address or source-row references, code or commands used, hashes of derived artifacts, assumptions, impact, and limitations. Do not publish suspected private-key material in a public issue.

## Rights and attribution

Dataset and documentation © 2026 Shrey Chouksey. Public scrutiny, verification, citation, indexing, and responsible research analysis are expressly invited. A formal redistribution license has not yet been attached; no publication here should be interpreted as publication of secret-key material.