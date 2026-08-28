# API Slice 5 Review — Installed Terminal Review Qualification

## Status

**Approved in principle; one narrow receipt-validator correction is required
before Slice 6/release preparation.** The installed-wheel qualification is the
right shape and proves the intended public path without provider/network access,
retained-QA access, or spend.

## What is approved

- The wheel exposes a small, provider-free public qualification surface and
  console command rather than asking API to reconstruct private workspace state.
- The qualification exercises the real exact-interactive public command: a
  validated v0.2 review result, canonical v0.1 receipt, and invocation-bound
  command-result envelope are published before exit 2.
- It then uses one scripted retrieval-only GET, performs the existing supported
  providerless denial, and reaches closeout without reopening authoring.
- The evidence covers immutable v0.2 predecessor bytes, contiguous custody-only
  successor lineage, v0.1 readability-but-not-v0.2 masquerade, receipt-mutation
  refusal, protected-sentinel exclusion, and fresh-workspace reproducibility.
- Scope remains correctly exact-interactive only. Batch/bounded and retained
  Pippin/Duchess workspaces remain untouched.

## Required narrow correction

`validate_terminal_review_qualification()` correctly freezes receipt shape and
digest, but it does not yet require the semantic values that Slice 5 says the
receipt proves:

- `reconciliation_action_ids` must be the exact one-member retained-provider
  inventory;
- `providerless_denial_action_ids` must be the exact one-member denied inventory;
- `successor_outcome` must be `review_required`; and
- `providerless_denial_outcome` must be `applied`.

Likewise, the reported action identity should be checked as the fixed scripted
identity (or, if the fixture is intentionally generalized, checked against a
separately explicit ordered inventory in the receipt). At present a caller can
change those fields and recompute `receipt_sha256`; the public validator would
accept the altered receipt despite the public documentation asserting those
facts.

Please make the validator assert those exact deterministic qualification values
and add one mutation test covering this semantic path (a recomputed-digest altered
receipt is the useful case). This is a small fixture/validator correction, not a
change to the terminal-review runtime or the API handoff design.

## After correction

I expect the installed-wheel gate can proceed to Slice 6. The companion API
sprint should wait for the immutable release identity, then consume the exact
v0.2 result and command-result envelope before interpreting exit 2.

## Re-review result

**Correction verified and Slice 5 is approved.**

The validator now requires the deterministic reported, reconciliation-only, and
providerless-denial action inventories, `successor_outcome=review_required`, and
`providerless_denial_outcome=applied`. The new mutation test changes each field,
recomputes the receipt digest, and proves the public validator still fails closed.
The rebuilt clean wheel also rejects that rehashed mutation.

SBE may proceed with Slice 6 broad regression and release preparation. This
approval does not itself authorize tag/publication, deployment, provider work, or
retained-QA mutation; those remain separate final gates.
