# Slice 6 — Closeout and Release Decision

Status: complete; released as immutable SBE 0.4.15.

## Classification

This candidate combines an in-place tightening of lifecycle inspection v0.5
combinations that were already invalid at the API boundary, native semantic/schema
validation and redacted diagnostic corrections, and qualification/test compatibility
updates.

It introduces no new public lifecycle state, scheduling choice, provider action,
spend authority, API ownership, or migration requirement. A fresh immutable patch
release (`0.4.15`) is recommended because packaged runtime/schema behavior changed.

## Full regression gate

The first complete run exposed two test-integration assumptions outside the focused
matrix: the lean schema resolver did not follow packaged cross-file references once
the fixture truthfully projected a typed refusal, and the lifecycle volatility test
did not normalize observation-bound embedded request/refusal time and digest.

Both were corrected without changing runtime behavior. The complete suite was then
rerun:

```text
Ran 558 tests in 529.888s
OK (skipped=27)
```

The skips are existing environment-dependent optional-schema/dependency checks.

## Installed candidate

Artifact source commit: `063dc0d` (Slice 5 packaged implementation). The later
closeout/evidence commit contains tests and sprint records only.

```text
astrowoof_natal_authoring-0.4.14-py3-none-any.whl
SHA-256 59053ac273d21f6d7b252d34b23a0757bacf1420baa855aee2b7612676d3f12b
```

From an isolated Python 3.11 installation and outside the source package path:

- installed release smoke passed;
- deterministic delivery produced 50 cards and 4 summaries;
- validation, lint, acceptance, and manifest hashes passed;
- installed resource count was 78;
- installed external-authority qualification passed every v2 assertion; and
- scripted creates were 6; real calls, retrievals, and spend were 0, 0, and USD 0.

## Privacy and integrity

- Sanitized fixtures contain no credentials, authorization headers, birth data,
  coordinates, prompts, provider payloads, subject views, or secrets.
- Their only token-related fields are intended bounded `maximum_output_tokens`
  authorization bindings.
- Python compilation, packaged JSON parsing, and `git diff --check` pass.
- The retained QA workspace was neither read nor mutated.
- Unrelated untracked work remains untouched and excluded.

## Decision gate

Native and API consumer gates passed. SBE 0.4.15 was tagged, published, and
independently verified without moving the immutable tag.
