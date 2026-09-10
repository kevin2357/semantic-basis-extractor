# SBE final 0.4.55 release qualification

## Authorized scope

Release the additive exact successful-delivery handoff approved by API and
explicitly authorized by the owner. The change preserves legacy plain-JSON CLI
state output and emits the new closed handoff only on successful structured
JSONL delivery.

## Source evidence

- focused terminal contracts: 16 passed;
- editorial contract/runtime: 35 passed;
- release contracts: 14 passed;
- manifest-governed broad suite: 1,157 passed, 60 expected skips, zero failures;
- broad inventory SHA-256:
  `2ea5b04a90ea355af63484f53788ed471c8083901834228da0007f92de342a38`;
- broad wall time: 989.694 seconds; and
- diff hygiene: clean.

## Pre-lock package evidence

- candidate version: `0.4.55`;
- two fixed-epoch wheels byte-identical;
- wheel size: 1,375,499 bytes;
- wheel SHA-256:
  `5f56c8ee6a1769eaef222765c5a4ae3554cbc2b5472c0af1a55511d0c4585314`;
- installed focused/editorial matrix: 51 passed with schema validation enabled;
- installed dependencies: SPC `0.11.1`, jsonschema `4.26.0`, tzdata `2026.3`;
  and
- `pip check`: no broken requirements.

## Immutable publication evidence

- release-lock commit:
  `22b31476d526ecba0303d511efc0f9b3e507f000`;
- annotated tag: `astrowoof-natal-authoring-v0.4.55`;
- two exact-commit fixed-epoch wheels were byte-identical;
- published wheel size: 1,375,499 bytes;
- published wheel SHA-256:
  `e16a538bc7821212a0fe2ddb91e3515aa3b3846b9659c50380c791c8003dd8f2`;
- GitHub's asset digest matched the qualified digest;
- a fresh release download independently matched the same digest and the
  published checksum manifest; and
- release URL:
  `https://github.com/kevin2357/semantic-basis-extractor/releases/tag/astrowoof-natal-authoring-v0.4.55`.
