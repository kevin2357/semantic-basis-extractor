# Evidence — run timeline progressive identity join correction

## Focused verification

```text
python -m unittest astrowoof_natal.tests.test_run_timeline astrowoof_natal.tests.test_run_report
Ran 40 tests
OK (skipped=1)
```

The skip is the expected optional `jsonschema` dependency cell.

## Production-shaped acceptance

Input:

`C:\tmp\astrowoof-most-recent-three-pup-cohort-inner-20260906.log`

Corrected artifacts:

- `C:\tmp\astrowoof-most-recent-three-pup-swimlane-corrected-20260906\report.timeline.json`
- `C:\tmp\astrowoof-most-recent-three-pup-swimlane-corrected-20260906\report.timeline.html`

| Measure | Released 0.4.52 behavior | Corrected behavior |
|---|---:|---:|
| wrapper candidates | 193 | 193 |
| accepted wrapper events | 66 | 138 |
| refused wrapper lines | 72 | 0 |
| unpaired API markers | 51 | 19 |
| observed allocation intervals | 0 | 24 |
| initial-wave intervals | 0 | 3 |
| reconciliation intervals | 0 | 13 |
| v2 dispatch intervals | 0 | 6 |
| delivery-validation intervals | 0 | 2 |

The 19 remaining unpaired markers comprise 14 `worker.job.claimed`, three
`sbe.closeout.completed`, and two `worker.job.completed` events. They are not
failed cycle/lease joins and remain conservatively visible pending any future
approved interval grammar for those standalone boundaries.

## Safety boundary

- No provider, R2, API database, or retained workspace access occurred.
- No authoring, lifecycle, custody, or command-result contract changed.
- The timeline remains diagnostic-only.

