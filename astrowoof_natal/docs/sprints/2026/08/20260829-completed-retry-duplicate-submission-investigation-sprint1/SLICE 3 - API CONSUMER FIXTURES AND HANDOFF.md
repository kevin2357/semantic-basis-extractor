# Slice 3 — API consumer fixtures and handoff

## Status

SBE implementation complete and provider-free focused tests passing. API fixture
review and consumer integration are required before installed-wheel/joint
qualification.

## Packaged public surface

SBE packages one closed bundle under
`astrowoof.duplicate_submission_fence_fixtures.v1` with a Python reader,
strict Python validator, JSON Schema reader, and immutable bundle digest. It has
two deliberately non-interchangeable cells.

### Generic provider-dispatch refusal

The `astrowoof.generic_provider_dispatch_refusal.v1` cell represents the
pre-provider generic-command fence:

- outcome `pre_provider_refusal`;
- reason `external_authority_v2_dispatch_required`;
- provider I/O `not_attempted`;
- `new_provider_create_permitted=false`; and
- next step `fresh_lifecycle_inspection`.

It is not a native execution publication, a grant, or a successful ordinary
resume. The API must capture this exact exit-0 stdout object, validate it, and
route to a fresh lifecycle inspection. If that inspection selects external
authority, API follows the existing constrained v2 request/grant/dispatch path.
It must not requeue generic resume merely because the process exited zero.

### Local-work progress contradiction

The second cell contains an exact three-way join:

1. `astrowoof.native_execution_result.v0.2` with cause
   `local_work_progress_contradiction`;
2. its canonical `astrowoof.native_publication_receipt.v0.1`; and
3. the invocation-bound `astrowoof.terminal_review_command_result.v0.1`
   exit-2 envelope.

The fixture includes a provider-bearing action whose custody is
`provider_reconciliation_only`. API must ingest the sealed result as
`review_required`, preserve its native cause, and retain provider/reservation
custody for the supported follow-up path. It must not flatten the invocation to
`sbe.dependency.command_failed`.

## Validation boundary

`validate_duplicate_submission_fence_fixtures()` validates the outer digest and
then invokes the strict public validators for every nested artifact and join. A
recomputed outer digest cannot conceal a changed refusal disposition, result
cause, receipt identity, or provider-custody row. The fixture contains no prompt,
provider request payload, subject content, credential, or retained-QA evidence.

## API integration gate

Before a live legacy-generic invocation can be enabled against the candidate:

1. API must add a strict capture/reader for the generic refusal schema.
2. Exit zero plus that schema must select fresh inspection, never generic success
   or an ordinary-resume retry.
3. API must prove a v0.8 external-authority selection reaches constrained v2
   dispatch without relying on the defensive fallback.
4. API must validate the terminal-review result/receipt/envelope join and retain
   the provider-bearing action custody.
5. Replay and malformed/recomputed-digest fixtures must fail closed without a
   second provider create.

SBE does not assert API lease, capacity, reservation, or queue facts. No retained
Marmalade recovery and no selection between its historical duplicate provider
responses is authorized by these fixtures.
