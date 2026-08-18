# Bounded Authoring Topology and Transport Parity Sprint 2 Evidence

Status: Slices 0-5 complete; Slice 5 awaiting API fixture/lifecycle review

No provider operation was submitted. Slice 0 added one provider-free exact request-
parity regression and recorded the current route/topology baseline.

Planning facts:

- starting SBE release: `0.4.5`;
- exact default split policy: deterministic `stratified-v1`;
- intended topology: five ten-card passes plus one summary/theme pass;
- current bounded interactive topology: one whole-deck Responses operation;
- current bounded Batch disposition: fail closed before submission; and
- planning provider operations/spend: 0 / USD 0.

## Slice 0

Result: [results/SLICE 0 - Baseline and Editorial Invariant.md](results/SLICE%200%20-%20Baseline%20and%20Editorial%20Invariant.md)

Focused command coverage:

- exact deterministic stratification, balance, and canonical reassembly;
- exact live/Batch normalized logical-request parity;
- exact six-pass fake interactive completion;
- exact six-member Batch completion and Batch detach/resume;
- bounded OpenAI provider request/hydration/Batch-refusal suite; and
- provider-pending route/capacity baseline suite.

Outcome: 36 tests passed in 23.412 seconds.

Provider operations: 0. Spend: USD 0.

## Slice 1

Contract: [BOUNDED AUTHORING TOPOLOGY CONTRACT PROPOSAL.md](BOUNDED%20AUTHORING%20TOPOLOGY%20CONTRACT%20PROPOSAL.md)

Result: [results/SLICE 1 - Contract Identity and Resource Freeze.md](results/SLICE%201%20-%20Contract%20Identity%20and%20Resource%20Freeze.md)

Proposal artifacts:

- `fixtures/bounded-authoring-topology.proposal.schema.json`;
- `fixtures/bounded-split-assignment.proposal.json`;
- `fixtures/bounded-authority-aggregation.proposal.json`;
- `fixtures/bounded-editorial-resource-parity.proposal.json`; and
- `fixtures/route-parity-transition-oracle.v2.proposal.json`.

Verification:

- Python 3.11 local SBE worker image: 6 strict proposal tests passed;
- desktop focused runtime baseline: 31 tests passed, with 5 `jsonschema`-dependent
  proposal tests explicitly skipped because that lean interpreter lacks the module;
- both bounded editorial resource copies match their exact counterparts byte for
  byte at the working-tree gate; and
- `git diff --check` passes.

Provider operations: 0. Spend: USD 0.

## Slice 2

Result: [results/SLICE 2 - Bounded Six Pass Packets.md](results/SLICE%202%20-%20Bounded%20Six%20Pass%20Packets.md)

Runtime contracts admitted:

- `astrowoof.bounded_natal.split_assignment.v1`;
- `astrowoof.bounded_natal.authoring_pass_packet.v1`; and
- bounded six-pass compilation under `astrowoof.bounded_natal.authoring_run.v2`.

Verification:

- focused desktop bounded authoring/provider/product-QA/lifecycle suite: 39 tests
  passed in 45.660 seconds;
- Python 3.11 Linux worker image: all 12 bounded-authoring tests passed;
- generated assignment and all six packets validate against the two packaged strict
  schemas;
- mutation checks reject extra transport guesses, altered membership, duplicate or
  missing claims, changed ordering, and incomplete pass output; and
- `git diff --check` passes (Git reports only the repository's expected checkout
  line-ending notices).

Provider operations: 0. Spend: USD 0.

## Slice 3

Result: [results/SLICE 3 - Shared Pass Seam.md](results/SLICE%203%20-%20Shared%20Pass%20Seam.md)

Verification:

- shared logical-pass identity, replay, conflict, route-crossing, and bounded adapter
  suite plus the complete exact semantic-closure regression suite: 90 tests passed
  in 214.081 seconds;
- bounded protocol/provider/packet focused suite: 21 tests passed in 1.215 seconds;
- Python 3.11 Linux worker image: 10 focused shared-pass, bounded-provider, and exact
  live/Batch parity tests passed; and
- `git diff --check` passes with only expected checkout line-ending notices.

Provider operations: 0. Spend: USD 0.

## Slice 4

Result: [results/SLICE 4 - Bounded Interactive Six Pass Lifecycle.md](results/SLICE%204%20-%20Bounded%20Interactive%20Six%20Pass%20Lifecycle.md)

Verification:

- desktop bounded lifecycle/product-QA/provider suite: 31 tests passed in 110.463
  seconds;
- desktop shared provider-capacity, lifecycle inspection/contracts/consumer/
  closeout, native-transition, and spend-enforcement suite: 109 tests passed in
  21.780 seconds;
- Python 3.11 Linux container with the repository mounted read-only: the same 31
  focused bounded tests passed in 21.955 seconds;
- six initial isolated calls preserve exact pass membership and canonical assembly;
- authorization waits are exercised at every pass boundary, and one rejected pass
  produces only one pass-local retry;
- the post-wave scheduler regression reaches the next durable external-authority
  boundary without retaining a lease or duplicating provider work;
- v1 legacy state refuses with `legacy_bounded_topology_unsupported`; and
- `git diff --check` passes with only expected checkout line-ending notices.

Provider operations: 0. Spend: USD 0.

## Slice 5

Result: [results/SLICE 5 - Bounded Batch Transport.md](results/SLICE%205%20-%20Bounded%20Batch%20Transport.md)

Consumer handoff: [BOUNDED BATCH SLICE 5 CONSUMER HANDOFF.md](BOUNDED%20BATCH%20SLICE%205%20CONSUMER%20HANDOFF.md)

Review fixture: [fixtures/bounded-batch-slice5-consumer-review.json](fixtures/bounded-batch-slice5-consumer-review.json)

Verification:

- actual recorded bounded interactive request versus bounded Batch member: exact
  equality after removing only interactive `background`;
- one six-member initial Batch round and one-member pass-local retry round;
- one paid action/aggregate commitment per round, never per member;
- detach/resume and post-provider-identity interruption retrieve the same Batch ID
  with no duplicate upload or creation;
- output/error partial failure, provider-terminal failure, duplicate member,
  unknown/missing inventory, strict round-state, fully unavailable usage, and
  mixed member-usage cases;
- aggregate settlement requires complete usage for every potentially billable
  member; a partial total is never reported or settled as the round total;
- retrieval-only route-neutral reconciliation with bounded v2 route/mechanism
  identity and unchanged upload/create counts;
- exact semantic-closure compatibility: 85 tests passed in 207.894 seconds;
- desktop bounded/lifecycle/transition/capacity gate: 120 tests passed in 124.146
  seconds;
- Python 3.11 Linux with a read-only repository mount: 120 tests passed in 27.162
  seconds; and
- `git diff --check` passes with expected checkout line-ending notices only.

Provider operations: 0. Spend: USD 0.
