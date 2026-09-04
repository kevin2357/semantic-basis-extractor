# Plan — terminal-dominance handoff

**Status:** Slices 0–3 complete; final `0.4.46` wheels are byte-identical and
their installed-wheel qualification passed. Awaiting final tag/publication
approval.

## Slice 0 — Source and trace contract freeze

Map terminal-result publication, optional-stage preparation, lifecycle
inspection, and provider-cycle result construction. Prove the exact ordering
that permits an optional action after `DELIVERY_COMPLETE` or local progress
after `FINAL_QA_FAILED`. Freeze the public result fields API may consume.

Do not infer terminal dominance from a status label or from the word
`review_required`: distinguish an exact sealed terminal result with resolved
native custody from a review result that still truthfully retains provider
reconciliation custody. Map both ordinary reconciliation coordinator paths
before choosing a shared gate. The frozen consumer surface must bind result ID,
receipt ID/digest, terminal outcome/reason, checkpoint/snapshot identity, and
the post-cycle no-new-work assertion.

## Slice 1 — Terminal-dominance implementation

Place one narrow terminal gate before optional-stage selection/authority
preparation. Once terminal, return the exact sealed terminal result and do not
construct a successor request or action inventory. Preserve strict typed
refusal for contradictory terminal metadata.

## Slice 2 — Provider-free reproduction matrix

Add a faithful fixture/harness covering:

1. direct authoring -> `DELIVERY_COMPLETE` -> delivery handoff;
2. exact interactive reconciliation -> terminal finalization;
3. exact Batch reconciliation -> terminal finalization; and
4. finalization conclusion plus a pre-existing local successor (typed review,
   not an ordinary resume).

Assert zero new provider action, request, or grant after terminality, and
assert stable exact result/receipt identities.

Include a control where review-required evidence retains real provider custody:
that path may reconcile already-durable work but must not be mislabeled as a
fully terminal handoff. This preserves the prior mixed-custody boundary while
the terminal-dominance cases prove that no new qualitative work is selected.

## Slice 3 — Packaged-boundary qualification and release

Exercise the installed/package command path using the provider-free fixtures.
The receipt must be joined through the published result/receipt/snapshot
identity—not a latest-result lookup—and must distinguish fully resolved custody
from reconciliation-only retained custody. Run relevant focused and broad
tests, document cross-repo contract evidence, and pause for release review. A
new immutable SBE release is expected if source code changes.
