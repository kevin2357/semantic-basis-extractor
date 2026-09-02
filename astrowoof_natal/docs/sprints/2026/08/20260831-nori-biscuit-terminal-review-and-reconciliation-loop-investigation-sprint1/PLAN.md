# Plan — Nori / Biscuit terminal review and reconciliation loop

## Status

Slices 0–6 complete. The narrow Nori-only `0.4.38` candidate is reproducible,
installed-wheel qualified, and free of reporter package content. Paused for
final API/owner release review. The exact
approved read-only checkpoint access is complete; no retained-workspace
execution/mutation, provider work, release, or recovery action has occurred.

## Objective

Explain, with exact native and public evidence:

- why Nori converted completed provider reconciliation into a sealed
  `review_required` terminal closeout; and
- why Biscuit repeatedly advertises executable ordinary local work while the
  accepted API checkpoint remains generation 13.

Then freeze the narrowest general invariant and provider-free regression needed
to prevent the class of failure. Do not assume both manifestations share one
cause until their checkpoint joins prove it.

## Working model to test

The trace suggests both runs may reach a seam where completed provider evidence
is represented as a blocking local-ingestion dependency, but the selected
ordinary-resume path does not consume that stage's exact semantic operation.
Nori converts the contradiction to review; Biscuit continues cycling. Exact
checkpoint evidence may confirm, refine, or reject this model.

## Evidence precedence

1. Hash-verified restored checkpoint and snapshot-valid native files.
2. Sealed native result, receipt, journal, action/binding, and v2 intent facts.
3. API checkpoint/storage receipts supplied in `BACKGROUND.md`.
4. Sanitized `✨🐶` and API execution-event traces.
5. Reporter matrices and no-progress candidates as navigation aids only.

No causal statement may be based solely on a status name, an API projection, or
the absence of a log line.

## Slice 0 — evidence freeze and production-path map

- Hash the supplied log and record exact coverage/time bounds.
- Generate deterministic reporter JSON/HTML/Markdown for both native run IDs.
- Extract a sanitized event table around:
  - provider retrieval completion;
  - lifecycle branch selection;
  - local-work selection/commit;
  - native publication;
  - API checkpoint acceptance and readiness; and
  - terminal closeout or job deferral.
- Map the relevant source path from `_local_dependencies()` through
  `_execution_branch()`, ordinary resume, stage-specific fan-in/adoption,
  `commit_local_work_progress()`, and native result publication.
- Freeze hypotheses separately for Nori and Biscuit.

Deliverables:

- `SLICE 0 - TRACE AND SELECTOR EVIDENCE MAP.md`
- reporter identity/coverage receipt
- initial causal-hypothesis matrix

**Voof-paws 1:** review the evidence map before protected checkpoint access.

## Slice 1 — exact read-only checkpoint recovery

For each exact coordinate in `BACKGROUND.md`:

1. verify the coordinate packet fields locally;
2. issue exactly one object `HEAD`;
3. require exact byte length, object identity, and SHA-256 agreement;
4. issue exactly one conditional `GET`;
5. validate archive safety and inventory digest;
6. restore only into a new local temporary directory; and
7. run provider-free, nonmutating snapshot validation and offline inspection.

Inspect only the evidence needed to join:

- run identity, route, status, and state revision;
- pass/attempt lineage;
- complete action inventory and binding identities;
- provider ID and reconciliation timing/outcome;
- v2 request/grant/intent state and ordered members;
- local-work operation inventory and consumed-operation history;
- native result index, result, receipt, and journal; and
- subject/final-QA state required to explain terminal review.

Deliverables:

- exact access manifest and read receipt for each object;
- snapshot-validation receipts; and
- sanitized checkpoint comparison table.

No provider adapter, CLI resume, reconciliation, repair, or workspace write is
allowed.

## Slice 2 — causal reconstruction and classification

Build one append-only timeline per run and one comparison matrix.

For Biscuit, prove:

- the exact provider-local dependency and whether it is due, completed,
  adopted, rejected, or internally contradictory;
- the semantic operation advertised by local work;
- whether ordinary resume consumes it or merely republishes checkpoint bytes;
- whether generation 13 is byte-identical, semantically identical, or replaced
  by a successor the API does not adopt; and
- whether the correct posture is release-until-due, reconciliation, local work,
  typed review, or another existing closed disposition.

For Nori, prove:

- the exact cause/evidence bound into `nres_cca6d3bd230517d294e57cef` and
  `nreceipt_7bcbf15b34b652a2b87f4ff1` if those IDs join the restored checkpoint;
- whether any provider-backed or local semantic work remained unresolved;
- whether `semantic_work_not_consumed` is an expected fail-closed terminal
  contradiction or the result of selecting a nonexistent stage consumer; and
- whether terminal closeout satisfied the complete closure/custody assertions.

Classify each finding as:

- expected policy/editorial review;
- SBE selector defect;
- SBE stage-specific adoption defect;
- SBE progress/publication contract defect;
- API checkpoint/result-ingestion defect;
- combined seam; or
- evidence insufficient.

Deliverable: `SLICE 2 - NATIVE CAUSAL MATRIX AND FINDING CLASSIFICATION.md`.

**Voof-paws 2:** API review of the evidence and ownership classification before
contract or runtime design.

## Slice 3 — provider-free production-boundary reproduction

**Status: complete.** Nori's public-boundary ordering defect reproduced;
Biscuit's retained outcome did not reproduce as a general creative-retry defect.

Only after Slice 2 identifies an exact seam, create minimal production-shaped
fixtures through supported native/runtime boundaries.

Required candidate cells:

- completed creative-retry evidence awaiting adoption;
- completed polish evidence awaiting adoption;
- legitimate not-due provider custody control;
- successful completed-evidence adoption control;
- rejected/malformed evidence control; and
- interruption/replay at the adoption checkpoint.

Drive the actual public resume/inspection/commit/publication path with scripted
provider results already present in native state. Assert zero create/POST and no
real retrieval.

For a loop reproduction, prove the full cycle:

```text
inspection selects ordinary_resume
→ command executes
→ exact semantic operation remains unconsumed
→ no authoritative successor truth is created
→ same semantic operation is selected again
```

For terminal review, prove whether the sealed result is truthful under the
frozen closure/custody contract.

## Slice 4 — invariant and public-contract freeze

**Status: complete.** Existing public contracts are sufficient. The correction
aligns optional-stage progress sealing with the real finalization consumer and
preserves cumulative consumed-key state in the coordinator.

Freeze only conclusions supported by Slices 1–3. Candidate invariants include:

- An advertised local operation must identify a supported consumer and be
  consumed by the command, or the successor must publish a different typed
  disposition.
- Completed provider evidence is not equivalent to unresolved provider I/O, but
  it must remain durably visible until stage-specific adoption or a typed
  terminal refusal accounts for it.
- `progressed_local` requires a meaningful native truth change; a snapshot-only
  republication cannot satisfy progress.
- Terminal review cannot silently erase unresolved action, intent, provider
  evidence, or local-operation inventory.
- A repeated semantic operation against a new snapshot remains no progress.

Decide whether existing lifecycle v0.7/v0.8, native-result v0.2, and
local-work-progress contracts already express the correction. Version only a
public shape that genuinely must change.

Deliverables:

- contract/invariant document;
- API consumer handoff;
- explicit compatibility statement for the two retained checkpoints; and
- test matrix with route/stage applicability.

**Voof-paws 3:** schema/runtime design review before implementation.

## Slice 5 — narrow runtime correction, conditional

**Status: complete for exact-interactive optional-stage adoption.** No
Biscuit-shaped change was made.

Implement only if the earlier slices prove an SBE defect. Prefer one shared
stage-aware adoption/progress boundary over special cases named after Nori or
Biscuit.

The correction must preserve:

- provider-custody precedence;
- v2 constrained create fencing;
- retrieval-only reconciliation;
- cumulative local-operation consumption history;
- immutable sealed results/receipts;
- interruption ambiguity rules; and
- exact replay behavior.

No retained checkpoint is executed or repaired during implementation.

## Slice 6 — holistic qualification and handoff

**Status: complete for the exact-interactive Nori correction.** Candidate wheel
SHA-256: `c50fe0faca9e3f29bfa56a3e9a43cca3733497946223ee240926f8db967e5feb`.

- Re-run the provider-free production reproductions.
- Cover exact and bounded routes where the shared mechanism actually applies;
  explicitly defer unsupported Batch topology.
- Prove no duplicate create/retrieval, no semantic-operation resurrection, and
  no terminal closeout with unaccounted work.
- Add an installed-wheel qualification only if public/package behavior changes.
- Provide fixtures and a concise receipt API can ingest without private
  workspace reconstruction.

**Voof-paws 4:** joint qualification and release-scope review.

## Slice 7 — release or investigation-only closeout

Choose one honestly:

- investigation closes with no SBE change and an API-owned handoff;
- focused SBE patch release; or
- broader follow-up sprint if the evidence reveals multiple independent seams.

Any release requires a fresh version, committed-source identity, reproducible
artifact evidence, installed qualification, and risk-proportionate regression
gate chosen before testing.

## Guardrails

- No real provider calls, creates, retrievals, or spend.
- No R2 listing or write; only the two exact `HEAD` + `GET` pairs described.
- No retained QA mutation, resume, repair, denial, retirement, or deletion.
- No API resource/lease/capacity claim from SBE-native evidence.
- No inference from `WAITING_FOR_RESPONSE`, `review_required`, `quiescent`,
  `progressed_local`, or `terminal_closed` without their complete contract join.
- Reporter output is diagnostic, never transition authority.
