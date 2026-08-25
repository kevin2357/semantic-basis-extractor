# Slice 4 — Whole-Cycle Binding Integrity Fence

Status: implemented and source-qualified; installed-wheel/release qualification pending

## Public correction

Before SBE selects a bounded provider-retrieval subset, it now validates every
retained provider-backed action against the native run identity and the complete
public binding shape.

The preflight validates:

- the exact closed binding field set;
- native `run_id` equality;
- profile and request SHA-256 syntax;
- prepared revision type, range, and relationship to current native revision;
- closed provider-custody stage;
- nonempty route and model;
- interactive/Batch service mechanism spelling;
- positive maximum output;
- nonnegative commitment; and
- nonempty versioned price-book identity.

Any contradiction produces one whole-cycle `review_required` result with zero
retrievals. It has no result checkpoint because no reconciliation result is
published. The complete authoritative workspace remains byte-identical.

The closed v0.2 result schema has no refusal-reason field. Its supported
machine-readable signal is therefore `outcome: review_required`. The exact closed
reason `provider_binding_integrity_mismatch` is emitted separately as a
failure-isolated, non-authoritative `execution.failed` diagnostic event with no
bindings, provider payload, subject data, or action identifiers. Consumers must
not infer the reason from text logs or treat the event as execution authority.

## Why whole-cycle refusal

A binding/native-identity mismatch is not ordinary per-member provider variance.
It calls the authority and integrity of the retained inventory into question. SBE
therefore does not skip only the malformed action and continue polling other
members.

This preflight runs before native due-subset selection. A malformed fifth or sixth
member consequently prevents retrieval of an otherwise valid first-four wave.

## Preserved behavior

- Internally consistent inventories retain native maximum-four selection and 4+2
  reconciliation.
- Retrieval remains GET-only.
- No authority/grant input is admitted.
- Provider identity conflict after a legitimate GET retains its existing native
  review behavior.
- Incomplete snapshots continue to refuse before this preflight.

## Qualification

- Malformed first member: `review_required`, zero GET, zero publication,
  byte-identical workspace.
- Malformed fifth member: the same whole-cycle refusal before the first four GETs.
- Focused bridge/lifecycle/capacity result: 46 passed, 1 installed-wheel opt-in
  test skipped.
- Complete repository result: 592 passed, 29 existing environment/opt-in skips.
- External provider calls, creates, spend, and retained-Aster access: zero.
