# API review — final 0.4.31 release gate

**Decision: approved for commit, tag, publication, and post-publication wheel
verification.**

## Reviewed surface

- additive `astrowoof.native_transition_result_availability.v1` schema, strict
  reader/validator, root exports, contract-catalog entry, and
  `astrowoof-native-transition-availability` CLI;
- result-index, publication-inventory, sealed-exact-reader, snapshot-identity,
  and canonical-digest joins;
- the 0.4.31 version and corrected terminal-review qualification receipt; and
- Slice 7's release-shaped wheel/install evidence.

The public surface remains discovery-only: `none_available` is explicit, malformed
or unjoinable evidence is typed failure rather than absence, and `available`
supplies one exact result ID which the API must still read through the existing
strict reader. It grants no transition, recovery, provider, or spend authority.

## Independent API check

The API review independently ran the focused availability module with the source
package and test helper paths configured:

```text
Ran 5 tests in 0.330s
OK (skipped=1 optional JSON Schema dependency)
```

`git diff --check` is clean apart from informational Windows line-ending notices.

## Full-suite record

The candidate's once-run full suite is **not** represented as wholly green. Its
single failure was the deterministic release-identity mismatch in the packaged
terminal-review fixture after the candidate was advanced from 0.4.30 to 0.4.31.
The narrowly corrected fixture/digest is covered by the reported focused gate and
the final installed-wheel terminal-review qualification. That is proportionate for
this fixture-only correction and is accurately retained in the release review.

## Consumer follow-through

API Sprint 58 can consume this release to add terminal-result availability
preflight and pass only the returned exact ID into strict terminal ingress. The
API must not reconstruct, select a dashboard-visible result, or treat availability
as mutation authority.
