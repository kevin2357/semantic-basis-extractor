# Slice 4: Consumer Surfaces and Handoff

## Outcome

The required-denial terminal contract and retained-workspace reconciler are now
available through supported source and installed-wheel interfaces. The API can
deny new required work, recover an exactly recognized retained 0.4.1 denial,
inspect the resulting native authority, close it out, and release its own capacity
without editing SBE files or constructing a provider client.

## Supported interfaces

The existing installed lifecycle command retains `inspect`, single denial, atomic
batch denial, and `closeout`, and adds:

```text
astrowoof-authoring-lifecycle --run-dir RUN reconcile-required-denial \
  --reconciled-at 2026-08-15T23:30:02Z
```

The command returns `astrowoof.authoring_lifecycle_inspection.v0.1`. With
`--stdout-jsonl`, first application emits one redacted, non-authoritative
`terminal.transitioned` event followed by `sbe.command_result.v1`. Exact replay
emits no duplicate transition event. Event sink failure remains isolated from
native mutation.

The matching Python surface is
`astrowoof_natal_authoring.lifecycle.reconcile_required_providerless_denial`.
Normal exact resume, bounded resume, and closeout also invoke the same narrow
recognizer automatically.

## Packaged contracts

The packaged catalog now identifies v0.2 as the current successful single and
batch negative-authorization result. Historical v0.1 results remain explicitly
identified for readers; request schemas remain v0.1. Existing packaged v0.2
fixtures and strict schemas remain the canonical examples.

Installed lifecycle smoke now additionally proves:

- current single success schema v0.2;
- a returned terminalized run transition;
- terminal `budget_exhausted` inspection;
- zero local dependencies;
- atomic batch denial and replay;
- closed, stable closeout; and
- the expected bounded event sequence.

## API mapping

The consumer handoff documents the complete sequence and machine mappings:

- release API authority only from exact successful native evidence;
- retain `denied_action_ids` separately from causal `required_action_ids`;
- distinguish external-spend exhaustion from SBE's own frozen ceiling by terminal
  reason, not status alone;
- treat an accepted denial, including `reservation_unavailable`, as final;
- preserve optional-stage skip and accepted-delivery precedence;
- require fresh terminal, quiescent, dependency-free inspection plus closed
  closeout before releasing worker capacity; and
- retain any workspace outside the exact legacy recognizer for review.

SBE does not own API reservations, quotas, circuit breakers, entitlements, leases,
billing reconciliation, publication policy, HTTP status, or workspace deletion.

## Verification

Focused consumer/lifecycle suite:

```text
python -m unittest \
  astrowoof_natal.tests.test_lifecycle_consumer \
  astrowoof_natal.tests.test_negative_authorization \
  astrowoof_natal.tests.test_batch_negative_authorization \
  astrowoof_natal.tests.test_bounded_lifecycle \
  astrowoof_natal.tests.test_lifecycle_closeout \
  astrowoof_natal.tests.test_lifecycle_contracts -q
Ran 79 tests in 23.393s
OK
```

Complete repository suite:

```text
python -m unittest discover -s astrowoof_natal/tests -p "test_*.py"
Ran 310 tests in 134.137s
OK
```

Fresh Windows Python 3.11 installed-wheel qualification:

```text
pip wheel --no-deps --no-build-isolation --wheel-dir <qualification>/dist .
python -m venv <qualification>/venv
<venv>/python -m pip install --no-index --no-deps <candidate-wheel>
<venv>/python -m astrowoof_natal_authoring.lifecycle_smoke \
  --require-installed --work-dir <qualification>/smoke-work
status=pass
```

The installed `astrowoof-authoring-lifecycle` command returned a valid terminal,
quiescent inspection and advertised `reconcile-required-denial`. The temporary
qualification wheel was `astrowoof_natal_authoring-0.4.1-py3-none-any.whl`, SHA-256
`12f91c8a7c61612ee901726c444ee130004e0765933b375d165527b37c4c145e`.
It is qualification evidence only, not a release artifact. The complete temporary
build/venv tree was removed after retaining this compact evidence.

Provider operations: 0. Paid spend: `$0`. API key used: no.

## Gate assessment

Slice 4 is complete. Supported Python, CLI, packaged contract, installed smoke,
structured-event, and consumer documentation surfaces agree. Final evidence lock,
release recommendation, reproducible build comparison, Linux installed smoke, and
the source-request response remain Slice 5 work.
