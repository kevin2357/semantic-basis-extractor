# Slice 0 — State Catalog, Joint Projection, and Muffin Trace

Date: 2026-08-26
Status: SBE analysis complete; paused for joint vocabulary/protocol review

## Result

The current repositories already contain most of the ingredients needed for an
adversarial simulator, but they are not yet one uniform harness. SBE has durable
native workspaces, strict public readers, provider injection seams, failure hooks,
and installed qualification commands. API has a pure transition oracle, injectable
clocks and failure hooks, database fixtures, fake storage, synthetic workers, and
production service boundaries.

The missing join is now explicit:

```text
complete materialized state
    -> tested semantic projection
    -> enabled-event inventory
    -> real boundary invocation
    -> successor materialized state
    -> semantic progress/fairness judgment
```

Execution-event JSON is diagnostic input only. It is neither a complete history nor
the materialized state.

## 1. Materialized scenario-state catalog

### Simulator-owned facts

| Fact | Meaning |
|---|---|
| logical step | Monotonic count of selected simulation events. |
| canonical time | One injected UTC clock shared by all simulated actors. |
| seed/branch | Exact replay and branch identity. |
| construction class | `legally_reached`, `historical_shape`, or `synthetic_invalid_state`. |
| enabled events | Closed events derivable from current actors/resources/facts. |
| explored frontier | Explicit bounded unexplored successors. |

### SBE-owned materialized facts

| Entity | Explicit/derived state relevant to future behavior |
|---|---|
| native run | run ID, route contract, route family, aggregate status, state revision, logical workspace root |
| pass | pass ID, membership, state, accepted attempt, retry eligibility |
| attempt | attempt number, state, request/response evidence, acceptance/rejection |
| initial wave | wave identity, ordered members, preparation/authorization/submission state |
| paid action | action ID, stage, mechanism, complete binding, state, authorization, consumption, denial |
| provider custody | operation kind/ID, returned identity evidence, ambiguity, reported usage/status |
| local work | operation ID/key, inventory, cumulative consumed keys, selected command |
| temporal schedule | per-action `resume_not_before`, checkpoint basis, due subset selected by SBE |
| external authority | request/grant/document identities and constrained intent/dispatch evidence |
| editorial evidence | accepted passes/cards, QA, retry/polish/critic/candidate decisions |
| terminal/delivery | terminal status/cause, delivery/review/publication eligibility |
| integrity/publication | state hash, complete snapshot, journal range, native result, immutable receipt |

### API-owned materialized facts

| Entity | Explicit/derived state relevant to future behavior |
|---|---|
| generation run | product execution state and pinned generation profile |
| job/attempt | stage, availability, disposition, attempt/failure evidence |
| lease | owner/token, acquired/renewed/expiry/release facts |
| capacity | slot allocation and release facts |
| native observation | exact validated SBE schema/result/checkpoint identities persisted by API |
| paid action | API admission/reservation/provider-operation and reconciliation facts |
| scheduler | eligible inventory, ordering, due time, selected job |
| artifacts/storage | staged/available object references and validation/publication state |
| reading | product delivery/public visibility state |
| operator control | typed request, custody fence, audit and replay evidence |

### Fake-provider materialized facts

| Entity | State |
|---|---|
| create invocation | definitely not entered, entered, returned identity, or entered/identity unknown |
| operation | pending, completed, failed, cancelled, expired, malformed, conflicting |
| retrieval script | ordered outcomes, HTTP class, duration, usage availability |
| Batch | File/Batch identity, ordered members, member outcomes, usage completeness |

## 2. Materialized-to-oracle projection

The oracle is deliberately smaller than materialized state. Slice 1 must publish and
test one explicit projection. The initial projection proposal is:

| Oracle dimension | Materialized source | Why future-affecting |
|---|---|---|
| native disposition | validated SBE lifecycle/result | Selects the only supported native/API branch. |
| native checkpoint | run, route, mechanism, basis, revision/snapshot | Fences stale or cross-route commands. |
| native work | ordered actions/bindings, local operation keys, consumed keys | Prevents reconstruction, replay, and no-op renaming. |
| provider custody | operation identities/statuses/ambiguity/due boundary | Separates create, retrieve, wait, and review. |
| external authority | request/grant/intents and action inventory | Fences paid dispatch. |
| API execution | run/job/attempt and validated native observation | Determines product execution transitions. |
| lease/capacity | owner, validity, allocation, availability | Determines who may mutate and which run may execute. |
| API spend authority | reservation/admission/action settlement | Prevents authority loss or duplication. |
| publication | native delivery plus API artifact/publication authority | Determines safe reader delivery. |
| scheduler | eligible/due ordering and available capacity | Supports fairness/starvation proofs. |
| time | canonical time plus declared boundaries | Determines due/expiry without incidental wall clocks. |

Excluded from semantic progress but retained in raw evidence:

- text logs and structured observational events;
- observation timestamps that cross no boundary;
- worker retry/generation counters that record only another look;
- file/hash rewrites with no future-affecting fact change; and
- diagnostic duration/cost observations that do not control execution.

Any later field exclusion requires a written proof that it cannot alter future legal
commands, authority, scheduling, terminality, or publication.

## 3. Actor catalog

| Actor | Permitted role |
|---|---|
| scheduler | Select an API-eligible job under queue/capacity policy. |
| claimed worker | Act only with current job lease and assigned capacity. |
| replacement worker | Restore and continue only through supported fencing/replay. |
| SBE command | Inspect or mutate one native workspace under SBE rules. |
| external-authority service | Admit/deny exact SBE requests under API-global policy. |
| fake provider | Accept/create, advance, retrieve, or return scripted failures. |
| lease clock/reaper | Advance canonical time and expire/reap through API contracts. |
| storage publisher | Stage, validate, publish, fail, or replay object operations. |
| operator | Invoke only supported typed dry-run/execute/replay commands. |
| crash injector | Interrupt at a named hook without inventing completion. |

## 4. Resource catalog

| Resource | Authority owner | Important independent dispositions |
|---|---|---|
| API job lease | API | absent, active, expired, released |
| execution capacity slot | API | free, allocated, released |
| global reservation/admission | API | absent, retained, releasable, settled, review |
| native workspace writer | SBE | absent, held, released; never inferred from API lease |
| native checkpoint | SBE | valid, stale, incomplete, contradictory |
| provider custody | SBE evidence/API retention mapping | none, pending, completed-local-work, ambiguous, terminal |
| provider operation | provider/SBE identity evidence | unentered, identity unknown, durable identity |
| publication authority | SBE delivery + API product authority | ineligible, eligible, committed, review |

Releasing one resource never implies release of another unless an explicit validated
transition says so.

## 5. Enabled-event catalog

The explorer derives events; it does not mutate arbitrary status fields.

### Time and scheduling

- advance one base time unit;
- advance to next declared boundary;
- select eligible job;
- claim, renew, defer, release, expire, reap, or replace a lease through API services.

### Native inspection and execution

- inspect lifecycle at exact canonical time;
- invoke the exact SBE-selected run-level command;
- supply or withhold a compatible external grant;
- execute a supported typed operator command;
- replay a sealed result;
- attempt a stale/unsupported/mismatched command and require typed refusal.

### Provider

- refuse before provider entry;
- enter create and return a durable identity;
- enter create and lose identity;
- advance known operation to pending/completed/failed/cancelled/expired;
- retrieve a known operation with scripted HTTP/transport/content outcomes;
- return partial Batch members or incomplete usage.

### Persistence/process

- interrupt at a named native or API hook;
- restart in a fresh process;
- restore complete workspace at its required logical path;
- fail state/snapshot/journal/result/receipt/storage/transaction boundaries;
- ingest or replay validated native evidence.

An intentionally non-enabled event is a negative test and must return a typed refusal
without unauthorized side effects.

## 6. Legal state construction

`legally_reached` scenarios must use production builders, repositories, services,
public commands, and persistence paths. The harness may replace provider transport,
clock, storage, and process survival, but not native/API mutations it claims to test.

`historical_shape` fixtures may construct old released evidence directly, but must
name the exact release/schema and compatibility purpose.

`synthetic_invalid_state` fixtures may introduce one declared contradiction for
negative validation. They must never be presented as a reachable predecessor.

## 7. Closed route/stage/mechanism matrix

`supported` means the released route accepts the stage under that mechanism.
`explicitly_refused` means provider dispatch under that mechanism must fail closed.

| Route | Mechanism | Initial | Creative retry | Polish | Critic | Candidate | Closeout |
|---|---|---:|---:|---:|---:|---:|---:|
| exact Natal | Response | supported | supported | supported | supported | supported | supported (local-only) |
| exact Natal | Batch | supported | supported | explicitly_refused | explicitly_refused | explicitly_refused | supported (local-only) |
| bounded Natal v2 | Response | supported | supported | supported | supported | supported | supported (local-only) |
| bounded Natal v2 | Batch | supported | supported | explicitly_refused | explicitly_refused | explicitly_refused | supported (local-only) |

Notes:

- Batch authority is one paid action/API reservation per round; members are evidence.
- Initial/retry interactive authority is per pass/attempt.
- Optional polish, critic, and candidate remain interactive Response operations even
  when initial/retry authoring used Batch.
- Closeout is shown in both rows only to keep the product closed; it performs no
  provider operation and must not acquire new paid authority.
- Legacy bounded v1 Batch remains a typed unsupported historical route.

## 8. Existing SBE tooling and missing seams

### Available now

- Strict public lifecycle v0.5, temporal v0.6, and local-work v0.7 readers.
- Public external-authority, native-transition, retirement, economics, and diagnostic
  schemas/readers.
- Provider create/retrieve callables in initial-wave, reconciliation, and constrained
  authority paths.
- Deterministic monotonic clock injection for initial-wave coordination.
- Named failure injectors around writer, validation, intent, provider-entry,
  returned-identity, checkpoint, and snapshot boundaries.
- Failure-isolated structured event sinks.
- Provider-free installed qualification CLIs for multiple contracts/routes.

### Missing/unified work

- No single named-checkpoint registry spans all routes/stages.
- Clock injection is not uniform across every path.
- Existing qualification commands build different bespoke fixture shapes.
- No public scenario capsule or enabled-event reader exists.
- No shared semantic fingerprint/progress classifier exists.
- No branch cloning/deduplication or frontier accounting exists.
- Some broad qualifications have historically used helper-injected mutation rather
  than the production executor being claimed.

## 9. Incident taxonomy

| Incident class | Representative example | Layer |
|---|---|---|
| platform-sensitive fixture | Linux smoke normalized-passage collision | qualification fixture |
| snapshot ordering | polish retry after rewritten final artifacts | native persistence |
| provider ambiguity | create entered before durable identity | native/provider fence |
| authority lineage | retained initial wave could be recreated | native authority fence |
| custody precedence | prepared authority masked retained provider work | native selector |
| payload recovery | redacted payload could not reproduce binding | native compatibility |
| temporal observation | same basis changes from not-due to due | joint clock/contract |
| local-work replay | semantic operation renamed by incidental snapshot | native progress contract |
| wrapper translation | typed non-local result became local continuation | API adapter |
| starvation | Muffin retained capacity while Biscotti was due | API scheduler/resources |
| expired cleanup | expired lease row blocked reset | API operator/resource cleanup |

## 10. Minimal Muffin counterexample

This is a provisional semantic trace, not the Slice 1 serialized contract.

### Initial state

```text
tick = 0
capacity slots = 1
Muffin job = leased; slot = allocated
Biscotti job = eligible and due
SBE result for Muffin = retain_for_review/no-action
Muffin immediate local-work inventory = empty
```

### Historical four-step path

1. Claimed worker receives and validates Muffin's typed SBE result.
2. API wrapper computes `local_continuation_required = not release_until_due`.
3. Because `retain_for_review` is not `release_until_due`, API records local
   continuation/defer while retaining or promptly reacquiring the constrained slot.
4. Scheduler selects Muffin again; the semantic fingerprint repeats while Biscotti
   remains continuously eligible.

### Violation

```text
classification = cycle + starvation
Muffin semantic progress = none
Muffin legitimate wait = false
Biscotti eligible_since = tick 0
Biscotti progress = none
```

### Correct successor

The API preserves the typed non-local review/no-action disposition, releases the
execution lease/capacity as required, retains only independently required review/
spend/provider authority, and permits Biscotti to claim the available slot.

No SBE-native mutation is required to correct this trace.

## 11. Proposed semantic fingerprint

Slice 1 should version this proposal. The fingerprint must include:

- native run/route/mechanism/checkpoint basis;
- selected command/disposition;
- ordered public action/binding identities;
- provider custody/status/due boundary;
- local operation keys and cumulative consumed keys;
- external-authority identities;
- terminal/delivery/publication disposition;
- API run/job/attempt/lease/capacity;
- API reservation/provider-action/publication authority;
- scheduler eligibility/available-at; and
- canonical simulated time only where crossing it changes an enabled event.

## 12. Slice 0 decisions requested

Joint reviewers should confirm:

1. the materialized/oracle split and proposed projection dimensions;
2. the actor/resource/enabled-event catalogs;
3. legal versus historical/invalid construction classes;
4. the closed route/stage/mechanism matrix;
5. the provisional fingerprint inclusions/exclusions;
6. the seven progress classifications;
7. the four-step Muffin counterexample and corrected successor; and
8. the early installed vertical slice before broad framework expansion.

No provider, retained-QA, production database, or release activity occurred in this
slice.
