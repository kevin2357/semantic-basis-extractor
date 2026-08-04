# Post-Sprint Private Launch Process and Repository Strategy

## 1. Purpose

The editorial-quality sprint ended with a live, complete Ella run and a
production-candidate authoring worker. This document describes how that worker
can become part of a private AstroWoof service, how its runs should be operated
and reviewed, and where its code should live while the product matures.

The central conclusion is that the difficult domain workflow is no longer a
research sketch. `author_semantic_closure.py` already provides durable
orchestration from SPC projected-chart files through SBE, six-pass LLM
authoring, pass QA, retry, assembly, whole-deck QA, bounded mechanical polish,
accounting, and final delivery. The missing work is primarily the conventional
service control plane around it.

## 2. Current capability boundary

Given one subject directory containing four projected canine natal contexts and
`params.json`, the semantic-closure runner can currently:

1. invoke SBE;
2. build the selected authoring packet and compact whole-chart context;
3. split fifty cards across six deterministic, stratified authoring passes;
4. submit authoring through OpenAI Responses or Batch;
5. persist remote response, file, and Batch identifiers;
6. detach and resume without repeating accepted work;
7. reconstruct complete authored Markdown workspaces from structured field
   transport;
8. run opaque per-pass acceptance;
9. repair invalid constrained metadata without buying new prose;
10. route genuine creative failures to a configured retry model;
11. assemble the final fifty-card/four-summary deck;
12. validate structure and lint the complete editorial artifact;
13. run sparse mechanical polish when blocking findings remain;
14. package the deck and QA reports; and
15. record attempts, states, model routing, token usage, estimated cost, QA
    results, and artifact paths in atomic `run.json` state.

The runner does not currently provide user accounts, dog records, an HTTP API,
a database, distributed worker leases, object storage, product notifications,
or deployment infrastructure.

## 3. Proposed private-service lifecycle

The private AstroWoof service should own the following larger workflow:

```text
Authenticated user creates a dog
                 |
                 v
Persist dog identity, pronouns, and birth data
                 |
                 v
AGF generates the canonical natal chart
                 |
                 v
SPC generates four canine projection contexts
                 |
                 v
Create a durable natal-authoring run
                 |
                 v
Semantic Closure runs SBE and LLM authoring
                 |
                 v
Validate, mechanically polish, and package
                 |
                 v
Persist an immutable reading version and mark it ready
```

A default production invocation would be equivalent to:

```powershell
python author_semantic_closure.py `
  --input-package <projected-dog-directory> `
  --subject <stable-subject-slug> `
  --run-dir <durable-run-directory> `
  --provider openai `
  --service-level batch `
  --routing-policy cost_optimized `
  --split-assignment-policy stratified-v1 `
  --max-attempts 3 `
  --polish `
  --batch-detach
```

These choices should be application configuration associated with a versioned
authoring profile, not options supplied by end users.

## 4. API and job-control shape

A minimal API could expose:

```text
POST /dogs
POST /dogs/{dog_id}/natal-readings
GET  /authoring-runs/{run_id}
GET  /dogs/{dog_id}/natal-readings
GET  /dogs/{dog_id}/natal-readings/{reading_id}
GET  /dogs/{dog_id}/natal-readings/{reading_id}/deck
GET  /dogs/{dog_id}/natal-readings/{reading_id}/delivery
```

`POST /dogs/{dog_id}/natal-readings` should be idempotent for a caller-supplied
request key and return `202 Accepted` with a run ID. It should not hold the HTTP
connection open while charts or prose are generated.

The product-facing status vocabulary should be stable and simpler than the full
runner state machine. For example:

```text
queued
generating_canonical_chart
projecting_canine_chart
extracting_semantic_basis
authoring
quality_review
ready
requires_review
failed
```

The detailed runner states should remain available to operators.

### Polling rule

A user's `GET /authoring-runs/{run_id}` request should never make a remote
OpenAI call or resume a worker. It should only read persisted state.

Instead:

1. a worker submits a Batch round with `--batch-detach`;
2. a scheduler periodically enqueues a poll/resume job;
3. the worker invokes the same run with `--resume --batch-detach`;
4. the runner ingests completed rows and advances its atomic checkpoint;
5. the API mirrors the normalized state to the database; and
6. terminal success promotes final artifacts and notifies the product.

Only one worker may mutate a run at a time. The service must provide a database
or queue-backed lease keyed by `run_id`; atomic local JSON replacement is not a
distributed lock.

## 5. Persistence model

Useful initial database entities include:

- `users`;
- `dogs`;
- `canonical_charts`;
- `projected_charts`;
- `natal_readings`;
- `authoring_runs`;
- `authoring_attempts`;
- `editorial_findings`; and
- `artifacts`.

Large JSON files and ZIPs should live in object storage. Database artifact rows
should contain at minimum:

- user and dog ownership;
- run and reading IDs;
- artifact type;
- object-storage key;
- SHA-256;
- byte size;
- schema version;
- generator/release versions; and
- creation and retention timestamps.

Final readings should be immutable and versioned. Regeneration should create a
new reading version rather than silently replacing a delivered deck.

For a first single-instance private deployment, a durable mounted volume can
host each active run directory. The database remains the product source of
truth, and completed artifacts should still be promoted to object storage.

## 6. Failure, cost, and quality policy

The API service should turn the runner's detailed evidence into explicit
product policies:

- cap attempts and estimated spend per run;
- stop and flag repeated provider or structural failure;
- alert on unusual latency or cost;
- preserve error codes and affected claim IDs;
- distinguish constrained metadata repair from creative retry;
- never deliver a structurally invalid deck;
- run bounded mechanical polish for blocking whole-deck lint;
- retain unresolved advisory warnings for sampling; and
- clean expanded workspaces after artifact promotion and a short debugging TTL.

The current qualitative critic should not block every private-launch reading.
Initially it should be sampled, explicitly requested, or triggered by unusual
signals such as high cost, multiple retries, a new prompt/model release, or a
random quality cohort. Critic candidate prose remains non-authoritative until
reviewed.

## 7. Periodic operational and editorial review

Collecting `run.json` files manually would work for the first handful of runs,
but the durable process should expose a deliberate, redacted telemetry export.

`run.json` should remain the complete per-run recovery and audit record. A
separate export job should derive one compact JSONL record per run containing:

- pseudonymous run, dog, and authoring-profile IDs;
- release and schema versions;
- start, finish, and stage durations;
- terminal state;
- pass attempts and acceptance attempt numbers;
- issue codes and metadata repairs;
- token use and estimated cost by stage/model/service level;
- mechanical-polish targets and edit counts;
- validation error/warning counts;
- lint codes/counts;
- critic finding summaries when sampled; and
- final artifact hashes.

The export should omit API credentials, absolute server paths, raw birth data,
user identifiers, and unnecessary personal information. OpenAI response IDs
should remain operator-only unless specifically needed for provider support.

### Suggested cadence

For an early private launch:

- **Per run:** automatic terminal-state, cost-cap, and failure alerts.
- **Weekly:** operational review of every run while volume is small.
- **Every 10–20 completed decks:** literary sample review of several complete
  decks, including summaries and random cards across claim types.
- **Monthly:** aggregate prompt/model/release review and a decision about any
  upstream authoring change.
- **Before every authoring release:** replay deterministic fixtures and run one
  fresh or controlled live QA.

Useful aggregate measures include:

- delivery success rate;
- first-attempt pass-acceptance rate;
- creative retry rate and reason;
- metadata-repair frequency;
- median/P90/P99 latency;
- median/P90/P99 total and per-stage cost;
- mechanical-polish invocation and edit rates;
- validator and lint findings by code;
- sampled critic findings by dimension;
- summary-lens convergence rate from sampled review; and
- cross-deck recurring comic or rhetorical mechanisms.

When reviewing here, the preferred handoff is a ZIP containing the redacted
JSONL export, version manifest, aggregate report, and a small pseudonymous
sample of final decks. Failed-run packages may additionally include QA reports
and the relevant run checkpoint. It should not be necessary to gather every
expanded workspace.

## 8. Repository ownership decision

### Do not move the runner into the API repository now

The runner is AstroWoof-specific, but it is tightly coupled to SBE packet
schemas, generated handoff workspaces, authoring guidance, gold references,
assembly, validators, and deterministic acceptance. Moving it today would
either split one behavioral release across two repositories or encourage the
API repository to own copied SBE internals.

The API should own transport and product orchestration:

- HTTP endpoints;
- authentication and authorization;
- user/dog/database models;
- queues, schedules, and worker leases;
- object storage;
- notifications;
- quotas and operational policy; and
- invocation of versioned domain runtimes.

It should not own duplicated extraction, authoring, validation, or editorial
policy code.

### Short-term recommendation

Keep semantic closure in `semantic-basis-extractor` and make the repository a
real versioned runtime dependency:

1. add a `pyproject.toml` and installable package/CLI boundary;
2. enumerate required package data, including static guidance, validators, and
   approved references;
3. define a stable input, invocation, state, and delivery contract;
4. make runtime version/provenance explicit in `run.json` and final artifacts;
5. build a self-contained wheel and/or worker container;
6. run deterministic fixtures plus a packaged-runtime smoke test;
7. tag the known-good release with an AstroWoof-scoped tag, such as
   `astrowoof-natal-authoring-v0.1.0`; and
8. have the API pin the immutable tag, wheel digest, or image digest.

Until packaging exists, the API can pin a Git commit SHA in a worker image for
an internal prototype. A hand-copied source ZIP is acceptable only as a
temporary release artifact if its commit SHA, file manifest, checksums, and
smoke-test result accompany it.

The current sprint-ending commit is an excellent release candidate, but it is
not yet a formal release because the repository has no packaging manifest or
existing tag convention.

### Long-term recommendation

Do not make the API repository the permanent home of the authoring engine.
There are two clean long-term outcomes:

1. **Remain in SBE** while extraction, handoff contracts, and authoring policy
   continue to evolve atomically and AstroWoof remains the principal consumer.
2. **Extract a dedicated package/repository**, such as
   `astrowoof-natal-authoring` or `astrowoof-semantic-closure`, when the runner
   needs an independent release cadence, multiple consumers, or independently
   deployable workers. That package would depend on a versioned SBE library and
   own AstroWoof authoring protocols, references, assembly, QA, and provider
   orchestration.

The extraction trigger should be operational evidence, not merely the fact that
the runner is product-specific. Good triggers include:

- SBE is reused by non-AstroWoof products that should not ship canine assets;
- the authoring worker and extractor require independent releases;
- API workers need a smaller standalone image;
- multiple services consume semantic closure; or
- ownership and testing are repeatedly impeded by the shared repository.

The transition should move one coherent package with tests and history. It
should not copy files into the API repo and allow two implementations to drift.

## 9. Suggested implementation sequence

### Phase A — Freeze the runtime contract

- Specify projected-input directory and `params.json` schemas.
- Specify `run.json` public/operator fields and terminal states.
- Specify final delivery contents and artifact hashes.
- Add explicit runtime and authoring-profile versions.

### Phase B — Package and release

- Add Python packaging and a console entry point.
- Include and verify package data.
- Produce a wheel or worker image.
- Run fake-provider and packaged-runtime smoke tests.
- Tag the first private-launch release.

### Phase C — Build the API control plane

- Add users, dogs, readings, runs, and artifacts.
- Add authenticated creation/status/artifact endpoints.
- Add idempotency and ownership checks.
- Add the worker queue, scheduler, and per-run lease.

### Phase D — Integrate AGF and SPC

- Generate canonical charts from persisted birth data.
- Generate and validate all four projected contexts.
- Promote source artifacts with provenance.
- Invoke the pinned authoring runtime.

### Phase E — Operate safely

- Add cost/attempt/time limits.
- Add terminal alerts and notifications.
- Add object-storage promotion and workspace cleanup.
- Add redacted telemetry export and dashboards.
- Run one staging end-to-end reading and failure/recovery drills.

### Phase F — Private launch

- Enable a small invited cohort.
- Review every run operationally at first.
- Sample complete decks editorially.
- Hold authoring-profile changes behind versioned releases and regression QA.

## 10. Immediate recommendation

The next work should be a compact release-engineering sprint in SBE, followed by
creation of the AstroWoof API repository. Package and tag the current known-good
behavior before the API begins depending on it. The API should initially run the
pinned worker artifact as a subprocess or container job and treat its state and
delivery contracts as external interfaces.

This preserves the strongest property of the current system: extraction,
authoring, QA, retry, and delivery evolve and ship as one tested semantic
runtime, while the API remains a conventional product service rather than a
second home for domain logic.
