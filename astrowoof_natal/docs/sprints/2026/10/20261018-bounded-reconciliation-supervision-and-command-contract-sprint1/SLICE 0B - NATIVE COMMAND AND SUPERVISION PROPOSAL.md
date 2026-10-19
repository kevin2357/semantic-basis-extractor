# Slice 0B — proposed native command and supervision contract

**Proposed for joint Gate A; not implemented or approved.** SBE proposes the
native executable and what it can honestly attest. API must review this against
its actual worker, lease, child, checkpoint, custody and economics paths and
specify its half. No provider, QA, deployment or release authorization follows.
The [0A inventory](SLICE%200A%20-%20NATIVE%20AND%20API%20BOUNDARY%20INVENTORY.md)
distinguishes existing behavior from this proposal.

## 1. Executable, input and transport

Extend the existing installed `astrowoof-run-bounded-natal` rather than invent
a second native coordinator. For a supervised bounded interactive cycle API
launches that executable with its **bounded** frozen profile/runtime arguments,
`--run-dir`, `--resume`, `--provider-reconciliation-cycle`, `--provider openai`,
`--observed-at`, `--events-stdout-jsonl`, `--supervision-envelope` and
`--suspension-control-root`. The last two are paired, exact command argv is
bound in the prelaunch envelope, and the run/workspace/profile, route family
`bounded_natal`, interactive mechanism and `authoring_run.v2` must be checked
against the frozen workspace and admitted release context. Reject incomplete,
conflicting, unsupported or cross-route combinations before provider I/O or
workspace mutation. New-run-only inputs and spend/initial-wave/dispatch grants
are not accepted in reconciliation. API must stop passing exact-only arguments;
the precise closed allowed argv/profile flags must be captured in fixture and
reviewed, not inferred from this sketch.

Keep the existing legacy bounded plain JSON behavior when the new stdout flag
is absent, and retain `--events-jsonl` file behavior. Specify and test whether
simultaneous file and stdout event sinks are supported; reject ambiguity until
frozen. In stdout mode use existing `sbe.command_result.v1` wrappers and
recognized `sbe.execution_event.v1` diagnostics, never log prose mixed into
stdout. Diagnostics are not authority; redact paths, prompt/deck data, raw
provider responses, credentials and exception prose. API retains its bounded
stdout limit and rejects invalid JSON, unknown/duplicate/mixed authority records.

For an ordinary cycle emit exactly one wrapped
`astrowoof.provider_reconciliation_cycle_result.v0.2`. A newly sealed terminal
delivery **or** review may additionally emit the corresponding existing exact
same-call command-result companion; never emit both. If cooperatively
suspended, emit exactly one wrapped
`astrowoof.native_suspension_command_result.v1` and no ordinary or terminal
companion. Reuse the existing schemas only if all invariants are satisfied;
introduce/review a successor rather than silently changing their meaning.
Preserve existing 0/3 ordinary exit conventions and define suspension exit 0;
parser/validation/unexpected failures must not be interpreted as successful
authority merely from an exit code. API accepts only verified stdout plus the
appropriate direct-child and sealed-evidence joins, not diagnostic events.

## 2. Identity, publication and API joins

The ordinary result retains its native run, v2 inspection, decision snapshot,
operation summaries and optional result checkpoint; no new provider identity
is invented. `not_due` has no retrieval or successor checkpoint. A sealed
native transition has an SBE-owned publication invocation, exact result ID,
receipt ID and digests bound to the just-published result/receipt and snapshot.
API owns its job/attempt/lease/supervision identities and pre-persists the
expected native run and release/profile identity; these are not interchangeable
with SBE's publication invocation. Terminal companion references must be
produced from the same call's actual sealed publication and read by exact ID;
they must not be reconstructed from latest-result discovery.

The current API bounded worker uses `read_latest_sealed` for native transition
ingestion. Gate A must settle an **exact same-call transition join for both
terminal and nonterminal publications**, not merely assume that terminal
companions solve every publication: if existing ordinary result/checkpoint
does not carry a sufficient exact selector, agree on a compatible typed
successor/companion and its digest before implementation. Do not require a
fictional selector for `not_due`. The joint gate must prove API's intended
persisted identities, replay/idempotency and remote checkpoint ordering, and
handle an already-published result when output is lost without inventing a new
result or granting authority from a generic latest lookup.

API must validate the native inspection with an explicit route/profile-bound
v1/v2 compatibility policy, maintaining support for actually admitted old
runs and rejecting wrong route, schema, invocation, snapshot, profile, receipt,
digest, executable or release context. API owns lease authority, native result
receipt ingestion, exact durable checkpoint publication, cost/reservation and
terminal disposition. No native local state alone proves these API facts.

## 3. Fence, observation and ordinary-result precedence

Use a writer-held observer at least before the **wave** and after its responses
have been adopted and a validated local snapshot durably written. A request
validly observed before the wave means no GET is started by that cycle. A
request arriving once the wave is admitted cannot retroactively prevent or
cancel that wave: up to four selected retrievals may be in flight or queued,
and one may begin after the fence. Once all returned results are safely
checkpointed, observe again and suspend before more continuation or provider
work. A stuck GET, forced process death or expired/invalid request is not an
acknowledged suspension; API must use its independently authorized escalation
and preserve unproven provider custody. No assumed strict wall-clock deadline.

There is a further race after the post-response check: local continuation and
native publication can run before another observation. SBE proposes explicit,
writer-held observation boundaries before local adoption/continuation and
before publication **only where a validated checkpoint and trustworthy
predecessor chain can actually be provided**. If those boundaries cannot be
implemented safely, narrow the promise and rely on the post-wave safe point
plus ordinary-result precedence and API escalation; do not claim they already
exist. Agree how the admission anchor is joined across multiple snapshots;
never label an old anchor as an immediate predecessor without proof.

An already sealed ordinary terminal result that precedes a valid suspension
observation wins; API must independently validate its identity and ordering.
A fence that arrives after the last effective observation can race with
ordinary completion: report the actual outcome; do not manufacture both a
suspension and an ordinary result to satisfy the caller. A native suspension
receipt means the **local** writer reached and recorded the stated safe point;
API still requires the matching direct-child exit and verified remote
checkpoint/custody evidence before its own downstream action. A timed-out or
killed child cannot use the cooperative receipt to assert it has exited.

### Gate A decision: time and replay

Existing observer code uses the command's fixed launch `observed_at` for
freshness, precedence and recorded suspension time even when a fence appears
later. Proposed resolution: distinguish cycle decision time from a real UTC
observation time sampled when reading a request; validate a supported UTC
clock, request creation/expiry and grace ordering, and ensure persisted replay
uses the original recorded observation rather than minting a new one. API and
SBE must agree the clock source, skew/precision, ordering and deterministic
test seams before freezing the schema or semantics. A stale launch timestamp
must not prove that a later request was fresh. Review impacts on shared exact
behavior and old records; if a schema/semantic change is needed, version it
instead of rewriting historical evidence. No shared observer behavior changes
are assumed approved by this proposal.

## 4. Crash/restart and no-duplicate boundary

- Before GET: with a valid observed fence, no provider call; invalid identity,
  stale control or ambiguous checkpoint is a refusal, not a successful stop.
- During GET: process loss can leave the provider response unknown. On an
  authorized later continuation, retrieve only an already proven operation ID;
  a repeat GET is not a new create. Never infer completion, cancellation or
  cost from missing output. Exactly how API obtains the durable checkpoint and
  honors a hold remains API-owned.
- After response, before or after local snapshot: preserve the precise durable
  boundary, resume from validated retained evidence and avoid duplicate create;
  test local crash before/after each write. Failure to prove snapshot ancestry
  or custody is fail-closed.
- After SBE publication but before stdout, API ingestion, DB commit or remote
  checkpoint: simulate each loss independently; replay must join the same
  sealed identities or remain unresolved. A remote checkpoint and API receipt
  do not follow from an SBE-local file. No paid follow-up is authorized merely
  because a reconciliation or replay succeeded.

## 5. Joint provider-free matrix

| Case | Native proof | API joined proof |
| --- | --- | --- |
| Six known IDs, mixed pending/completed/failed; more than one wave | Max four per wave, correct identity and state, no POST/create | Real installed CLI and worker consume each result; preserve all custody and idempotency |
| Fence before wave / during blocked GET / after responses | No GET before observed fence; in-flight wave and post-checkpoint suspension as above | Valid control joins, direct-child exit, exact checkpoint and fence handling |
| Fence during local continuation / around terminal seal | Only claimed safe points, ordinary precedence; no double authority | No premature release; exact receipt/terminal join and actual child outcome |
| Missing, expired, tampered, duplicate or cross-route controls; wrong profile/root/ID | Refuse before unsafe work; preserve evidence | Reject wrong lease/command/digests, mixed or duplicate envelopes and bad exit |
| Crash before/during/after GET, checkpoint, publication, stdout, DB or remote checkpoint | No invented identity, safe repeat retrieval and local recovery | No duplicate create or receipt; replay/refusal under real transaction and checkpoint failure |
| Not due, nonterminal, delivery and review | Correct v2 result/companions; no fabricated terminal selector | Correct return, exact receipt ingress, idempotency and route-bound v1/v2 validation |
| Economics export match/mismatch/missing | Export reflects actual native evidence, no invented costs | Exact run/snapshot join and nonfatal unavailable diagnostics; no causal assumption |
| Exact-route and historical context controls | Existing public behavior and suspension tests remain sound | Old admitted version routes to its own compatible worker, no substitution |

The fixture must use synthetic bounded v2 data, six identifiable operations,
barrier-controlled fake transport, tests that forbid POST, and no real provider
network or retained QA workspace. Installed-command tests should use a
test-only injected transport or isolated fake endpoint without changing
production provider semantics; a native function test alone is insufficient.
Local fake storage cannot prove actual Render/remote-storage guarantees, and
provider-free proof does not authorize live QA.

## 6. Successor release and profile

Create a new immutable bounded profile ID and package descriptor for the new
SBE version, bind the appropriate existing or explicitly successor prompt
release and its allowlist, recompute all affected catalog/profile/component
digests, and qualify the actual wheel and worker context. Do not mutate the
0.4.72 profile or declare newer code equivalent. API must explicitly bind and
route each persisted run to its admitted compatible worker context; the old QA
run's custody, disposition and context retirement are separate decisions.
Whether exact profiles need successors is an independent operational choice;
do not invent them merely to make bounded rollout work. Wheel, full API join,
package release, deployment, profile activation and paid QA each retain their
own gates.

## Gate A questions for API

1. Does the existing consumer accept this argv, stream cardinality and exit
   contract once made route-specific? Which exact profile flags must be frozen?
2. How should nonterminal same-call publication identities cross the boundary,
   and how does API durably recover an output-lost publication without latest
   discovery or duplicate custody?
3. What exact wall-clock/ordering and checkpoint-ancestry contract can both
   systems verify, including already-running GETs and clock skew?
4. Which direct-child, lease/fence, checkpoint, economics and reservation
   evidence is required in each success/crash/escalation case?
5. Which historical worker contexts and exact-route regression cells must stay
   available for the intended rollout? What evidence is required before a
   fresh QA canary, without modifying the earlier run?
