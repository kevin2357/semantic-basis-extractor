# Bounded Authoring Topology and Transport Parity Sprint 2 Log

## 2026-08-18 — Planning

- Opened the sprint for review; no implementation began.
- Recorded that six-pass fan-out is a writing-quality invariant intended to prevent
  templated bulk generation, not a performance optimization.
- Separated semantic route from provider transport: exact/bounded determine evidence
  and authority; interactive/Batch determine submission and retrieval only.
- Confirmed exact `stratified-v1` assignment is deterministic for a frozen packet,
  subject, and policy identity rather than randomly reshuffled on every run.
- Planned separately versioned bounded editorial resources whose intended shared
  content initially matches exact resources.
- Identified current bounded whole-deck interactive authoring as part of the topology
  correction, not merely a prerequisite for adding bounded Batch.
- Confirmed no new public lifecycle vocabulary is expected. The sprint must still
  version SBE's route-parity oracle because v1 explicitly rejects bounded Batch, and
  must provide bounded live/Batch traces through the API's existing route-neutral
  transition oracle. Discovery of an unrepresentable state pauses for contract
  review.
- API plan review approved the sprint with clarifications now incorporated: the
  post-wave scheduler must re-drive bounded work through its next authorization or
  provider boundary; interactive authority is one action per pass/attempt; Batch
  authority is one action/global reservation per round with member settlement;
  request parity compares bounded live to bounded Batch rather than exact packet
  bytes to bounded packet bytes; and legacy one-operation bounded state fails closed.
- Provider operations: 0. Spend: USD 0.

## 2026-08-18 — Slice 0 baseline and editorial-invariant evidence

- Added a provider-free regression proving exact interactive and Batch builders
  produce identical logical pass requests after removing the documented interactive-
  only `background` transport-envelope field. The test disables explicit cache
  controls because Batch intentionally omits those transport options.
- Reconfirmed `stratified-v1` determinism, complete 50-claim assignment, improved
  claim-type/category balance, and canonical-order reassembly.
- Reconfirmed exact fake interactive and Batch paths each author six isolated passes;
  Batch detach/resume ingests the same durable Batch rather than creating another.
- Reproduced the bounded baseline from the compiled provider fixture: 50 claims and
  four summaries are sent through one bounded pass/whole-deck provider operation.
- Reconfirmed bounded Batch rejects during provider construction before any provider
  submission and the current route-parity oracle labels it `bounded_batch_rejected`.
- Inventoried the reuse seam: Files/Batch transport, JSONL correlation, durable Batch
  identifiers/artifacts, polling, cost disposition, and reconciliation are reusable;
  exact `PassSpec`, Markdown workspace reconstruction, pass acceptance, and assembly
  are route-specific and must sit behind a shared pass protocol rather than be copied.
- Identified the required state migration boundary: current bounded runs persist one
  pass ID and stage/attempt route. New six-pass runs need a new route/run contract;
  legacy one-operation workspaces must fail closed.
- Focused provider-free baseline: 36 tests passed in 23.412 seconds.
- Provider operations: 0. Spend: USD 0.
- Slice 0 is complete and paused for the planned review gate.

## 2026-08-18 — Slice 1 contract, identity, and resource freeze

- Proposed `astrowoof.bounded_natal.authoring_run.v2` for six-pass state. Existing
  v1 one-operation runs remain historical and fail closed; no implicit migration or
  fabricated pass history is supported.
- Proposed strict v1 split-assignment and authority-aggregation contracts with
  canonical fixtures. The assignment binds five ordered ten-claim passes, one
  summary/theme pass, source deck, deterministic policy/seed, canonical order, and
  assignment digest.
- Froze interactive authority at one paid action per route/pass/attempt and Batch
  authority at one paid action/API global reservation per round with member evidence
  settling beneath it. Immutable aggregate/stage run ceilings apply to both.
- Froze request parity as bounded interactive versus bounded Batch for the same
  frozen bounded pass, with only documented interactive cache/background and outer
  Batch envelope differences. Exact versus bounded route packet/schema bytes are not
  parity targets.
- Added separately named bounded story-workspace brief and guiding-lights resources.
  Their entry bytes exactly match the exact resources and are hash-frozen in a
  proposal manifest. Runtime does not consume them until Slice 2.
- Proposed route-parity oracle v2 scenarios that admit bounded Batch using existing
  lifecycle outcomes. Packaged v1 remains unchanged with its historical
  `bounded_batch_rejected` refusal.
- Added six strict proposal tests covering schema validity, cardinality/closure,
  additional-field refusal, authority units, resource hash parity, and oracle
  evolution. All six passed under the local Python 3.11 SBE worker image.
- The bundled desktop Python lacks `jsonschema`; its broader focused run passed 31
  executable runtime tests and explicitly skipped five strict schema tests. No
  validation claim relies on those skips; Docker supplied the six strict passes.
- A Ruff invocation was attempted in the worker image, but that image does not
  install Ruff. Unit/schema execution and `git diff --check` are the applicable gate
  evidence here.
- Provider operations: 0. Spend: USD 0.
- Slice 1 is complete and paused for API contract review before runtime admission.
- API review approved the Slice 1 identities, authority aggregation, interactive
  binding, parity normalization, oracle direction, and state-vocabulary reuse.
  Requested hardening was incorporated before commit: explicit Batch round aggregate
  commitment/member/settlement evidence; terminal cause
  `legacy_bounded_topology_unsupported` with observed v1 identity; and an oracle trace
  for typed terminal failure before native/provider evidence exists.

## 2026-08-18 — Slice 2 deterministic bounded six-pass packets

- Admitted the bounded split-assignment and pass-packet contracts into the packaged
  schema catalog rather than treating the Slice 1 proposals as loose examples.
- Implemented deterministic bounded assignment across five ten-card passes plus one
  summary/theme pass. Every selected claim occurs exactly once, while the assignment
  algorithm balances claim kind, editorial tier, proof scope, and priority band and
  reduces homogeneous adjacency inside each pass.
- Built six self-contained minimized provider views. Each pass binds the v2 route,
  assignment identity, exact ordered membership, bounded authority notice, minimized
  subject, selected registry, whole-dog context, and separately named bounded
  editorial resources. Transport selection is deliberately absent.
- Added strict native validation for assignment and packet key sets, identities,
  ordering, membership, summary scope, registry closure, resource identity, digest,
  and provider-visible privacy.
- Added deterministic canonical reassembly from unordered pass results. Card rows
  return to claim-deck order and summaries return to the frozen summary-field order
  before immutable authority is reattached and final bounded QA runs.
- Kept execution state untouched in this slice: `create_bounded_run()` still uses
  the historical one-operation lifecycle. Slice 4 will admit v2 six-pass lifecycle
  execution; compilation alone cannot silently reinterpret an existing v1 run.
- Focused desktop suite: 39 tests passed in 45.660 seconds. Python 3.11 Linux worker
  image: 12 bounded-authoring tests passed. Generated assignment and all six packets
  also passed their packaged strict schemas.
- Provider operations: 0. Spend: USD 0.
- Slice 2 is complete and paused for the planned gate review.

## 2026-08-18 — Slice 3 shared pass seam and exact compatibility

- Added a small transport-neutral logical-pass protocol. It binds route family and
  contract, assignment, pass, attempt, stage, resources, prompt, output schema, and
  maximum output into one deterministic request identity, plus a route-bound result
  identity. It intentionally contains no Responses/Batch mechanism selection.
- Routed exact interactive request construction through the identity seam after its
  existing payload is built. No exact provider payload byte, prompt, schema, cache
  option, workspace behavior, or idempotency calculation was changed.
- Routed exact Batch request construction through the same seam and bound the actual
  attempt number supplied by the round scheduler. The existing normalized live/Batch
  logical-request parity remains unchanged.
- Added the bounded pass adapter over the Slice 2 packets. It validates the packet
  content digest and binds the separately named bounded resources and route contract.
- Tightened bounded pass output schemas to the exact assigned inventory: a card pass
  requires exactly ten known claim IDs and zero summaries; the summary pass requires
  zero cards and exactly its four known summary IDs.
- Added deterministic replay, binding-change, and exact/bounded route-crossing
  refusal tests. Exact-shaped output cannot hydrate bounded authority.
- Complete exact semantic-closure compatibility plus protocol suite: 90 tests passed
  in 214.081 seconds. Focused bounded suite: 21 passed. Linux Python 3.11 worker:
  10 focused tests passed.
- Provider operations: 0. Spend: USD 0.
- Slice 3 is complete and paused for gate review before lifecycle execution changes.

## 2026-08-18 — Slice 4 bounded interactive six-context authoring

- Replaced the bounded whole-deck provider operation with the frozen five card
  passes plus one summary/theme pass under
  `astrowoof.bounded_natal.authoring_run.v2`.
- Bound every interactive paid action to the bounded v2 route, assignment, pass,
  attempt, stage, and exact logical request. Each pass crosses its own external
  authorization boundary and persists provider evidence before later mutation.
- Added independent result validation and authority hydration for every pass,
  canonical assembly after all six are accepted, and pass-local creative retry.
  A rejected pass carries minimized native QA feedback and does not regenerate any
  accepted pass.
- Kept legacy one-operation v1 workspaces fail closed with the typed cause
  `legacy_bounded_topology_unsupported`; no synthetic six-pass history is created.
- Extended native transition and reconciliation route recognition for bounded v2
  while retaining bounded v1 as inspectable historical evidence.
- Corrected lifecycle-capacity precedence so due or completed pass work is driven
  locally, prepared work waits for external authority, and genuinely scheduled
  future work releases capacity until due. The blocking scheduler regression proves
  a completed initial wave reaches its next authorization boundary without an
  indefinite lease, silent stop, or operator repair.
- Desktop focused bounded suite: 31 tests passed in 110.463 seconds.
- Desktop shared lifecycle/native-transition/reconciliation/spend regression suite:
  109 tests passed in 21.780 seconds.
- Python 3.11 Linux read-only-container qualification: 31 tests passed in 21.955
  seconds.
- `git diff --check` passes with only expected checkout line-ending notices.
- Provider operations: 0. Spend: USD 0.
- Slice 4 is complete and paused for gate review before bounded Batch work.

## 2026-08-18 — Slice 5 bounded Batch transport

- Added bounded Batch as a provider transport over the same six frozen bounded
  logical pass requests. An actual recorded interactive payload matches its Batch
  member after removing only the interactive `background` field.
- Persisted closed bounded Batch round/member records with exact JSONL hash, File
  and Batch identities, ordered `custom_id` inventory, aggregate maximum output,
  aggregate commitment, request counts, output/error File identities, terminal
  status, and cost disposition.
- Bound one paid action and one external reservation unit to each Batch round. The
  six initial members and any later retry members remain audit/settlement detail;
  they do not multiply global reservation authority.
- Implemented one six-member initial round and pass-local retry rounds. A rejected
  or provider-error member retries only its pass; a provider-terminal failed round
  retries its six affected passes under creative-retry authority.
- Added durable upload/create/detach/retrieve/download/ingest behavior. Interruption
  after durable Batch identity resumes by retrieving that identity and never
  uploads or creates another Batch.
- Added bounded Batch to native transition, lifecycle inspection v0.3, custody,
  neutral reconciliation dispatch, and CLI reconciliation. Reconciliation is
  retrieval-only and preserves the 40-second Batch cycle bound.
- Missing provider usage is explicitly
  `provider_usage_unavailable_billing_reconciliation_pending`: provider retrieval
  custody ends, while consumer billing authority remains retained. It is never
  represented as reported zero spend.
- API gate review required and received one conservative correction: aggregate
  `provider_usage_reported` now requires usage for every potentially billable
  member. Any missing member usage—including a mixed reported/unreported round or
  an error-file member—keeps the whole round at billing reconciliation pending;
  SBE never settles the action from a partial total.
- Duplicate, missing, unknown, output/error-overlapping, or malformed member
  inventories fail closed before any member is ingested. Strict native round/member
  key and binding validation rejects consumer guesses and mixed authority.
- Historical bounded v1 Batch remains `bounded_batch_unsupported`; only bounded v2
  round bindings are admitted.
- Exact semantic-closure compatibility: 85 tests passed in 207.894 seconds.
- Desktop bounded/lifecycle gate: 120 tests passed in 124.146 seconds.
- Python 3.11 Linux read-only-container gate: 120 tests passed in 27.162 seconds.
- Provider operations: 0. Spend: USD 0.
- Slice 5 is complete and paused for API fixture/lifecycle review before Slice 6.

## 2026-08-18 — Slice 6 assembly, whole-deck QA, and optional continuity

- Proved bounded interactive-initial and Batch-initial runs converge on the same
  canonical final cards and the same enabled optional-stage sequence.
- Added an explicit paid-action binding regression showing that a Batch-initial run
  prepares polish as an interactive Responses action. Under the approved contract,
  Batch covers initial authoring and creative retries; polish, critic, and
  qualitative candidate remain interactive. Optional-stage Batch transport is
  deferred to the separate cost-calibration work rather than being inferred here.
- Added a cross-pass normalized-repetition regression: duplicate prose originating
  in two distinct bounded authoring passes is still rejected by whole-deck final QA.
- Preserved optional-stage reconciliation, polish retry snapshot/resume, canonical
  assembly, and delivery behavior without adding a public lifecycle state.
- Desktop bounded/lifecycle gate: 135 tests passed in 132.412 seconds.
- Python 3.11 Linux read-only-container gate: 135 tests passed in 31.004 seconds.
- Provider operations: 0. Spend: USD 0.
- Slice 6 is complete and paused for gate review before public lifecycle fixtures
  and consumer handoff work.

## 2026-08-18 — Slice 7 public lifecycle, fixtures, oracle, and handoff

- Promoted the reviewed `astrowoof.route_parity_transition_oracle.v2` from sprint
  proposal to a packaged installed resource while preserving immutable v1 refusal
  evidence.
- Added `astrowoof.bounded_route_parity_traces.v1` with route-specific interactive
  multi-pass/retry and Batch pending/`not_due`/reclaim, partial-member retry,
  unavailable-usage, ambiguity, provider-failure, and delivery trajectories.
- Added strict public Python readers/validators and the provider-free
  `astrowoof-route-parity-evidence` CLI. Unknown fields, versions, vocabulary,
  duplicate scenario names, and unordered trace steps fail closed.
- Added the two contracts to the installed contract catalog and lifecycle installed
  smoke, then pinned their SHA-256 identities in a compact API consumer-review
  manifest.
- Published the consumer handoff covering request parity, paid-action cardinality,
  capacity/custody/consumer-authority separation, billing-unavailable handling,
  provider atomicity gaps, v1 migration refusal, optional interactive stages, and
  API-owned global authority.
- Desktop lifecycle/bounded/native-transition gate: 132 tests passed in 156.449
  seconds with 6 optional `jsonschema` skips in the lean runtime.
- Python 3.11 Linux read-only-container gate: 132 tests passed in 19.832 seconds with
  the same 6 optional skips.
- Provider operations: 0. Spend: USD 0.
- Slice 7 is complete and paused for API consumer review before installed release
  qualification.

## 2026-08-18 — Slice 8 installed qualification and release recommendation

- API review approved Slice 7 with two release conditions: use a fresh immutable
  version rather than changing 0.4.5, and carry the accepted fixture hashes into
  the final release handoff. Kevin approved the same conditions.
- Full repository qualification passed 423 tests in 428.695 seconds with 10
  expected environment-dependent skips. A separate environment with Draft 2020-12
  validation passed all 48 focused contract/release checks without skips.
- Built two fixed-epoch qualification wheels from source commit `58f6779`; both are
  byte-identical at SHA-256
  `bf864e2376ba36f3a8a292b3092c095ee52fac2ce8fcf081521f6ad3a3350ff2`.
- Verified 106 wheel entries, 61 resources, `py.typed`, packaged oracle v2 and
  bounded traces, no tests, and no bytecode/cache entries.
- Isolated Windows CPython 3.12 and fresh Linux CPython 3.11 installs passed `pip
  check`, lifecycle smoke, release smoke, route evidence export, and installed fake
  route checks for exact interactive, exact Batch, bounded interactive, and bounded
  Batch.
- Prepared a 0.4.6 release recommendation, compatibility contract, API handoff,
  known limitations, and candidate manifest. Both API-approved Slice 7 resource
  hashes are repeated verbatim.
- The current wheel retains version 0.4.5 and is qualification-only. It must never
  replace the published immutable 0.4.5 artifact. Final release authorization must
  bump to 0.4.6, commit the exact source, rebuild twice, and rerun final installed
  gates before tag/publication.
- Provider operations: 0. Spend: USD 0.
- Slice 8 is complete; the sprint recommends 0.4.6 and pauses for explicit release
  authorization.

## 2026-08-18 — Authorized 0.4.6 final artifact

- Kevin authorized the 0.4.6 version bump, exact final rebuild, tag, GitHub release,
  and publication.
- Committed the exact versioned artifact source as
  `ac86613b42ebc4f7d86cb557be9fbf82aaa1900d`.
- Two final fixed-epoch builds (`SOURCE_DATE_EPOCH=1787067938`) were byte-identical
  at SHA-256
  `1770d5c361b81ac5ed90b5b1a825da70aec108a665ac251a13a520d1af66e788`.
- The final wheel is 800,957 bytes and retains the qualified 106-entry/61-resource
  inventory, `py.typed`, frozen oracle/trace hashes, no tests, and no bytecode.
- Exact final Windows CPython 3.12 and Linux CPython 3.11 installs passed `pip
  check`, lifecycle smoke, release smoke, route-evidence export, version identity,
  and all four fake-provider routes.
- Provider operations: 0. Spend: USD 0.

## 2026-08-18 — 0.4.6 publication

- Committed and pushed release lock
  `62205d2ea2345667d265d0acaf25ae537b05cb15`.
- Created and pushed annotated tag `astrowoof-natal-authoring-v0.4.6`; tag object
  `208cb8a3efce069c1e169c16f609e640acb55bcf` targets the release lock.
- Published GitHub release `372473332` at
  `https://github.com/kevin2357/semantic-basis-extractor/releases/tag/astrowoof-natal-authoring-v0.4.6`.
- Wheel asset `519659679` is 800,957 bytes and GitHub reports digest
  `sha256:1770d5c361b81ac5ed90b5b1a825da70aec108a665ac251a13a520d1af66e788`.
- Checksum asset ID is `519659678`.
- Authenticated re-download independently matched the qualified wheel SHA-256.
- The immutable tag remains fixed; this post-publication documentation records
  external publication evidence only.
