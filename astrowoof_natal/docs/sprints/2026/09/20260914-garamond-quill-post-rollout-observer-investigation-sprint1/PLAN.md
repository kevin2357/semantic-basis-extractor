# Plan — Garamond / Quill Post-Rollout Observer Investigation

## Working classification

Sprint 96's delivery-retry correction worked for both runs. Each retry reached
the observer with the exact native result ID emitted by SBE. Both observations
then completed locally as `branch=unavailable`,
`failure_kind=capture_or_preflight`, with no editorial delivery and zero
artifacts.

This rules out a missing observer invocation, disabled observer, missing exact
delivery identity, HTTP non-2xx, timeout, connection failure, and Better Stack
query access as the first failure. Exact-workspace reproduction then resolved
the local boundary: API supplied its outer checkpoint/run-label root where SBE
requires the native durable logical root bound into the workspace contract.
The same bytes produce complete captures at the correct root.

Do not add latest-result discovery or treat successful reading publication as
failed. The observer remains post-authoritative and best effort.

## Slice 0 — Freeze exact paired terminal and observer timelines

**Status: complete.** Read-only local evidence only.

- Hash and register all four raw Render exports, including the two legitimate
  empty windows.
- Record each exact delivery invocation, result, and receipt emitted by SBE.
- Bind the first publication attempt and retry attempt for each API job.
- Record the exact result ID reported by `editorial.observation.completed` and
  prove it equals the SBE delivery result.
- Correct the opening premise that no observer outcome event existed: both
  events are present near the end of the `19:00–19:15Z` export.

**Exit:** paired tables prove whether identity and invocation survived through
the observer entry without inference.

## Slice 1 — Provider-free capture/preflight exception localization

**Status: complete; live shape not reproduced.**

Use current checked-in source and provider-free fixtures only at first.

- Trace `EditorialReviewObserver.observe_terminal()` across:
  1. `build_editorial_review_runtime_capture()`;
  2. unsupported capture-status construction;
  3. native-event enveloping;
  4. editorial request preparation.
- Replace the broad outcome-only observation in a test harness with phase-
  bounded recording that identifies which call raises and its safe exception
  class/fingerprint without exposing authored prose, paths, tokens, or raw
  provider payloads.
- Exercise a delivery workspace containing six initial winners plus an accepted
  polish, matching both live runs' high-level shape.
- Test the restored publication-retry shape specifically: exact terminal result
  and receipt, current `run.json`, checkpoint metadata, final selected deck,
  validation/lint reports, and provider-response artifacts.
- Confirm whether a failed primary capture can always produce the typed
  `editorial_review_capture_status.v1` fallback. A fallback failure must remain
  separately visible from packet-construction failure.

**Exit:** identify the exact local function and safe failure class, or prove the
checked-in fixtures cannot reproduce the live workspace shape.

## Slice 2 — Conditional exact-workspace reproduction

**Status: complete.** Exact coordinates and owner authorization were supplied;
API performed the bounded reads and retained hash-verified local archives.
SBE reproduction identifies an API workspace-identity source defect.

- Obtain exact checkpoint coordinates from API persistence without discovering
  a latest run or result.
- With explicit owner authorization, perform at most one conditional metadata
  read and one bounded object read per named Garamond/Quill checkpoint.
- Restore each to a disposable local directory and call the public SBE runtime
  capture with only its already-proven exact result ID.
- Record safe inventory/digest evidence and phase-bounded failure data; do not
  commit decks, reports, responses, packet bodies, or other authored content.
- Perform no provider call, native mutation, retry, publication, Better Stack
  post, or QA state change.

**Exit:** exact live-shape reproduction identifies SBE capture construction,
typed fallback, or API preflight as the first failing boundary.

## Slice 3 — Conditional API configuration and transport verification

**Status: unnecessary.** The observer was enabled and invoked, the supplied
API/checkpoint root reproduces the failure before preflight, and the same exact
workspace captures successfully at its native durable contract root.

Run only if capture construction and request preflight succeed provider-free.

- Verify presence and safe shape—not values—of the five deployed observation
  settings.
- Confirm the observer was enabled for both events; the observed
  `branch=unavailable` already makes a disabled configuration unlikely.
- Exercise fake-client editorial/artifact posts and distinguish delivered,
  non-2xx, timeout, and connection outcomes from local preflight failures.
- Treat Render relay and Better Stack query health as observational diagnostics,
  never lifecycle evidence.

**Exit:** transport/configuration is either excluded or assigned to API with an
exact provider-free reproduction.

## Slice 4 — Joint ownership and correction decision

**Status: complete and API-reviewed.** Ownership is assigned to API's observer
workspace-root selection. The SBE investigation closes without implementation.

- Assign the defect at the first proven boundary only.
- Decide whether the minimum correction is SBE evidence collection, typed
  capture-status resilience, API phase diagnostics, or API request preflight.
- Check SBE test-manifest and Alloy impact explicitly. Observability-only or
  packet-projection work should not alter lifecycle semantics; any changed
  native eligibility or state rule requires separate model review.
- Stop for joint review before changing runtime code, package versions,
  deployment, or live state.

## Investigation boundaries

- No provider call, retry, recovery, resubmission, QA mutation, Better Stack
  write, or run reinterpretation is authorized.
- Slice 2 R2 access was separately owner-authorized and exhausted: exactly one
  conditional HEAD and one bounded GET per named object. No further access is
  authorized or required.
- Raw exports and any restored workspace remain outside Git.
- Do not expose secrets or authored/private payloads in logs or sprint docs.
