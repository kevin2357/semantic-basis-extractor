# AstroWoof Natal Authoring Test Suite Runner

## Supported broad-confidence command

Run the complete repository test inventory through the checked-in coordinator:

```text
python astrowoof_natal/scripts/run_test_suite.py
```

The supported default uses one worker. This is intentional: the first complete
qualification proved exact one-worker/two-worker equivalence, but two workers
were slower on the qualifying laptop while most modules remained in the serial
tail.

The default may be revisited after duration-led promotion expands the proven
parallel-safe set or when qualification runs on materially different hardware.
Do not describe a higher worker count as faster without repeated evidence for
that manifest and execution environment.

## What the runner provides

- a checked-in classification for every discovered `test_*.py` module;
- deterministic duration-weighted assignment of parallel-safe modules;
- unique temporary, cache, output, and result roots for every group;
- removal of inherited AstroWoof and external-service credentials;
- quiet routine logs with an explicit unquiet observability group;
- exact collected-test and outcome inventory digests;
- retained failure logs and exact group reproduction commands; and
- an explicit serial tail for provisional and serial-authority modules.

The coordinator is test/process tooling. Its receipt records evidence but does
not replace installed-wheel qualification, deterministic builds, release
receipts, or other release authority.

## Manifest completeness control

The runner discovers every immediate `astrowoof_natal/tests/test_*.py` module
before starting workers and validates the manifest fail-closed. It refuses to
run when:

- a discovered module is absent from the manifest;
- a manifest module no longer exists;
- a module appears in more than one classification; or
- the manifest names an unsupported schema version.

The focused runner test suite independently exercises repository completeness,
unclassified-module refusal, stale-entry refusal, and duplicate-classification
refusal. Therefore adding or renaming a test module requires an explicit
manifest disposition in the same change.

New modules should normally begin in `provisional` unless their isolation is
already directly proven. Moving a module to `parallel_safe` requires the
isolation and equivalence evidence described by the duration-led promotion
campaign. Modules whose purpose includes global state, locking, builds,
installed artifacts, or release authority remain serial.

## Profiles and reproduction

Current supported profile:

```text
python astrowoof_natal/scripts/run_test_suite.py --workers 1
```

Controlled parallel experiment:

```text
python astrowoof_natal/scripts/run_test_suite.py --workers 2
```

Use the command retained in a failed group's receipt to reproduce that exact
module inventory. Use a fresh `--work-root` and `--receipt` path when retaining
evidence from multiple runs.

Universal fallback using Python's direct discovery remains:

```text
python -m unittest discover -s astrowoof_natal/tests -p "test_*.py"
```

The fallback is valuable for diagnosing runner behavior. It does not exercise
the manifest completeness, credential sanitation, owned-root, quiet-output, or
receipt controls and is therefore no longer the preferred broad-confidence
entry point.

## Release boundary

The broad regression gate may use the runner's one-worker default. Candidate
wheel construction, deterministic rebuilds, package inventory, installed-wheel
qualification, and release-receipt generation remain serial operations against
one exact candidate identity.
