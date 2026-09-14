# Slice 1 — Provider-Free Route Reproduction

## Qualification

Six focused tests passed against current API `main` with provider operations
and external writes equal to zero.

Transport/projection set:

- `test_reconciliation_preserves_same_command_terminal_review_handoff`
- `test_reconciliation_preserves_terminal_review_after_diagnostic_event`
- `test_bounded_reconciliation_review_handoff_clears_legacy_terminal_result_id`

Worker/observer set:

- `test_sealed_native_delivery_ingress_publishes_successfully`
- `test_clean_editorial_closeout_observes_only_after_terminal_ingress`
- `test_terminal_cycle_forwards_one_preselected_sealed_result_id`

Pytest caches were disabled and temporary SQLite/test state was confined to
`C:\tmp`. No repository source was modified.

## Route results

### Didot

An exact sealed delivery ID causes one observer call only after successful API
publication. Current runtime source initializes the immediate
`delivery_validation` branch with `sealed_terminal_result_id = None`. The live
first attempt failed before observation, while the successful retry therefore
had no authority with which to call the observer.

The missing contract is durable, same-job, same-native-run carry-forward of the
already-ingested exact delivery result to the later publication attempt. A
latest-result lookup is neither needed nor acceptable.

### Erasmus A

The subprocess JSONL capture preserves the terminal-review command even when
diagnostic execution events are interleaved. Runtime projection retains that
command and clears a weaker legacy sealed-result candidate. The production
worker constructor, supplied with a recording observer, enters the observer
exactly once after strict terminal ingress and passes the command's result ID.

Current source therefore does not reproduce attempt 11's absent observer line.

### Erasmus B

A worker cycle carrying only a preselected sealed result forwards that ID to
strict ingress. It does not synthesize a terminal-review command and does not
enter the ordinary-review observer. That distinction is expected: a generic
result ID is not proof of the invocation/receipt command handoff required for
review observation.

## Conclusion

Didot is reproduced as an API identity carry-forward omission. Erasmus A is a
runtime/lineage/telemetry discrepancy relative to current source. Erasmus B is
not itself a defect; it exposes why validated review authority would need
durable preservation if a later claim is expected to observe it.

