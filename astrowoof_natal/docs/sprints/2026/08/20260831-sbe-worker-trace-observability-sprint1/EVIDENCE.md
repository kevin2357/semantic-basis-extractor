# Evidence — SBE worker trace observability

## Planning evidence

- Parent control-room issue:
  `https://github.com/kevin2357/astrowoof-api/issues/10`
- SBE trace sub-issue:
  `https://github.com/kevin2357/astrowoof-api/issues/11`
- Existing formatter:
  `astrowoof_natal/src/astrowoof_natal_authoring/application_logging.py`
- Existing structured-event emitter:
  `astrowoof_natal/src/astrowoof_natal_authoring/execution_events.py`

## Source implementation

- Safe projection helper:
  `astrowoof_natal/src/astrowoof_natal_authoring/trace_observability.py`
- Provider-free qualification:
  `astrowoof_natal/src/astrowoof_natal_authoring/trace_observability_qa.py`
- Closed qualification schema:
  `astrowoof_natal/src/astrowoof_natal_authoring/resources/contracts/sbe-trace-observability-qualification.v1.schema.json`
- Public command: `astrowoof-trace-observability-qa`

## Focused evidence

- Safe helper and qualification tests: 9 passed, 1 optional-schema skip.
- Bounded lifecycle, Glimmer mixed-custody, and observability matrix after the
  release-gate correction: 58 passed, 1 optional-schema skip.
- Qualification receipt:
  - exact route: passed;
  - bounded route: passed;
  - qualification SHA-256:
    `5625a9c2ea879ee4305dab90553873fc2dfd4b6dfbd44dbf9d643e437fc9cc2a`;
  - external provider/network calls: 0;
  - protected sentinel occurrences: 0.

## Regression evidence

Published `0.4.35` allowed generic persistence to discover a sealed result via
the strict result reader. That reader correctly requires the current snapshot,
but generic persistence is also used during the writer interval in which native
bytes have changed and the successor snapshot has not yet been published. The
new regression makes that interval explicit and proves:

- generic save does not inspect sealed results;
- coordinator persistence and successor snapshot complete;
- the new snapshot validates; and
- explicit reconciliation preservation remains covered by the Glimmer matrix.

## Current gate

## Installed candidate evidence

- Candidate version: `0.4.36` (frozen before candidate testing).
- Reproducible wheel SHA-256:
  `85b94911d82b1dd960c19f72e78ebc4cd6828378dddc8de1bacef3c4aee35841`.
- Installed qualification receipt file SHA-256:
  `82e8aa59c681a7064164569824cefee04fb3ee7473c064b46f1fe3abd81cc7c2`.
- Installed package version and packaged schema resource: verified.
- Generic installed release smoke: passed.
- Provider/network/R2/retained-QA activity: 0.

## Current gate

Implementation, focused regression, reproducible build, installed trace
qualification, and generic installed smoke are complete. Commit/tag/publication
remain owner-authorized release actions.
