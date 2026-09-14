# API final release review — SBE 0.4.61

## Decision

**Technical approval granted for owner-authorized tagging and publication.**

The approved immutable tag target is:

`477cfa2491f33377f1a873772c5e465c588f0741`

The approved wheel is:

`astrowoof_natal_authoring-0.4.61-py3-none-any.whl`

- Size: `1,383,877` bytes
- SHA-256: `8dd151fced3fc7823ef914c7642798a977eca93d19b1136bf34da55b589ef723`

This review does not authorize any QA deployment, live quarantine request,
provider operation, R2 operation, workspace mutation, or lifecycle mutation.

## Basis

SBE's release-lock record establishes:

- the exact retained Bodoni generation-3 local restore now passes the public
  relocated reader with the expected `provider_pending_known_identity` /
  `permitted` / `known_provider_operation_pending` assessment;
- the reader preserves authority/wrapper validation and all 387 workspace files
  byte-identically;
- canonical `PurePosixPath(relative).parts` order reproduces the original
  Linux-authored ordered inventory, while duplicate/content drift remains
  strictly refused;
- two exact-lock builds are byte-identical; and
- the full manifest suite passes: 1,192 passed, 60 expected skips.

## Independent API consumer gate

On 2026-09-14, API independently hashed the retained exact-lock wheel and ran
its real provider-free installed-wheel relocated-reader/writer qualification:

```json
{
  "provider_operations": 0,
  "provider_spend_usd": 0,
  "sbe_receipt_sha256": "f0d1d7c353b08c533d861471e08fc959f875f9596a080c692f17c2a09e0e09f8",
  "sbe_version": "0.4.61",
  "schema_version": "astrowoof.api_sbe_relocated_operator_disposition_qualification.v1",
  "wheel_sha256": "8dd151fced3fc7823ef914c7642798a977eca93d19b1136bf34da55b589ef723",
  "writer_completed": true
}
```

The gate installs only this exact wheel into a disposable local target, uses an
in-memory API fixture, and proves the validated wrapper reaches the API writer
without provider or spend activity.

Focused API regression also passed: 45 passed, 1 expected source-only wheel
skip; Ruff and `git diff --check` passed. The skipped test is the retained
0.4.60 path, not the reviewed 0.4.61 candidate.

## Remaining rollout boundary

Publication makes the API Sprint 90 Slice 2B local Bodoni correction eligible
to advance to its separately authorized release-intake and post-rollout QA
exercise. It does not itself complete that exercise.
