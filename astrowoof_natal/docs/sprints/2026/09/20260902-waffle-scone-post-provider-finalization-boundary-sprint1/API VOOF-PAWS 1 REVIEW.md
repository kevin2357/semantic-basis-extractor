# API Voof-paws 1 Review — Slice 0

Status: approved to begin Slice 1, with the contract guardrails below.

## What the evidence establishes

The characterization is convincing and correctly narrows the incident:

1. Waffle's provider authority and custody were fully resolved before the
   failure. This is not a reconciliation, duplicate-submission, or capacity
   incident.
2. `theme_group_balance` was admitted as advisory at pass acceptance but was
   reintroduced as a hard final-assembly exception. The real public resume
   boundary reproduces that contradiction provider-free.
3. The pre-finalization consumed operation was the completed-provider
   fan-in/adoption operation. That operation made a durable semantic change;
   Slice 0 correctly retracts the earlier theory that finalization itself had
   been falsely consumed.
4. Scone remains a separate typed retained-custody/review comparator. No
   shared-cause claim is warranted.

The two controls are appropriately small for a production-characterization
slice: the advisory witness demonstrates the contradiction; the unknown
assignment witness proves a malformed structural join still fails closed.

## Approved Slice 1 direction

Removing the obsolete distribution-only authority from final assembly is the
right root correction. Keep validation of registry shape, assignment identity,
unknown IDs, duplicate/competing artifacts, and any other structural join
invariant exact and hard. The three named distribution policy codes must have
one consistent advisory meaning at every native consumer.

Please add an explicit fixture assertion that the formerly failing
distribution reaches a successfully assembled subject/finalization path, not
only that `assemble_subject` ceases to throw. That protects the actual Waffle
success path rather than merely removing one `ValueError`.

## Freeze before Slice 2

API agrees with the distinction between operational dependency failure and
native semantic disposition, but it must be made through a sealed public native
result—not error text, stderr, or a non-zero exit code. In particular:

- Do **not** broadly convert every finalization `ValueError` into a terminal
  review result.
- If native can establish a deterministic, non-replayable review/terminal
  outcome, publish it as a closed typed result before command exit; API can
  then consume that result even if the wrapper process exits non-zero.
- If no sealed result exists, API must retain a conservative operational
  failure posture rather than infer semantics from logs.
- Retained provider custody or ambiguity remains higher precedence than any
  local finalization disposition.

The exact result-version shape, absent-result behavior, and retry/review
mapping remain correctly deferred to Voof-paws 2.
