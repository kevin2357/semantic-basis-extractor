# Slice 0 — logging characterization

## Decision

Proceed with a narrow test-runner-only `WARNING` default in Slice 2. Do not
change production defaults or either SBE/API sink. Logging-sensitive tests must
explicitly opt into the level and stream they verify.

## Source map

- `application_logging.add_logging_arguments()` gives production CLIs an
  explicit `--log-level` with default `INFO`.
- `configure_application_logging()` installs the structured stderr handler and
  sets the root logger level. Changing a parent test logger alone is therefore
  insufficient when a tested CLI reconfigures logging.
- In-process `logging.disable(logging.INFO)` suppresses routine records, but it
  is process-global and needs a restoring test harness boundary.
- Subprocess tests need an explicit test-only argument/environment convention;
  they do not inherit Python logging state from their parent.
- JSONL execution-event stdout and authoritative command-result stdout are
  separate surfaces and must not be silenced by the ordinary application-log
  setting.

## Protected modules

The initial explicit-INFO set is:

- `test_application_logging.py`
- `test_execution_events.py`
- `test_structured_logging_contracts.py`
- `test_trace_observability.py`
- `test_trace_observability_qa.py`
- `test_run_report.py`
- `test_run_timeline.py`
- `test_external_authority_v2_cli.py`

Additional tests that assert stderr or JSONL content must be added mechanically
when Slice 2 introduces the helper. Merely using `redirect_stderr` does not make
a test logging-sensitive; the assertion must depend on a structured record.

## Measurement

Representative production-shaped CLI module:
`test_external_authority_v2_cli.py`.

| Posture | Result | Wall time | Captured stderr |
|---|---:|---:|---:|
| current INFO | pass | 2.699 s | 304,919 bytes |
| test-only INFO suppression | pass | 2.471 s | 107 bytes |

This is an 8.4% wall-time improvement in the selected module and a 99.96%
output reduction. It supports quieting for usability and memory/capture cost,
but does not justify claiming that logging dominates the full 18-minute suite.
An attempted heavyweight sample was stopped after it exceeded three minutes;
its workload swamped the value of a quick logging-only comparison.

## Guardrail

The user explicitly prefers suppressing console sparkle-dog logs through the
test log level. No SBE or API sink alteration is needed or authorized.
