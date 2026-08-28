# Million-Address Perpetual Adversarial Exposure Experiment (MAPAE)

**Version:** 1.0.0  
**Canonical date:** 2026-08-28  
**Operator:** Shrey Chouksey

MAPAE is a lawful, open research experiment involving **1,000,000 public Bitcoin mainnet Bech32 (`bc1q...`) addresses**. Its purpose is long-lived adversarial scrutiny rather than privacy.

## Critical notice

This publication contains **public Bitcoin addresses only**. It contains no private keys, WIFs, seeds, mnemonics, entropy source, recovery material, extended private keys, signing secrets, or equivalent confidential material.

Do not send funds unless you independently understand and accept the risks. The initial publication treats the addresses as unfunded public research targets.

## Canonical public records

- **Long-term challenge and reporting issue:** https://github.com/ShreyChouksey/New/issues/15
- **Publication pull request:** https://github.com/ShreyChouksey/New/pull/11
- **Dedicated public branch:** `mapae-v1-publication`
- **Structured public project directory:** `MAPAE/`

Issue #15 is the canonical reporting and discussion surface. The branch contains the structured project record, address files, challenge rules, project charter, verification summary, and corpus commitments.

## Canonical corpus commitment

- Records: **1,000,000**
- Normalized form: one lowercase address per line, with a final LF
- Normalized size: **43,000,000 bytes**
- Canonical SHA-256:

```text
5bb9320bc93f07e3129cb6ef5aee4da2c245e0ca11279d4963244bead79a90df
```

The originally uploaded byte stream omitted the final LF while still containing 1,000,000 logical records. Its exact-byte SHA-256 is:

```text
b1bd11238815f4f86aa3ba3cee7a5daaa52a6f7578531b805be2a5272bd73abd
```

## Completed address-layer checks

- Valid Bitcoin mainnet Bech32 addresses: **1,000,000**
- Invalid addresses: **0**
- Unique address strings: **1,000,000**
- Exact duplicate extra rows: **0**
- Unique decoded 20-byte witness programs: **1,000,000**
- Duplicate witness-program extra rows: **0**

These checks do not claim exhaustive verification of every address against all historical blockchain activity.

## Live public exposure — GitHub Stage 1

Exactly **1,100 distinct individual addresses** are presently published in human-readable form in this public GitHub branch:

- `tier-omega-100.txt` — 100 deterministic Tier Ω flagship candidates
- `tier-a-public/tier-a-0001-0100.txt`
- `tier-a-public/tier-a-0101-0200.txt`
- `tier-a-public/tier-a-0201-0300.txt`
- `tier-a-public/tier-a-0301-0400.txt`
- `tier-a-public/tier-a-0401-0500.txt`
- `tier-a-public/tier-a-0501-0600.txt`
- `tier-a-public/tier-a-0601-0700.txt`
- `tier-a-public/tier-a-0701-0800.txt`
- `tier-a-public/tier-a-0801-0900.txt`
- `tier-a-public/tier-a-0901-1000.txt`

The ten Tier-A files are non-overlapping and contain 100 addresses each. The Tier Ω cohort and an initial Tier A cohort are also embedded in issue #15, creating an additional independently indexed presentation.

Additional files:

- `verification-summary.json` — machine-readable validation summary
- `PART_SHA256SUMS` — commitments for ten prepared 100,000-address canonical corpus parts
- `CHALLENGE_RULES.md` — permitted and prohibited activity
- `PROJECT_CHARTER.md` — governing research objective

The complete one-million-address corpus is cryptographically fixed by the canonical SHA-256 above. A compressed full-corpus artifact and complete public publication package have been prepared separately for a bulk-capable public archive or dataset host. This record deliberately distinguishes the fixed one-million-address corpus from the 1,100-address cohort already directly visible on GitHub.

## Open challenge

Researchers, cryptographers, developers, automated scanners, blockchain analysts, and future systems are invited to examine the exposed addresses and corpus commitment for:

- duplicates or malformed encodings;
- checksum or witness-program defects;
- statistical or structural anomalies;
- correlations, derivation patterns, or predictable adjacent outputs;
- prior public use or unexpected reuse;
- weaknesses traceable to the generation process;
- or a demonstrable method of controlling an address without being supplied its corresponding private key.

No unauthorized access, malware, phishing, deception, spam, circumvention, fabricated commerce, denial-of-service activity, or attacks against unrelated third parties are part of this experiment.

## Governing rule

**Maximum exposure. Maximum longevity. Maximum independent scrutiny. Zero private-key disclosure. Zero unauthorized activity. Zero spam. Zero deception. Zero circumvention.**

## Reporting

Use issue #15 for the canonical reporting thread, or open a separate issue for a substantial finding. Include reproducible evidence, exact address values or corpus row references, commands or code used, assumptions, impact, limitations, and hashes of derived artifacts. Do not publicly post suspected private-key material.

## Rights and attribution

Dataset and documentation © 2026 Shrey Chouksey. Public scrutiny, verification, citation, indexing, and responsible research analysis are expressly invited. A formal redistribution license has not yet been attached; publication of public addresses does not publish or waive rights in any private-key material.
