# API Slice 2 review — exact interactive publication before exit

Date: 2026-08-28
Status: approved for Slice 3; exact interactive only.

## Assessment

This closes the SBE half of the previously proven live-route publication gap.
The implementation now puts the required ordering on the exact-interactive
authoring paths:

1. fresh lifecycle truth establishes review retention;
2. the journal transition and v0.2 result carry the same review outcome/cause;
3. result, snapshot, and canonical v0.1 receipt are sealed and validated;
4. the exact invocation/result/receipt command-result envelope is emitted; and
5. only then is exit 2 exposed.

That is the right public handoff for API's future ordinary-resume ingestion. The
result identity is invocation-bound, so API need not—and must not—guess from a
historical latest-result index.

The corrected whole-second lifecycle observation and aligned journal cause are
both important: without them the new result could be internally valid but fail a
strict API causal join.

## Scope approval

Approve this Slice 2 exact-interactive implementation and its public command
result. Do not extend the runtime change to exact Batch or bounded routes under
this sprint slice; their stated matrix posture remains correct.

## Required Slice 3 qualification addition

Add one real public-command exact-interactive test that emits—not merely
constructs in a contract unit test—a v0.2 review result with all three custody
classes at once:

- one reported action;
- one `WAITING`/`PROVIDER_ID_RECORDED` action with a durable provider identity;
  and
- one `AUTHORIZED` action without provider identity.

Assert `custody_finality=mixed_resolution_required`, exact ordered
`reconciliation_action_ids` and `providerless_denial_action_ids`, false new
provider-create permission, receipt/command-result joins, and exit 2 after the
envelope. The existing contract-unit mixed fixture is useful, but the incident
requires this production-shaped command boundary witness before API consumes it.

Then exercise only the advertised custody-only operations: provider retrieval
and exact providerless denial. Prove neither path can re-enter authoring or
create a provider request.

No provider work, retained-QA recovery, deployment, or release is authorized by
this review.
