# Slice 0 — snapshot-validated checkpoint findings

## Read boundary

The API coordinate packet authorized only two exact checkpoint reads. SBE made
exactly one HEAD and one ETag-conditional GET for each archive. Both matched
the packet's frozen size and archive SHA-256. Offline validation then confirmed
that every declared archive member had a safe relative path, a unique declared
path, the declared size, and the declared SHA-256; aggregate member counts and
bytes also matched. No provider request, workspace execution, mutation, repair,
or API mutation occurred.

The retained API result/receipt identifiers in the packet were database records,
not separately addressable R2 objects, and were not accessed.

## Froth — provider completed; later reconciliation was not invoked

Generation 7 is `WAITING_FOR_RESPONSE` at state revision 49. Its six initial
actions are internally coherent:

- five are `REPORTED`, with completed reconciliation evidence;
- `paid_116427eacd41d98baf90de18` is `WAITING` with one durable response
  identity;
- that action's last recorded reconciliation outcome is `pending`, with
  `resume_not_before` `2026-09-03T21:16:06Z`;
- no local follow-on work is represented at this checkpoint; and
- the newest indexed native result is the API-provided
  `nres_972e366a3cded01e935ec18f`, a `provider_pending` reconciliation result
  published at `2026-09-03T21:12:06Z`.

This agrees with the trace's release-until-due posture at that moment. The
trace establishes that the POST returned a durable queued identity at
`2026-09-03T21:02:13Z`, and SBE's final retrieval at `21:12:11Z` returned
`in_progress`; the clean reconciliation command then published the detached
pending result at `21:12:16Z`. Its next retrieval was due at `21:16:06Z`.

The owner subsequently confirmed in the OpenAI dashboard that the exact
response completed. The supplied SBE trace continues through the later worker
window but contains no later Froth invocation, retrieval, or publication.
Therefore SBE did not have an opportunity to ingest the completion: this is a
post-release scheduler/worker-dispatch gap to be traced on the API side, not a
duplicate-create or native reconciliation defect. SBE's relevant obligation was
limited to publishing the durable provider ID, due posture, and retrieval-only
result—which it did.

## Ganache — completed retrieval had no durable successor publication

Generation 6 is `WAITING_FOR_RESPONSE` at state revision 44. It contains five
`REPORTED` initial actions and exactly one pending action,
`paid_d5b51ca74b5892acba11fada`, with its durable response identity and a
recorded `pending` reconciliation outcome. Its last native result is the
API-provided `nres_f580f8b22732cb913c298b93`, a `provider_pending`
reconciliation result published at `2026-09-03T21:11:19Z`. Its native result
index contains no terminal-review result or any successor after that state.

The later trace records that same durable response as completed at 22:09:18Z,
adopts/accepts pass 3, and then raises the deterministic assembly-contract
error. No successor checkpoint or sealed terminal-review result appears in the
frozen active generation. This is the expected footprint if the reconciliation
path saved transient local state but raised before publishing a snapshot-valid
successor; the next retry restores generation 6 and repeats the same
retrieval/finalization attempt.

## Causal matrix and next gate

| Run | Snapshot-backed truth | Trace-backed later event | Classification |
| --- | --- | --- | --- |
| Froth | one durable pending response, sealed `provider_pending` result | provider later completed; no subsequent SBE invocation | API scheduling/worker-dispatch gap after valid release |
| Ganache | five reported plus one durable pending response; no terminal successor | response completed, pass accepted, deterministic assembly failure, no typed result | source-consistent reconciliation-to-terminal-review publication gap |

The Ganache classification is strong enough for Slice 1's contract/ownership
review, but not permission to change or recover either retained run. Slice 1
must decide the exact sealed review result and API disposition for a
deterministic finalization failure after all provider custody is resolved.
