# Operator trace playbook

## Fast path

Filter the worker stream for `✨🐶`, then correlate one invocation by `run_id`
and, where present, `action_id`.

Read the lines in this order:

1. `workspace_fingerprint` — which validated checkpoint/native revision entered.
2. `native_state_summary` — action, custody, and dispatch-intent posture.
3. existing provider/fence events — whether create/retrieve was entered and the
   returned provider identity/status.
4. `native_decision_summary` — which validated public branch/result won.
5. `command_exit` — exact typed outcome, exit code, and authoritative output.

## Common interpretations

- `provider_reconciliation_cycle`: provider custody exists; creation is not
  implied. Check the SBE-selected due subset and retrieval lines.
- `await_external_authority`: SBE is quiescent and exposes a request; API still
  owns admission/reservation decisions.
- `retain_for_review` / `review_required`: inspect the named result and receipt;
  do not infer API terminalization from the word “review.”
- `pre_provider_refusal` / `ambiguous_submission`: distinguish
  `not_attempted` from `create_entered_unknown`; never retry ambiguity.
- `continue_local_cycle`: local work was selected. Its successor checkpoint must
  consume the advertised semantic operation rather than merely change revision.

## Escalation ladder

1. Trace logs for operational explanation.
2. Exact public artifact/result/receipt named by the trace.
3. Snapshot-valid public reader/qualification command.
4. Read-only checkpoint inspector/R2 restore only when the preceding evidence
   is missing or contradictory.

Logs are never transition authority and must not be parsed as a substitute for
the public JSON contracts.
