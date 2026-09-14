# Evidence

- API authoritative lifecycle snapshot recorded Aldine as `failed` / `native.terminal.review_required`; Moxon as `ready` / `succeeded`.
- Per-run SBE traces recorded terminal observer unavailability for both runs with `capture_or_preflight`.
- Unfiltered SBE worker export: `C:\tmp\astrowoof-sbe-worker-aldine-moxon-20260914T204522Z.jsonl`.
- Export bytes: `2,204,374`; SHA-256:
  `ffa4f936a2f09b5b1b80eaab0881ba1398ec0703265746197449087469935c25`.
- Export structure: 1,000 concatenated outer records, 989 parseable structured
  events, event range `2026-09-14T18:47:27.804Z` through
  `2026-09-14T19:08:05.978Z`.
- Aldine and Moxon API run IDs, native run IDs, and SBE job IDs each occur zero
  times. The supplied file therefore contains no current-cohort trace evidence.

## Replacement unfiltered segmented export

Do **not** use the server-side exact-run filtered exports as completeness
evidence: filtering has historically omitted relevant events. The replacement
is the original two-hour request split into eight non-overlapping unfiltered
15-minute UTC windows, each below Render's 1,000-record cap. Manifest:

`C:\tmp\astrowoof-sbe-worker-aldine-moxon-20260914T184500Z-to-204500Z-manifest.txt`

| UTC window | Bytes | Structured event count | SHA-256 |
| --- | ---: | ---: | --- |
| 18:45–19:00 | 717,649 | 273 | `f3c1d10016dd8463b9b8cc0fb39180f82bc778aab21dad718969b3ef6f6914fa` |
| 19:00–19:15 | 1,715,593 | 819 | `0a0485a530ebd8fb6179e01c4588b3bbcbeef2d65728b2a5f809abf60ee1c934` |
| 19:15–19:30 | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 19:30–19:45 | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 19:45–20:00 | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 20:00–20:15 | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 20:15–20:30 | 887,877 | 327 | `8c2f2c894b30c87d8ed355c16e2f51e17869e1ae043984fa5b7e44649d787e86` |
| 20:30–20:45 | 1,821,393 | 871 | `5a2f7d4d055c3c6db42ae90f2e09144676d4e20381772c4ab1345fc7df5d80bd` |

Files follow the manifest paths, e.g.
`C:\tmp\astrowoof-sbe-worker-aldine-moxon-20260914-2015-2030Z.jsonl`.
Counts are bounded occurrences of structured `event_name`, not outer JSON
object counts, because Render concatenates envelopes containing nested objects.

## Corrected cohort coverage

- Aldine: 607 target-bound structured rows from `20:27:35.820Z` through
  `20:37:22.226Z`; six worker claims/cycles and complete terminal closeout.
- Moxon: 572 target-bound structured rows from `20:29:31.769Z` through
  `20:41:28.945Z`; seven worker claims/cycles and complete delivery closeout.
- Aldine completed six initial provider results, assembled to
  `FINAL_QA_FAILED` with one validation error and four lint findings, then used
  two distinct authorized polish actions. Attempt 1 remained failed and caused
  attempt 2 to be prepared; attempt 2 was `POLISH_REJECTED` with two validation
  errors. Only then did lifecycle report `eligible_now=false`, zero provider
  actions, `retain_for_review`, and terminal closure.
- Aldine's exact terminal publication is native result v0.2
  `nres_d0568048c5fc2d9cfd68d7c7`, receipt
  `nreceipt_39f8305f65dcfe9b36751f65`, invocation
  `ninv_f1ecd81445294d8ea90a840f`, cause `final_qa_requires_review`.
- Moxon completed six initial results, entered polish from `FINAL_QA_WARN`, and
  accepted its first polish attempt. Exact delivery result
  `nres_5a90fadd039f369c7303ecd3` survived the bounded publication retry into
  delivery validation and observer invocation.
- Both exact terminal results reached `editorial.observation.completed` and
  returned `unavailable / capture_or_preflight / delivered=false / artifacts=0`.

## Slice 2 observer joins

- Both terminal observer rows preserve their exact sealed result IDs; no
  latest-result discovery or identity substitution is visible.
- All target SBE fingerprints report release `0.4.61`, SPC `0.11.1`, and
  `validation_outcome=valid`.
- Aldine carries one stable logical-root SHA-256 through terminal revision 64:
  `2efa0c6ebb7f71d77b5bffb607f1de67c3ca65d1f3312747038f68062a007d5e`.
- Moxon carries one stable logical-root SHA-256 through delivery revision 61:
  `a242cabd6f407a38970d248265aa3c65410bfb1a02c7a0597be21a6e6701918a`.
- API root correction `6411cf5` and rollout record `fe217d1` precede both live
  runs. Source passes the prepared registered workspace directly to the
  observer and corrected checkpoint writers persist its resolved root.
- Live checkpoint, registration, and observer-call root digests are absent
  from current events. The observer also collapses all pre-HTTP capture and
  preflight exceptions into one failure kind. Exact four-root equality and the
  first internal failing subphase therefore remain unproven without gated
  retained-workspace evidence or new phase-safe diagnostics.

## Slice 3 exact-workspace reproduction

- Authorized R2 operations: HEAD 2, GET 2, list/write/delete 0. Both archives
  match pinned byte counts, SHA-256 values, generation 9, and inventory digest.
- At exact contract roots, Aldine exact-read succeeds and resolves to a typed
  `contradictory_native_evidence` capture status. That singleton status succeeds
  through API envelope and deterministic request preflight.
- At its exact contract root, Moxon succeeds through exact read, evidence
  collection, packet/projection/artifact construction, editorial envelopes,
  and deterministic request preflight.
- The live shared failure is not reproduced before API's post/runtime boundary.
  The outer observer exception region includes posting despite its
  `capture_or_preflight` label, so absence of a surviving post outcome does not
  prove that no HTTP attempt began.

## Joint ownership ruling

- API approved Slice 3 and accepted the remaining defect at its live
  observer/runtime boundary.
- No further R2, provider, workspace, or live-run action is authorized or
  needed from SBE.
- No SBE implementation, version bump, package qualification, or release is
  required from this finding.
- Aldine's distinct `contradictory_native_evidence` status may receive a future
  independent classification; it is not the cause of the shared observation
  failure and does not keep this sprint open.
