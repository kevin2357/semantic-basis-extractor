# Slice 5: Public Interfaces and Consumer Handoff

Status: implementation complete; pending Kevin's Slice 5 gate review.

## Installed interfaces

The supported installed CLI now exposes bounded reconciliation through:

```text
astrowoof-semantic-closure --run-dir RUN --resume --provider openai \
  --service-level interactive --bounded-provider-reconciliation
```

The supported Python operation is:

```text
astrowoof_natal_authoring.reconciliation.run_bounded_authoring_reconciliation
```

The CLI accepts the existing model/routing/polish/critic configuration so the API
can replay the frozen launch profile. It rejects new-run, fake-provider, Batch,
and simultaneous spend-authorization/reconciliation combinations before native
work begins. Runtime route and request binding remain the final fail-closed check.

## Typed result and events

Every operation returns
`astrowoof.provider_reconciliation_cycle_result.v0.1`. The strict applied result
now explicitly admits bounded `local_continuation` evidence: pass IDs, exact closed
stage vocabulary, completed action IDs, and proof that newly available local work
was exhausted before detach.

Python and CLI use the existing non-authoritative redacted events. A checkpointed
cycle emits ordered `run.detached` and `checkpoint.committed` observations. An
early nonmutating `not_due` result has no new checkpoint and emits no false
checkpoint observation. Event sink failure remains isolated from native execution.

## Consumer mapping

The updated handoff documents:

- local capacity versus provider custody and API-owned financial authority;
- the durable lower-bound meaning of `resume_not_before`;
- exact handling for every closed cycle outcome;
- four-action/one-wave, 15-second GET, and 20-second cycle bounds;
- zero-submission semantics for known provider IDs;
- original frozen configuration retention;
- Batch and bounded-Natal fail-closed behavior;
- publishable delivery with nonblocking critic/candidate custody; and
- API-persisted HTTP status authority rather than live workspace or events.

The lifecycle installed smoke now explicitly loads the catalog, inspection v0.2,
reconciliation policy, and `not_due` fixture from package resources.

## Gate evidence

Focused consumer/contract/event qualification passed all 53 tests in 5.344
seconds. The complete repository suite passed all 338 tests in 158.531 seconds.

Provider operations: 0. Paid spend: `$0`. API key used: no. Runtime release remains
0.4.2; no wheel, version bump, tag, or publication occurred.
