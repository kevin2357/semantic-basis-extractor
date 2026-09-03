# Pre-Sprint Huddle — Waffle/Scone Post-Provider Finalization Boundary

## Initial read

The new `✨🐶` trace made Waffle substantially less ambiguous than earlier QA
incidents. The initial read identified one concrete defect and one ordering
question:

1. Pass 6 was accepted with `theme_group_balance` recorded as an advisory,
   but final assembly independently enforced the former hard two-claim/2:1 balance
   boundary and raised `ValueError`.
2. SBE emitted `lifecycle.local_work_consumed` before `finalize_subjects` began;
   Slice 0 needed to identify which operation that event represented.

The first concern is a concrete `0.4.39` policy-integration gap. The theme-group
policy was softened at pass acceptance and final validation, but the equivalent
assembly guard remained hard. Slice 0 disproved the broader premature-
consumption hypothesis: the consumed operation was completed-provider fan-in
and adoption, whose durable action/pass transition occurred before assembly.
Final assembly was the next phase in the same invocation, not the consumed
operation.

## Waffle evidence already visible in the trace

- All eight provider-backed authoring actions were `REPORTED`; provider custody
  was zero.
- Pass 6 attempt 3 returned acceptance exit 0 and emitted
  `pass_acceptance_advisory codes=theme_group_balance`.
- The run advanced to `AUTHORING_COMPLETE` and retired its v2 intent.
- Lifecycle selected one ordinary local continuation.
- `lifecycle.local_work_consumed` was emitted before `finalization_start`; the
  production characterization identifies it as the preceding fan-in/adoption
  operation.
- `assembly.py` rejected the interdogpendence distribution
  `{4, 3, 2, 6, 4}` under its two-claim/2:1 boundary.
- No sealed typed SBE result explained that deterministic failure; API saw
  `CalledProcessError`, mapped it to retryable `sbe.dependency.command_failed`,
  and re-entered the same boundary.

## Scone is a comparator, not a shared-cause assumption

Scone's visible trace has a live polish provider identity/custody and a sealed
native v0.2 `review_required` result. That makes it useful for comparing typed
native closeout and retained custody, but it does not presently support the
same assembly-failure cause as Waffle. Any Scone claim must remain independently
joined to its own checkpoint/result evidence.

## Working invariants

- Advisory-only theme-group distribution findings must remain advisory through
  assembly, final validation, and delivery. No later native layer may silently
  restore their former rejection authority.
- Structural failures remain hard: malformed registries, duplicate/invalid
  registry identity, unknown assignments, and invalid field structure are not
  downgraded.
- A local-work operation is consumed only after the operation's durable semantic
  effect is established, or the command publishes a different closed typed
  disposition which makes replay semantics explicit.
- Deterministic local failure must not escape solely as an untyped subprocess
  exit that invites indefinite API retry.
- Logs explain the sequence; snapshot-valid native documents remain authority.

## Protected checkpoint posture

The trace is sufficient to justify provider-free source characterization. The
current background identifies the checkpoint and hashes but does not provide a
complete exact R2 object key. Request a narrow coordinate packet only if the
reproduction cannot prove the consumed-key/checkpoint relationship. Any later
access remains exact HEAD/GET only, read-only, and separately recorded.

## Recommended first review gate

Owner review of this plan is sufficient to begin Slice 0. Cross-repository
review becomes valuable after Slice 0 proves the production-path behavior and
before Slice 2 freezes whether a failing local operation yields retryable,
review-required, or another typed result. No API review is needed merely to
characterize the native defect.
