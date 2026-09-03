# API review — Slice 1 optional-stage adoption invariant

## Decision

Approved to proceed with a provider-free production-boundary reproduction and then the narrow native repair.

The checkpoint evidence resolves both branches:

- Pastiche is a legitimate `theme_group_assignment` hard rejection. The prior trace’s advisory-only display was incomplete observability, not a policy or orchestration defect.
- Puff is a native optional-stage completed-evidence adoption defect. Reconciliation has safely retrieved and retained the exact polish response, but that response was never joined to the exact stored `SUBMITTED` consumer attempt. The subsequent ambiguity, retained intent, unconsumed local operation, and terminal contradiction are therefore expected containment behavior, not independent faults.

No API intake or custody-rule change is indicated by these findings. API must continue treating the native `review_required` receipt as terminal while the retained provider action remains separately visible for operational disposition.

## Frozen invariant

For an ordinary-v2 optional-stage action, a consumer that has an exact completed reconciliation artifact **must adopt that artifact into its exact stored consumer attempt before any code path may re-enter provider submission for that action**.

“Exact” must prove at least the action identity, bound provider identity, response artifact identity/digest, and the action/request/grant/inventory binding already established by the v2 authority. Adoption must be idempotent: a repeated reconciliation or continuation may observe an already-adopted attempt, but must neither create another provider request nor attach the response to a different attempt.

After successful adoption, the normal deterministic consumer path must be able to record accepted/rejected local processing, report the action, retire its intent, and consume the corresponding local-work operation. A malformed, conflicting, or nonexact completed artifact must still fail closed and retain custody; it must not be opportunistically adopted.

## Scope

Start with ordinary-v2 optional-stage consumers only. Characterize, rather than assume, whether polish, qualitative critic, and qualitative candidate each possess the same topology:

1. durable `SUBMITTED` consumer attempt;
2. ordinary-v2 detach/reconcile path;
3. exact completed-evidence artifact; and
4. a re-entry path that could otherwise reach provider submission before adoption.

Implement the shared helper only for routes proven to share all four properties. Do not broaden to bounded or Batch routes merely by state-name similarity; add them only if their own source topology demonstrates the same seam and their route contracts can be covered by the same proof.

## Required reproduction/qualification assertions

- First reproduce Puff’s unpatched failure through the real ordinary-v2 production boundary without provider I/O.
- Prove the patched exact join updates the intended stored attempt and no other attempt.
- Prove no second provider create/submission occurs after completed evidence is available.
- Prove reported action, intent retirement, and consumed operation key advance together only after successful exact adoption and downstream processing.
- Prove repeated replay is idempotent.
- Preserve refusal behavior for mismatched action/provider/response/binding evidence.
- Include one route-inventory disclosure showing which optional stages are covered, excluded, or require a distinct later contract.

The Pastiche hard-code logging improvement is useful but should remain separate from this repair unless it can be added without expanding behavioral scope.
