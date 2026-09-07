# Slice 6 — adoption and closeout

## Decision

The deterministic coordinator and checked-in classification manifest are now
the supported broad-confidence framework. The supported default uses one
worker. Two-worker execution remains an explicit experimental profile pending
duration-led promotion of more provisional modules or qualification on
materially stronger hardware.

This separates two conclusions that the evidence supports:

1. the framework is safe, deterministic, maintainable, and worth exercising;
2. the current conservative two-worker profile is not a performance win on the
   qualifying laptop.

Direct unittest discovery remains the universal diagnostic fallback. Build,
wheel, installed qualification, and release-receipt authority remain serial.

## Final supported-command qualification

The final invocation deliberately omitted `--workers`:

```text
python astrowoof_natal/scripts/run_test_suite.py
```

Result:

- receipt worker count: `1`;
- tests: `1,118`;
- skips: `58`;
- failures/errors/unexpected successes: none;
- wall time: `1,122.983334` seconds;
- test inventory SHA-256:
  `64540bf668560c4fcb3989673fac93fbead58aab9b9d56d46d2a9e53eef53c69`;
- outcome inventory SHA-256:
  `a400a525811fd41fa58bf97e45957110b0a29a85d0c955f06143c18133e593de`.

The three-test increase from the Slice 4 authority pair is intentional. The
new tests freeze the one-worker default and directly reject duplicate and
stale/nonexistent manifest classifications.

## Manifest maintenance control

Before worker execution, the coordinator discovers every immediate
`astrowoof_natal/tests/test_*.py` module and requires the manifest to classify
each exactly once. Execution fails closed for:

- any discovered but unclassified test module;
- any manifest entry whose file is absent;
- any duplicate classification; or
- an unsupported manifest schema version.

The focused runner suite exercises the live repository inventory and synthetic
missing, stale, and duplicate cases. Adding or renaming a test module therefore
requires an explicit manifest disposition in the same change.

## Documentation and follow-up

- Added `Test Suite Runner.md` as the supported maintainer guide.
- Updated the Maintainer Release Playbook's broad/full command.
- Preserved direct unittest discovery as a diagnostic fallback.
- Created a separate duration-led provisional-promotion campaign.
- Included a non-blocking distributed-growth manifest slice for future natal,
  synastry, transit, and simulation tiers across local and distributed CI.

## Release decision

No SBE package release is required. The sprint changes repository test/process
tooling, tests, and documentation only; installed runtime behavior and packaged
resources are unchanged.

## Closeout result

Sprint complete. Future CI must invoke the same repository coordinator and
manifest rather than reconstructing classification or sharding rules in CI
configuration. The default worker profile may change only after repeated
timing, isolation, and equivalence evidence.
