# Slices 2–3 — Typed Finalization Review Implementation

Status: complete.

## Runtime behavior

Assembly now distinguishes deterministic authored-evidence contradictions with
`AssemblyContractError`, a compatibility-preserving `ValueError` subclass.
Only that type is caught at the finalization coordinator boundary.

When every paid action is terminally accounted for, the coordinator:

1. records `FAILED_REQUIRES_REVIEW` and a durable finalization-contract terminal
   transition;
2. checkpoints the resulting native state;
3. publishes native-result v0.2 with
   `review_required / finalization_contract_invalid`;
4. validates final action custody and complete action-binding inventory;
5. emits the canonical invocation-bound terminal-review command envelope; and
6. exits 2 only after publication.

An exact rerun derives the cause from the durable transition and returns the
same sealed result/receipt identity without retrying assembly.

## Fail-closed distinctions

- `OSError` and other operational failures remain ordinary failures and do not
  mint semantic review authority.
- A `WAITING`, `SUBMITTING`, providerless, or ambiguity action prevents
  `finalization_contract_invalid` from claiming final custody.
- The Python validator and packaged JSON schemas both recognize the new closed
  cause. Semantic validation additionally requires `custody_finality = final`
  for this cause, even after all digests are recomputed.
- Logs retain only exception class and sanitized fingerprint. Authored payload
  and exception detail are absent from the public result and logs.

## Consumer boundary

The existing terminal-review command-result schema remains unchanged. API joins
the result's complete action-disposition inventory to its immutable per-action
bindings and treats the exact invocation-returned envelope as primary authority.
Result-ID availability lookup remains recovery-only.
