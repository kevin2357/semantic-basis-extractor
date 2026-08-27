# Post-Fan-In Routing Contract and Decision Matrix

Date: 2026-08-27
Status: proposed contract freeze; awaiting API review before runtime implementation

## Purpose

This contract separates immutable initial-wave lineage from current executable
native work. It governs how SBE routes exact and bounded Natal after the initial
six-member wave, especially when a creative-retry response has been retrieved and
must be fanned into deterministic local evaluation before any later paid action is
eligible for authority.

The contract tightens runtime command selection. It does not add a lifecycle state,
change lifecycle v0.7, change temporal v0.6, or transfer authority between SBE and
the API.

## Four distinct facts

These facts are never interchangeable:

1. **Initial-wave admission** — six initial members form one prepared v1 wave.
   Provider creation requires the exact v1 aggregate grant and six member
   authorization documents.
2. **Provider custody** — a paid action has provider identity or provider-call
   ambiguity. Reconciliation/review outranks local work and new authority.
3. **Local fan-in** — retrieved provider evidence is durable, but SBE has not yet
   applied it to pass/retry truth. This consumes no new authority and performs no
   provider I/O.
4. **Ordinary paid continuation** — after local fan-in, a new ordinary action may
   be `PREPARED`. Provider creation requires a fresh exact v2 request, v2 grant,
   and ordinary authorization document.

An authorization for fact 4 is not an input to fact 3. Initial-wave authority for
fact 1 can never authorize fact 4.

## Initial-wave state classification

The closed active-state set is:

```text
AWAITING_SPEND_AUTHORIZATION
AUTHORIZED
SUBMITTING
```

Only those states may activate the initial-wave constrained routing fence.

The closed historical-state set currently produced by supported v1 routes is:

```text
DETACHED
FAILED
```

Historical wave evidence remains immutable lineage and must remain joinable for
audit/replay safety. Its presence cannot activate initial-wave preparation,
authorization, submission, or result publication.

An unknown wave state fails closed as unsupported/contradictory evidence. Runtime
must not treat a negative check such as “not detached” as proof of active admission.

## Precedence

For one native checkpoint, SBE applies this precedence:

1. provider ambiguity or contradictory provider/native identity → review;
2. durable provider custody pending or due → retrieval-only reconciliation;
3. retrieved completion awaiting native application → concrete local operation;
4. other concrete local work that determines the next paid inventory → local
   operation;
5. prepared ordinary paid action → v2 external-authority request;
6. active initial-wave admission → v1 constrained initial-wave boundary where the
   initial wave is in fact the current work;
7. terminal/delivery/no-work → corresponding typed non-local disposition.

The initial-wave check is additionally route-phase scoped: historical initial-wave
lineage does not compete with current provider, local, or ordinary-authority facts.

## Normative routing matrix

The machine-readable companion fixture is
`fixtures/post-fan-in-authority-routing-matrix.v1.json`.

| Fact | SBE command/result | Provider behavior | API consequence |
| --- | --- | --- | --- |
| Initial wave awaiting authority | v1 initial-wave request | no I/O before exact aggregate grant | API may evaluate only that aggregate request |
| Initial wave authorized/submitting | constrained continuation, reconciliation, ambiguity, or review according to provider facts | generic resume cannot create | retain exact admitted authority/custody |
| Provider identity pending, not due | reconciliation `not_due` | zero retrieval this cycle | release capacity until SBE time |
| Provider identity due | reconciliation cycle | retrieve only SBE-selected subset | retain provider custody |
| Retrieved retry completion | `ordinary_resume` with one fan-in operation | zero provider I/O | no new authority |
| Fan-in consumed; next retry prepared | `await_external_authority` with exact ordinary v2 request | zero provider I/O | API may evaluate a fresh ordinary v2 grant |
| Ordinary intent/call entered | constrained v2 dispatch, reconciliation, ambiguity, or review | generic resume cannot create | retain corresponding admitted authority/custody |
| Completed initial-wave lineage only | route from current ordinary/provider/local facts | never reactivate v1 | historical authority has no current effect |
| No executable work | typed non-local disposition | zero provider I/O | do not retain capacity as local continuation |

## Consuming ordinary-resume rule

If lifecycle v0.7 selects `ordinary_resume` with a nonempty local-work inventory,
the supported invocation must do exactly one of the following:

- durably consume at least one advertised semantic `operation_key`, append it to
  cumulative consumed history, and publish a changed checkpoint basis; or
- return a typed non-local refusal/review/terminal disposition.

It must not publish unchanged semantic meaning as successful local progress.
Snapshot or revision churn alone is not consumption.

## Route and mechanism applicability

- **Exact interactive:** runtime correction required. Historical `DETACHED` lineage
  currently reactivates initial-wave routing and is the incident defect.
- **Bounded interactive:** parity/non-regression required. Its existing generic
  fence already names the three active states and must not be weakened.
- **Exact Batch:** existing initial Batch and provider reconciliation remain
  supported. New ordinary v2 Batch dispatch remains deliberately deferred.
- **Bounded Batch:** existing initial Batch and provider reconciliation remain
  supported. New ordinary v2 Batch dispatch remains deliberately deferred.

Batch deferral is a provider-creation limitation, not permission to ignore retained
Batch provider custody or completed local fan-in.

## Refusal precedence

When multiple facts conflict, the most safety-relevant durable evidence wins:

1. provider identity conflict / ambiguous call entry;
2. provider custody or consumption evidence;
3. binding/run/route mismatch;
4. stale checkpoint or request;
5. wrong authority family/version;
6. unsupported route/mechanism;
7. no executable local work.

Refusal is nonmutating unless a separately supported repair protocol explicitly
declares its write set. No refusal may publish a misleading successful local-cycle
result.

## Public contract conclusion

Lifecycle v0.7 already exposes the local operation, provider custody, ordinary v2
authority state, checkpoint basis, and consuming operation identity required here.
No new public command identity or field is needed. API continues to invoke only
SBE-selected run-level commands and never infers phase from private `run.json`.

## Recovery posture

This contract does not authorize recovery of Strudel, Princess, or any retained QA
workspace. Recovery requires a released installed-wheel candidate, joint
qualification, and a separate explicit owner/API decision.

