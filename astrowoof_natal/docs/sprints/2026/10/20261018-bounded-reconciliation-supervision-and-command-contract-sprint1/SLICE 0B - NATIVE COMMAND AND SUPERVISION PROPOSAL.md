# Slice 0B — proposed native command and supervision contract

> **Historical design; alpha scope narrowed.** The current proposal and test
> expectations are in [Slice 0C](SLICE%200C%20-%20ALPHA%20SAME-CALL%20HANDOFF%20AND%20CONTAINMENT.md).
> The durable attempt-binding/anchor/slot/automatic-reconstruction sections
> below are not alpha requirements. Their findings explain why this narrower
> contract fails closed on ambiguous lost output rather than guessing. Gate A
> remains open; other portions below are historical until checked against 0C.

**Proposed for joint Gate A; not implemented or approved.** SBE proposes the
native executable and what it can honestly attest. API must review this against
its actual worker, lease, child, checkpoint, custody and economics paths and
specify its half. No provider, QA, deployment or release authorization follows.
The [0A inventory](SLICE%200A%20-%20NATIVE%20AND%20API%20BOUNDARY%20INVENTORY.md)
distinguishes existing behavior from this proposal.

**Review update:** API's [Gate A review](API%20AGENT%20-%20GATE%20A%20CONTRACT%20REVIEW.md)
agrees with the direction and requests concrete identity, ordering and recovery
rules. SBE agrees with those requirements; the design below is a refined
proposal for API re-review, **not** a claim that Gate A is closed.
API's [v2 review](API%20AGENT%20-%20GATE%20A%20CONTRACT%20REVIEW%20V2.md)
approves the direction but correctly notes that anchor membership alone cannot
identify the producing attempt. See the [binding research](GATE%20A%20-%20ATTEMPT%20PUBLICATION%20BINDING%20RESEARCH.md)
for candidate mechanisms and the remaining proof obligations.

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

### Proposed invocation-scoped durable binding

For supervised bounded reconciliation, use the API-issued
`supervision_invocation_id` from the validated prelaunch envelope as the
candidate command-attempt key; it is unique per child launch and is **not**
the job's attempt ID or SBE's native publication `invocation_id`. Also bind
the native run, `provider_reconciliation` command kind, actual argv digest,
bounded v2 route, admitted profile ID/digest, decision snapshot and the
cycle-result checkpoint when there is one. API must validate these against its
persisted prelaunch authority and route/profile context. Reusing this key for
the new binding requires API's agreement and tests; it must not transfer or
log a supervision capability or treat the key alone as authority.

Propose a new, closed, versioned SBE publication-binding record with exactly
one of `published` or `no_publication` and a canonical digest. The published
variant identifies the native publication invocation, exact result ID/SHA,
exact receipt ID/SHA, and the receipt's snapshot and checkpoint-basis digests;
the no-publication variant carries null publication identities and is valid
only for a verified no-publication outcome such as `not_due`. A wrapper
returned on stdout and, **when publication occurred**, an exact attempt-keyed
recovery reader must return the same validated record. API's current collector
does not recognize this additional companion, so API and SBE must jointly
extend and freeze its stream cardinality rather than assume it is compatible.
The `not_due` path must retain its no-mutation/no-successor-checkpoint behavior:
do not create a workspace marker or seal simply to record `no_publication`.
If its output is lost, resolve only from independently valid retained evidence
or leave the command outcome unknown; do not infer it from no visible result.
A different binding or multiple candidates for the same attempt is a conflict,
not a reason to choose the newest. API independently
reads the exact native result/receipt, validates its IDs, digest, journal and
snapshot/checkpoint membership, and joins the attempt binding to its own
authority. A different attempt on the same run cannot claim the publication.

**Publication/snapshot ordering needs a deliberate implementation.** Current
`native_transitions.py::publish_native_execution_result` writes the result,
writes and validates the workspace snapshot, and only then writes its receipt;
`closure.py::snapshot_inventory` excludes `native-publication-receipts/`.
Simply writing a new attempt-to-receipt file as an ordinary included member
after the receipt would invalidate the already-sealed snapshot or change the
receipt identity. Nor is a self-hashed post-seal sidecar by itself proof that
this attempt caused this publication. SBE's proposed approach is:

1. Under the same validated single-writer boundary, write a closed,
   attempt-scoped **pre-seal intent/anchor** containing the prelaunch binding,
   route/profile and decision/cycle identities before native publication. Its
   inclusion in the publication's checkpoint basis and receipt-retained
   snapshot must be verifiable without circularly referring to the later
   result or receipt. Reject an existing conflicting intent.
2. Seal the native result and receipt as normal, then write the complete
   immutable attempt-keyed binding in a designated publication-evidence area
   whose snapshot and archive treatment has been explicitly specified and
   tested. An exact reader validates an **unambiguous publication-to-specific-
   attempt link**, plus the sealed result/receipt and mapping; mere anchor
   membership or a sidecar's digest alone is insufficient. In particular, an
   old anchor may also be a member of a later publication's snapshot.
   It must not use latest-result discovery. A typed stdout companion carries
   the same binding, but stdout is not its only recovery location.
3. Prove that API's actual checkpoint archive retains this evidence and that
   restore preserves the exact logical root and validates all joins. A locally
   durable binding is not remote durability. If the child dies between intent,
   seal, receipt and binding, repair only when an exact unique attempt-to-seal
   relationship is provable from retained validated evidence; otherwise return
   unresolved, not a guessed result. If the workspace and any checkpoint
   containing the evidence are both lost, the outcome remains unknown.

   Current API `services/checkpoint_archive.py::inventory_workspace` walks
   all regular workspace files, including publication-receipt files; this is
   encouraging source evidence that such a sidecar could be archived. It is
   not a proof that a particular post-seal sidecar has been written, archived,
   remotely committed or correctly restored, so the joined test remains needed.

The reconciliation result's pre-publication `result_checkpoint` snapshot and
the later publication receipt snapshot are distinct digest domains and may
legitimately differ. The design must name both, join each to its own artifact
and prove the transition/ancestry; do not equate them merely to pass an API
check. Confirm also that the proposed anchor, excluded evidence location,
existing native journal repair/replay, and terminal-review exact-replay
behavior really support one-to-one attempt attribution before freezing this
mechanism. If not, agree a versioned journal/result successor or another
verifiable design; fail closed in the meantime. This is a design proposal,
not a claim that an existing receipt already binds the API attempt.

The current journal and execution result do not carry the API supervision
invocation as an explicit publication field. A candidate singleton active
publication slot tied to a preallocated native invocation may avoid changing
the closed result schemas, but only if its exact retained-basis association,
writer exclusion, crash repair and old-terminal replay are proven. A versioned
journal/result successor is the fallback if that proof cannot be made. Neither
mechanism is selected as final until API reviews concrete fields and tests.

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
writer-held observation boundaries before post-wave local continuation and
before publication **only where a validated checkpoint and trustworthy
predecessor chain can actually be provided**. If those boundaries cannot be
implemented safely, narrow the promise and rely on the post-wave safe point
plus ordinary-result precedence and API escalation; do not claim they already
exist. Agree how the admission anchor is joined across multiple snapshots;
never label an old anchor as an immediate predecessor without proof.

At the SBE safe point, an already sealed ordinary terminal result that precedes
the child's valid suspension observation may take the **native** ordinary
path rather than emitting a competing suspension. This alone does not grant
API pre-fence precedence or release capacity: API's conservative rule requires
the parent to have observed the exact terminal command strictly before its own
force-fence observation, with the required persisted authority and joins.
If ordering evidence is missing, contradictory, simultaneous at the agreed
resolution, or not durably recoverable, keep custody and the applicable fence
unresolved. A child seal timestamp alone cannot override the parent fence.
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

For API's strict parent-observation predicate, propose one serialized parent
observation domain with an ordered event/sequence record, plus UTC audit times
and optionally a process-local monotonic clock. Such monotonic readings must
never be compared across processes or assumed durable across restart; absent a
durable ordering proof after a crash, retain the ambiguous fenced posture.
The native child separately samples and persists actual request-observation
time for request freshness. Any disagreement or uncertain clock fails closed;
cross-process UTC comparison alone is not proof of causal ordering. API must
review whether this fits its worker/DB authority and describe exact persistence
and loss semantics before acceptance.

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

For joint replay, separately inject unknown checkpoint write/acknowledgement;
checkpoint durable then outer DB rollback; custody ingestion followed by
economics savepoint failure and outer commit; successful savepoint then outer
rollback; and successful commit with lost acknowledgement. Confirm actual
durable state, not merely invoked methods. Economics uses a nested savepoint,
not an independent commit; logs cannot prove its outer transaction committed.
Retry only from exact retained evidence and applicable lease/fence authority;
conflicting replay or missing proof stays unresolved.

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

Add explicit cells for two attempts on one run; wrong attempt/predecessor and
preexisting older/newer result; conflicting attempt binding; stdout lost after
seal with and without a recoverable checkpoint; receipt/snapshot digest-domain
differences; terminal sealed before the child reads the request but observed
by the parent only after its fence; expired request, equal/ambiguous ordering
and lost parent ordering on restart; and every checkpoint/outer-transaction
boundary above. Confirm an authorized repeat GET is not treated as a paid
create and that no next wave starts after a request is validly observed.

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
