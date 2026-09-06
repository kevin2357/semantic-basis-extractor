# API Slice 5 Relay Qualification Result

## Verdict

Passed provider-free. The API-owned subprocess routes have an explicit tested
structured-log transport matrix. No API runtime behavior changed.

## Focused test evidence

```text
.venv\Scripts\python.exe -m pytest tests\test_sbe_provider_orchestration.py -q
37 passed in 1.95s
```

The API companion evidence is in:

`C:\dev\github\astrowoof-api\docs\sprints\2026\09\20260906-structured-sparkle-log-relay-qualification-sprint84\EVIDENCE.md`

## Exact route matrix

| API route | Event-stream configuration | stderr | Authoritative result transport | Classification |
| --- | --- | --- | --- | --- |
| Provider reconciliation | N/A | `PIPE`, relayed byte-for-byte line by line | private captured stdout JSON | `verbatim` |
| Ordinary resume | enabled | inherited (`None`) | separately captured stdout JSONL | `inherited` |
| Ordinary resume | disabled | `DEVNULL` | `DEVNULL` | `intentionally_suppressed` |
| Constrained v2 dispatch | enabled | inherited (`None`) | exact command-result output file | `inherited` |
| Constrained v2 dispatch | disabled | `DEVNULL` | exact command-result output file; process stdout `DEVNULL` | `intentionally_suppressed` |

The reconciliation fixture is a closed
`astrowoof.sbe_worker_log.v1` application-log record. The test proves it is
relayed unchanged on API-facing stderr while its reconciliation command result
remains private to the API parser. A structured application log on the resume
JSONL channel cannot satisfy the terminal command-result discriminator.

The privacy fixture models an already-sanitized SBE record. Its raw relayed
line and bounded API stderr tail contain no pre-sanitization sentinel. This is
not a claim that API generically redacts native output.

## Identity and scope

The local API test environment has `astrowoof-natal-authoring` 0.4.50
installed; the fixture is explicitly shaped as SBE's v1 log contract. No
provider call, QA/R2/database access, retained-run operation, deployment, or
configuration change occurred. No route treats an application-log record as an
authority-bearing command result or execution event.
