# Bounded Authoring Topology and Transport Parity Sprint 2 Evidence

Status: Slices 0-8 complete; 0.4.6 release recommendation awaiting authorization

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

## Slice 6

Result: [results/SLICE 6 - Assembly Whole Deck QA and Optional Continuity.md](results/SLICE%206%20-%20Assembly%20Whole%20Deck%20QA%20and%20Optional%20Continuity.md)

Verification:

- interactive-initial and Batch-initial bounded runs assemble byte-identical final
  cards before and through the enabled optional stages;
- Batch initial authoring and creative retries remain Batch transport, while
  polish, critic, and qualitative-candidate actions are explicitly bound to
  interactive Responses transport under the approved release contract;
- normalized duplicate prose authored in two independently assigned passes is
  rejected by whole-deck final QA;
- existing optional-stage reconciliation and polish crash-checkpoint regressions
  remain green;
- desktop bounded/lifecycle gate: 135 tests passed in 132.412 seconds;
- Python 3.11 Linux with a read-only repository mount: the same 135 tests passed in
  31.004 seconds; and
- `git diff --check` passes with expected checkout line-ending notices only.

Provider operations: 0. Spend: USD 0.

## Slice 7

Result: [results/SLICE 7 - Public Lifecycle Fixtures Oracle and Handoff.md](results/SLICE%207%20-%20Public%20Lifecycle%20Fixtures%20Oracle%20and%20Handoff.md)

Consumer handoff: [BOUNDED ROUTE PARITY CONSUMER HANDOFF.md](BOUNDED%20ROUTE%20PARITY%20CONSUMER%20HANDOFF.md)

Review manifest: [fixtures/bounded-route-parity-slice7-consumer-review.json](fixtures/bounded-route-parity-slice7-consumer-review.json)

Verification:

- strict installed Python readers and provider-free CLI export reject unknown
  schemas, fields, vocabulary values, duplicate names, and unordered trace steps;
- packaged route-parity oracle v2 admits bounded Batch without changing the public
  lifecycle vocabulary and preserves legacy v1 as historical refusal evidence;
- route-specific traces cover interactive multi-pass/retry; Batch pending,
  `not_due`, reclaim, partial-member retry, unavailable usage, ambiguity, provider
  failure, and delivery;
- consumer-review manifest pins both packaged resources by SHA-256;
- desktop lifecycle/bounded/native-transition gate: 132 tests passed in 156.449
  seconds (6 optional `jsonschema` tests skipped in the lean runtime);
- Python 3.11 Linux read-only-container gate: 132 tests passed in 19.832 seconds
  with the same 6 optional skips; and
- lifecycle installed-resource smoke passes with the v2 oracle and trace readers.

Provider operations: 0. Spend: USD 0.

## Slice 8

Result: [results/SLICE 8 - Installed Qualification and 0.4.6 Recommendation.md](results/SLICE%208%20-%20Installed%20Qualification%20and%200.4.6%20Recommendation.md)

Release records: [../../../../../releases/0.4.6/RELEASE NOTES.md](../../../../../releases/0.4.6/RELEASE%20NOTES.md)

Verification:

- full repository suite: 423 passed in 428.695 seconds with 10 expected
  environment-dependent skips;
- strict contract/release subset under an environment with Draft 2020-12
  `jsonschema`: 48 passed;
- two fixed-epoch candidate builds were byte-identical at SHA-256
  `bf864e2376ba36f3a8a292b3092c095ee52fac2ce8fcf081521f6ad3a3350ff2`;
- candidate inventory: 800,957 bytes, 106 entries, 61 resources, `py.typed`, both
  accepted Slice 7 resources, no tests, and no bytecode/cache entries;
- isolated Windows CPython 3.12 installation: `pip check`, lifecycle smoke, release
  smoke, route-evidence CLI, and exact/bounded interactive/Batch fake routes passed;
- fresh Linux CPython 3.11 installation: the same installed gates and all four fake
  routes passed;
- exact SPC 0.11.0 wheel hash reverified as
  `82290df44fe5697e87df2e27eb0aa4bab3b7954c66ce988efda0962964e1366d`;
- approved oracle/trace hashes are repeated in the 0.4.6 release handoff and
  candidate manifest; and
- the `0.4.5`-named qualification wheel is explicitly non-publishable. Final
  release requires an authorized 0.4.6 version bump and exact rebuilt artifact.

Provider operations: 0. Spend: USD 0.

## 0.4.6 final artifact qualification

- Artifact source commit:
  `ac86613b42ebc4f7d86cb557be9fbf82aaa1900d`.
- Final wheel: `astrowoof_natal_authoring-0.4.6-py3-none-any.whl`.
- Bytes: 800,957.
- SHA-256:
  `1770d5c361b81ac5ed90b5b1a825da70aec108a665ac251a13a520d1af66e788`.
- Fixed epoch: `1787067938`; two builds byte-identical.
- Exact final Windows and Linux installed gates: pass.
- Installed exact interactive, exact Batch, bounded interactive, and bounded Batch
  fake-provider routes: pass.
- Provider operations: 0. Spend: USD 0.
