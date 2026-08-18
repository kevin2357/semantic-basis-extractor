# Slice 6: Cross-Platform and Cohort Qualification

## Result

Slice 6 passes the SBE-native qualification gate. Exact Natal Responses, exact
Natal Batch, and bounded-Natal Responses can coexist as independent retained
workspaces, reconcile through bounded worker cycles, and release native worker
capacity while provider work is pending. No provider operation was performed and
paid spend was `$0`.

The API companion qualification remains API-owned. This slice proves native SBE
checkpoint, custody, scheduling, and route behavior; it does not claim that API
queue slots or financial reservations have been released.

## Defect found and corrected

The mixed-route cohort exposed one route-parity defect before release:

- a bounded-Natal workspace with a durable pending provider action still projected
  the generic `AUTHORING` local dependency;
- that projection incorrectly retained local execution capacity after a bounded
  poll, even though only provider-result reconciliation remained;
- lifecycle dependency projection now recognizes authoritative bounded provider
  wait state and emits only the provider-result reconciliation dependency.

The correction is deliberately narrow. It does not weaken provider identity,
snapshot, ambiguity, authorization, or single-writer checks.

## Cohort and regression evidence

- A deterministic, concurrent three-workspace cohort covered exact Responses,
  exact Batch, and bounded Responses.
- Every member detached as `detached_provider_pending` with capacity disposition
  `release_until_due` and preserved its native route/mechanism identity.
- Existing tests cover not-due, due, partial-progress, terminal/review,
  fresh-worker replay, concurrent claim, stale checkpoint, stage routing, provider
  conflicts, and injected persistence failures.
- The complete repository suite passed: `356` tests in `244.061` seconds.
- The existing API transition-oracle suite passed independently: `18` tests in
  `0.08` seconds. The new packaged route-parity oracle remains the handoff fixture
  for API adoption; no API-owned source or authority was changed here.
- Output document/card contracts did not change, so QA rendering would add no
  visual evidence. Lifecycle correctness was qualified from schemas, artifacts,
  checkpoints, and typed results.

## Reproducible candidate wheel

Two fixed-epoch builds were byte-identical.

| Property | Evidence |
|---|---|
| `SOURCE_DATE_EPOCH` | `1786924800` |
| Candidate filename | `astrowoof_natal_authoring-0.4.3-py3-none-any.whl` |
| SHA-256 | `1a305a15eb9b01860de79bfd6c525b312189b5a46809e894a867ba39a99d69ef` |
| Size | `751149` bytes |
| Wheel members | `91` |
| Packaged resources | `50` |
| Cache artifacts | `0` |

Inspection confirmed the wheel contains `py.typed`, the lifecycle contract
schemas, and `route-parity-transition-oracle.v1.json`. The `0.4.3` metadata is the
current source version and is qualification evidence only; version selection and
release authorization remain Slice 7 decisions.

## Installed-runtime evidence

### Linux

- Clean `python:3.11-slim` container.
- Installed the exact local SPC 0.11.0 wheel and the candidate SBE wheel with
  declared dependencies.
- `pip check` passed.
- Installed-only lifecycle smoke passed.
- Public typed Python surface and packaged-resource smoke passed.
- Both exact and bounded CLIs exposed the neutral
  `--provider-reconciliation-cycle` interface.

### Windows

- Clean isolated virtual environment using the locally available CPython 3.12.13.
- Installed the exact local SPC 0.11.0 wheel and candidate SBE wheel.
- An initial dependency-free diagnostic correctly reported SPC's absent
  `jsonschema` dependency; after installing the declared dependency closure,
  `pip check` passed.
- Installed-only lifecycle, public typed surface, and packaged-resource smokes
  passed.

The required Python 3.11 installed-wheel boundary was exercised under Linux. The
Windows host did not have Python 3.11 installed, so its clean installed-runtime
check used Python 3.12.13 and is recorded without implying otherwise.

## Gate assessment

PASS for Slice 6. The three supported route/mechanism combinations satisfy the
native worker-capacity release/reclaim contract under isolated, concurrent, and
installed-runtime checks. Bounded Batch remains explicitly unsupported and
fail-closed. Slice 7 may now perform closeout, consumer review, and the release
recommendation.

