# Slice 6 — installed intent-retirement qualification

## Candidate

- Version: `0.4.34`
- Wheel: `astrowoof_natal_authoring-0.4.34-py3-none-any.whl`
- Reproducible SHA-256:
  `20a64e366840e143f1f9cb6cd936a7dd15341dc2041562e8f33860eb4ed70b2d`
- Compatibility dependency: `semantic-projection-core==0.11.1`

The version was frozen before the build and installed gates. Two controlled
builds using the same source epoch are byte-identical.

## Public qualification surface

The candidate adds:

- console command `astrowoof-v2-intent-retirement-qa`;
- Python reader `read_intent_retirement_qualification_schema()`;
- Python validator `validate_intent_retirement_qualification()`;
- Python runner `run_intent_retirement_qualification()`; and
- packaged schema
  `external-authority-v2-intent-retirement-qualification.v1.schema.json`.

This surface is qualification-only. It accepts no production workspace,
provider credential, authority document, request payload, or remote coordinate.
All provider behavior is scripted inside a temporary workspace.

## Proved sequence

The installed command exercises the real v2 intent, dispatch, reconciliation,
settlement, and coordinator checkpoint boundaries and proves:

1. a complete predecessor intent is retired in the published coordinator
   checkpoint;
2. the live singleton is absent and the immutable retired record is present;
3. exact predecessor replay returns `exact_replay` and invokes no provider
   preparation or creation;
4. a fresh successor receives a distinct intent and exactly one scripted
   create;
5. incomplete terminal inventory retains the live intent and admits no
   successor; and
6. conflicting retained response identity fails `native_evidence_invalid`,
   retains the live intent, and admits no successor.

The closed Python validator independently checks every nested cell, rather than
trusting the assertion summary or requiring optional `jsonschema`.

## Installed results

- Two qualification files were byte-identical:
  `a5aea64d753995050defa832842a83e905313181a76cc8d42cf0a7fb9b2e5abc`.
- Their canonical receipt SHA-256 is
  `0b2c6b1d201f59a9ecfbfa37f608af282726cbba881d518457399f5ca8381f5e`.
- The installed runtime reported `0.4.34`.
- `pip check` passed with SPC `0.11.1`.
- Generic release smoke and the installed v2, post-fan-in, terminal-review, and
  new retirement qualifications passed.
- Final affected source matrix: 49 passed, with 3 expected optional-schema
  skips in the lean host interpreter.
- External provider/network calls: `0`.
- Real provider creates/retrievals: `0`.
- Provider spend: `$0`.
- Retained Delerium access or mutation: `0`.

## Release posture

The candidate is ready for final API/owner review. No commit, tag, publication,
deployment, or retained-run recovery is authorized by this document.
