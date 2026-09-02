# Slice 3 — provider-free production-boundary reproduction

## Result

Slice 3 reproduces Nori's native ordering seam through the real public
`closure.main()` resume boundary. It does **not** reproduce Biscuit's retained
behavior as a general creative-retry defect.

No retained checkpoint was executed, no provider adapter performed I/O, and no
external storage was accessed or mutated.

## Nori reproduction

The production-shaped fixture contains completed provider reconciliation for a
polish action and a `FINAL_QA_WARN` subject awaiting the stage-specific polish
consumer.

The public resume sequence is:

```text
v0.7 advertises provider_result_fan_in_and_retry_evaluation(stage=polish)
→ author_pending_passes completes without consuming polish evidence
→ the first checkpoint_spend_boundary calls seal_local_progress()
→ commit_local_work_progress detects the unchanged polish operation
→ a v0.2 local_work_progress_contradiction result and receipt are sealed
→ closure.main exits 2 before finalize_subjects() can run the polish consumer
```

The sealed result truthfully retains the polish action in
`reconciliation_action_ids`, sets `new_provider_create_permitted=false`, and
does not claim complete-custody terminal closure. API's later terminalization
of that result remains the separately confirmed API disposition defect.

The positive control consumes the completed polish evidence before the first
progress seal. The prior semantic operation is then consumed and the real
stage-specific boundary becomes reachable. This proves the failure depends on
checkpoint ordering, not on completed polish evidence being intrinsically
unadoptable.

The not-due control advertises no local operation. It remains a non-eligible
provider-reconciliation decision, preserving genuine provider custody.

## Biscuit reproduction result

The production-shaped creative-retry fixture includes:

- completed provider evidence;
- an ambiguous matching pass attempt;
- an exact response artifact;
- no prior consumed-operation history; and
- the ordinary public resume boundary.

With provider I/O forbidden, the current runtime adopts the response, applies
deterministic rejection, removes the prior semantic operation, advances the
checkpoint basis, and publishes one fresh `await_external_authority` successor.

Therefore the retained Biscuit observation is **not reproduced** by the general
creative-retry path represented by this fixture. The retained checkpoint still
proves that its operation remained unconsumed, but the exact failed runtime
predicate is narrower than the static action/attempt/response join recovered in
Slices 1–2. It must not be invented from the successful control.

Existing adjacent production-boundary regressions retain the required malformed
identity, interruption-before-adoption, interruption-after-adoption, rejection,
and replay cells. They remain part of this slice's focused evidence matrix.

## Ownership classification after reproduction

| Finding | Classification |
|---|---|
| Nori polish operation sealed before its consumer | Confirmed SBE checkpoint-ordering defect |
| Nori result terminalized despite retained custody | Confirmed API disposition defect |
| Biscuit retained semantic operation repeated | Confirmed retained outcome; general SBE cause not reproduced |
| Biscuit sole-slot repetition | Confirmed API no-progress/capacity containment gap |

## Gate

Pause for contract/invariant review before runtime mutation. The Nori correction
can be designed narrowly. Biscuit needs either a more exact provider-free
fixture derived from the missing predicate or an explicit evidence-insufficient
closeout; Nori's proof must not be used as a substitute cause.
