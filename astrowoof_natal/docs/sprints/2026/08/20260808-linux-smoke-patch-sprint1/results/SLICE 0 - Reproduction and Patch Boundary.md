# Slice 0 - Reproduction and Patch Boundary

Status: complete; gate approval pending.

## Frozen baseline

- Sprint planning commit:
  `06b99773b05f0027d682bc106c1d84babac2c868`
- Published release: `astrowoof-natal-authoring 0.2.0`
- Annotated tag object:
  `8e441796d2aa33c5189f718e9e9fc199a7d9b396`
- Immutable peeled tag commit:
  `9c3ec9e59da7ad5ec87e0dc43cb9582913d6b7ac`
- Published wheel: 623,777 bytes, SHA-256
  `cbc8e82da546c1dd4a13a60544f31c5627365167c8c7c48f3114b5fd1f4c03e4`
- Proposed patch coordinates: version `0.2.1`, tag
  `astrowoof-natal-authoring-v0.2.1`

## Exact Linux failure

The retained installed run used fake/interactive authoring, contains zero spend
ledger actions, and stopped at `FINAL_QA_REQUIRES_REVIEW`. Its production lint
report rejected exactly one repeated-ngram group across three claims:

```text
insight a d e reveals one memorable behavior through an independent cadence
```

The three distinct source bodies begin with hexadecimal fake tokens
`a15d982e5900`, `a50063702d8e`, and `a835d46e7773`. Production
`editorial_lint.words()` retains alphabetic sequences and discards digits, so
all three tokens normalize to `a d e`. This is a deterministic fake-fixture
defect; changing or weakening the production linter would be incorrect.

## Platform ordering proof

`fill_fake_workspace` increments one ordinal across
`sorted(workspace.rglob("*.md"))` and includes it in fake identity material.
For the retained 27-file pass workspace, `PurePosixPath` and `PureWindowsPath`
sorting diverge at index 1: POSIX proceeds through uppercase root documents,
while Windows ordering proceeds into lowercase `cards/`. Consequently the same
logical field receives different ordinals and fake values by platform.

The correction should remove the tree-global ordinal, use stable POSIX logical
path/field identity plus a local occurrence only if necessary, and encode a
contiguous alphabetic digest token that survives the real tokenizer unchanged.

## Cleanup masking proof

`run_smoke` records an error when status is not `DELIVERY_COMPLETE`, but then
unconditionally calls `cleanup_completed_run`. Cleanup correctly refuses the
nonterminal state and raises `ValueError`, preventing the intended JSON failure
report from being returned and written.

The correction should gate delivery-dependent checks and cleanup on successful
delivery, retain observed QA/lint state in the report, and exit through the
documented failed-smoke result.

## Approved patch surface proposed at this gate

- `closure.py`: fake value identity/token generation only;
- `smoke.py`: delivery-dependent checks, structured failure, cleanup gating;
- focused fake/smoke tests;
- later patch-version and release records after source approval.

No extraction, scoring, OpenAI, Batch, spend, disclosure, snapshot, production
lint/acceptance, assembly, provenance, or real delivery behavior needs to
change. No live provider test is justified.
