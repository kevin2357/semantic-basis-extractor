# Python 3.11 packaged-resource traversal compatibility sweep

## Purpose

Audit and correct the remaining SBE packaged-resource accessors that rely on
Python 3.12's variadic `Traversable.joinpath(...)` behavior but are unsupported
on SBE's declared minimum runtime, Python 3.11.

This is the companion SBE sprint for Control Room child
[`astrowoof-api#23`](https://github.com/kevin2357/astrowoof-api/issues/23).

## Trigger and dependency

The predecessor live-defect sprint confirmed that SBE 0.4.62 terminal capture
failed at `editorial_review_contracts._resource_bytes()` because Python 3.11's
concrete traversable accepts one child per `joinpath()` call. Its narrow Slice
1 repair passes focused tests on Python 3.11 and 3.12.

The broader Python 3.11 editorial-contract suite then produced eight errors at
the already inventoried `editorial_review_fixtures.py:628` variadic traversal.
API approved the live fix but blocked candidate-wheel qualification until this
separate sweep is completed and reviewed.

Predecessor:
`../20260915-python311-editorial-contract-resource-compatibility-sprint1/`.

## Scope

The initial static inventory contains ten explicit multi-argument calls and
one starred-component call across seven modules:

- `editorial_review_fixtures.py:628`;
- `resource_access.py:16`;
- `adversarial_consumer.py:64,65,70`;
- `adversarial_trace.py:577,781`;
- `external_authority_v2.py:276`;
- `provider_economics.py:570,578`; and
- the predecessor's already corrected
  `editorial_review_contracts.py:221` control.

The sweep must classify real callers before editing, exercise real packaged
resources rather than permissive mocks, and preserve exact bytes and failure
behavior on Python 3.11 and 3.12.

## Non-goals

- No API, schema, lifecycle, authority, custody, packet, transport, or Better
  Stack behavior change.
- No provider, R2, queue, workspace, or live-runtime mutation.
- No generic exception suppression or fallback resource discovery.
- No assumption that fixture/adversarial code is harmless merely because it is
  qualification-oriented; supported public entry points must work on the
  declared runtime.
- No version bump, candidate wheel, tag, publication, deployment, or live
  witness before explicit later gates.

