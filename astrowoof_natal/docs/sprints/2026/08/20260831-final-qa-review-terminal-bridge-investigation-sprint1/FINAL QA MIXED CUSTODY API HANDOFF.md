# Final-QA mixed-custody API handoff

## Consumer rule

API should continue consuming SBE's exact public result and lifecycle fields;
it must not infer terminality from the outer final-QA status alone.

- Durable provider custody means reconciliation-only, even when a separate
  action is prepared or budget-blocked.
- `astrowoof.external_authority_v2_command_result.v3` with dispatch-result v4
  and reason `post_intent_lifecycle_contradiction` is a typed pre-provider
  refusal. `provider_io_disposition = not_attempted` proves no provider create
  crossed the fence.
- The refused grant invocation remains immutable and cannot be reused. Any
  later action requires a fresh SBE inspection/request and fresh API decision.
- A sealed native terminal-review v0.2 result remains the editorial authority.
  Later retrieval/denial successors settle its custody; they do not reopen the
  editorial run or replace the immutable predecessor.

## Version compatibility

The existing successful ordinary-v2 command-result v2 remains unchanged. API
needs v3 support only for the new typed post-intent refusal. Lifecycle schemas
are unchanged because they already express the corrected nonterminal custody
truth.

The packaged qualification command is not execution authority and should never
be invoked with a retained or production workspace. API may run it against an
installed wheel as a deployment gate and validate the returned closed receipt.
