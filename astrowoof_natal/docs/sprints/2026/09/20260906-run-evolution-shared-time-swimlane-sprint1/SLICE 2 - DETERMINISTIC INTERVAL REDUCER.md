# Slice 2 — deterministic interval reducer

## Outcome

Implemented the first executable cohort-timeline projection over one exact log
and its already validated run-report v1 artifact.

The reducer accepts two explicitly different evidence families:

- native SBE structured/legacy trace records parsed by the existing reporter;
- approved API `astrowoof.execution_event.v1` wrapper records.

It never flattens the latter into SBE authority. Every boundary retains its
source line, raw-line digest, producer, correlation, evidence family, canonical
timestamp field, optional outer timestamp, and clock relation.

## Pairing rules implemented

- job start to completion/failure: deterministic work;
- SBE cycle start to completion: initial wave, reconciliation, v2 dispatch,
  delivery validation, or unknown according to the completed wrapper payload;
- lease acquired to released: observed execution-allocation window only;
- job deferred to next claim for the same run/job: observed API defer/queue
  interval;
- native terminal-review publication: terminal review only when native evidence
  itself carries the review result;
- API reading publication: delivered observation;
- API job failure: failure/refusal observation, never terminal review.

Starts without ends remain open. Approved but unpaired wrapper events remain
visible as instantaneous unknown evidence. A witnessed start/end pair whose
clocks reverse is published as contradictory rather than silently reordered.

## Handoff semantics

Cross-run handoffs are derived only between chronologically consecutive
completed SBE-cycle intervals witnessed on the same producer instance. They are
diagnostic cohort observations with `witness_only_not_sla=true`. Ordering is by
the exact preceding end and following start timestamps, then digest.

## Verification

The focused run-timeline plus existing run-report suites cover:

- real mixed native/API projection;
- exact source-byte and normalized-trace binding;
- deterministic replay;
- evidence-family clock ownership;
- chronological handoff ordering and derived duration;
- malformed and unsupported wrapper accounting;
- orphan completion visibility;
- end-before-start contradiction; and
- compatibility with run-report v1.

Result: 33 tests passed with one expected optional JSON Schema validation skip.
No external or mutable systems were used.
