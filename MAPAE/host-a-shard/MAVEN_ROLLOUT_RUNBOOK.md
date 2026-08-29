# MAPAE Host-a-Shard — MAVEN Rollout Runbook

## MAVEN operating standard

- **Measured:** no exposure is counted without a concrete, publicly retrievable URL.
- **Auditable:** consent, authority verification, assignment, checksum and recheck history are recorded.
- **Verified:** exact bytes, 100-line count, final LF, address form and SHA-256 must pass.
- **Ethical:** only owned, authorized or expressly opted-in destinations are used.
- **Networked:** expansion prioritizes independently administered infrastructure rather than duplicate pages inside one ecosystem.

## Phase 0 — completed

- Fixed the canonical one-million-address corpus.
- Excluded the 1,100-address base cohort already directly public.
- Deterministically partitioned the remaining 998,900 addresses into 9,989 shards.
- Generated one SHA-256 per 100-address shard.
- Published a 100-shard pilot manifest and a ten-shard Wave-1 manifest.
- Published the host protocol, registry, machine-readable status and verifier.
- Published and verified `MAPAE-HAS-00001` on two operator-controlled GitHub repositories as a reference proof.

The reference shard added 100 unique public addresses, bringing current direct exposure to 1,200. It is not an independent-host achievement.

## Phase 1A — first independent host

**Gate:** do not fan out until one real outside operator completes the full lifecycle.

1. Volunteer registers through issue #20.
2. MAPAE verifies that the volunteer controls or is authorized to publish at the destination.
3. Reserve `MAPAE-HAS-00002`.
4. Supply the exact TXT bytes and declared SHA-256.
5. Volunteer stores an actual public copy.
6. Retrieve the public file without authentication.
7. Verify 4,300 bytes, 100 lines, final LF, address form, internal uniqueness and SHA-256.
8. Add the destination to `HOST_REGISTRY.csv` as `VERIFIED_PUBLIC`.
9. Recheck after 24 hours and again after seven days.

### Phase-1A exit gate

All must be true:

- one independently administered destination;
- recorded consent and authority proof;
- exact hash match;
- public access without login;
- 24-hour recheck passed;
- no conflicting registry state.

## Phase 1B — complete Wave 1

After Phase 1A passes, assign `MAPAE-HAS-00003` through `MAPAE-HAS-00010` one at a time.

Target:

- nine independent hosts;
- nine independently hosted shards;
- 900 newly exposed addresses outside operator-controlled repositories;
- provider and administrative diversity;
- zero unexplained checksum mismatches.

Initial cap: one shard per new host unless there is a documented operational reason for more.

### Wave-1 exit gate

- all nine placements verified;
- at least five independent administrative operators;
- at least three infrastructure providers or self-hosted stacks;
- seven-day survival rate of at least 95%;
- registry complete for every placement.

## Phase 2 — 100-shard pilot

Target: use the full pilot pool only after Wave 1 survives its rechecks.

- Expand in batches of ten shards.
- Prefer different domains, owners, countries, hosting providers and repository forges.
- Reject hotlinks, iframes, private links and destinations that cannot preserve exact bytes.
- Recheck daily for the first three days, then weekly for one month.

### Pilot exit gate

- 100 pilot shards assigned or intentionally held in reserve;
- at least 50 independently administered destinations;
- no single provider carries more than 25% of counted placements;
- at least 9,000 of the 10,000 pilot addresses remain verifiably public after 30 days.

## Phase 3 — controlled full coverage

Target: first direct publication of all remaining addresses.

- Scale from 100 to 1,000 shards only after the pilot exit gate.
- Then scale in audited waves, never by blind bulk submission.
- Permit proven hosts to take multiple shards while preserving administrative and provider diversity.
- Maintain reserve hosts for dead links.
- Preserve historical records when a host withdraws or disappears.

## Phase 4 — redundancy and longevity

- Replicate Tier Ω and Tier A deliberately.
- Replicate a statistically selected sample of ordinary shards.
- Add full-corpus archival copies on legitimate research, dataset and content-addressed systems.
- Measure exposure-years, host survival and independent administrative domains.

## Counting rules

A placement counts only when:

- consent or authority is recorded;
- the destination is public without login;
- an actual copy is hosted by the assigned operator;
- exact-byte or documented normalized-content verification passes;
- the public URL and verification timestamp appear in the registry.

A link, iframe, redirect, private Drive file, failed upload, merely reserved assignment or operator-controlled duplicate does not count as an independent host.

## Stop conditions

Pause expansion immediately if:

- any private-key or recovery material is suspected to have entered a publication package;
- a shard hash differs without a documented normalization explanation;
- destination authority is disputed;
- the process generates complaints suggesting unsolicited or misleading use;
- registry state cannot be reconciled.

**Slow expansion is a feature. Every verified independent host matters more than hundreds of unverified placements.**
