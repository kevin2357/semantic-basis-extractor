# Executable Lifecycle Adversarial Simulation — SBE Sprint 1

Date: 2026-08-25
Status: Slice 7 API review approved; Slice 8 provider-free qualification in progress;
joint API campaign remains the final tag/adoption gate
Companion: AstroWoof API Sprint 52

## Objective

Build the SBE half of a provider-free, model-based campaign that drives actual
installed SBE lifecycle commands through generated failure/interleaving traces and
allows the API to test its real worker and scheduler against the resulting public
evidence.

## Non-goals

- No real provider traffic or paid qualification.
- No mutation of retained QA or production state.
- No generic native-state editor.
- No replacement queue or orchestration framework.
- No claim that random tests prove correctness exhaustively.
- No API-global state represented as SBE authority.

## Exploration modes

The primary mode is a systematic discrete-step explorer, not blind randomized
failure injection.

For one abstract state at logical step `N` and simulated canonical time `T`, the
explorer enumerates every meaningful enabled event, applies each event on its own
branch, validates the successor, and continues breadth-first to a bounded depth.
Logical steps and time are separate: every selected event advances the step counter,
while only an explicit clock event changes `T`.

Supported clock events include:

- advancing one frozen base unit;
- advancing by an explicit duration; and
- accelerating to the next declared due/lease/authority boundary, with an
  equivalence check against repeated base-unit advancement.

This systematic mode is complemented by seeded state-aware random walks for deeper
traces that bounded exhaustive branching cannot afford. Every randomized failure
must be exactly replayable and shrinkable into a deterministic fixture.

Progress is evaluated using two distinct identities:

- byte/checkpoint identity protects integrity and exact replay; and
- a canonical semantic fingerprint contains only authoritative facts that determine
  future behavior.

Observation timestamps, logs, wrapper counters, and rewritten files that do not
change future behavior do not constitute semantic progress.

The explorer classifies transitions as:

- `productive`: meaningful native truth or disposition advances;
- `legitimate_wait`: semantic truth is stable, capacity is released, and a declared
  external/time boundary is required;
- `idempotent_replay`: one supported nonmutating replay;
- `stutter`: the same semantic work/disposition returns without justified waiting;
- `cycle`: a prior semantic fingerprint recurs without progress; or
- `refused`: a valid closed fail-closed answer to an inadmissible event; or
- `contradictory_evidence`: materialized/public facts admit no truthful legal
  interpretation.

Repeated stutter or a progress-free cycle is a failing trace, regardless of changing
revision numbers, timestamps, or raw JSON hashes.

Starvation is a separate multi-run temporal property/witness, not another
per-transition classification.

## Slice 0 — Inventory, route matrix, and counterexample taxonomy

Map existing scripted transports, installed qualification commands, lifecycle
versions, failure hooks, and API Sprint 20 trace vocabulary. Classify known incidents
by the layer that failed: native transition, artifact publication, reader/validator,
wrapper translation, persistence, scheduling, or resource cleanup.

Produce a closed route/stage/mechanism matrix for exact/bounded × Response/Batch ×
initial/retry/polish/critic/candidate/closeout. Each cell must be `supported`,
`explicitly refused`, or `deferred`; absence is not a classification.

Testing/gate:

- Reproduce the Muffin wrapper counterexample as a pure trace.
- Identify which existing qualification would and would not detect it.
- Freeze the minimal SBE/API simulation protocol at a joint review pause.

## Slice 1 — Trace and fault-language contract

Define a versioned, closed, provider-free trace contract containing:

- seed, step index, simulated canonical time, run identity, and route;
- invoked public command and input artifact identities;
- scripted provider outcome and persistence/process fault;
- pre/post public checkpoint identities and typed result;
- expected oracle transition and observed transition;
- redacted invariant violations; and
- enough information for exact replay without credentials or subject data.

The trace also carries logical step, simulated time, enabled-event inventory,
selected event, byte identity, semantic fingerprint, progress classification, and
cycle/stutter witness where applicable.

Provider outcomes include pre-entry refusal, entered/identity-lost ambiguity, durable
identity, pending N times, completion, terminal failure, timeout, HTTP classes,
malformed response, identity conflict, and Batch partial-member/usage outcomes.

Persistence outcomes include interruption around intent, identity, state, journal,
snapshot, result, and receipt publication boundaries.

Testing/gate:

- Strict Python validation without optional `jsonschema`.
- Canonical serialization/digest and replay identity.
- Extra-key, malformed, privacy-sentinel, and contradictory-event refusal.
- Joint schema/authority review before executable adapters.

## Slice 2 — Real installed-SBE simulation adapter

Create a qualification-only adapter that constructs disposable workspaces through
supported runtime code and invokes actual installed-wheel commands/readers. It may
inject scripted transports and deterministic clocks internally, but may not replace
the native mutation it claims to test.

Start with one narrow installed vertical slice before expanding the route matrix:

1. materialize a public SBE review/no-action result matching the Muffin semantic
   boundary;
2. pass only packaged public evidence to the API's real production translation;
3. prove the historical reduction creates the minimal loop in a two-run/one-slot
   scenario;
4. prove the corrected translation releases capacity and permits the eligible second
   run to progress; and
5. freeze the shared progress/fairness assertion from observed composed behavior.

Pause for joint review after this vertical slice. Only then expand the adapter across
the broader route/stage/mechanism matrix below.

Cover:

- exact and bounded routes;
- interactive Response and supported Batch paths;
- initial fan-out/fan-in and ordinary action sets;
- retry, polish, critic, candidate, delivery, denial, and closeout where supported;
- fresh-process detach/restore/reconcile/resume; and
- snapshot/result/receipt validation.

Testing/gate:

- Network and credential use structurally impossible.
- Every advertised command is invoked through its public packaged boundary.
- Each returned identity is made durable using production persistence logic.
- Unsupported cells fail closed before provider I/O or native mutation.

## Slice 3 — Native progress and safety oracle

Implement SBE-scoped invariants over public native evidence:

- create-at-most-once by action/binding;
- retrieval-only after durable provider identity;
- ambiguity after entered call without durable identity;
- exact replay and stale observation nonmutation;
- advertised local-work consumption or typed disposition change;
- no same-basis/same-semantic-command spin;
- append-only evidence and monotonic accepted work;
- complete snapshot and publication-receipt joins; and
- unknown/unavailable distinct from zero.

Define the SBE semantic fingerprint and a progress relation independent of snapshot
rewrites. At minimum, the fingerprint covers native run/route identity, checkpoint
basis, action inventory and bindings, provider identities/statuses, authority facts,
selected command/operation keys, due boundary, terminal/delivery disposition, and
publication identities.

Testing/gate:

- Table tests for every invariant and intentional refusal.
- Metamorphic cases: replay, reorder harmless observations, advance time, interrupt,
  restore elsewhere at the required logical path, and retry readers.
- Each historical SBE incident is represented as a minimal regression trace.

## Slice 4 — Systematic branch explorer

Before exploration, define a closed internal action/member projection that joins
each opaque action reference and binding digest to create-entry, durable provider
identity, retrieval, and terminal evidence. Trace v1 remains frozen and must not be
widened. Only this joined projection may enforce create-at-most-once per exact
action/binding; aggregate provider-operation presence is insufficient.

Implement bounded breadth-first exploration. At each state:

1. derive the complete enabled meaningful-event set;
2. fork one disposable successor per event;
3. invoke the actual supported boundary;
4. validate safety and progress invariants;
5. canonicalize/deduplicate equivalent semantic states; and
6. retain the shortest witness for a refusal, stutter, cycle, or contradiction.

Include explicit one-unit clock advancement and accelerated-next-boundary
equivalence tests. A state may be quiescent only when no immediate native event is
enabled and any future dependency has a declared owner/boundary.

Testing/gate:

- Breadth-first exploration finds the minimal encoded historical counterexamples.
- A no-op checkpoint rewrite cannot masquerade as progress.
- Same semantic state reached by different harmless histories is deduplicated.
- Exploration bounds and truncation are explicit in the receipt.

## Slice 5 — Seeded random campaign and shrinking

Generate state-aware traces rather than arbitrary byte mutations. The generator may
choose only events allowed or intentionally adversarial at the current abstract
state. On failure, shrink time steps, runs, actions, provider outcomes, and crash
points while preserving the violation.

Testing/gate:

- Small fixed seed set in ordinary CI.
- Broader bounded seed/time campaign for nightly or explicit qualification.
- Exact trace replay produces the same public evidence and violation.
- Minimal counterexamples are promoted to named deterministic fixtures.
- Coverage reports transitions, route cells, refusal classes, and invariant checks,
  not merely line coverage.

## Slice 6 — Public qualification surface

Package a provider-free Python API and CLI that runs or replays the SBE half and
emits one concise closed receipt. The receipt reports package identity, schema and
corpus digests, seeds, transition coverage, invariant counts, counterexample
references, network/provider totals, and success/failure.

Testing/gate:

- Installed Python 3.11 wheel in isolation.
- No source-tree imports or test-helper imports.
- Output path cannot enter a native workspace.
- Receipt contains no prompt, payload, protected subject data, credentials, or
  unbounded exception text.

## Slice 7 — Joint API adapter and composed traces

Publish the trace/schema/readers and a sanitized fixture corpus for API consumption.
Pair with the API's production worker adapter so an SBE result is translated by real
API code, persisted transactionally, and scheduled under a small multi-run cohort.

Required composed traces include:

- Muffin: typed review/no-action must not become local continuation;
- provider pending 4+2 reconciliation with another runnable run;
- external-authority wait/grant/dispatch/reconciliation;
- ambiguity versus provider-pending custody;
- optional critic after delivery;
- providerless denial and terminalization;
- expired/lost lease with compatible replacement; and
- malformed/contradictory public evidence.

The joined campaign must include a systematic multi-run branch where each tick asks
which run/worker/time/failure events are enabled. It must detect both exact semantic
cycles and starvation witnesses where a continuously eligible run is denied progress
by another run's repeated nonproductive capacity use.

Gate: explicit API review of every fixture and the joined invariant mapping.

## Slice 8 — Release qualification and adoption handoff

Run focused, full, installed-wheel, deterministic-build, privacy, and joint replay
qualification. Document CI versus nightly seed budgets, how to add a new incident,
and which corpus/schema changes require synchronized release adoption.

Release only if a packaged SBE surface changes. API adoption remains separately
versioned and pinned.

Final gate:

- Zero external provider calls and USD 0 spend.
- Zero retained-QA access or mutation.
- All fixed seeds and historical counterexamples pass.
- Joint API campaign proves progress/fairness under at least three runs and bounded
  capacity.
- Owner and API review precede any tag/publication.

## Review pauses

1. Before Slice 0: owner/API approval of scope.
2. After Slice 0: taxonomy, matrix, and protocol review.
3. After Slice 1: schema/authority freeze.
4. During Slice 2: first installed Muffin vertical-slice review.
5. After Slice 3: native invariant/fingerprint review.
6. After Slice 4: systematic-explorer review.
7. After Slice 6: packaged consumer fixture review.
8. After Slice 7: joint composed-system review.
9. Before release/adoption.
