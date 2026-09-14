# API Review — Initial Investigation Plan

## Decision

Approved to complete Slice 0 as corrected and proceed to Slice 1's
provider-free, phase-bounded capture/preflight localization.

API independently verified the raw `19:00–19:15Z` export:

- Garamond's `editorial.observation.completed` event at
  `2026-09-14T19:06:09.708Z` carries the exact delivery result
  `nres_8a0f803d144b9430fe945e6c`.
- Quill's corresponding event at `2026-09-14T19:10:15.699Z` carries
  `nres_52b2b0fb130ed0fdca2dcbeb`.

The two exact result IDs match the respective native publication evidence.
Both outcomes are `branch=unavailable`, `failure_kind=capture_or_preflight`,
`editorial_delivered=false`, and `artifact_count=0`.

Accordingly, Sprint 96's exact delivery-retry authority carry-forward worked
for both accepted deliveries. Neither missing observer invocation, disabled
observer, missing terminal identity, nor Better Stack query access is the
first demonstrated failure.

## Approved scope fence

1. Keep the phase recorder provider-free and safe: record phase name plus a
   bounded exception class/fingerprint only. Do not record authored deck prose,
   prompts, provider payloads, workspace paths, request bodies, or tokens.
2. Distinguish failure of the primary runtime capture from failure of the typed
   capture-status fallback. A fallback that itself cannot be built is a
   separate fact, not a reason to flatten the diagnostic.
3. Do not use R2 for Slice 1. Request the exact conditional-coordinate gate
   only if provider-free evidence cannot reproduce or classify the live shape.
4. Do not fabricate a result identity, add latest-result discovery, or let an
   observation failure affect terminal delivery, custody, cleanup, spend, or
   retry semantics.
5. If capture and preflight both pass provider-free, return to API for the
   narrow configuration/transport boundary; it should verify only relevant
   key presence/shape and never expose secret values.

No SBE runtime/package change is authorized by this review.
