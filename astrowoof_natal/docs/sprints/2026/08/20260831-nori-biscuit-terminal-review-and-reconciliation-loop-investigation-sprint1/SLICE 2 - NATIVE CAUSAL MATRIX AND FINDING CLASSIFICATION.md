# Slice 2 — native causal matrix and finding classification

## Executive finding

The two runs share a violated high-level progress invariant but expose two
different native mechanisms. Nori additionally proves an API consumer defect.

| Run | Native defect candidate | API seam | Current classification |
|---|---|---|---|
| Nori | Polish evidence is advertised as local work, but progress is sealed at the earlier authoring-pass checkpoint before polish consumption. | API terminalized a valid v0.2 review result that explicitly retained reconciliation custody. | Combined seam: SBE stage-specific progress ordering plus API result-ingestion/disposition defect. |
| Biscuit | Completed creative-retry evidence is statically adoptable but remains an ambiguous pass attempt after the real consumer runs. | API repeatedly restores the same generation and treats the unchanged operation as executable local continuation. | SBE stage-specific adoption/commit defect candidate plus API no-progress/capacity-loop guard gap; exact internal failure predicate awaits reproduction. |

## Nori causal sequence

```text
polish provider response completes
→ lifecycle advertises completed polish ingestion as ordinary local work
→ ordinary resume captures that operation
→ author_pending_passes runs with no applicable pass work
→ first quiescent callback checks progress before finalize_subjects/polish
→ polish operation remains advertised
→ local_work_progress_contradiction seals v0.2 review result
→ result explicitly retains polish reconciliation custody
→ API nevertheless maps review to non-retryable terminal failure/cleanup
```

Native classification: **SBE selector/consumer-boundary and progress-publication
defect candidate**, strongly supported by exact state plus source ordering.

API classification: **confirmed result-ingestion/disposition defect**. The API
may treat editorial review as a stable decision, but it cannot erase the
result's explicit reconciliation-only custody.

## Biscuit causal sequence

```text
creative-retry provider response completes
→ response ID/artifact/reconciliation evidence are durable and joined
→ lifecycle advertises work_c2a017… as ordinary local work
→ author_one_pass reaches the matching pass/attempt
→ attempt remains AMBIGUOUS_PROVIDER_SUBMISSION without adoption metadata/QA
→ no consumed-operation history is committed
→ generation 13 remains the accepted immutable checkpoint
→ API later restores the same basis and reselects the same semantic operation
```

Native classification: **SBE stage-specific adoption defect candidate**. The
checkpoint proves the static adoption join is available. A provider-free test
must identify whether failure occurs at adoption preparation, provider-marker
reuse, state persistence, parsing, or QA transition.

API classification: **no-progress/capacity-loop guard gap**. Even if the SBE
operation fails to advance, an unchanged checkpoint plus the same semantic
operation must not retain the only slot indefinitely.

## Rejected explanations

- Neither run is waiting for a provider response to become due; the relevant
  responses are already completed.
- Nori is not a custody-final terminal result; its sealed contract says
  reconciliation is required.
- Biscuit's providerless pass-6 retry does not explain the pass-2 completed
  dependency and must not supersede it.
- The runs do not currently justify one stage-specific code fix: Nori concerns
  polish ordering, while Biscuit reaches the creative-retry consumer.

## Frozen invariant for reproduction

An advertised local operation must be consumable by the selected command at the
checkpoint where progress is evaluated. If consumption fails, the successor
must publish a different typed, non-spinning disposition. Reissuing the same
operation key from the same immutable checkpoint is not progress.

## Next gate

Stop at Voof-paws 2. API review is required before provider-free production-path
reproduction or contract/runtime design. No retained-run action is authorized.
