# Release candidate — SBE 0.4.45

## Scope

This patch repairs a narrow ordinary-v2 dispatch seam found in Hound. During
reconciliation, a live intent is now retired within the same native checkpoint
only after every exact member has durably adopted complete, reported response
evidence and has neither provider custody nor ambiguity. The CLI refuses, with
no provider I/O, when a fresh authority encounters that exact stale completed
intent before the checkpoint is repaired.

It does not manufacture API authority, reconstruct API private state, resume a
retained run, or change initial-wave, Batch, or bounded dispatch semantics.

## Candidate identity and qualification

- Version: `0.4.45`
- SPC compatibility: `semantic-projection-core==0.11.1`
- Controlled wheel SHA-256:
  `bcee274df15e877ca54efecbada15bed8565a604493689fdc9790e6178aeb42b`
- Reproducibility: two byte-identical controlled builds
- Source focused suite: 17 provider-free tests passed
- Installed qualification: public v2 intent-retirement QA and the three-case
  stale-intent CLI regression passed outside the checkout
- Packaged resources: v5 dispatch-result and v4 command-result readers resolved
  their exact schemas from the installed wheel
- Dependency audit: exact SPC `0.11.1` plus declared `jsonschema`; `pip check`
  passed with no broken requirements
- Provider/R2/retained-QA work: none

## Release decision

API technical review and owner approval were received. Release commit
`6cba751bc8d90d1561fecae7ede89d90ba29ff15` was tagged as
`astrowoof-natal-authoring-v0.4.45`, pushed to `origin`, and published on
GitHub. The downloaded published wheel matched the qualified SHA-256 exactly.

## Deployment sequencing

Publication alone does not authorize a QA-fleet rollout. API must first add and
qualify intake for this exact closed v4/v5 refusal pair. Until then, an unknown
result remains fail-closed: it must not be treated as success, retried, or used
to create provider work.
