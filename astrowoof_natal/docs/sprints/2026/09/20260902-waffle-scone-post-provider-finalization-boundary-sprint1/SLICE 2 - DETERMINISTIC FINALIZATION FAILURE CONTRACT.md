# Slice 2 — Deterministic Finalization Failure Contract

Status: proposed; runtime implementation paused at Voof-paws 2.

## Problem boundary

Slice 1 removes Waffle's concrete deterministic failure. A general retry-loop
hazard nevertheless remains: assembly currently expresses all deterministic
content/structure contradictions as ordinary `ValueError`, and `closure.main()`
does not publish a typed result when one escapes finalization.

API must not interpret exception text, stderr, or exit status as native
disposition. SBE likewise must not convert every finalization exception into a
semantic terminal result: subprocess, filesystem, interruption, and dependency
failures may be operational and conservatively retryable.

## Proposed narrow contract

1. Introduce `AssemblyContractError` as a `ValueError` subclass.
2. Assembly raises that type only for deterministic contradictions in the
   restored authored artifacts and their native joins. Existing callers which
   catch `ValueError` remain compatible.
3. Catch only `AssemblyContractError` at the finalization coordinator boundary,
   after revalidating that no provider custody or ambiguity outranks it.
4. Under the native writer, checkpoint the truthful review posture and publish
   a sealed native-result v0.2 plus canonical terminal-review command envelope.
5. Add closed cause code `finalization_contract_invalid`; do not expose the
   exception message as authority. Sanitized logs may retain a fingerprint.
6. Exit 2 only after emitting the invocation-bound result envelope. The sealed
   result outranks exit status for API ingestion.

The result must prove:

- `outcome = review_required`;
- `cause_code = finalization_contract_invalid`;
- exact invocation/result/receipt and checkpoint identities;
- zero provider custody and zero ambiguity;
- no locally runnable continuation; and
- the failed finalization operation is not recorded as successfully consumed.

## Explicit exclusions

- Do not catch broad `ValueError` around the whole command.
- Do not classify `CalledProcessError`, `OSError`, interruption, timeout, or
  provider exceptions as deterministic native review.
- Do not infer retry/review from message matching.
- Do not alter Scone's retained-custody semantics.
- Do not version lifecycle or command-result artifacts unless their exact
  closed shape changes; adding a closed native-result cause should follow the
  existing v0.2 extension/versioning rules confirmed at review.

## Proposed tests

- Inject one real `AssemblyContractError`: sealed v0.2 result and command
  envelope precede exit 2; exact replay creates no second semantic transition.
- Inject operational subprocess and filesystem failures: no fabricated review
  result.
- Provider custody and ambiguity fixtures: their existing disposition wins.
- Interruption around checkpoint/result publication: recovery either adopts the
  exact sealed result or refuses; it never reclassifies from logs.
- Protected sentinel: no authored content or exception detail enters public
  result/event fields.

## API decision requested

Confirm that `finalization_contract_invalid` maps to stable operator review and
that API consumes the exact invocation-returned result envelope first. Result
availability discovery remains recovery-only when no result ID was returned.
