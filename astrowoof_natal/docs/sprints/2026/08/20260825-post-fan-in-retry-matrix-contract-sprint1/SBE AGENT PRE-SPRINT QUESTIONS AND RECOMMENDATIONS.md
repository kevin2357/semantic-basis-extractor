# SBE Agent Pre-Sprint Questions and Recommendations

Status: proposed for owner/API review

## Recommendations

### 1. Treat this as an evidence-and-selector correction, not a new scheduler

The API behaved correctly by honoring SBE's public next action. SBE should make
that next action truthful and sufficiently evidenced. The API should not learn
retry heuristics or inspect native internals.

### 2. A generic dependency is not an executable operation

Current `local_dependencies` remain useful for closeout and human explanation,
but they are too broad to authorize scheduling. For example, a status-derived
`retry_preparation / authoring_continuation` does not prove which retry can be
prepared, which evidence it consumes, or whether preparation is presently legal.

Keep dependencies as explanatory/blocking facts. Add a separate closed inventory
whose members mean: "SBE can execute this operation now against this checkpoint."

### 3. Put local-work truth in the immutable checkpoint basis

Recommended ownership:

- native lifecycle inspection owns the exact local-work inventory;
- temporal lifecycle commits it into `checkpoint_basis`;
- temporal decision may select the already-proven run-level command but may not
  invent, remove, or reorder local operations as time advances.

Local executability changes only when native bytes change, not because the clock
moves.

### 4. Publish a real v2 qualification instead of rewriting v1 history

The current `astrowoof.provider_pending_lifecycle_qualification.v1` proves initial
create/detach, 4+2 retrieval, fan-in, and first authority selection. A receipt that
also proves multiple creative retries, exhaustion, and ambiguity is substantively
broader. The clean approach is a v2 receipt/schema/reader while retaining v1 as a
legacy readable proof with an explicit scope statement.

## Decisions requested at voof-paws 1

1. **Lifecycle versioning — decided.** Adding a top-level inventory to a strict
   v0.5 document is structurally incompatible for exact-key consumers. Publish a
   fresh native lifecycle schema version and retain v0.5 unchanged/readable.
   Version temporal/checkpoint evidence only where its exact public shape changes.
   Do not smuggle the inventory into an unvalidated object.

2. **Operation granularity.** Should `provider_result_fan_in` include the subsequent
   retry evaluation/preparation atomically, or should those be separately
   checkpointed operations? Recommendation: decide from the production path in
   Slice 0. Do not model finer granularity than native durable checkpoints support.

3. **Authorized/no-provider retry posture.** The background says retry #2 was
   prepared/authorized but lacked a provider operation. The retained rejected
   lifecycle bytes were not supplied here, so it is not yet safe to declare whether
   the correct branch is constrained dispatch, fresh authority, pre-submit refusal,
   or ambiguity. Slice 0 should freeze this from native fields and writer-fence
   history.

4. **Batch coverage.** Interactive post-fan-in retries are release-blocking. Batch
   should use production route mechanisms in qualification when supported; otherwise
   it should be explicitly deferred/fail-closed rather than delaying the core fix.

5. **Terminal exhaustion vocabulary.** Prefer existing terminal statuses and causes
   if they truthfully express retry exhaustion. Introduce a new public outcome only
   if existing terminal evidence cannot distinguish exhaustion from review or
   budget/policy stop.

6. **Progress invariant — decided.** Every advertised `ordinary_resume` operation
   must either be consumed and advance the checkpoint/basis or produce a different
   typed disposition. Returning the same eligible ordinary-resume decision against
   the same basis is a contract failure, not merely quiescence.

## Confidence

| Assessment | Confidence | Reason |
| --- | --- | --- |
| API followed the supported SBE branch correctly | High | Background and current ownership contract agree |
| Current status-derived dependency is insufficient scheduling proof | High | Current selector accepts any nonempty dependency |
| A public concrete local-work inventory is the right correction | High | It closes the inference gap without moving native authority |
| Runtime selector/state logic also needs a patch | Medium-high | The repeated no-op loop strongly suggests it, but Slice 0 must reproduce the exact native shape |
| Qualification receipt should become v2 | Medium-high | Its intended semantic scope is materially broader; exact naming inventory is still pending |
| Existing lifecycle schema versions can be tightened in place | Low-medium | Exact-key consumers likely require fresh versions for a new top-level field |

API review resolved the final row: a new closed lifecycle version is required.
Existing lifecycle versions remain historical readable contracts.

## Explicit non-decisions

- No Crumpet recovery procedure is authorized.
- No retained QA mutation is authorized.
- No provider call or credential use is authorized.
- No new retry count, creative policy, or product policy is chosen here.
- No blanket v1-to-v2 rename is proposed.
