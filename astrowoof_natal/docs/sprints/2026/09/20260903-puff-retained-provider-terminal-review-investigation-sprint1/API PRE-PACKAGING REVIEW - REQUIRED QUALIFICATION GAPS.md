# API pre-packaging review — required qualification gaps

## Status

The implementation shape is aligned with the approved invariant, but packaging
is **not yet approved**. Two focused regressions need to be strengthened first.

## 1. Critic and candidate need positive adoption tests

`test_optional_stage_completed_evidence_adoption_slice2.py` currently proves
that critic and candidate can reach their respective spend callbacks before
adoption by supplying a controller with an empty state. That is valuable route
characterization, but it does not execute the newly added helper for either
stage and does not prove their stage-specific stored attempt records can adopt
the exact completed artifact.

Because the runtime change calls
`prepare_completed_optional_stage_for_adoption()` for both stages, add one
provider-free positive adoption regression for each—or remove that route from
this release’s runtime scope. Each positive test must use a real ordinary-v2
intent/action/reconciliation artifact and assert:

- the correct stage-local marker/attempt is joined;
- the provider transport is forbidden and receives zero calls;
- the other optional-stage attempt is not modified; and
- the stage-specific lineage (especially candidate’s critic predecessor) is
  preserved through its normal deterministic consumer result.

The existing mismatch-refusal test is a good control, but it is polish-only.

## 2. The dormant theme-group test needs a real non-theme control

`test_non_theme_hard_gate_remains_active` currently asserts values in an
in-memory report; it never executes `pass_acceptance.main()` or a production
acceptance path. It therefore cannot prove that the new dormant branch leaves a
non-theme hard gate effective.

Replace or supplement it with a workspace fixture that exercises the actual
acceptance command with a known non-theme hard failure (for example the
existing invalid-context-filter route), while patching
`theme_group_plan_issues` to raise if invoked. Assert nonzero exit, `reject`,
and the expected non-theme hard code. Keep the existing acceptance test proving
theme metadata cannot itself cause rejection.

## Approved portions

The narrow ordinary-v2 boundary, exact binding checks, no-intent non-broadening,
and exclusion of Batch/bounded remain approved. Once the two regressions above
pass, return for a brief packaging re-review with the focused results and
explicit zero provider/R2/spend counts.
