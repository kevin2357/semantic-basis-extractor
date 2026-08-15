# API Consumer Response

Status: final sprint response

## 1. Is terminal `DELIVERY_COMPLETE` supported?

**Answer:** Yes. SBE permits batch denial in `DELIVERY_COMPLETE` when every
requested action is independently authorized/prepared but unconsumed and has no
provider identity, evidence, or submission ambiguity. The operation does not reopen
editorial processing and preserves accepted deck/delivery bytes exactly.

**Confidence:** High. This is explicit contract policy and is exercised by the
baseline, successful mutation, replay, recovery, and installed smoke fixtures.

## 2. Must every action independently qualify, all or none?

**Answer:** Yes. One locked preflight evaluates every exact member before semantic
mutation. One duplicate, unknown, stale, mismatched, provider-bound, ambiguous, or
otherwise ineligible member refuses the complete batch. No member becomes release
eligible and no authoritative workspace byte changes on an ordinary refusal.

**Confidence:** High. Each refusal category and mixed eligibility is directly tested
with before/after authoritative workspace hashes.

## 3. What result fields distinguish outcomes?

**Answer:** The public v0.1 result contains:

- top-level `applied` and closed `outcome`;
- exact `run_id`, `batch_request_sha256`, and `request_observation`;
- on success/replay, locked `decision_basis`, ordered `actions`, one
  `post_mutation_observation`, and shared `result_checkpoint`;
- on refusal, ordered member assessments, bounded `review_reasons`, and
  `actual_observation` when safely available; and
- per successful member, exact `action_id`, immutable `binding`, outcome,
  `DENIED_PROVIDERLESS` disposition, denial reason, prior-authorization fact,
  `release_eligible`, and external authority reference.

Closed batch outcomes distinguish application/replay, stale observation, binding,
unknown/duplicate action, provider identity/evidence/consumption, ambiguous
submission, ordinary ineligibility, invalid native state, exclusivity/race, and
review-required refusal. A refused member may be `eligible` or `not_evaluated`, but
neither is release evidence.

**Confidence:** High. Strict schemas, four packaged fixtures, canonical digest tests,
runtime refusal tests, and installed resource loading cover this contract.

## 4. Does single-action denial remain supported?

**Answer:** Yes, unchanged. `deny_providerless_action()` and
`deny-providerless` remain the supported choice for a genuine one-action decision.
Consumers must use the batch operation rather than reusing one inspection across a
sequential multi-action loop.

**Confidence:** High. Existing single-action tests, smoke coverage, CLI, and
batch-versus-single contention tests all remain green.

## 5. Can batch closeout run/replay on a retained terminal workspace without provider work?

**Answer:** Yes. Restore the complete workspace at its stable logical absolute path,
hold the API-owned fence, inspect, call `deny_providerless_actions()` or
`deny-providerless-batch`, persist the result in API authority, inspect again, and
close out. Exact retry after interruption either safely restarts before mutation,
narrowly completes the recorded write set, or returns idempotent replay. The batch
operation accepts no provider client and cannot submit or resubmit work.

**Confidence:** High for SBE-native behavior. Windows and Linux installed-wheel
smokes pass without dependencies, network, API key, or provider calls. SBE cannot
make claims about API lease correctness, API transactional release, or external
provider atomicity; those remain API/provider boundaries.

## Acceptance-expectation disposition

- Public Python interface: delivered.
- Public CLI interface: delivered.
- Strict versioned schemas and four fixtures: delivered and packaged.
- Two-action application and exact replay: tested.
- Stale/mixed/duplicate/unknown/binding/provider/ambiguity refusal: tested.
- Terminal delivery preservation: tested.
- Ordered, replay-safe, failure-isolated events: tested.
- Interrupted-write recovery: tested at every native boundary.
- Installed-wheel smoke: passed on Windows Python 3.12 and Linux Python 3.11.
- API handoff and migration guidance: delivered.

The API retains ownership of PostgreSQL paid-action rows, leases, reservations,
capacity, publication, and audited repair of previously affected Aster/Bramble
records.
