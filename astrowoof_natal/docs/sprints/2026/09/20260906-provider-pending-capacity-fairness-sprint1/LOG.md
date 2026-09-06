# Log

## 2026-09-06 — pre-sprint planning

- Recorded reciprocal API and SBE initial thoughts.
- Completed the shared pre-sprint huddle.
- Replaced the unavailable historical eight-run reconstruction as the primary
  causal strategy with deterministic code-history replay.
- Prepared the detailed sprint plan.
- Owner directed both repositories to complete Slices 0–1 before the first joint
  review.
- Committed the planning packet as `6808b0d`.

## 2026-09-06 — Slice 0

- Froze local trace, Sprint 58, and SBE companion evidence sources.
- Mapped the current native lifecycle and API allocation/release/claim paths.
- Recorded the historical evidence ceiling.
- Found a retained post-Sprint-58 pair whose initial waves began 97 seconds
  apart, followed by September 2–3 overlap with larger five-to-nine-minute gaps.
- Corrected the investigation target from binary loss of overlap to progressive
  peer-latency degradation culminating in Podium/Laurel's terminal-boundary wait.
- Per owner direction, proceeded directly into Slice 1 without a joint pause.

## 2026-09-06 — Slice 1

- Diffed Sprint 58's exact-result ingress and terminal preflight changes.
- Confirmed Sprint 58 did not modify nonterminal provider-pending release,
  continuation allocation retention, queue ordering, or the native four-action
  reconciliation bound.
- Confirmed the SBE companion shipped an availability reader rather than a
  capacity semantic change.
- Classified Sprint 58 as a negative-control boundary rather than a supported
  hard cutoff for the peer-latency degradation.
- Identified the post-September-3 API history/configuration window for the
  counterpart investigation.
- Froze negative-control and actual-divergence replay assertions.
- Paused at Voof-paws 1 for joint review before harness construction or runtime
  mutation.

## 2026-09-06 — Voof-paws 1

- API confirmed the September 2–3 witnesses derive from post-Sprint-58
  deployment eras.
- Joint review approved the progressive peer-latency framing and provider-free
  characterization.
- Froze the replay order: Sprint 58 absence/terminal negative control, then API
  `d451a88 → 8c389b3` with separate healthy and retry-ceiling cells.
- Recorded SBE's reciprocal review in the API sprint.
- No runtime policy change was authorized.

## 2026-09-06 — Slice 2 SBE native-input freeze

- Confirmed the existing production-path fixture covers not-due release, due
  reconciliation, completed-evidence local work, and the six-due/four-cap case.
- Strengthened the bounded-cycle regression to freeze the exact provider
  retrieval order, exact untouched suffix, and final public scheduling result.
- The first tightened assertion exposed the real canonical ordering:
  due-time/action ordering selects responses `1,4,5,6`, not numeric-prefix
  `1,2,3,4`; the test now records the production truth.
- Ran 66 focused tests successfully with one expected optional-schema skip.
- Recorded the native replay input and handed the actual historical revision,
  allocation, and next-claim experiment to the API-owned half of Slice 2.
- No runtime policy, public schema, provider operation, or QA state changed.

## 2026-09-06 — API review of SBE native input

- API approved SBE's native replay input and its canonical `1,4,5,6` selected /
  `2,3` due-suffix evidence.
- API completed the Sprint 58 and `d451a88 -> 8c389b3` controls and confirmed
  neither is a demonstrated healthy provider-pending regression boundary.
- The present mechanism is now explicit: exact not-due release admits a peer;
  actionable continuation retains the incumbent allocation and excludes the
  peer while the one-slot pool is full.
- Kept the joint policy gate open because SBE's reciprocal API review requested
  a distinct `local_work_ready` characterization, which is not yet present in
  the API test or evidence tree.
- No runtime policy or public-contract change was approved.

## 2026-09-06 — Slice 3 policy proposal

- Verified API commit `2a7e0d7` and independently ran its five-test fairness
  module successfully.
- Confirmed local-work-ready has zero provider operations but shares current
  allocation retention and owner-only reclaim behavior with due reconciliation.
- Classified the cause as legitimate actionable native topology plus unbounded
  API incumbent allocation retention, not a historical healthy-path regression.
- Proposed an API-only `N=1` cooperative scheduler turn after a validated final
  result, newer accepted checkpoint, persisted readiness, and completed writer-
  free command boundary when a compatible peer is ready.
- Explicitly retained all native/provider/authorization/spend/workspace custody.
- Declined to promise a strict wall-clock bound without a proven universal
  command deadline.
- Paused at Voof-paws 3 before any runtime mutation.

## 2026-09-06 — Voof-paws 3

- API approved the API-owned `N=1` durable post-command rotation direction.
- Refined eligibility so `ordinary_resume` alone never authorizes rotation:
  API must join the exact persisted, validated `local_work_ready` decision to
  this command's newer accepted checkpoint.
- Applied the analogous exact persisted decision requirement to due provider
  reconciliation.
- Required atomic defer plus capacity release and direct proof that B claims
  before A's ordinary defer matures.
- Added absent, wrong-reason, stale, and checkpoint-mismatched decision cases to
  the fail-closed implementation matrix.
- API Slice 4 implementation is authorized. SBE requires no schema, runtime, or
  release change.
