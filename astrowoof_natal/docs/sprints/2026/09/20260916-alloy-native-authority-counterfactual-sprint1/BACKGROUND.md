# Alloy Counterfactual — Native-Authority Seam Failures

## Status and purpose

This is a documentation-first, provider-free counterfactual investigation. It asks
whether a small Alloy model of the **SBE/API control-plane boundary**, had it existed
in August 2026, would have exposed several historical lifecycle and authority seam
failures before live qualification cohorts encountered them.

It does not propose that Alloy become the pipeline's backbone, replace executable
tests, reconstruct historical state, or authorize any provider, R2, database,
deployment, or release operation. The goal is narrower: identify which historical
failure shapes are small enough to be found by bounded state exploration, and which
were inherently empirical integration failures.

## The question

The useful counterfactual is not “could a formal model have predicted every bug?”
It is:

> If SBE's sealed result, API's custody/authority records, and the cross-package
> command adapter had been represented as a small transition system, which unsafe
> traces would have existed as automatic counterexamples before a live run?

The likely payoff is early discovery of **missing precedence and authority rules**.
The likely limit is that Alloy cannot execute Python, inspect a wheel, observe a
filesystem path, call a provider, or discover an emitted log record by itself.

## Vocabulary

### Native result and native authority

SBE is authoritative for validated native lifecycle facts: sealed result identity,
receipt, snapshot/binding identity, route, and the exact command shape it exposes.
The API is authoritative for its PostgreSQL-owned custody, leases, capacity,
spend/admission policy, and persisted authorization/grant records. Neither side may
replace an absent exact identity with a plausible guess.

### Adapter

An **adapter** is the deliberately narrow translation layer between two systems with
different representations. Here, it reads a public SBE result/inspection/request,
validates its schema and identity joins, translates it into API-owned persistence or
an exact command invocation, and applies API policy without reading private SBE
workspace state.

Examples:

- the worker's terminal-result intake adapter turns a sealed SBE terminal result
  into an API terminal/custody transition before generic process-exit handling;
- the lifecycle-command adapter chooses a retrieval-only reconciliation command
  rather than ordinary resume when provider identities are pending; and
- the external-authority adapter takes SBE's exact public request, obtains API's
  matching grant, and invokes only the constrained dispatch command bound to both.

An adapter is not a second lifecycle engine. Its safety rule is: it may translate
validated facts, but never infer an unexposed SBE state or synthesize continuation
authority.

### “No invented continuation”

The recurring native-authority invariant is:

> A new provider-creating continuation is allowed only when one exact, live,
> unconsumed SBE request joins one matching API grant and one matching native
> dispatch boundary. Partial, stale, ambiguous, contradictory, or merely plausible
> evidence yields a typed refusal/review posture—not fresh work.

This slogan is intentionally broader than one schema version. It covers initial
waves, ordinary post-fan-in retries, retained workspace recovery, and ambiguous
post-intent state.

## Danish-adjacency map: Aster and Bramble

The original Aster/Bramble incidents were temporally adjacent and involved the same
SBE/API boundary, but they were **not one defect**. A counterfactual model should
retain them as separate witnesses; collapsing them would hide the distinctions that
eventually made the contracts reliable.

### Aster: terminal result lost to generic retry

In the August paid qualification route, SBE durably reached
`FAILED_REQUIRES_REVIEW` and emitted a native terminal observation. The API worker
observed the nonzero subprocess exit first, classified it as a generic retryable
dependency failure, reclaimed the job, and re-entered SBE. Further provider work
occurred under the same logical paid-action identity before the run eventually
delivered.

The failure was not “logs were missing” and not “SBE should write API tables.” It
was an ordering/ingress defect: valid terminal native meaning had no required,
durably ingestible path that outranked generic exit-code fallback.

The historical invariant is compact:

> Once a valid sealed terminal result is available for this invocation, generic
> retry cannot be selected for that invocation.

### Bramble: stale terminal closeout replay

Bramble reached native `DELIVERY_COMPLETE` with a complete delivery package. API
closeout subsequently attempted two sequential providerless-denial operations from
one inspection observation; the stale second operation was refused. This was not an
unrecognized native terminal. It was an exact-once custody-release problem: native
completion and API-owned release must be paired once, without inventing provider
work or consuming the same observation twice.

Its invariant is different:

> One validated terminal observation can settle/release each corresponding API
> custody resource at most once.

### Aster: pending responses selected ordinary resume

In the next relevant cohort, six initial provider responses had durable identities
but SBE was repeatedly invoked through ordinary semantic-closure resume rather than
the retrieval-only provider-reconciliation command. It continued publishing waiting
state and held the sole worker slot. No duplicate submission occurred.

This is a next-command-selection defect:

> Pending durable provider identities select the bounded reconciliation route;
> ordinary authoring resume is not a substitute retrieval command.

### What genuinely unifies the three

They share a control-plane rule, not a common implementation cause: API process
mechanics and scheduler policy cannot outrank validated native facts or select a
different native command by inference. They therefore belong in one *terminal and
command-selection* Alloy model, with three distinct forbidden traces.

## The tighter native-authority family

This family is the cleanest candidate for a second Alloy model because every member
is a variation of missing exact create authority.

### Retained initial-wave reanimation (Aster)

The API already held immutable initial-wave authority and six original provider
operation records. The retained SBE workspace took a fresh initial-wave path,
prepared a different six-action inventory, and created six new Responses. API
rejected the incompatible native publication, but only after the external side
effect. The required correction was an exact public SBE request, a matching API
aggregate grant, and native single-writer validation at dispatch.

The crucial negative branch is historical lineage that cannot prove one exact
reusable inventory. Such lineage is `initial_wave_lineage_unjoinable`, not fresh
admission and not an inferred retained resume.

### Post-fan-in retry request/grant/dispatch gap (Diffie and Hellman)

Later creative retries could be locally prepared and API-authorized, yet lack the
exact external-authority-v2 request/grant/dispatch envelope SBE requires to create.
SBE safely refused provider I/O. API initially treated that as a generic retryable
posture instead of completing the exact handoff or stabilizing at a typed refusal.

An API authorization is therefore not itself a native create permission. It is one
member of an exact join.

### Ambiguous post-intent submission

When SBE has durably recorded pre-submit intent but lacks a durable provider
identity, a provider call may or may not have happened. The state is ambiguity,
not authority to try a fresh create. The safe outcome is review/retention and zero
new create calls.

### Review with mixed retry custody

Pippin and Duchess reached terminal-review posture while their API records still
showed mixed retry custody. That observation initially looked like a skipped retry
branch, but action/pass lineage and final-QA evidence showed that terminal review
and unconsumed-looking unrelated retry rows must not be collapsed into “permission
to reopen.” This witness informs precedence: a terminal review result is not a
generic continuation grant.

### Shared authority invariants

1. Provider create requires an exact request, matching grant, and matching,
   unconsumed dispatch boundary.
2. Prior provider/authority lineage plus no exact reusable inventory forbids fresh
   initial-wave creation.
3. Submitted intent without provider identity forbids a new create.
4. Terminal/review evidence cannot be relabeled as continuation permission.
5. A generic retry response cannot repeatedly stand in for a missing exact
   request/grant/dispatch handoff.

## Recommended bounded Alloy models

The models should be small and intentionally non-production. They represent closed
state categories and relations, not workspace contents, prompts, provider payloads,
or SHA-256 implementations.

### Model A — terminal ingress, custody, and command selection

**Entities:** one run, native result/receipt, API observation, process outcome,
API custody resource, and candidate command.

**State dimensions:** terminal availability/validation, whether API ingested it,
generic exit classification, custody settled/released, provider identities pending,
and selected command (`retry`, `ordinary_resume`, `reconcile`, `terminal_closeout`,
or `refuse`).

**Checks:**

- valid terminal result implies no generic retry for the same invocation;
- a terminal observation can settle one custody resource no more than once;
- pending provider identities select reconciliation rather than ordinary resume;
- a stale or invalid result cannot settle custody;
- a terminal closeout creates no provider work.

**Historical witnesses:** Aster terminal reanimation, Bramble duplicate closeout,
and Aster provider-pending loop.

### Model B — exact external authority and provider-create permission

**Entities:** run, initial-wave/retry action inventory, request, grant, dispatch,
intent, provider identity, lineage evidence, and result disposition.

**State dimensions:** request identity/order/snapshot binding; grant matching and
consumption; prior lineage; exact reusable inventory; intent state; provider
identity; and create count.

**Checks:**

- `ProviderCreate` implies one exact live request, matching grant, and unconsumed
  dispatch;
- prior lineage without one exact reusable inventory implies refusal/review and
  zero create;
- intent without provider identity implies no fresh create;
- one consumed grant/dispatch cannot authorize another create;
- terminal review cannot be a create-capable state.

**Historical witnesses:** retained Aster reanimation, Diffie/Hellman retry
handoff, ambiguous submission, and review-with-mixed-custody precedence.

### Model C — optional adapter/translation refinement

This is useful only after Models A and B. It makes adapter behavior explicit:
public SBE evidence may be admitted, rejected, or unavailable; API can persist a
validated translation or choose a defined no-op/refusal; it may not derive a
different native request from API state alone.

This model would test the architectural boundary directly, but should not attempt to
model JSON serialization, subprocess stdout, wheel metadata, R2 paths, or log
delivery. Those belong to executable integration tests.

## What Alloy would and would not have caught

Likely early counterexamples:

- terminal result versus generic retry precedence;
- duplicate/stale terminal closeout;
- pending-provider reconciliation versus ordinary resume selection;
- retained initial-wave reanimation;
- missing v2 dispatch envelope treated as a generic retry loop; and
- ambiguous post-intent state reopened as new provider create.

Not directly discoverable by these models:

- Python 3.11 variadic `joinpath` behavior;
- fixture line endings, wheel byte identity, or package metadata;
- a formatter rejecting an uppercase exception token;
- a missing Better Stack event caused by a Python exception boundary; or
- a wrong concrete R2 root/path/digest value.

For the latter cases, a model can clarify the desired rule—for example, “all joins
share one canonical root identity”—but executable tests, installed-wheel gates, and
retained-workspace reproductions remain the actual detection tools.

## Success criterion

The sprint succeeds if it produces a small, replayable counterfactual corpus that
answers with evidence:

1. which historical traces are satisfiable in an intentionally permissive old model;
2. which one or two invariants eliminate each trace;
3. whether the resulting corrected model still permits ordinary success,
   reconciliation, terminal closeout, and valid externally authorized continuation;
4. which conclusions are formal-design insights versus empirical claims requiring
   executable tests; and
5. whether the effort is useful enough to retain as a small design aid.

