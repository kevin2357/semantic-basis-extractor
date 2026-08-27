# Slice 3 — Native Progress and Safety Oracle

Status: implemented and focused-qualified; paused for joint review

## Result

SBE now derives transition classifications from validated public trace evidence
instead of trusting a fixture's expected label. The oracle distinguishes productive
progress, legitimate provider waiting, idempotent inspection, stutter, semantic
recurrence, typed refusal, and contradictory native evidence.

The history evaluator retains prior semantic fingerprints so recurrence is a real
history property. The safety evaluator additionally detects the v1-expressible
forms of:

- provider work after identity-less call-entry ambiguity;
- advertised local work that is neither consumed nor replaced by a typed
  disposition; and
- consumed local work being advertised again.

## Two digest roles

The trace contract's checkpoint-basis digest remains semantic for stale authority
and replay fencing. The progress oracle separately projects away snapshot, revision,
raw-evidence, and checkpoint-publication churn. This is intentional: changing a
stale-binding fence can invalidate an invocation without proving useful application
progress. A regression demonstrates that a no-op republish is still classified as
stutter by the progress oracle.

## Evidence boundary

Trace v1 does not contain every private ledger/card/publication member. The oracle
therefore validates only properties supported by public trace evidence; it relies on
the source qualification receipts' strict readers for snapshot/result/receipt joins
and route-specific append-only facts. It does not invent missing action or billing
facts.

In particular, v1's opaque provider operations are not joined to an opaque
action/binding identity. The oracle therefore does **not** infer duplicate creation
from "some provider member already exists" plus "some create occurred": that would
falsely reject legitimate partial-wave progression. Slice 4's explorer state must
carry the exact redacted action/binding join before claiming create-at-most-once.

## Focused qualification

- 27 adversarial tests passed.
- One optional `jsonschema` check skipped in the lean interpreter.
- Zero external provider/network calls and USD 0 spend.
- `git diff --check` passed with non-failing Windows line-ending notices only.
