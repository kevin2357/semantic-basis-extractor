# API Review — Slice 3 First-Polish Authority Correction

## Assessment

The selected seam is correct. The implementation keeps the correction in
native lifecycle selection, preserves API's strict action-inventory/terminal
consumer guards, and does not broaden into Batch, bounded, recovery, or other
route families. The request-sidecar equality, matching binding, current state
revision, status, and action custody checks are the right shape for the live
authority exception.

## One required fail-closed correction before approval

The approved predicate requires **one exact** matching `SUBMITTED` polish
consumer attempt. `_live_exact_first_polish_authority_request()` currently
sets a Boolean when it finds a match, so two duplicate matching attempts still
qualify for `await_external_authority`.

Please count matching attempts and require `count == 1`; zero or more than one
must retain the existing closed/review posture. Add a provider-free regression
cell which duplicates the otherwise exact matching attempt and asserts that no
external-authority request is selected. This is not a request to change normal
authoring behavior—it is a corruption/ambiguity fence for the narrowly opened
exception.

## Approval boundary after that correction

Once the exact-one regression is green alongside the current stale/missing,
mismatched, and committed-terminal controls, API will approve Slice 3 for the
normal SBE package/release gates. No API runtime change, schema change, or
contract expansion is needed.
