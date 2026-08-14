# Slice 2 - Experimental Exact Axis-Aware Policy

## Result

SBE now offers the opt-in exact-Natal policy `axis_aware.v1` while preserving
`legacy_atomic.v1` as the CLI, closure-runner, API-profile, and installed-runtime
default.

The experimental generator recognizes complete ASC–DSC or MC–IC endpoint pairs
for a planet or point. One `axis_configuration` candidate represents the pair while
retaining both component candidate IDs, all canonical source relationship
references, all four-context evidence, aspect/orb details, and deterministic
transformation provenance.

Structural and represented edges remain visible in the candidate pool and
unselected-claim inventory. Their closed dispositions are:

- `structurally_inevitable`; and
- `represented_by_axis_configuration`.

An eligible candidate is forbidden from depending on a policy-excluded candidate,
preventing excluded angle edges from leaking back into the portfolio through
synthesis closure. Incomplete endpoint pairs do not generate an axis candidate and
leave their surviving atomic edge eligible.

## Bre comparison

The deterministic Bre experiment produced:

- 50 selected claims under both policies;
- six selected axis configurations;
- zero selected pure angle-frame relationships, down from six;
- twelve component relationships preserved as
  `represented_by_axis_configuration`;
- six frame relationships preserved as `structurally_inevitable`;
- 37 retained selected IDs and portfolio Jaccard `0.587302`;
- selected source-reference coverage of 64 versus 48 in the baseline;
- dependency totals of 75 versus 73; and
- twelve explicitly carried axis component relationships.

The canonical comparison-report SHA-256 is
`ad159290c997aa3f9d964eb7c2dff6c588d4fcad248092c5022bb084ced05de4`.
These figures are experimental evidence, not an API enablement recommendation.

## Consumer seam

Both extraction entry points accept:

```text
--exact-natal-policy axis_aware.v1
```

The closure runner freezes the selected identity into the authoring generation
profile and forwards it to extraction. Axis runs emit
`<subject>.policy-comparison.json`; legacy runs do not. Unknown policy identities
fail closed.

## Verification

- deterministic axis inventory, stable IDs, full evidence, and dependency closure;
- structural-frame and represented-component dispositions;
- incomplete-axis negative fixture;
- baseline-versus-axis topology, coverage, drift, and closure report;
- explicit proof that omitted/default policy retains all Slice 0 identities;
- 13 focused policy/baseline tests passed; and
- all 228 repository tests passed in 127.692 seconds.
- freshly built offline-installed wheel lifecycle smoke: passed;
- freshly built offline-installed wheel complete default release smoke: passed;
- installed opt-in `axis_aware.v1` closure run with the fake provider: reached
  `DELIVERY_COMPLETE`, persisted the policy in the authoring profile, and emitted a
  six-configuration comparison artifact; and
- `git diff --check`: passed with only expected Windows line-ending notices.

## Gate status

Gate 2 is ready for review. The API default is unchanged, and no bounded-release
dependency is created by this experiment.
