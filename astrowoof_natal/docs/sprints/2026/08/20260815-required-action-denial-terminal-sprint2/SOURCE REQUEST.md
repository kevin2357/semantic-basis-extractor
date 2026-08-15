# API Handoff: Required-Action Providerless Denial Must Reach Native Terminal State

We found a lifecycle gap while recovering a retained API-authorized SBE run. This
is likely relevant to normal production runs once the API's global spend authority
denies a required action.

## Context

SBE correctly supports:

- exact providerless denial of one or more native actions;
- atomic batch denial for several actions;
- durable snapshots and replay;
- lifecycle inspection and closeout.

The API owns global/cross-run spend policy. It may deny a native action even though
SBE's frozen per-run spend policy would otherwise permit it—for example, a rolling
global ceiling, circuit breaker, account quota, or entitlement decision.

The API records that refusal and calls SBE's supported providerless-denial
operation. No provider request is created.

## Observed behavior

For retained run `a5270c02...`:

1. API atomically denied two previously authorized but providerless creative-retry
   actions with `denial_reason: external_authority_denied`.
2. SBE correctly persisted both as `DENIED_PROVIDERLESS`.
3. API released its matching providerless authority.
4. `closeout_run()` then returned:

```json
{
  "disposition": "continuation_required",
  "local_dependencies": [
    {
      "kind": "retry_preparation",
      "reason_code": "authoring_continuation",
      "blocking": true
    }
  ],
  "unresolved_action_ids": [],
  "terminal": {
    "terminal": false,
    "provider_continuation_remains": false,
    "local_continuation_remains": true
  }
}
```

Repeated normal resume calls remain in this same state. No provider dependency
exists, no new provider work is authorized, and the run never becomes
`BUDGET_EXHAUSTED` or another terminal policy outcome.

The same fundamental pattern appears applicable to a fresh run where the API
denies one newly prepared required action because the global spend reservation
cannot be acquired.

## Requested behavior

Please add a supported native lifecycle transition so that an externally denied
required action cannot leave the run indefinitely in
`retry_preparation / continuation_required`.

Recommended semantic rule:

A providerless denial of a required action—whether the action was newly prepared
or already authorized but has no provider/consumption evidence—must
deterministically transition the native run to an appropriate terminal
non-delivery outcome.

`BUDGET_EXHAUSTED` is probably the clearest current status when the denial is due
to external spend authority.

If you prefer a distinct native policy-stop status/reason, that is fine as long as
the public/lifecycle contracts map it unambiguously to a terminal non-delivery
outcome and the API can consume it.

Existing optional-stage behavior must remain distinct: an optional stage whose
policy says "skip" should still skip rather than terminate the run.

Preserve all existing provider-safety constraints: anything with provider
identity, consumption, reported cost, or ambiguity must still refuse providerless
denial / require review as appropriate.

## Consumer requirement

After the API applies a valid providerless denial and then follows the normal
supported resume/closeout sequence, it needs one deterministic result:

```text
terminal = true
provider_local_dependency_count = 0
local_continuation_required = false
status/outcome = budget exhaustion or explicit policy stop
```

At that point the API can safely mark its job/run/reading terminal and release
capacity. It must not infer terminal failure merely because SBE has no provider
dependencies.

## Why this matters

This is not just retained-run cleanup. The API now has global spend authority
above SBE's immutable per-run policy, so ordinary runs can encounter valid external
refusals. SBE needs a native terminal interpretation for that outcome; otherwise a
correctly denied spend request becomes an infinite deferred-worker loop.

## Requested outcome, as understood for planning

When external authority providerlessly denies an action that SBE itself marks
required, the native run must reach an explicit durable terminal state. Inspection
and closeout must not advertise provider or local continuation that cannot legally
occur. The result must remain machine-distinguishable, snapshot-safe, replayable,
and incapable of provider submission.

The final paragraph is a planning normalization of the handoff title and observed
gap; the preceding context, JSON, requested behavior, and consumer requirement
preserve the complete supplied report.
