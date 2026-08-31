# API final review — 0.4.34 candidate

## Decision

**API review approves the 0.4.34 candidate for owner-authorized commit, tag,
and publication.**

The candidate's installed qualification is reproducible and demonstrates the
production lifecycle property that failed in Delerium: a completed v2 intent is
retired in the published coordinator checkpoint; exact replay performs zero
provider work; and a fresh successor receives distinct authority and exactly
one create.

## Boundary assessment

- No API request/grant/lifecycle result schema changed.
- Existing public v3 `exact_replay` semantics remain the consumer result.
- The added qualification command/reader/validator/schema are provider-free,
  temporary-workspace-only validation tooling and do not accept production
  coordinates, credentials, or authority documents.
- SBE continues not to claim API reservation, lease, slot, or global-capacity
  facts.

## Evidence reviewed

- frozen candidate version `0.4.34`;
- two byte-identical wheels, SHA-256
  `20a64e366840e143f1f9cb6cd936a7dd15341dc2041562e8f33860eb4ed70b2d`;
- two byte-identical installed qualification receipts;
- installed SBE `0.4.34`, SPC `0.11.1`, and clean `pip check`;
- installed release smoke plus v2, post-fan-in, terminal-review, and
  intent-retirement qualifications passed; and
- final affected source matrix: 49 passed, with only the documented optional
  schema skips.

This approval does not authorize retained Delerium recovery, QA resume, or
provider work. Those remain separate decisions after the released wheel is
available and the API side has been assessed.
