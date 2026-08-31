# Slice 6 — SBE 0.4.35 release candidate

## Candidate identity

- Version: `0.4.35`
- Wheel: `astrowoof_natal_authoring-0.4.35-py3-none-any.whl`
- Wheel SHA-256:
  `830a4cd9288628c399a79f9d255edbb49caa5ab608046af6f12cfec8bbe34cfb`
- Reproducibility: two controlled builds were byte-identical.
- Dependency identity: `semantic-projection-core==0.11.1`.

## Verification

The broad suite ran once against the already-frozen 0.4.35 source:

```text
Ran 945 tests in 1053.606s
FAILED (failures=3, skipped=49)
```

The three failures were not runtime exceptions or unrelated regressions. Two
were historical characterization assertions that still expected a separate
prepared action to outrank completed provider evidence. The third demonstrated
that generic checkpoint persistence needed the same sealed-review predecessor
continuity already enforced in the reconciliation wrapper.

After those narrow corrections, the directly affected five-module matrix ran:

```text
Ran 31 tests in 49.539s
OK
```

The full suite was not repeated. This is an explicit risk-proportionate release
decision for review, not a claim that the final source produced a green 945-test
run.

Final installed-wheel gates:

- `pip check`: pass;
- generic `astrowoof-release-smoke --require-installed`: pass;
- `astrowoof-terminal-review-qa`: pass;
- `astrowoof-final-qa-mixed-custody-qa`, twice: pass and identical;
- qualification receipt SHA-256:
  `a9123f0d8f09d66083209db2573f99937f63c95917ef11e989fcb2d1f6e59599`;
- installed Draft 2020-12 schema validation: pass; and
- installed Python semantic validation: pass.

## Safety statement

All release qualification was provider-free. It performed no external network
call, real provider create/retrieval, spend, R2 access, or retained Glimmer
workspace access/mutation.

## Release gate

Source is uncommitted and no tag or publication exists. Commit, tag, and publish
only after explicit API and owner approval.
