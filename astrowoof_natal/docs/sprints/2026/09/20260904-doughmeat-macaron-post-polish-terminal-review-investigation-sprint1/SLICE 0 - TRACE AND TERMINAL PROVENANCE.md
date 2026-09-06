# Slice 0 — Trace and terminal provenance

## Result

The available evidence supports ordinary bounded polish exhaustion for both
runs. It does not presently support a runtime correction.

Both runs completed the same lawful sequence:

1. six initial provider actions reconciled and were adopted;
2. final assembly passed structural validation but retained lint findings;
3. polish attempt 1 was authorized, dispatched, reconciled, and joined to its
   exact submitted attempt;
4. polish attempt 2 followed through the same boundary;
5. the second completed intent was retired;
6. every paid action was `REPORTED`, with no retained provider or authority
   custody; and
7. SBE published a sealed `review_required` result.

Polish improved both decks but did not clear every finding within the configured
two attempts: Doughmeat moved from 3 to 1 and Macaron from 8 to 7.

## Apparently odd trace fields

The terminal inspection's `local_dependencies=1` is source-consistent. For
`FINAL_QA_REQUIRES_REVIEW`, SBE publishes one blocking review dependency:

```text
kind=native_state_repair_review
reason_code=final_qa_review_required
```

That dependency is not an executable operation. The same closed inspection says
`execution_branch=none`, `eligible_now=false`, and
`capacity_disposition=retain_for_review`. It therefore does not contradict the
absence of runnable continuation or provider custody.

Likewise, the state temporarily passes through `FINAL_QA_REQUIRES_REVIEW` after
the first polish result is evaluated. No terminal result is sealed there; the
exact second polish action is prepared and the outer state advances to
`AWAITING_SPEND_AUTHORIZATION`. The immutable terminal publication occurs only
after attempt 2 is adopted and its intent is retired.

## Remaining evidence gap

Trace logs expose counts but not the exact surviving lint finding codes or
reports. To decide whether the final editorial judgments themselves were
correct, request an API-owned packet binding each run's final checkpoint and
terminal result to the following exact artifacts:

- the final accepted/best deck digest;
- the final structural validation report;
- the final editorial lint report;
- both polish-attempt validation and lint reports; and
- the sealed native result and receipt identities/digests.

If those artifacts confirm one and seven genuine non-theme findings respectively,
the investigation should close without a code change. If they expose stale,
removed-policy, or incorrectly recomputed findings, later slices can target that
narrow defect.

No storage access, provider activity, recovery, or mutation was performed.
