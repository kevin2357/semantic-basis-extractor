# AstroWoof Natal Authoring 0.4.28

Status: candidate qualified; tag and publication require explicit owner approval

SBE 0.4.28 makes exact-interactive editorial review a complete native handoff
rather than a process-exit inference. Before exit 2, the public command now seals
an invocation-bound `astrowoof.native_execution_result.v0.2`, validates its
canonical v0.1 publication receipt, and emits a closed command-result envelope.

The v0.2 result separates the editorial `review_required` decision from action
custody. Its ordered projection distinguishes terminally accounted actions,
durable provider work that is reconciliation-only, unused authorized actions that
remain providerless-denial-only, and ambiguity or contradiction requiring review.
It explicitly forbids new provider creation after the editorial terminal decision.

Custody follow-up preserves that decision. Retrieval of an already durable
provider identity publishes a journal-contiguous successor and never reopens
authoring. Existing providerless-denial operations remain the only native evidence
that unused authority was denied. The original review result and receipt remain
immutable throughout both operations.

The release adds the provider-free `astrowoof-terminal-review-qa` installed-wheel
qualification, packaged schema, deterministic receipt fixture, and public Python
reader/validator/runner. It also aligns the post-fan-in inspection-bundle JSON
Schema with the already canonical `work_<24 hex>` operation-key identity exposed
by its runtime and Python validator.

## Candidate qualification

- Artifact source commit: `25e0be9ce670b3643f47f6cdd0a71de7d00ad11e`.
- Fixed build epoch: `1787911516`.
- Strict broad source suite: 860 passed; 3 expected skips; 750.136 seconds.
- Two byte-identical candidate wheels; SHA-256
  `365ab0bc63a03e2c9c06638631b5e47c78ce494331f014741472a3e59fa58fb4`.
- Generic installed release smoke and lifecycle smoke: pass.
- Installed terminal-review, post-fan-in, and adversarial qualifications: pass.
- Terminal-review receipt SHA-256:
  `6289962655c36e4c2cab5828c30499a75155094c0437898c7f68fdf4e0afeb6d`.
- Exact installed dependency: `semantic-projection-core==0.11.1`.
- External provider/network calls and spend: 0.
- Retained Pippin/Duchess access or mutation during implementation/qualification: 0.

This evidence recommends the candidate for final API and owner review. It does not
authorize tagging, publication, deployment, or retained-run recovery.
