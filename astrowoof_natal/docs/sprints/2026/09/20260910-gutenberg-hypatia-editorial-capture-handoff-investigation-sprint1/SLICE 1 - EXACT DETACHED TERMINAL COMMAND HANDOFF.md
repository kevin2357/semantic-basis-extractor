# Slice 1 — Exact Detached Terminal Command Handoff

## Status

SBE producer correction implemented provider-free and ready for joint review.

## Correction

`reconcile_authoring_provider_cycle` now accepts an optional terminal-command
output callback. When that exact reconciliation invocation publishes a native
result, it immediately derives an existing public command contract from the
returned `sealed` result/receipt pair:

- `delivery_complete` produces
  `astrowoof.terminal_delivery_command_result.v0.1`;
- `review_required` produces
  `astrowoof.terminal_review_command_result.v0.1`;
- every nonterminal outcome produces no terminal command handoff.

The semantic-closure CLI supplies its normal structured output callback. This
preserves the detached provider-reconciliation exit convention while adding
the missing same-invocation command envelope to stdout JSONL.

The requested CLI regression exposed one deeper prerequisite: detached
reconciliation had published `review_required` through native result v0.1.
That version does not carry the closed custody fields required by the terminal
review command contract. Reconciliation now requests native terminal-review
v0.2 whenever its exact cycle result is `review_required`; delivery and
nonterminal publication versions are unchanged.

## Identity and side-effect fence

- The command is built only from the in-memory return value of the publication
  performed by that invocation.
- There is no directory scan, latest-result discovery, filename inference,
  synthetic identifier, or mutable-state reconstruction.
- Existing public command validators bind invocation, result, receipt, native
  run, outcome, hashes, and custody semantics.
- Nonterminal detached exit-3 paths still emit no terminal handoff and retain
  their existing behavior.
- No provider, R2, retained workspace, API state, packet builder, or Better
  Stack operation was used.

## Alloy impact

Retrospective assessment: no model change or rerun is required. This correction
changes result versioning, same-invocation command serialization, and transport
identity without changing editorial lineage, deck selection/delivery, or any
modeled ownership relationship. See
[0.4.58 and 0.4.59 Alloy impact assessment](../20260907-editorial-review-packet-collection-contract-sprint1/POSTSCRIPT%20-%200.4.58%20AND%200.4.59%20ALLOY%20IMPACT%20ASSESSMENT.md).

## Provider-free qualification

Focused source-tree qualification passed after the API-requested CLI addition:

```text
24 tests run
OK (4 skipped)
```

Coverage includes exact review emission, exact delivery emission, no emission
for provider-pending publication, the real terminal Batch reconciliation path,
and the existing terminal command contract suite. The CLI-level regression
also proves that detached review exits `3`, stdout JSONL contains exactly one
valid review command bound to the just-published v0.2 result/receipt plus the
ordinary reconciliation result, and a nonterminal detached exit-3 invocation
contains no terminal command.

## API companion work

SBE now supplies the missing original-invocation evidence. API still owns two
consumer changes under its review fence:

1. accept the exact terminal-review command envelope on the detached
   provider-reconciliation exit-3 route without changing ordinary nonterminal
   exit-3 behavior;
2. establish accepted-delivery authority from the fresh terminal-delivery
   command before publication, preserving that same result identity only if a
   publication retry is required.

The later delivery-validation cycle remains non-authoritative as an identity
source.
