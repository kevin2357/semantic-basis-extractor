# Aldine / Moxon Terminal Observation Investigation

## Final disposition

SBE's investigation is closed. Aldine's terminal-review progression was
legitimate, and exact retained-workspace reproduction cleared the native
reader/root/capture path plus API's deterministic envelope and request
preflight. API owns the remaining live observer/runtime diagnosis. No SBE
package change or release is warranted.

## Purpose

Investigate two separate but potentially related outcomes from the fresh QA two-pup cohort launched after the observer-root-identity rollout:

1. **Aldine Apricot** reached `native.terminal.review_required` unusually quickly (six SBE job attempts). Establish the actual native/provider/editorial sequence and whether this is a legitimate fast editorial terminal outcome or a regression.
2. Neither Aldine nor the successfully delivered **Moxon Muffin** produced the expected BetterStack editorial-review packet or longitudinal artifacts. Both SBE traces report `editorial.observation.completed` with `editorial_delivered=false`, `artifact_count=0`, `branch=unavailable`, and `failure_kind=capture_or_preflight`.

This begins as read-only evidence and contract diagnosis. Do not resume, reconcile, repair, mutate retained workspaces, call providers, alter QA state, or retry either run.

## Cohort and authoritative identities

| Pup | API run | Native run | SBE job | Authoritative terminal result |
| --- | --- | --- | --- | --- |
| Aldine Apricot | `6a683b9a-fa00-4ad6-8e23-b6d8d5d9524a` | `3ab7cd6e857b6f3ee5947ca6302adab41a0054b988bafdc99697e8f3425e4d96` | `1a7e1a8a-656c-46fe-b9c1-ced99300dc96` | failed: `native.terminal.review_required` |
| Moxon Muffin | `137f3968-239b-4a01-9d8e-61b98ed6601e` | `3ebaec3c5c954a63b14519a7b0e8ba300384263be3ea0fd079ca181701e52520` | `8606bcc8-7b33-4248-be40-43545370e807` | succeeded / delivery accepted |

Observed SBE result IDs: Aldine `nres_d0568048c5fc2d9cfd68d7c7`; Moxon `nres_5a90fadd039f369c7303ecd3`.

## Frozen observed facts

- Aldine terminalized at approximately `2026-09-14T20:37:22Z`; worker trace reports `provider_reconciliation`, `retain_for_review`, `terminal_closed`, generation 9, zero provider-local dependencies, then non-retryable `native.terminal.review_required`.
- Moxon reconciled from six to one provider-local dependency, later reached `delivery_validation` / `delivery_accepted`, published the reading, and released capacity/lease cleanly.
- Both terminal traces emitted an unavailable observer result rather than a BetterStack delivery. This occurred on the freshly deployed API/SBE observer stack, so it requires source-level comparison with Sprint 97's logical-root correction and SBE's exact capture-status implementation.

## Supplied Render worker log export

The API agent exported the unfiltered two-hour SBE worker window (Render's 1,000-record limit applied) to:

`C:\tmp\astrowoof-sbe-worker-aldine-moxon-20260914T204522Z.jsonl`

Requested window: `2026-09-14T18:45:22.3212236Z` through
`2026-09-14T20:45:22.3212236Z` UTC. The file does **not** include either
Aldine or Moxon. Render's 1,000-record cap retained only the front of the
requested range: 989 parseable events from `18:47:27.804Z` through
`19:08:05.978Z`, overwhelmingly belonging to the earlier Garamond/Quill
cohort. All six current API/native/job identities occur zero times.

The export is useful only as evidence of truncation and must not support a
current-cohort timeline. Obtain narrowly filtered or segmented later windows
before classifying either run. Treat worker logs as non-authoritative progress
evidence; API/PostgreSQL governs lifecycle and custody.

## Initial read-only concerns

1. Aldine's fast terminal review and the two shared observer failures are
   separate questions until exact evidence proves a common cause.
2. Sprint 97 corrected checkpoint `logical_restore_path` persistence. The API
   observer still receives the worker's current runtime `workspace`; exact
   evidence must show whether those identities remained equal through restore
   and terminal-publication retry.
3. Provider-free capture/preflight fixtures passed in the immediately preceding
   Garamond/Quill investigation. Do not repeat broad gates before recovering
   the missing cohort-specific timeline.
