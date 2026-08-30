# API Slice 3 review — approved for classification with ownership corrections

## Decision

API approves the adversarial matrix and SBE may proceed to Slice 4
classification. The matrix did what the audit was meant to do: it confirmed
most broad fears are already contract-backed and isolated three specific,
reachable consumer seams rather than declaring the whole boundary unreliable.

## Classification corrections to carry into Slice 4

| Finding | Correct preliminary class | Reason |
|---|---|---|
| Generic `read_latest_sealed` terminal-ingress fallback | **API mapper defect** (with a missing negative test), not an SBE cross-artifact join gap | SBE already offers the required public exact-read and availability artifacts. The unsafe choice is API's optional no-ID fallback that treats generic latest discovery as enough to select terminal ingress. |
| Absent explicit readiness → inferred local continuation | **API mapper/interface defect** | SBE does not need a new fact. API must require an explicit validated readiness fact before writing readiness, or keep the state unknown/refused. |
| Bounded `retain_for_review` / `unsupported_retain_capacity` → `TERMINAL_CLOSED` | **API mapper defect**, high priority | No exact terminal result identity or invocation-bound terminal-review envelope exists at that mapping site. `unsupported` in particular has no positive permission to enter terminal ingress or select a latest result. |

No SBE release should be proposed for these three unless later source tracing
proves the API cannot consume an already-published fact.

## Review and outer product status

The matrix correctly separates valid v0.2 terminal editorial review from the
nonterminal lifecycle review branch. Current API behavior maps both to an outer
failed job/run/reading while retaining action-specific custody where required.
That may be an acceptable present product policy, provided it is documented as
an **API policy**, not inferred native terminality.

For the implementation handoff, preserve that outer-status policy unless the
owner explicitly chooses a distinct review product state. The immediate safety
correction is narrower: bounded review/unsupported must use the appropriate
review/refusal route and must never manufacture terminal evidence through
latest-result discovery.

## Slice 4/5 handoff requirements

- Split terminal ingress into exact-identity-required normal ingress and any
  separately named historical recovery path. Do not leave a generic
  `read_latest_sealed` default on a method whose caller can be a live worker.
- Make the readiness test boundary explicit: terminal/nonterminal outcome
  handling may differ, but no absent readiness value may be converted to
  `local_continuation_required=True` by fallback.
- Add the named due/not-due runtime spy as a valuable regression, but classify
  it as test coverage for an already contract-backed SBE-owned subset, not as
  a missing SBE contract.
- Every implementation plan should prove the old bounded `unsupported` branch
  cannot call terminal ingress, mutate outer terminal state via a fabricated
  terminal result, or release action-level custody.

No source, provider, retained-QA, deployment, or configuration mutation was
made by this review.
