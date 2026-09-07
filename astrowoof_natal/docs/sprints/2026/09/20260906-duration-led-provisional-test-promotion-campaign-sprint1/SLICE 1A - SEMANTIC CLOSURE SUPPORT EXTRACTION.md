# Slice 1A — semantic-closure support extraction

## Result

The approved support-only phase is complete. Shared fixture material now lives
in the non-discovered test-only module
`astrowoof_natal/tests/_semantic_closure_support.py`. The original
`test_semantic_closure.py` remains a single serial-only module with the same
class and all 98 test methods in place.

No behavioral family moved, no test identity changed, no manifest
classification changed, and no production code or patch target changed.

## Extracted support

- process-local `SemanticClosureFixture` and its compiled packet setup;
- deterministic authored-field and completed-response builders; and
- the scripted interactive transport shared by external-authority fixtures.

The support module has no `test_` prefix and therefore is not discovered by
the manifest's closed `test_*.py` inventory. It uses no persisted or
cross-process cache. Every importing worker compiles one process-local packet
template, and every test receives its own deep copy; mutable fixture state is
never shared between tests.

Fourteen modules—including the original semantic-closure module—now import the
support directly. The dormant-theme fixture was tightened further: it imports
production `build_story_workspace` and `fill_fake_workspace` from their actual
production modules rather than relying on re-exports through a test module.

## Frozen pre-extraction identity

The checked-in
`SEMANTIC CLOSURE PRE-SPLIT IDENTITY INVENTORY.json` freezes:

- source checkpoint: `e6b38f3`;
- 98 exact discovered IDs;
- successful outcome with no failures, errors, skips, expected failures, or
  unexpected successes;
- identity SHA-256:
  `09e21da6a7941622e1af6388e8ae36973099d2568d82e40d9e602f650c797ed8`;
- outcome SHA-256:
  `36f64afd5edbd4ee1c69a2bf3a2e71500a8cdb445a4ef3a8ff65a86033e60c97`.

## Post-extraction serial equivalence

The supported sanitized runner executed `test_semantic_closure.py` alone:

- 98 tests;
- success;
- no failure/error/skip outcome;
- exact same ordered identity inventory;
- exact same identity and outcome SHA-256 values;
- final wall time after per-test packet isolation: 206.186 seconds.

This duration is not treated as a performance improvement claim. It is one
serial equivalence sample on a resource-variable laptop.

## Direct-consumer verification

The thirteen other direct consumers were run together through the supported
child harness. The first deliberately quiet probe passed 69 of 70 tests and
failed only the known logging-sensitive assertion in
`test_external_authority_execution.py`; quiet mode suppresses the root INFO
record that test exists to prove. This is a harness-posture negative control,
not a support-extraction regression. The affected module was then rerun in its
manifest-declared unquiet posture.

The final supported-posture pair passed all consumers: 59/59 quiet tests in
292.218 seconds and 11/11 unquiet tests in 50.319 seconds. They ran in separate
worker processes concurrently, providing an additional process-isolation
witness without promoting either group or making a performance claim.

## Permanent guard

`test_test_suite_runner.py` now proves:

- `_semantic_closure_support.py` exists;
- it is excluded from `test_*.py` discovery; and
- no test module other than the semantic-closure owner imports shared helpers
  from `test_semantic_closure.py`.

## Pause boundary

Stop here. The next semantic-closure phase would move cohesive behavioral
families and therefore rename test identities. That requires the explicit
semantic-closure move paws-point. Slice 2's unrelated two-module collision
qualification also remains unstarted.
