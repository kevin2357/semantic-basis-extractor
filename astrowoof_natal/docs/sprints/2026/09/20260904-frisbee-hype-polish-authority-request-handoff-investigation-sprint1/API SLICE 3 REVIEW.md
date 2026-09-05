# API Slice 3 Review — Release-Decision Gate

## Decision

**Approved to begin the Slice 3 installed-wheel and release-decision gate.**

The Slice 2 schema-parity correction fully addresses the only condition from
`API SLICE 2 REVIEW.md`.

## Verified

- The packaged schema now fixes the exact six `negative_cases` in order and
  declares the exact four `checks` keys with `additionalProperties: false`.
- The direct schema-only test rejects both an alternate case inventory and an
  alternate check vocabulary; this no longer depends on a Python consumer also
  invoking the receipt validator.
- The test module bootstraps the source tree explicitly, preventing accidental
  import of an older installed package during source qualification.
- The public command remains registered in `pyproject.toml`.

Provider-free local verification:

```text
python -m unittest \
  astrowoof_natal.tests.test_polish_authority_handoff_qa \
  astrowoof_natal.tests.test_polish_authority_handoff_slice0 \
  astrowoof_natal.tests.test_terminal_dominance_slice1 -v

Ran 12 tests in 0.666s — OK
```

## Slice 3 requirements

Please build two clean candidate wheels, verify byte identity and SHA-256, then
install one into a fresh isolated environment. Run the public
`astrowoof-polish-authority-handoff-qa` command from that installed wheel and
validate its receipt against the packaged schema and public validator. Record
the exact candidate coordinates, digest, installed command result, and zero-I/O
qualification counts in the sprint evidence.

No API implementation, live provider activity, or retained-QA mutation is
needed for this SBE package gate. API will consume the released native ordinary-
v2 authority request in the existing runtime path; the qualification receipt is
release-pair evidence, not runtime authority.
