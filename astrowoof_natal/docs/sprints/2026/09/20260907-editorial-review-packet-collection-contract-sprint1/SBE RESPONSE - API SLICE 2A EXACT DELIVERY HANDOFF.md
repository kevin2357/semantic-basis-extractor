# SBE response — API Slice 2A exact delivery handoff

## Decision

API's blocker is confirmed. Ordinary successful authoring already seals an exact
`astrowoof.native_execution_result.v0.1` result and its immutable publication
receipt, but the structured API-facing command result discarded that identity
and emitted mutable run state instead. API must not repair that omission with
latest-result discovery.

## Additive handoff

SBE now defines the closed
`astrowoof.terminal_delivery_command_result.v0.1` handoff. It carries only:

- `outcome=delivery_complete` and `exit_code=0`;
- the exact native invocation, result ID, and result digest; and
- the exact receipt ID and receipt digest.

Construction first validates the v0.1 native delivery result against its
canonical receipt and refuses non-delivery outcomes. A second validator joins a
received handoff back to that exact sealed publication.

On successful ordinary authoring, the handoff replaces mutable run state only
inside the existing `--events-stdout-jsonl` command-result envelope. Legacy
human/plain-JSON CLI output remains the run state. No result-index search,
provider call, workspace mutation, lifecycle authority, custody change, or
editorial capture occurs.

## API consumer shape

API may extend its existing structured stdout capture to recognize exactly one
delivery handoff, validate it through the installed public SBE validator, and
carry `result_id` into `SbeCycleResult.sealed_terminal_result_id`. Native ingress
then performs its existing exact reader validation before any editorial packet
collection. Multiple or conflicting terminal handoffs must fail closed.

## Qualification state

The closed schema, public builders/readers/validators, catalog entry, focused
contract tests, and editorial-review regression set are implemented and green.
A fresh package version and installed API consumer qualification remain required
before API Slice 2B/2C proceeds.
