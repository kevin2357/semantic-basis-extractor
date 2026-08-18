# Slice 0: Baseline and Aster-Shape Reproduction

Status: complete; API-approved for Slice 1 contract freeze.

## Result

The Aster-shaped handoff gap is reproducible without OpenAI, historical data
mutation, or API database access.

Current SBE 0.4.4 durably preserves the final native truth. A review-terminal
workspace contains `run.json`, `public-run.json`, a complete validated snapshot,
the provider metadata retained on the current attempt/action, and a derivable
lifecycle inspection v0.3 whose terminal outcome is `review_required`.

What it does not preserve is the invocation-scoped, append-only handoff needed to
prove that this terminal meaning was published and available before a consumer
applied generic subprocess fallback. The ordinary exact CLI prints current state,
emits non-authoritative events, and then exits 2; neither stdout nor the event stream
is an authoritative workspace result. A consumer that handles the exit first can
therefore miss native terminal meaning even though the final workspace is coherent.

## Provider-free reproduction

The sanitized fixture
`fixtures/aster-shaped-authoritative-gap.v0.json` models:

- one durable provider operation ID attached to the failed attempt;
- native and public `FAILED_REQUIRES_REVIEW`;
- complete snapshot validation;
- lifecycle inspection v0.3 `review_required` terminal truth;
- diagnostic-only exit 2 followed by hypothetical generic retry/reclaim; and
- the intended successor rule: generic fallback and a second provider operation are
  both forbidden after valid native review-terminal evidence.

The characterization test constructs that workspace entirely in a temporary
directory and verifies both the authoritative present facts and the absent journal/
execution-result capabilities. Provider operations and spend are zero.

## Current durable boundary inventory

### Exact ordinary authoring

1. Paid action preparation/authorization/consumption and provider ID/result updates
   call `persist_state()` at their individual boundaries.
2. Worker-thread persistence writes `run.json`, `public-run.json`, and spend-
   authorization requests, but deliberately does not publish a snapshot.
3. After workers and final QA unwind, the main command calls `save_state()`, which
   writes current state/public state/authorization requests and then publishes the
   complete workspace snapshot.
4. Only after that snapshot does the command emit checkpoint/terminal events, print
   the result to stdout, and convert review/failure status to exit code 2.

### Bounded ordinary authoring

1. Each attempt/stage mutation uses `save_state()` and publishes a snapshot.
2. A failed bounded pass becomes `FAILED_REQUIRES_REVIEW` and returns current state
   from the lifecycle function.
3. The bounded CLI prints `public-run` state. Unlike the exact CLI, its ordinary
   path currently has no explicit review-terminal exit conversion or durable
   invocation result.

### Neutral provider reconciliation

1. Inspection v0.3 validates route/mechanism/action/checkpoint identity.
2. Reconciliation retrieves only known provider work, persists resulting native
   mutations, publishes a snapshot, derives cycle result v0.2, and returns it.
3. The typed result is printed by the CLI but is not itself an invocation-bound
   authoritative workspace artifact. It describes one cycle, not the complete
   earlier ordinary-submission/terminal chronology.

### Events and stdout

- Events are intentionally redacted, optional, failure-isolated, and non-
  authoritative.
- stdout is an ephemeral transport and may be unavailable or handled after process
  exit classification.
- Neither is suitable as the sole duplicate-provider-work prevention boundary.

## Missing authoritative facts

The current workspace cannot independently establish:

1. a complete ordered cross-invocation transition sequence;
2. every provider-operation observation beneath one logical paid action;
3. which journal range one command invocation consumed and produced;
4. a terminal result cryptographically bound to the exact snapshot/state revision;
5. that native terminal meaning was valid before exit-code fallback; or
6. that the API transactionally acknowledged/ingested that exact evidence.

The final item remains API-owned and must not be forged by SBE.

## Crash-window inventory

| Boundary | Current durable observation | Safe interpretation for new contract |
|---|---|---|
| Provider accepted work before ID persistence | State may remain `SUBMITTING` | Ambiguous; fail closed, never resubmit |
| Provider ID persisted before later attempt state | Ledger has authoritative ID; other projection may lag | Reconcile known ID; do not submit |
| `run.json` written before public/auth companion files | Snapshot no longer matches | Partial publication invalid; fail closed |
| Worker-thread state persisted before main snapshot | New state exists under an older snapshot | Incomplete checkpoint; fail closed until republished |
| Terminal state/snapshot committed before event | Native terminal is durable; event may be absent | Event irrelevant to correctness |
| Terminal state/snapshot committed before stdout | Native terminal is durable; command result transport may be absent | API must ingest workspace result, not depend on stdout |
| stdout/event observed without matching complete snapshot | Observation can race or be incomplete | Refuse as non-authoritative |
| Reconciliation snapshot committed before returned cycle result | Provider/native progress is durable; invocation result is lost | Fresh inspection/replay may recover, but the invocation handoff is incomplete |
| New result file written without matching journal/snapshot hashes | Some files may exist after interruption | Result is invisible/invalid until all identities validate together |

The irreducible provider gap remains: provider submission and native persistence are
not one transaction. The new protocol can classify ambiguity and prevent duplicate
submission; it cannot claim atomicity the provider does not offer.

## Baseline tests

- New focused Aster-shaped characterization: 1 passed in 1.256 seconds.
- Complete repository suite: 357 passed in 237.475 seconds.
- An earlier targeted invocation named one nonexistent test module and therefore
  reported a harness import error after 155 real tests passed. It was replaced by
  the authoritative full discovery result above and is not a product failure.
- `git diff --check`: pass.

## Questions for the required API review

1. Does this inventory capture the exact missing facts needed by API transactional
   ingestion, especially the distinction between SBE publication and API
   acknowledgement?
2. Is it acceptable that the native execution result proves SBE publication but
   cannot prove API ingestion, which must be an API-owned record?
3. Should Slice 1 freeze one latest invocation-result artifact plus an append-only
   journal, with replay/cursor ingestion bound to journal sequence and digest?
4. Does API agree that bounded ordinary review behavior must join the same explicit
   terminal-result contract even though its current CLI exit behavior differs from
   exact authoring?
5. Are any additional provider-operation facts required beyond action/request
   binding, provider kind/ID/status, submission/result observations, cost
   disposition, journal sequence, and explicit supersession (if ever supported)?

## Gate assessment

PASS for the SBE characterization gate. Slice 1 must not begin until the API agent
confirms that this reproduction, missing-fact list, and crash-window inventory solve
the intended cross-repository problem.

## API review resolution

The API agent approved the reproduction and all five answers. Slice 1 must include:

- an SBE record identity distinct from provider external ID plus closed observation
  kind and `observed_at`;
- versioned price/usage evidence reference for reported amounts without raw provider
  bodies or prompts;
- immutable per-invocation result artifacts, never a mutable authoritative latest;
- replay binding across result identity, journal range/digest, and native run;
- frozen request/profile digest in the action binding; and
- refusal of any second distinct provider ID because supersession remains
  unsupported this sprint.

SBE publication proves only native publication. API acknowledgement remains an
API-owned PostgreSQL receipt. The gate is approved for Slice 1.
