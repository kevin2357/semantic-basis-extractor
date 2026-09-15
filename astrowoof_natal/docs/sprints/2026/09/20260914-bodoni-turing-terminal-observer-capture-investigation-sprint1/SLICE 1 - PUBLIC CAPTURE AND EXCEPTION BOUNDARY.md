# Slice 1 — Public capture and exception boundary

## Outcome

Provider-free mapping is complete. The live signature proves that the installed
public SBE capture callable raised one of the local exception classes caught by
API. It does not yet prove whether that exception represents a contractually
expected native-evidence refusal or a defect.

The absent `capture failed` event has an independently reproduced API cause:
Python exception class names such as `ValueError` violate the lowercase
`FieldKind.REASON` contract. `EventEmitter` therefore rejects the event and,
by design, returns `None` without propagating the diagnostics failure.

## Public export verification

The API virtual environment contains `astrowoof-natal-authoring==0.4.61`.
Provider-free introspection proved:

- package-root export and implementation callable have object identity;
- implementation module is
  `astrowoof_natal_authoring.editorial_review_runtime`;
- signature is `(run_dir, result_id, *, exact_reader=read_native_transition_result)`;
- no adapter, discovery helper, or alternate result selection lies between the
  API import and the native implementation.

The suspected defect is therefore not a missing or stale `__init__` export.

## Source exception map

`build_editorial_review_runtime_capture()` first calls
`collect_editorial_review_runtime_evidence()` **outside** its packet-assembly
`try` block. The collector and its exact reader may directly raise local
`ValueError`, `OSError`, `KeyError`, or `TypeError` for malformed/missing exact
result evidence, source identity, paths, pass/action joins, files, or mapping
shape. API catches those classes and returns `branch=unavailable` at phase
`capture`.

Once collection succeeds, packet assembly catches its own bounded native
evidence failures and normally converts them to a typed
`unsupported/incomplete_native_evidence` status. Validation contradictions also
become typed unsupported status. This produces a meaningful asymmetry:

| Failure location | Public SBE behavior | API behavior |
| --- | --- | --- |
| exact reader / eligibility / evidence collector | local exception may escape | `unavailable`, capture phase |
| packet assembly bounded evidence error | typed `unsupported` status | status envelope/preflight/POST path |
| completed packet validation contradiction | typed `unsupported` status | status envelope/preflight/POST path |

Whether the witness evidence belongs in the first row legitimately, or should
be normalized into a typed status, requires an exact retained-workspace
reproduction and is intentionally unresolved at this gate.

## Provider-free executable checks

- API's focused transport suite passed: **23 passed**.
- Installed-wheel export identity/version/signature checks passed.
- An `editorial.observation.phase` payload containing
  `failure_exception_class=ValueError` was rejected as invalid.
- The same payload with `failure_exception_class=value_error` was accepted:
  emitter totals were one accepted and one invalid event.

This also explains why API unit tests did not catch the live telemetry loss:
transport tests collect the phase callback payload directly, where `ValueError`
is allowed as an ordinary string; they do not pass that failure payload through
the production event contract and emitter.

## Review Gate A recommendation

The source/public mapping does not identify the witness's first failing evidence
operation. Proceed to exact retained-workspace reproduction only after API
provides hash-pinned Bodoni and Turing coordinates and the owner separately
authorizes the bounded reads in the plan.

Ownership is currently split:

- API owns the proven failure-phase token/schema mismatch and its missing
  production-path regression.
- SBE ownership of the original capture refusal remains possible but unproven.
  It depends on whether the exact witness condition should be a typed capture
  status rather than a public exception.

No runtime correction, provider operation, retained-workspace read, or external
POST occurred in this slice.
