# Slice 0 — source and trace identity map

## Decision

The trace does **not** show one immutable v2 authority request changing identity.
It shows three different public document identities under labels that all contain
the word `request`:

| Digest | Producer and contract | Meaning | Slice 0 conclusion |
|---|---|---|---|
| `a838af88442a…` | `read_external_authority_request()` / v1 | Standalone v1 request over the current action binding and its own observation | Stable on every revision-75 read from 01:52:27 through 02:01:18 |
| `c5ac689b83f…` | `inspect_lifecycle()` / lifecycle v0.5 embedded v1 request | A separately rebuilt v1 request using the lifecycle inspection observation | One of several lawful time-bearing v0.5 identities; not the v2 dispatch request |
| `07300bd27a5…` | `build_external_authority_request_v2()` and the v2 dispatch command | Basis/inventory-bound v2 request supplied by API | Stable across every constrained-dispatch attempt |
| `bb3aea3813f…` | API v2 grant / `grant_sha256` | Exact aggregate grant for `07300bd…` | Stable; not a request digest |
| `d307b779e27…` | temporal lifecycle v0.6 / `checkpoint_basis_sha256` | Immutable checkpoint-basis identity | Stable; not a request digest |
| `20c0572af49…` | paid-action binding / binding digest | Immutable polish action binding identity | Stable; not a request digest |

The lifecycle-v0.5 request includes an observation containing `observed_at`.
`inspect_lifecycle()` reads the current actions and rebuilds that request with
the current lifecycle observation. Its digest therefore changes when only the
observation time changes. The v2 request intentionally excludes observation
time and binds the immutable checkpoint basis plus ordered inventory; focused
tests confirm it is byte-identical across later observation time.

## Trace-backed sequence

The corrected full log export is 845,872 bytes and 1,200 lines, with SHA-256
`61813d879183d4637553f96875df6459335b2b24a21bd7098ee33df10808e087`.
It is non-authoritative diagnostic evidence and is not copied into this sprint.

1. Revision 74 produces v1 request `bc7678…` and lifecycle-v0.5 embedded request
   `758a17…`.
2. Revision 75 produces standalone v1 request `a838af…` and lifecycle-v0.5
   embedded request `abcad4…`.
3. The ordinary resume then reaches polish preparation, but checkpoint closeout
   fails in `commit_local_work_progress()` with
   `Local-work consumption history is not append-only`.
4. The first constrained v2 invocation rereads the same standalone v1 request
   `a838af…`, creates a new time-bearing lifecycle-v0.5 identity `c5ac68…`, and
   selects the supplied v2 request `07300bd…` with grant `bb3aea…`.
5. Writer-fenced v2 intent revalidation refuses because the native action state
   or custody is not dispatchable. The CLI deliberately defers that error so an
   already-committed matching intent may be replayed/recovered.
6. Dispatch then reads native intent and refuses because its persisted
   request/grant identity does not match the supplied pair.
7. The same sequence repeats at roughly one-minute intervals: `a838af…`, a new
   time-bearing lifecycle-v0.5 digest, stable `07300bd…`/`bb3aea…`, then the same
   two refusal reasons. No provider create is reached.

## Source producers

- `external_authority.py::build_external_authority_request()` hashes the entire
  closed v1 request, including its observation.
- `external_authority.py::read_external_authority_request()` logs that v1 digest
  as `external_authority_request_read_complete ... request=`.
- `lifecycle.py::inspect_lifecycle()` rebuilds a v1 request using its current
  observation and logs the embedded digest as `request_sha256=`.
- `temporal_lifecycle.py::build_external_authority_request_v2()` binds the
  checkpoint-basis digest, request kind, and ordered action IDs; it omits
  observation time.
- `external_authority_v2_execution.py::commit_external_authority_v2_dispatch_intent()`
  emits `external_authority.request_selected` for the supplied v2 request only
  after current-inspection and grant validation under the writer.
- `cli/external_authority_v2.py` treats
  `action_state_or_custody_mismatch` as potentially recoverable through an
  already durable intent, then calls dispatch. Dispatch separately emits
  `authorization_mismatch` when that intent belongs to another request/grant.

The shared event name `external_authority.request_selected` is used at more than
one authority phase elsewhere in SBE. Consumers must use the selected command
and contract version, not the event name alone, to interpret its digest.

## Three propositions from the API review

1. **One immutable request mutated:** the trace shows the same `07300bd…` v2
   digest on every observed constrained invocation, and source makes that
   identity basis/inventory-bound. The retained canonical object remains the
   authority; the trace alone does not prove global immutability of every
   historical v2 object.
2. **Multiple lawful observations produced multiple request objects:** proven
   for lifecycle-v0.5. Its embedded v1 digest changes with observation time.
3. **Logs used incomparable digest labels:** proven. Standalone v1, embedded v1,
   v2, grant, basis, and binding digests were adjacent in one flow.

This resolves the apparent identity drift, but it does **not** yet prove why the
native polish action was not providerless `PREPARED`, nor which older native
intent occupied the workspace. Those are retained-state questions.

## Concrete retained facts needed from generation 11

- Polish action `paid_c90cf4073c936d22e27e16ae`:
  state, provider identity, authorization, consumption, binding, and payload
  reference.
- The complete `external_authority_v2_dispatch_intent`, including state,
  request/grant digests, ordered inventory, active cursor, and provider-bound or
  ambiguous member inventories.
- Stored temporal/lifecycle documents or enough immutable state to reproduce
  them through existing validators.
- Append-only local-work consumption history and the prior/successor operation
  keys around revision 75.
- Journal/checkpoint evidence around creative-retry adoption, finalization,
  polish preparation, and the failed local-progress closeout.
- Any immutable command result, refusal, receipt, or dispatch history associated
  with the mismatching native intent.

Generation 10 is not yet justified: generation 11 can answer whether the polish
action and native v2 intent disagree. A predecessor differential should be
requested only if generation 11 cannot establish how that intent arose.

## Oauf-paws 1 request

Authorize the exact generation-11 access manifest in this sprint for:

- one `HEAD` of
  `v1/checkpoint/60c09a6f14264c2aa38e77e8662aaac1`; and
- one `GET` of that same object, contingent on the `HEAD` matching the frozen
  coordinates.

No listing, write, provider operation, worker resume, reconciliation, repair, or
retained-run mutation is requested.

## Inspector-tooling delta

The future general offline inspector should expose contract-qualified digest
names rather than a generic `request_sha256`: standalone v1 request, lifecycle-
embedded v1 request, temporal v2 request, checkpoint basis, binding, grant, and
native intent. It should also project v2 intent/action dispatchability and
append-only local-work history using existing validators, without exposing
payloads or treating reconstructed observations as persisted authority.
