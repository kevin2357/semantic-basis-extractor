# Bounded Authoring Topology Contract Proposal

Date: 2026-08-18
Status: Slice 1 proposal for SBE/API review; not admitted by runtime

## Decision summary

Bounded Natal adopts the exact route's editorial topology without adopting exact
semantic authority:

- five isolated ten-card story passes;
- one isolated summary/global-theme pass;
- deterministic heterogeneous assignment and canonical final reassembly;
- one paid action per interactive pass/attempt;
- one paid action and one API global reservation per Batch round; and
- identical bounded logical pass requests across interactive and Batch after
  documented transport-envelope normalization.

No new public lifecycle, terminal, custody, consumer-authority, or cost-disposition
vocabulary is proposed. New native pass/round/member evidence composes through
existing states. Discovery of an unrepresentable fact returns this contract to
review.

## Contract identities

| Artifact | Proposed identity |
|---|---|
| Bounded authoring run | `astrowoof.bounded_natal.authoring_run.v2` |
| Split assignment | `astrowoof.bounded_natal.split_assignment.v1` |
| Logical pass request | `astrowoof.bounded_natal.logical_pass_request.v1` |
| Authority aggregation | `astrowoof.bounded_natal.authority_aggregation.v1` |
| Route-parity oracle | `astrowoof.route_parity_transition_oracle.v2` |

The existing `astrowoof.bounded_natal.authoring_run.v1` identifies one-operation
bounded state and is not silently upgraded. Resume under a v2-only runner fails
closed through the normal terminal evidence path with native outcome
`terminal_failure`, cause `legacy_bounded_topology_unsupported`, and the observed v1
contract identity before provider work or mutation. This is distinct from an
accidental unknown/incompatible contract. No fabricated six-pass history or generic
snapshot blessing is supported.

## Assignment artifact

The assignment artifact binds:

- subject and source 50-claim deck SHA-256;
- policy and algorithm version;
- explicit replay seed and seed basis;
- exactly five ordered card passes of ten unique claim IDs;
- one separate summary/theme pass;
- canonical selected-claim order; and
- assignment digest used by every logical request and run/action binding.

The seed is deterministic for the frozen input/policy contract. It is evidence, not
provider data. Transport never selects, shuffles, or repartitions claims.

Bounded assignment initially targets the exact `stratified-v1` goals through a
bounded feature adapter. It distributes bounded claim families and editorial tiers
and avoids homogeneous adjacency without inventing exact-placement features or
epistemic scores.

## Logical pass identity

Closed pass purposes are:

- `card_story`, pass numbers 1-5, exactly ten ordered claim IDs; and
- `summary_theme`, pass number 6, no card claim membership.

The stable pass ID is `<subject>_bounded_<N>`. An attempt route is:

```text
bounded_natal.v2:<pass_id>:attempt-<NNN>
```

Every request/action binds route family, run contract, assignment SHA-256, pass ID,
pass purpose, pass number, ordered member IDs, attempt, stage, resource-set SHA-256,
output-schema SHA-256, model, reasoning configuration, service level, maximum output,
price book, and exact request digest.

For interactive authoring, provider operation kind is `response`. For Batch, the
logical pass identity is a member of a round and provider operation kind is `batch`;
the member's optional Response ID is ingestion evidence, not a separate authority.

## Request-parity rule

The release-blocking comparison is bounded interactive to bounded Batch for the
same frozen bounded pass/attempt. Normalize only:

- interactive `background` behavior;
- explicit interactive prompt-cache options/key/breakpoints that Batch does not
  support through this contract; and
- the outer Batch JSONL `custom_id`, method, URL, and body wrapper.

After normalization, model, reasoning configuration, system bytes, ordered user
segments, strict structured-output schema, maximum output, safety identifier, retry
feedback, and semantic membership are identical.

Exact and bounded prompt-resource bytes may intentionally match. Exact and bounded
route packets, authority notices, and schemas are not parity targets.

## Prompt/resource boundary

Bounded receives separately named and versioned copies of the exact story-workspace
editorial resources. Initial proposed names are:

- `Bounded Natal Story Workspace Authoring Brief.md`; and
- `Bounded Natal Authoring Guiding Lights.md`.

At first admission their content must match the corresponding exact resources byte
for byte. A resource manifest binds both copies and their hashes. Later bounded-only
guidance may diverge only through explicit resource-contract versioning, prompt-
geometry identity, tests, documentation, and consumer qualification.

Bounded route-specific packet construction additionally supplies its established
invariant-only authority notice and forbids representative time, exact placement,
orb, strength, confidence, houses, and angles. Those route bytes are not copied into
exact Natal.

## Authority aggregation

### Interactive

- One SBE paid action per pass/attempt.
- One exact API authorization/reservation reference per action.
- Binding includes route/pass/attempt and the exact request digest.
- Known Response identity is durable before further local mutation.
- Polling a known Response adds no commitment.
- Pass-local creative retry creates a new action and never replaces prior evidence.

### Batch

- One SBE paid action per Batch round.
- One API global reservation per Batch round.
- Aggregate maximum output and commitment cover every ordered member.
- The round artifact carries the exact aggregate maximum commitment, member count,
  ordered member identity inventory, and settlement basis bound by the action.
- Member usage, Response IDs, outcomes, and estimated cost settle beneath the round.
- Members never multiply global reservations or become independent authority keys.
- A retry round contains only eligible rejected/error passes and receives a new exact
  round action/reservation.

Both modes are bounded by the same immutable aggregate and stage ceilings in the
frozen SBE run policy. The API remains authoritative for cross-run/global authority.

## Lifecycle composition

The six-pass topology reuses existing outcomes:

- `awaiting_external_authority`;
- `detached_provider_pending` and nonmutating `not_due`;
- `progressed_local` / local continuation;
- delivery, review, budget exhaustion, policy stop, ambiguity, and provider terminal
  failure; and
- existing provider-custody and consumer-authority cost dispositions.

After an initial wave completes, the run must be re-driven through its next required
authorization/provider/local boundary. Native `awaiting_external_authority` is a
durable scheduling fact, not permission for the API worker to retain a lease forever
or silently abandon the run.

## Oracle evolution

The packaged v1 oracle remains immutable historical evidence that bounded Batch was
unsupported. Proposed v2 replaces that refusal with supported route-specific
scenarios while reusing the closed existing outcome/disposition vocabulary.

Required v2 traces include prepared/authorization wait, pending, `not_due`, reclaim,
completed, mixed member failure and local continuation, pass-local retry, unavailable
usage with consumer authority retained, ambiguity/review, provider terminal failure,
legacy-topology terminal failure, failure before native/provider evidence exists with
a typed reason, and final delivery.

The API's effective oracle remains route-neutral and requires no new enum/event. The
consumer handoff will supply bounded route traces through its existing transitions.

## Review questions

1. Are the proposed v2 run and v1 assignment/request/aggregation identities suitable
   for strict API validation?
2. Is one API reservation per Batch round with member settlement sufficient for API
   audit and release decisions?
3. Is the interactive route/pass/attempt binding sufficient to distinguish six
   initial actions and later pass-local retries?
4. Are the request-parity normalization fields complete and narrow enough?
5. Is `terminal_failure` plus `legacy_bounded_topology_unsupported` and the observed
   v1 contract identity sufficient for retained-workspace disposition?
6. Do the revised oracle v2 scenarios cover the API adoption needs without adding a
   public state?
