# API Agent Response to SBE LLM Prompt Versioning — Slice 0 Findings

## Response

Approved in principle. A prompt release binding—not a free-form
`--prompt-version` string—is the correct durable abstraction. It makes the
selected reusable prompt assets explicit while preserving the important
distinction among release assets, job-specific workspace evidence, retry
feedback, and the fully rendered private request.

The existing private attempt custody and historical recovery path are valuable
assets, but they should not be retrofitted into a release-selection mechanism.
New release binding applies when a new provider action is created. Historical
workspaces retain their existing private rendered request and legacy recovery
rules; they must not receive synthetic prompt-release provenance.

## API ownership and durable evidence

At new-run admission, API should bind the selected processing profile and,
through it, its approved prompt release before any provider action is prepared.
The durable run/action evidence must retain safe, immutable provenance such as:

- prompt release ID and semantic version;
- prompt-release map digest;
- selected component asset digest inventory for the applicable stage; and
- rendered-request digest for the concrete provider request.

The first three identify reviewed reusable assets; the rendered-request digest
joins the actual request without exposing prompt text, dog data, feedback,
workspace paths, raw provider response text, or secrets. Where the economics
and editorial evidence models need a safe correlation field, they should join
on action/run identity plus the allowed release/request digests—not on normal
logs or a reconstructed request.

API must reject an absent, unknown, deprecated, wrong-environment,
wrong-route, or wrong-profile release before provider work starts. The API
cannot "helpfully" substitute its current default. For a resume,
reconciliation, retry, polish, or detached continuation, the persisted binding
wins; a conflicting CLI argument is a fail-closed configuration error.

## CLI selector policy

The eventual command-line selector remains useful for local and qualification
work, but it should be a request to resolve an approved release through the
same registry and policy—not an authority to choose arbitrary prompt text or
override a persisted run. A workable shape is an explicit release identifier
at new-job creation, with API/SBE validation that it is allowed by the selected
profile, route, environment, and installed package bundle. The chosen ID and
digest then become immutable action/run evidence.

This gives release experiments a clean boundary: a new QA run can deliberately
select an approved experimental profile/release, while production defaults and
older admitted runs remain unchanged. It also makes rollback a selection of an
older still-approved immutable release, not an in-place edit under a familiar
version string.

## Gate A additions from the API perspective

The proposed provider-free matrix is approved. In addition, the integrated
consumer test should prove that API admission persists and returns the same
profile/prompt binding across handoffs, and that an action cannot be prepared
when SBE's installed release bytes do not match the expected digest. It should
also prove that ordinary structured operational events contain only safe
identifiers/digests and cannot be used to reconstruct prompt text or subject
data.

The current direct-to-dog/full-astrology copy issue is a legitimate candidate
for a later release experiment, but the finding is correct: do not tune live
wording before this provenance boundary can identify exactly which request
formulation produced a card.

## Decision

Proceed to freeze the durable action/run locations for the prompt-release
binding and the profile-to-release compatibility rule. Do not change prompt
wording, add an implicit default fallback, or backfill legacy workspaces in
this sprint slice.
