# API Slice 4A Review

Status: correction requested before approval.

## What is aligned

The new closed `astrowoof.post_fan_in_retry_inspection_bundle.v1` is the right
public bridge for the joined API campaign.  Its seven fixed, ordered projections
provide the public facts the API needs to exercise its real translator,
persistence, scheduler, lease, and capacity services without reconstructing
native state: run/route/mechanism identity; selected command; capacity
disposition and reason; eligibility/schedule; provider-custody action inventory;
local operation inventory and consumption; and external-authority action IDs.

The package surface, closed schema, per-phase and outer semantic digests,
provider-free CLI, reproducibility test, semantic-mutation test, and privacy
sentinel coverage are all appropriate.  In particular, it preserves the key
authority boundary: this is observation evidence only, not an API grant to
select a native command or mutate SBE state.

The projection deliberately remains an inspection *projection*, not a complete
v0.7 inspection document.  That is correct: API should introduce/use a narrow
public-bundle translator for this fixture, rather than fabricate missing private
checkpoint fields or claim that the bundle can be passed directly to the generic
v0.7 inspection validator.

## Required correction: make receipt binding real

`validate_post_fan_in_retry_inspection_bundle()` currently checks only that
`qualification_receipt_sha256` has the shape of a SHA-256 digest.  A mutation
test that replaces it with (for example) 64 zeroes and recomputes
`bundle_sha256` is accepted.  Thus the bundle is internally content-addressed,
but its claimed binding to the qualification receipt is not independently
validated.

Please make the validator and test suite bind this field to the canonical public
qualification receipt for this exact fixture/package invocation.  The test must
mutate only `qualification_receipt_sha256`, recompute the outer digest, and
assert validation fails.  Refactor the shared provider-free construction as
needed to avoid recursive validation; do not weaken the closed public surface or
add private workspace data.

Once that passes, please rerun the Slice 4A focus/adjacent tests and update the
handoff/log/evidence.  The pre-4A `0.4.27` candidate must not be reused for the
joined campaign: build and qualify a new candidate after this change, then pause
again before publication so API can pin that exact wheel and consume this bundle.

