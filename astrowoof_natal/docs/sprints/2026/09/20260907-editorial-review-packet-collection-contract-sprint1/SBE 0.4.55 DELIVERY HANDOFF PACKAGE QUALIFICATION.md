# SBE 0.4.55 delivery-handoff package qualification

## Candidate

- Version: `0.4.55`
- Scope: additive exact successful-delivery command handoff
- Wheel size: 1,375,499 bytes
- Wheel SHA-256:
  `5f56c8ee6a1769eaef222765c5a4ae3554cbc2b5472c0af1a55511d0c4585314`
- Fixed `SOURCE_DATE_EPOCH`: `1789023600`
- Reproducibility: two source builds byte-identical

## Source qualification

- focused terminal handoff contracts: 16 passed
- editorial contract/runtime set: 35 passed, one optional-schema skip in the
  source runtime lacking jsonschema
- release contracts: 14 passed
- API-requested dead-expression cleanup: complete
- structured delivery versus legacy plain-output regression: passing

## Installed qualification

The candidate wheel was installed into a clean virtual environment with:

- semantic-projection-core `0.11.1`;
- jsonschema `4.26.0`; and
- tzdata `2026.3`.

Imports resolved from the isolated environment's site-packages. The packaged
delivery schema resolved as
`astrowoof.terminal_delivery_command_result.v0.1`, `pip check` reported no
broken requirements, and the installed focused/editorial matrix passed 51 tests
with zero skips.

## Remaining gates

The manifest-governed broad source suite subsequently passed 1,157 tests with
60 expected skips and zero failures in 989.694 seconds. Its test inventory
SHA-256 is
`2ea5b04a90ea355af63484f53788ed471c8083901834228da0007f92de342a38`.

Release-lock commit, exact-commit rebuild, immutable tag, publication, renewed
API package pin, and installed API-consumer qualification remain outstanding.
API Slice 2B/2C must remain paused until those gates complete.
