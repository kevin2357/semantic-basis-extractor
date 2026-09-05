# Operator trace playbook

## Fast path

Filter the worker stream for `✨🐶`, then correlate one invocation by `run_id`
and, where present, `action_id`.

Read the lines in this order:

1. `workspace_fingerprint` — which validated checkpoint/native revision entered.
2. `native_state_summary` — action, custody, and dispatch-intent posture.
3. `native_stage_evidence_summary` — which optional-stage attempt was durably
   classified, including accepted/improved state, bounded counts, report
   presence, and typed exception class/fingerprint.
4. `native_validation_evidence_summary` — exact report status/digests and
   closed warning/acceptance/rejection code counts, without finding prose.
5. existing provider/fence events — whether create/retrieve was entered and the
   returned provider identity/status.
6. `native_decision_summary` — which validated public branch/result won.
7. `native_publication_evidence_summary` — the explicit published outcome/cause,
   result/receipt/checkpoint identities, and bounded native evidence totals.
   Publication does not imply terminality.
8. `command_exit` — exact typed outcome, exit code, and authoritative output.

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
- `POLISH_ACCEPTED` followed by residual validation/lint codes means the stage
  ran and was classified; it is not a missing adoption or provider failure.
- `POLISH_ERROR`, `CRITIC_ERROR`, or `CANDIDATE_ERROR` with no report present
  identifies a stage exception before deterministic report production. Use its
  class/fingerprint for correlation; raw exception prose remains protected.
- A publication summary must be interpreted from its explicit `outcome` and
  `cause`, never from the existence of a receipt or the word `sealed`.

## When logs are sufficient

Logs normally suffice to classify optional-stage exhaustion/errors,
completed-evidence adoption posture, due/not-due provider custody, ambiguity,
pre-provider refusal, and published review with retained custody.

Use the named public result/receipt when making a transition or disposition.
Escalate to an exact checkpoint for field-level binding disputes,
snapshot/journal contradictions, interrupted-publication survival questions,
or historical runs produced before the evidence summaries existed.

## Escalation ladder

1. Trace logs for operational explanation.
2. Exact public artifact/result/receipt named by the trace.
3. Snapshot-valid public reader/qualification command.
4. Read-only checkpoint inspector/R2 restore only when the preceding evidence
   is missing or contradictory.

Logs are never transition authority and must not be parsed as a substitute for
the public JSON contracts.

## Provider-free installed qualification

```text
astrowoof-decision-evidence-observability-qa --output qualification.json
```

The closed receipt proves the three new trace units are packaged, parseable,
privacy-bounded, and preserve code distributions. It also records the eight-case
log-first matrix and the one intentionally artifact-bound case.
