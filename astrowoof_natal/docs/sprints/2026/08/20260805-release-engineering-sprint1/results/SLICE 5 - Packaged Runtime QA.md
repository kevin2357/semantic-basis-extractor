# Slice 5 — Packaged Runtime QA

## Result

Slice 5 passed. The wheel now carries its own deterministic projected fixture
and release smoke command, and the complete workflow has passed outside both
the source tree and the repository working directory.

## Candidate artifact

- Filename: `astrowoof_natal_authoring-0.1.0-py3-none-any.whl`
- Bytes: 612,568
- SHA-256: `11a1fa255720e9d73c1b1e42bafe937773ec1db544dd62aec786fe89a986e1b7`
- Wheel entries: 39
- Projected fixtures: 4
- Bytecode/generated-workspace leakage: 0
- ZIP integrity: pass

This remains a sprint candidate. Slice 7 will build and identify the final
release wheel after live verification.

## Installed execution

The wheel was installed without dependencies into a fresh virtual environment.
The smoke runtime resolved from:

`C:\tmp\astrowoof-release-slice5-venv\Lib\site-packages\astrowoof_natal_authoring`

The definitive run was launched with `C:\tmp` as the process working directory.
No source-tree package path was available to satisfy imports or resources.

## Smoke results

- initial checkpoint: `AUTHORING`;
- resume result: `DELIVERY_COMPLETE`;
- forced pass-1 attempts: 2;
- first attempt: rejected;
- retry: accepted;
- accepted passes: 6;
- cards: 50;
- summaries: 4;
- delivery members: 5;
- delivery ZIP integrity: pass;
- delivery-manifest hashes: all matched;
- packaged resource count: 19;
- resource-set SHA-256:
  `67be96ba08fbd89ab379d1ebf247ef011d595bd4446c4534edd5072a503dcdf2`;
- cleanup targets: 20;
- cleanup reclaimed bytes: 4,627,864;
- retained run/public state and delivery: pass.

## Test suite

Complete repository suite: 116 tests passed.

The live OpenAI boundary remains intentionally untested here and is the sole
focus of Slice 6.
