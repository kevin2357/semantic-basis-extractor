# Evidence

- SBE release under test: `astrowoof-natal-authoring 0.4.42`
- Wheel SHA-256:
  `58ccfaa319a244afea177e40e7c83e40b0e220c9bd86fe0034512ee19a28dc8d`
- API source dispatch: `f305c5493c3fb35df2f6260157faf88a51a9c770`
- Failed GHCR workflow: `33834841337`
- Failing installed command: `astrowoof-release-smoke --work-dir /tmp/sbe-smoke --require-installed`
- Non-failing independent command: `astrowoof-deployed-qa` (provider-free pass)
- Raised exception: `ValueError: Terminal result requires a paid-action inventory`

## Slice 0 reproduction

The installed `0.4.42` release-smoke command was run provider-free with
`--require-installed`. Its journal reaches `FINAL_QA_FAILED` and records the
expected `review_required / final_qa_requires_review` transition before the
terminal-result builder raises the reported exception.

The restored smoke state has no `spend_ledger` key at all; it is not an
explicit `{"actions": []}` ledger. This confirms both sides of the intended
boundary:

- the fixture truly has no paid-action lineage; and
- accepting its current omitted inventory as action-free would weaken the
  production contract incorrectly.

No provider, network, R2, retained-QA, or production run action occurred.

## Slice 1 contract/runtime proof

- Added `astrowoof.native_execution_result.v0.3` and matching closed command
  envelope `astrowoof.terminal_review_command_result.v0.2`.
- The smoke materializes `spend_ledger: {"actions": []}` before resume and
  invokes its private, fake-provider-only zero-action terminal path.
- A source-runtime smoke sealed a v0.3 `review_required` result and immutable
  v0.1 receipt with `paid_action_count: 0`,
  `provider_operation_count: 0`, and no paid-action projection.
- Focused contract suite: 12 passed, 3 expected optional `jsonschema` skips.
  The provider-free non-delivery smoke regression also passed.

## Slice 2 installed-wheel qualification

- Disposable candidate wheel: `astrowoof_natal_authoring-0.4.42-py3-none-any.whl`
- Candidate SHA-256:
  `4cab32770d7f8d943fd6d1d68288c87ad488c1b9fdb2608707395435db7beb3d`
- Installed under a fresh `site-packages` directory; both v0.3 result and v0.2
  command schema readers resolved from the wheel.
- The real `python -m astrowoof_natal_authoring.smoke --require-installed`
  command passed provider-free and sealed `nres_8ae9bb3f402553d8ed38d896` as
  an explicit zero-action terminal review result.

This is a disposable pre-version-bump candidate only. Slice 3 must rebuild from
the eventual fresh release version before publication.

## Slice 3 pre-release candidate

- Candidate version: `0.4.43`
- Candidate wheel SHA-256:
  `ccf8c3ad0035f345cc8ccf6ad0182913b7a1f23f00179cdfa2e0beaace1003b6`
- Focused source suite: 36 passed, 3 expected optional-schema skips. It covers
  terminal contracts, native result publication/reading, and the structured
  non-delivery smoke boundary.
- The installed-wheel smoke gate was run provider-free against the fresh
  candidate; its v0.3 result/receipt joined successfully.

The candidate has not been committed, tagged, published, deployed, or used for
QA reset. Final release review remains required.
