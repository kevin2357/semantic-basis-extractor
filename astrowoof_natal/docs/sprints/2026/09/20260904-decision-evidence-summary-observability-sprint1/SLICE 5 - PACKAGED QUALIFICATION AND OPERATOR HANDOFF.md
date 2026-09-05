# Slice 5 — packaged qualification and operator handoff

## Packaged public boundary

Added the provider-free public command:

```text
astrowoof-decision-evidence-observability-qa --output qualification.json
```

Its closed receipt and packaged JSON Schema prove:

- the stage, validation, and publication evidence events are present;
- all three survive the run-reporter parser;
- closed warning/rejection distributions remain visible rather than becoming
  opaque hashes;
- the protected payload/finding sentinel is absent;
- no absolute workspace path is emitted;
- the eight replay cases retain their frozen log-sufficiency classification;
  and
- provider create/retrieval and external network counts are zero.

The qualification is diagnostic only. It grants no lifecycle, custody,
settlement, publication, or recovery authority.

## Operator handoff

Updated the operator trace playbook and Run Evolution Reporter guide with:

- the new evidence-order reading sequence;
- stage error versus accepted-but-residual-findings interpretation;
- explicit publication-is-not-terminal guidance;
- the seven routine log-sufficient classes;
- the interrupted-publication escalation boundary; and
- the installed qualification command.

## Before/after investigation target

| Question | Before | With this release |
|---|---|---|
| Did both polish attempts actually run and improve? | Checkpoint/archive | Stage summaries |
| Which attempt raised before producing reports? | Checkpoint/archive | Stage state + error class/fingerprint + report presence |
| Which deterministic codes remained? | Checkpoint report read | Validation summary code counts |
| Was review published with retained provider evidence? | Result/receipt plus often checkpoint | Publication identity join plus state/custody summary; result remains authority |
| Was provider work due, ambiguous, or never attempted? | Mixed logs/public readers | Existing typed decisions plus the new publication join |
| Did a valid publication survive an interrupted finalization? | Checkpoint/result inspection | Still checkpoint/result inspection by design |

## Source qualification

- Decision-evidence qualification tests: 2 passed, 1 expected optional-schema
  skip where `jsonschema` is unavailable.
- Combined observability/reporter tests: 26 passed, 1 expected optional-schema
  skip (27 collected).
- Provider calls: 0.
- External network calls: 0.
- R2 operations: 0.
- Retained QA access/mutations: 0.

Installed-wheel qualification remains the next release-candidate gate after the
fresh patch version is selected.
