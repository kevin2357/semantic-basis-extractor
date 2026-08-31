# Pre-sprint huddle — final-QA review terminal bridge

## Initial assessment

The supplied SBE log export changes one important premise in `Background.md`.
Glimmer's polish action was not merely authorized without provider work. The
trace proves the following ordered sequence:

1. final assembly produced `FINAL_QA_WARN` with three lint findings;
2. SBE prepared one polish action and published an ordinary-v2 authority
   request;
3. the API supplied a matching grant;
4. SBE authorized and consumed the polish action;
5. persistence changed the outer run status from
   `AWAITING_SPEND_AUTHORIZATION` to `FINAL_QA_REQUIRES_REVIEW`;
6. SBE then permitted and issued the provider POST;
7. response identity `resp_0adb…` was durably recorded; and
8. the following API lifecycle read rejected the workspace because the public
   temporal lifecycle was terminal.

The leading defect is therefore not simply “API attempted continuation after a
clean native terminal.” Current source shows that `persist_state()` always calls
`update_run_status()`. That reducer preserves or derives review status from the
subject's `FINAL_QA_WARN` state, but does not give an ordinary polish action in
`SUBMITTING`/provider custody precedence over that provisional editorial state.
The constrained v2 executor then continues into provider I/O even though its own
intent checkpoint now carries a terminal-looking outer status.

This is a seam between native status reduction, v2 dispatch, lifecycle
inspection, and terminal-result publication. Both SBE and API behavior must be
evaluated against the exact mixed-custody facts rather than against the word
`terminal` alone.

## Predicate Paws

Predicate Paws is useful comparison evidence, not proof of the Glimmer cause.
Its trace shows a creative retry reaching its maximum attempts, an immutable
`review_required` native result being published, and API closeout consuming that
result. That is a legitimate native editorial review outcome.

The comparison suggests the key distinction is not whether review terminals
exist—they do—but whether all provider custody and local publication work has
been resolved before a review terminal becomes externally authoritative.

## Safety posture

- No recovery, resume, reconciliation, denial, retirement, or provider work.
- No API reservation or lease mutation.
- Generation 18 may be inspected with the exact one-HEAD/one-GET budget if the
  protected-access gate is reviewed.
- Generation 17 is optional and requires a concrete differential question.
- The live polish response identity is custody evidence. This sprint will not
  retrieve it or select an outcome for it.
