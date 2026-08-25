# AstroWoof Natal Authoring 0.4.22

Status: release candidate qualified; tag/publication pending owner authorization

SBE 0.4.22 corrects lifecycle next-command precedence when one workspace contains
both retained provider work and a later prepared paid action.

Retained provider custody now always precedes new external authority. Due work uses
SBE's bounded reconciliation subset; not-due work releases local capacity until the
native lower bound; completed provider evidence is consumed by deterministic fan-in
before a later authority request appears.

Lifecycle v0.5 and temporal lifecycle v0.6 remain the public contracts. No new API
state, command, routing inference, paid operation, retry, or provider idempotency
claim is introduced.

## Qualification

- Artifact source commit: `f68c7ac0d161f8bac81a72e01824d18d7627a88f`.
- Fixed build epoch: `1787649544`.
- Full source suite: 700 passed; 36 expected environment/opt-in skips.
- Two byte-identical candidate wheels; SHA-256
  `5ead8d317d81bbcc5c38132c3b81d2ca380911088f4b8c6866dc3f333003f47d`.
- Generic installed release smoke: pass with 50 cards and four summaries.
- Installed provider-pending qualification: pass; 4+2 retrieval and post-fan-in
  authority assertion passed.
- Exact installed dependency: `semantic-projection-core==0.11.1`; `pip check` pass.
- External provider/network calls and spend: 0.
- Frozen QA cohort access/mutation: 0.

Before a new paid QA cohort, AstroWoof API and its worker image must pin this fresh
artifact together, deploy/attest the matching runtime and profile configuration,
and complete the separate release-pair qualification.
