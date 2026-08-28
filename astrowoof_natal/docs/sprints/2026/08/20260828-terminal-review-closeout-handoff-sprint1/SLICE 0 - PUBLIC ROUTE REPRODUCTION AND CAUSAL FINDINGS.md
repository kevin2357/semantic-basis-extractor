# Slice 0 — Public Route Reproduction and Causal Findings

## Status

Complete; paused for owner/API review before Slice 1 contract freeze.

No provider/network request, paid work, retained-QA workspace access, deployment,
or release action occurred.

## Executive finding

The broad incident hypothesis needs qualification.

Against current SBE `main`, the public exact-Natal ordinary-resume command **does**
publish and validate a sealed `review_required` native execution result before
returning exit code 2. It also does so when the run begins with an earlier sealed
`provider_pending` result and reaches review during a mixed-custody local fan-in.

Therefore Slice 0 did not reproduce a generic SBE publication-order failure. The
retained API evidence alone does not prove that the SBE workspace lacked a result;
it proves that the API did not ingest one. The retained Pippin/Duchess workspaces
were intentionally not opened, so this document makes no claim about whether their
native result namespace contains an unconsumed review result.

Two real integration gaps are proven:

1. The API ordinary-resume path does not perform terminal-result ingestion after
   native resume. A later lifecycle `retain_for_review` observation is deliberately
   mapped to the API's nonterminal review path, which explicitly bypasses native
   terminal ingress.
2. SBE native execution result v0.1 is too coarse for the requested mixed-custody
   closeout. It lists all `action_ids` and separately copies provider objects, but
   those provider projections do not strictly join to action IDs and the result
   does not project exact providerless-authorized versus reported disposition for
   every ordered action.

The companion work remains justified, but its purpose is now precise: publish a
strict mixed-custody terminal projection and give the API one reliable terminal-
first ingestion boundary. It is not a blanket repair to the visible exit-2 ordering.

## Provider-free public-command characterization

The Slice 0 test enters through `closure.main()` with the same public
`--run-dir ... --resume` command boundary used by the worker.

### Case A — already review-required

- Workspace begins in `FAILED_REQUIRES_REVIEW`.
- The public command publishes an immutable result and receipt.
- The result outcome is `review_required` with cause
  `final_qa_requires_review`.
- `native.result_published` precedes the command-result envelope.
- The command then exits 2.

### Case B — prior provider-pending result, then mixed-custody review

- The initial checkpoint contains a completed durable provider action and a
  prepared successor and selects v0.7 `ordinary_resume`.
- A first sealed native result records `provider_pending`.
- Provider-free local fan-in changes the completed action to `REPORTED`, leaves a
  later action `AUTHORIZED` without provider identity, and makes a pass
  `FAILED_REQUIRES_REVIEW`.
- The spend-boundary unwind consumes the advertised local-work operation.
- SBE publishes a second immutable result with outcome `review_required`.
- The result index contains exactly the prior provider-pending result followed by
  the review result.
- No provider create or retrieval function is available to the test.

This disproves the simple hypothesis that review reached during local fan-in always
escapes before `publish_native_execution_result()`.

## API production-path finding

Read-only inspection of the API source found this sequence:

1. A validated v0.7 `ordinary_resume` enters
   `DurableSbeProviderCycleService.advance()`.
2. The service invokes the SBE resume process, reconciles API paid-action rows,
   calls lifecycle closeout, and returns `ProviderProgress`.
3. Unlike the external-authority v2 path, it does not read and ingest the latest
   sealed native transition immediately after native execution.
4. On a later inspection, SBE v0.7 reports `retain_for_review` / command `none`.
5. `_inspection_cycle_result()` maps this to API `REVIEW_REQUIRED`.
6. The worker's review branch explicitly describes that evidence as nonterminal,
   fails the API execution job, releases local capacity, and deliberately does not
   invoke terminal ingress.

That implementation exactly explains why PostgreSQL can retain the earlier
`provider_pending` receipt even when the native command has published a successor.
It also explains why a bare API `native.review.requires_review` record is not proof
of a missing SBE result.

The absence of forwarded `native.result_published` trace events is useful but not
authoritative; it may indicate event-forwarding or subprocess-capture behavior and
cannot override an unread native workspace.

## SBE v0.1 evidence limitation

`astrowoof.native_execution_result.v0.1` currently exposes:

- one ordered-ish `action_ids` list copied from the ledger; and
- a separate `provider_operations` list copied only from actions that carry a
  provider object.

It does not provide one closed per-action projection joining:

- action ID and binding;
- native action state;
- provider identity/custody class;
- consumption/reporting status;
- providerless-denial applicability; and
- terminal accounting/closure disposition.

Consequently the API cannot use v0.1 alone to prove which retained reservation is
submitted versus never submitted without reconstructing private state. Slice 1
must version and close this public boundary.

## Applicability assessment

| Route | Slice 0 finding |
| --- | --- |
| Exact interactive | Public review publication ordering works; mixed-custody result projection is insufficient |
| Exact Batch | Existing common publication helper applies, but production-path terminal/mixed-member parity remains unproven |
| Bounded interactive | CLI also calls the common publisher before its nonzero non-delivery exit; production-shaped mixed-custody parity remains unproven |
| Bounded Batch | No release claim; characterize after the contract is frozen |

Only exact interactive is release-blocking for this incident.

## Tests

Focused command and adjacent native-transition/local-work gate:

- 29 tests passed in 7.580 seconds.
- External provider/network calls: 0.
- Provider creates: 0.
- Provider retrievals: 0.
- Spend: USD 0.
- Retained-QA access/mutation: 0.

## Questions for API review

1. Does API agree that the missing PostgreSQL receipt must be distinguished from
   an absent native-workspace receipt until the retained workspace is separately
   authorized for inspection?
2. Should the companion API change ingest the latest validated sealed result
   immediately after every ordinary resume, before interpreting closeout/process
   disposition?
3. Does API agree that a fresh closed SBE result version containing a per-action
   mixed-custody projection is the appropriate contract, rather than reconstructing
   it from private `run.json` or API action state alone?
4. Should `review_required` be terminal for editorial execution while carrying a
   separately explicit provider-reconciliation continuation inventory?

## Gate disposition

Slice 0 is complete. Pause for the first planned voof-paws before Slice 1.
