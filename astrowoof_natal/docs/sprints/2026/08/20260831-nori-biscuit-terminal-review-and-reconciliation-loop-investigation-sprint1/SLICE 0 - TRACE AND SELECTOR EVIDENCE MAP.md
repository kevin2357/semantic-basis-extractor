# Slice 0 — trace and selector evidence map

## Gate result

Slice 0 is complete. The supplied trace and current source support two distinct
causal candidates, but neither is yet proven without the protected checkpoint
joins. This document authorizes no R2 access, provider operation, retained-run
execution, recovery, repair, or mutation.

Most importantly, this investigation does **not** equate SBE's
`terminal_closed` execution outcome with API's later
`native.terminal.review_required` failure reason. They are adjacent trace facts.
Their exact relationship remains unproved until the Nori checkpoint's result,
receipt, journal, snapshot, and invocation identities are joined.

## Frozen evidence

| Evidence | Identity / coverage | Authority |
|---|---|---|
| SBE/API log export | `C:\Users\kevin\Downloads\sbe logs.txt`; 1,714,322 bytes; 2,000 lines; SHA-256 `a0267e1984311ff067027c3897833cd8ce704ed6cee5fc0d3bcb0fa7f8c4fe20` | Diagnostic only |
| Trace time ceiling | Through approximately `2026-08-31T15:55:44Z` | Does not contain Biscuit's later API loop beginning around `16:25Z` |
| Reporter JSON | SHA-256 `a4335c25350f26689ddcfe1a5ff59d287932a081d2c0e8fb8985ca6334e894a9` | Diagnostic navigation only |
| Reporter HTML | SHA-256 `bc62e8520d82b8c07514cf15c3013f32b34ba00561da7a7c0396f20ff0b92011` | Diagnostic navigation only |
| Parsed marked trace | 1,641/1,641 records; 265 JSON envelopes; 0 malformed marked records | Coverage receipt, not transition authority |

The reporter found four candidate semantic-republication windows for Biscuit
and three for Nori. Reporter v1 does not reduce the API JSON envelopes into a
final posture, so those candidates are pointers rather than causal proof.

## Production source path

| Boundary | Source | Relevant behavior |
|---|---|---|
| Native dependency projection | `lifecycle.py:537`, `_local_dependencies()` | Completed provider evidence becomes `provider_evidence_ingestion_required`; unfinished provider custody does not become local work. |
| Branch selection | `lifecycle.py:872`, `_execution_branch()` | Due reconciliation precedes local continuation; local dependencies can select `ordinary_resume`. |
| Public local-work projection | `post_fan_in_contracts.py:216`, `_runtime_local_operations()` | Completed actions become stage-bound `provider_result_fan_in_and_retry_evaluation` operations. |
| v0.7 inspection | `post_fan_in_contracts.py:275`, `inspect_post_fan_in_lifecycle()` | Binds the semantic operation to the current checkpoint. |
| Progress commit | `post_fan_in_contracts.py:375`, `commit_local_work_progress()` | Refuses when the basis is unchanged or the prior semantic operation remains advertised. |
| Resume capture / seal | `closure.py:8370–8420` | Captures prior local inspection and seals progress; contradiction can publish native v0.2 review evidence. |
| First quiescent boundary | `closure.py:8589` | `author_pending_passes` invokes the local-progress seal. |
| Later subject/polish boundary | `closure.py:8646–8650` | A second boundary precedes `finalize_subjects()`; polish is therefore later than the authoring-pass checkpoint. |
| Completed creative-retry adoption | `closure.py:4181–4251` and `author_one_pass()` | Adoption requires an exact action/binding/provider/reconciliation/artifact join; failure retains ambiguity. |

## Nori trace reconstruction

Native run: `e0b406dbacf2edf0ce7b421586e7464d8056fe0f893033a03edfdee957f6a9a0`.

| Trace evidence | Observation |
|---|---|
| Lines 1083 onward | Polish action `paid_d359bb2e972cc3a7a7ac806f` is prepared. |
| Lines 1234–1239 | Reconciliation retrieves its durable response `resp_055d13…` as completed. |
| Line 1242 | Lifecycle immediately projects one provider action and one local dependency, selecting `ordinary_resume`. |
| Lines 1244–1246 | During the reconciliation coordinator, `finalize_subjects` / polish starts and revision 83 is saved. |
| Lines 1249–1257 | The command still publishes provider-pending/progressed-local evidence and exits for continuation. |
| Lines 1272–1278 | The next ordinary resume sees the same local dependency; authoring runs with zero selected passes, while the polish action remains `WAITING` and its v2 intent remains `PROVIDER_PENDING`. |
| Subsequent marked trace | `commit_local_work_progress()` refuses `semantic_work_not_consumed`; SBE publishes result `nres_cca6d3bd230517d294e57cef` and receipt `nreceipt_7bcbf15b34b652a2b87f4ff1` with `review_required`. |
| Later JSON envelopes | API records `execution_branch=local_resume`, SBE outcome `terminal_closed`, accepts a checkpoint, then records `native.terminal.review_required`. These facts are not yet a proven identity join. |

### Nori hypothesis matrix

| Hypothesis | Slice 0 status | Reason |
|---|---|---|
| Polish completed evidence is advertised as a local semantic operation. | Supported by trace and source. | Completed action projection is stage-generic. |
| Ordinary resume attempts to seal that polish operation at the authoring-pass checkpoint before polish executes. | Strong source-consistent candidate. | The first `seal_local_progress` callback is attached to `author_pending_passes`; `finalize_subjects` is later. |
| The sealed native v0.2 result truthfully accounts for all action/custody evidence. | Unknown. | Requires exact result/receipt/journal/checkpoint join. |
| API's failure reason is the direct interpretation of this exact sealed result. | Unknown; explicitly not asserted. | Invocation/result/checkpoint identities have not been joined. |
| Nori is ordinary editorial review unrelated to local-work consumption. | Disfavored, not refuted. | Trace contains the explicit semantic-work contradiction immediately before review publication. |

## Biscuit trace reconstruction

Native run: `8a7c25e37385ef75e95d8b72a7efe7bdb1355495df4195cf1bab93f0d821dd84`.

| Trace evidence | Observation |
|---|---|
| Lines 948–950 | Creative-retry action `paid_53ffdebdecec2cfdd1cd373e` is prepared. |
| Earlier completed retrieval sequence | `paid_53ff…` / `resp_0176…` becomes completed, but adoption is logged as unavailable/ambiguous. |
| Lines 1968–1973 | Remaining action `paid_b189bb35484c70459a799f8c` / `resp_0de681…` is selected and retrieved completed. |
| Lines 1975–1983 | Lifecycle exposes completed evidence as local work; the real authoring consumer runs, but the attempt remains `AMBIGUOUS_PROVIDER_SUBMISSION`. |
| Lines 1989–1996 | Revision 88 still contains `WAITING:1`, `PREPARED:1`, custody 1, and the two-member `PROVIDER_PENDING` intent; SBE publishes `nres_bbb1350a6758739d3e89f142` / `nreceipt_e1741d2ab35d1109428f0055` as `provider_pending`. |
| API/background evidence after log ceiling | Generation 13 is reportedly selected repeatedly for ordinary resume. This later loop is not present in the supplied log and remains a separate API-owned observation pending the protected join. |

### Biscuit hypothesis matrix

| Hypothesis | Slice 0 status | Reason |
|---|---|---|
| Creative-retry completed evidence reaches its nominal stage consumer. | Supported. | `author_one_pass()` runs for the matching pass/attempt. |
| The exact adoption join fails and leaves the semantic operation unconsumed. | Supported as an observed result; underlying failed predicate unknown. | Trace logs `authoring_attempt_ambiguous`; source has multiple exact join predicates. |
| A snapshot-only republication causes the later API loop. | Candidate only. | Reporter flags candidates, but the later loop is beyond the log ceiling. |
| API repeatedly invokes the same semantic operation from byte-identical generation 13. | API/background claim awaiting exact checkpoint join. | Need checkpoint bytes, operation key, consumed-key history, and API checkpoint identity. |
| Biscuit shares Nori's authoring-before-polish ordering defect. | Disfavored. | Biscuit is a creative-retry operation and reaches the authoring consumer; Nori is polish. |

## Minimal protected checkpoint field list

Only these native/public facts are needed in Slice 1:

1. Run identity, route family, state revision, snapshot digest, and logical root.
2. Complete relevant action records: action ID, state, complete binding, stage,
   route, provider identity, reconciliation outcome/timestamps, response-artifact
   reference, authorization consumption, and reporting disposition.
3. Matching pass/attempt records: pass ID, attempt number/state, paid-action ID,
   provider metadata, QA/adoption state, error, and accepted-workspace evidence.
4. v2 live and archived intent: request/grant digests, ordered members, call-entry
   states, durable returned identities, current state, and retirement evidence.
5. Lifecycle v0.7/v0.8 operation inventory, stable operation keys, source action
   IDs, stage, and cumulative consumed-operation keys.
6. Subject/polish attempt and final-QA state needed to explain Nori's operation.
7. Native result index plus exact result, receipt, journal, predecessor/successor,
   action inventory, custody assertions, cause, and snapshot bindings.

API checkpoint generation/acceptance remains API evidence and must be joined to,
not synthesized from, these native facts.

## Slice 0 conclusion and pause

The evidence supports a shared high-level invariant: once SBE advertises a
semantic local operation, the selected command must have a real stage-specific
consumer capable of consuming it, or publish a different truthful typed
disposition. It does **not** yet support one shared implementation cause.

- Nori: strong stage-ordering/consumer-boundary defect candidate.
- Biscuit: strong completed-creative-retry adoption-join defect candidate;
  ownership of the later generation-13 loop remains unresolved.

Stop at Voof-paws 1. No protected checkpoint object has been accessed.
