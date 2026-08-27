# Adversarial Lifecycle Simulation Playbook

```yaml
status: accepted
owner: semantic-basis-extractor
scope: provider-free lifecycle modeling, counterexample reduction, joint SBE/API qualification, and release evidence
introduced_in: astrowoof-natal-authoring 0.4.26
last_reviewed: 2026-08-27
```

## Purpose

Use this playbook to test how SBE native lifecycle truth composes with API worker,
lease, capacity, persistence, and scheduler behavior. The simulator is especially
useful when a run changes bytes or revisions without making semantic progress, when
several actors can observe the same checkpoint, or when a non-runnable run may retain
capacity and starve another run.

The simulator is qualification infrastructure. It is not a second scheduler and is
never runtime authority. Production decisions still come from validated SBE
lifecycle artifacts and API-owned transactional state.

## Released toolkit

SBE 0.4.26 packages public builders, readers, validators, schemas, fixtures, and a
provider-free aggregate command for:

- lifecycle adversarial traces;
- route/mechanism qualification;
- systematic bounded branch exploration;
- deterministic fixed-seed campaigns and counterexample shrinking;
- an aggregate qualification receipt; and
- a closed 15-case SBE/API consumer catalog.

Run the public installed command from outside the source checkout:

```text
astrowoof-adversarial-qa --output <path-outside-any-native-workspace>
```

Use `astrowoof-adversarial-qa --schema` to inspect the aggregate receipt schema.
The command requires no provider credential, performs no provider operation, and
must report zero network calls, provider creates, and spend.

The API companion campaign consumes the installed SBE package through these public
surfaces and then drives applicable cases through real API repositories, workers,
leases, capacity services, and scheduler selection. It does not inspect SBE private
workspace files to reconstruct a command.

## Authority boundary

The simulator may assert only what its validated evidence proves.

SBE owns native checkpoint and lifecycle facts, route/mechanism/action/binding and
provider-custody evidence, native event admissibility, transition outcomes, and
packaged SBE fixture identities.

The API owns product jobs/readings, leases, capacity, queue ordering, reservations,
global spend policy, billing reconciliation, PostgreSQL/R2 transactions,
publication, and multi-run scheduler fairness.

The simulator never grants:

- permission to submit or retrieve provider work;
- spend authorization or reservation release;
- permission to mutate, repair, close, publish, or delete a workspace;
- API lease or capacity ownership;
- provider billing settlement; or
- product delivery/publication eligibility.

Do not route production from a qualification receipt. Do not use logs, private
`run.json`, prompts, packets, or provider IDs to fill a missing public fact.

## State model

Keep complete materialized test state separate from its semantic projection.

Materialized state contains redacted facts required to invoke a test adapter:
native evidence, API state, provider state, resource ownership, canonical time, and
construction class. It may retain revision or byte-level details needed for exact
reproduction.

Semantic state contains only future-affecting facts:

- native checkpoint identity;
- selected command and capacity disposition;
- advertised and cumulatively consumed local-work keys;
- provider custody and external-authority posture;
- API job, lease, capacity, reservation, and publication state;
- eligible competing runs; and
- the next meaningful time boundary.

Cycle and stutter detection use semantic fingerprints. A rewritten timestamp,
snapshot, revision, or result file is not progress when the same work and ownership
posture remain.

## Construction classes

Every scenario declares how its starting state exists:

- `legally_reached`: produced through supported current runtime behavior;
- `historical_shape`: a faithful provider-free reconstruction of previously
  observed behavior that current code may no longer produce; or
- `synthetic_invalid_state`: deliberately contradictory evidence used to prove
  validators and consumers fail closed.

Never label a hand-authored historical or contradictory state `legally_reached`.
Never present a historical-shape failure as evidence that corrected current code
still has the defect.

## Transition classifications

- `productive`: future-affecting state advanced.
- `legitimate_wait`: nothing is due before a declared boundary and execution
  capacity has the expected released posture.
- `idempotent_replay`: the same decision/evidence was safely observed again.
- `refused`: a selected event was inadmissible and produced one closed refusal.
- `stutter`: the same semantic state returned without justified waiting.
- `cycle`: an earlier semantic fingerprint recurred with a prior-step witness.
- `contradictory_evidence`: public/materialized facts cannot describe one truthful
  legal state.
- A starvation witness means a continuously eligible run was denied progress while
  another run repeatedly made no useful progress or retained capacity.

`refused` and `contradictory_evidence` are often successful negative-test results.
A trace identifies a product defect only when a legal productive/wait/replay outcome
was expected and the supported boundary produced a stutter, cycle, contradiction,
unsafe mutation, duplicate side effect, or starvation condition.

## Choose the right test mode

Use the smallest mode that proves the claim:

1. **Named deterministic fixture** for a known incident or malformed input.
2. **Production-shaped adapter test** for one command/result/persistence boundary.
3. **Systematic bounded exploration** when several events are enabled and ordering
   matters.
4. **Fixed-seed campaign** for combinations beyond practical enumeration.
5. **Joint installed-wheel campaign** when correctness depends on API translation,
   persistence, leases, capacity, or scheduler fairness.

Random exploration finds candidates; shrinking and deterministic fixture promotion
make findings durable.

## Model time deliberately

Use a simulated canonical clock. Support both one base-unit tick at a time and
acceleration to the next declared meaningful boundary. The paths must produce the
same semantic successor when no intermediate event is meaningful.

Provider-pending wall time is not provider compute time. Repeated early polling must
remain a legitimate nonmutating wait and must not manufacture revisions merely to
look active.

## Build a scenario

Specify before writing the adapter:

1. route family and provider mechanism;
2. current checkpoint and lifecycle contract version;
3. local work, provider custody, external authority, and terminal/review posture;
4. API job, lease, capacity, reservation, and publication state;
5. simulated time and next due boundary;
6. every enabled meaningful event;
7. expected classification for each event;
8. allowed mutations and forbidden side effects; and
9. construction class and privacy posture.

An adapter may call production-shaped code, but the explorer must not become a copy
of the production scheduler. The adapter owns materialization and invocation; the
shared oracle owns projection, classification, deduplication, and witnesses.

## Provider and failure injection

Use scripted transports and durable fake provider identities. Cover applicable
boundaries such as:

- definitely unattempted create;
- call entered but identity unknown;
- durable provider identity;
- pending N observations followed by completion;
- terminal provider failure, timeout, and HTTP classes;
- malformed response or identity conflict;
- partial Batch-member usage;
- interruption around ledger/state/snapshot/result/receipt writes;
- stale observation, duplicate delivery, lost lease, and competing writer; and
- storage/publication failure after native evidence exists.

Patch external provider/network entry points to fail if a provider-free campaign
unexpectedly attempts them. Every receipt records network, provider, spend, and
retained-QA totals even when all are zero.

## Systematic exploration and shrinking

Bound exploration explicitly by depth, state count, run count, action count, seed,
and time. Canonicalize semantic state so incidental byte churn does not expand the
frontier indefinitely. Retain the shortest witness for refusal, stutter, cycle, and
contradiction, plus any starvation witness.

When a generated failure appears:

1. rerun the exact seed and limits;
2. remove unrelated runs and actions;
3. remove irrelevant time advances and provider outcomes;
4. minimize the event sequence;
5. prove the minimized trace reproduces exactly and semantically;
6. assign ownership and construction class; and
7. promote it to a named deterministic fixture.

Record any unexplored frontier. A bounded campaign cannot claim proof over states it
did not visit.

## Promote an incident into the corpus

1. Stop retries/resubmission and preserve authoritative evidence externally.
2. Diagnose through supported read-only SBE and API surfaces.
3. Create a sanitized provider-free reduction; never commit the retained workspace.
4. State the original symptom, violated invariant, owner, and expected behavior.
5. Add/update strict schema, builder, reader, validator, fixture hash, and catalog
   case as applicable.
6. Prove the fixture was consumed by its adapter—not merely copied into a receipt.
7. Run SBE-local qualification and, for shared behavior, the API joint campaign.
8. Preserve minimized trace and exact digests in sprint/release evidence.

Packaged fixture identity and adapter-result identity are separate facts. A joint
receipt preserves the exact catalog fixture SHA-256 and separately binds the result
of driving it through its real adapter.

## CI, nightly, and release policy

- **PR/focused:** named incidents, contract validators, fixed seeds 7, 19, and 41,
  and affected route cells.
- **Nightly/explicit local:** wider bounded seed/depth/time campaigns with recorded
  limits and frontier counts.
- **Lifecycle release:** complete aggregate qualification from the exact installed
  SBE candidate wheel.
- **Joint-contract release:** exact public catalog consumed by real API adapters and
  persistence services, producing a strict joined receipt.

A changed schema, catalog assertion, fixture hash, semantic fingerprint, ownership
mapping, lifecycle result, wrapper translation, or scheduler rule requires focused
requalification. A shared public-boundary change requires API review. Increasing
non-normative seed budgets alone does not change a contract.

## Read campaign results correctly

A passing SBE aggregate receipt proves only its declared route cells, invariants,
fixtures, seeds, and provider-free totals. It does not prove API leases or fairness.

A passing joined receipt additionally proves listed API adapter and persistence
cases. It must match the ordered SBE catalog, use closed evidence shapes, retain
fixture and adapter-result hashes separately, bind corrected and historical traces
separately, and report zero prohibited external activity.

Expected refusals and deliberate contradictions pass only when their exact closed
disposition occurs with zero forbidden mutation or side effect.

## Current baseline

SBE 0.4.26 established:

- 15 catalog cases;
- 22 route cells;
- 32 invariant checks;
- fixed seeds 7, 19, and 41;
- installed SBE aggregate qualification;
- final joint validation of all 15 discharges; and
- zero provider/network calls, spend, and retained-QA access.

Muffin's review/no-action wrapper was the principal real integration defect
reproduced by the campaign. Intentional historical, refusal, ambiguity,
duplicate-create, stale-writer, contradiction, cycle, and starvation cases are
successful safety tests when current code returns their expected fail-closed result.

## Related procedures

- [Native Worker Change Playbook](Native%20Worker%20Change%20Playbook.md)
- [Maintainer Release Playbook](Maintainer%20Release%20Playbook.md)
- [SBE Authoring Execution and Authority Model](SBE%20Authoring%20Execution%20and%20Authority%20Model.md)
- [Runtime Contracts](Runtime%20Contracts.md)
- [Authoring Lifecycle Consumer Handoff](Authoring%20Lifecycle%20Consumer%20Handoff.md)
- [SBE 0.4.26 API Consumer Handoff](../../releases/0.4.26/API%20CONSUMER%20HANDOFF.md)
- [Adversarial Simulation Sprint Plan](../sprints/2026/08/20260825-executable-lifecycle-adversarial-simulation-sprint1/PLAN.md)
