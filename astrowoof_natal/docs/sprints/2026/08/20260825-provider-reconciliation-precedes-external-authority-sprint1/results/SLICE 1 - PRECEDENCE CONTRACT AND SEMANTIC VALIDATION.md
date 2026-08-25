# Slice 1 — Precedence Contract and Semantic Validation

Date: 2026-08-25
Status: complete; awaiting API review before selector implementation

## Compatibility decision

Lifecycle inspection v0.5 and temporal lifecycle v0.6 are tightened in place.
The previously accepted combinations were internally contradictory; they were not
legitimate scheduling choices that require a new schema version.

No new public command, state, result schema, or API routing rule is introduced.

## Closed precedence predicates

The v0.5 Python semantic validator now rejects `await_external_authority` whenever
the same inspection retains provider custody:

- `retained_provider_custody_precedes_authority`; and
- additionally `provider_fan_in_precedes_authority` when custody is classified as
  `completed_evidence_pending_local_work`.

These names are deterministic, redacted semantic predicate identifiers. They carry
no provider payload, binding, credential, response text, or subject data.

The v0.6 semantic validator independently rejects a rehashed checkpoint basis that
contains both an external-authority request and retained provider-custody actions.
This prevents a consumer from constructing a structurally valid digest around the
same contradiction.

## Valid public combinations

| Condition | Capacity/decision | Command |
|---|---|---|
| Provider custody due | local cycle eligible | `provider_reconciliation_cycle` |
| Provider custody not due | release until native `not_before` | `provider_reconciliation_cycle` |
| Completed evidence needs fan-in | local cycle eligible | `ordinary_resume` |
| No preceding custody/fan-in; prepared actions valid | awaiting authority | `await_external_authority` |
| Contradiction/ambiguity/integrity failure | retain/review | `none` |

The due action subset remains SBE-selected and bounded to four. API neither selects
nor reconstructs members.

## Authority identity across observation time

Authority-request digest stability remains valid for an authority-only checkpoint
basis. Focused tests now prove this using a real snapshot-valid ordinary-action
workspace. They no longer manufacture a request over provider-bound actions.

For a provider-custody basis, authority state remains absent at both not-due and due
times. Trusted time may change only reconciliation eligibility, the SBE-selected due
subset, and derived `not_before`. Retrieval/fan-in must create a new checkpoint basis
before an authority inventory may appear.

## Transitional behavior before Slice 2

The selector still constructs the now-invalid not-due/fan-in branches. During this
review pause the public validator therefore raises rather than publishing unsafe
evidence. Slice 2 will reorder native classification so the public reader again
returns a valid reconciliation/fan-in decision. This is intentional fail-closed
sequencing, not a release candidate state.

## Diagnostic contract for Slice 2

Existing failure-isolated event/log surfaces will report only:

- provider action count;
- due/selected count;
- prepared action count;
- selected command and closed reason; and
- one of the closed precedence/refusal predicate names above.

No new event schema or authoritative log meaning is required.

