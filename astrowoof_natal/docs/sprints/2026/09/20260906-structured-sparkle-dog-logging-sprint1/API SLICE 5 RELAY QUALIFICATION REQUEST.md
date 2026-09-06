# API Slice 5 relay qualification request

## Purpose

SBE Slices 0–4 are complete. Slice 5 requires evidence through API's actual
subprocess construction and stderr handling; an SBE-only relay imitation would
not prove the production boundary.

## Exact API surfaces already identified

The relevant implementation is
`src/astrowoof_api/services/sbe_provider_orchestration.py`:

- ordinary resume selects inherited stderr only when event streaming is
  enabled and otherwise selects `subprocess.DEVNULL`;
- v2 dispatch follows the same configured inherit/suppress distinction; and
- provider reconciliation captures child stderr with `subprocess.PIPE` and
  writes each received line verbatim to API-facing stderr.

Existing tests near the following cases already prove pieces of the transport:

- `test_live_process_runtime_heartbeats_without_capturing_provider_output`
- `test_live_process_runtime_can_inherit_native_event_stream`
- `test_live_process_runtime_relays_sanitized_reconciliation_trace_and_keeps_json_private`

## Requested qualification matrix

1. Replace/add a reconciliation fixture containing one exact valid
   `astrowoof.sbe_worker_log.v1` line. Prove the API-facing stderr receives the
   identical bytes as one line—no prefix, wrapper, escaping, splitting, or
   field rewriting. Prove authoritative JSON stdout remains private to parsing.
2. For ordinary resume with event streaming enabled, prove `stderr=None` and
   structured logging cannot contaminate captured command-result stdout.
3. For ordinary resume with event streaming disabled, prove
   `stderr=subprocess.DEVNULL`, `stdout=subprocess.DEVNULL`, and classify the
   absence of Render-facing SBE diagnostics as intentional suppression.
4. Repeat the enabled/disabled assertions for v2 constrained dispatch. When
   enabled, command-result/event stdout parsing remains authoritative and
   independent of inherited application stderr.
5. Assert no route interprets an application-log record as a command result or
   execution event.
6. Use a privacy sentinel in an SBE-generated test record and prove it is absent
   from relayed stderr, API's bounded stderr tail, and any parsed diagnostic
   artifact. Do not claim API performs general redaction; the expected
   protection is SBE handler sanitization.

## Evidence requested back to SBE

- API commit/revision under test;
- installed SBE source/wheel identity used to generate the record;
- focused test names and results;
- exact route matrix showing `verbatim`, `inherited`, or
  `intentionally_suppressed`;
- confirmation that stdout command results and execution-event JSONL are
  unchanged; and
- any route where deployed configuration differs from the tested default.

This request authorizes provider-free tests only. It does not authorize a live
provider call, QA mutation, deployment, or an API authority-contract change.
