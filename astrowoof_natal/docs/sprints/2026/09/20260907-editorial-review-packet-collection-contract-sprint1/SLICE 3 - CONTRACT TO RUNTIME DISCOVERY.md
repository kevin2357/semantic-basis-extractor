# Slice 3 — Contract-to-runtime discovery

Status: paused before runtime implementation for one joint contract decision.

## Outcome first

The exact-result publication boundary is suitable for the builder: the public
`read_native_transition_result(run_dir, result_id)` reader validates the explicit
invocation-returned result, its canonical receipt, bounded journal range, current
workspace snapshot, retained snapshot, and checkpoint basis without using latest
result discovery.

The adopted packet model nevertheless has one concrete mismatch with production
native evidence. The prose contract says the six initial authoring passes are
parallel and must not fabricate deck chaining. The frozen decision schema requires
every decision, including every `initial_pass`, to carry a `transition` containing
`input_deck` and `output_deck` references whose artifact kind is
`assembled_deck`.

Production does not have six sequential or independently assembled decks at that
boundary. Each initial pass consumes a released pass workspace and produces an
authored claim workspace. The first whole-subject deck is produced only by the
later assembly boundary. Representing those workspaces as assembled decks, or
pointing all six decisions at a convenient later deck, would manufacture evidence
and violate the adopted semantic contract.

## Evidence mapped

- `native_transitions.read_native_transition_result` is the correct explicit-ID
  reader. `latest_native_transition_result` is unnecessary and remains forbidden.
- `run.json.passes[*].attempts[*].response_workspace` binds an initial pass attempt
  to its authored workspace.
- `run.json.passes[*].accepted_workspace` identifies the accepted pass workspace.
- `run.json.subjects[*].deck` and the final subject directory identify the first
  assembled whole-subject deck and later optional-stage candidates.
- The sprint-local private calibration builder treated initial pass records as
  pass decisions without pretending that they were whole-deck mutations. That
  evidence shape cannot currently be expressed by the decision v1 schema.
- The synthetic v1 fixtures avoid a schema failure by inventing synthetic base and
  per-pass deck values. They remain useful relationship fixtures, but they do not
  prove production constructibility for this particular relation.

## Narrow decision required

Recommended correction: discriminate the decision transition by stage.

1. `initial_pass` decisions carry a closed initial-pass materialization relation
   joining released pass identity, exact input workspace/source digest, exact
   authored-output workspace/content digest, adoption outcome, action/binding, and
   provider response. It must not call either side an assembled deck.
2. `creative_retry`, `polish`, `critic`, and `candidate` retain the current
   whole-deck transition algebra.
3. Add one closed artifact kind for the initial-pass authored output (and, only if
   the released source itself must be retained, one source-basis record). A leaner
   alternative is to keep those digests directly in the initial-pass transition
   and reserve full artifact records for assembled decks and provider responses.
4. Preserve exactly six initial decisions, total contiguous ordinals, action and
   Response joins, and the independently evidenced initial assembly boundary.
5. Update both positive fixtures and add a mutation proving an initial pass cannot
   masquerade as a whole-deck transition.

This is a contract-shape correction, not a lifecycle, custody, provider, or API
transport change. Runtime construction remains provider-free and read-only.

## Work deliberately not performed

- No workspace, provider, R2, Better Stack, API, database, or network access.
- No runtime builder was written around fabricated initial-pass deck evidence.
- No adopted v1 schema or fixture was silently changed before joint review.
- No latest-result discovery was used.
