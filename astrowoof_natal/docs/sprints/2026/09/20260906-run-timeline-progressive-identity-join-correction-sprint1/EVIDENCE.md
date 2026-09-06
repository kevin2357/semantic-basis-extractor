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

## Focused release gate

Selected because the final diff changes one diagnostic reducer and its
enumerable reporter/CLI consumers. It does not change a lifecycle, workspace,
provider, custody, authority, scheduler, or cross-repository public contract.

```text
Ran 52 tests in 17.175s
OK (skipped=4)
```

The complete repository suite was deliberately not run. This proportionate
gate is owner-approved subject to the final immutable publication decision.

## First committed-source candidate

- Artifact source commit: `0c183f7`
- `SOURCE_DATE_EPOCH`: `1788730669`
- Wheel: `astrowoof_natal_authoring-0.4.53-py3-none-any.whl`
- Size: `1,248,102` bytes
- SHA-256: `78db0fae4f7858b831a0c036cb3bf693a9f9bd38cceafb2b0a729cedc22a5f04`
- Independent clean builds: byte-identical
- Wheel members: 273; forbidden cache/bytecode/build members: zero
- Installed SBE: `0.4.53` from `site-packages`
- Installed SPC: `0.11.1`
- `pip check`: no broken requirements
- Provider calls during qualification: zero
- Timeline qualification receipt SHA-256:
  `2d65be16c87eb1a6f104868957bc3b1b16980f6ca556aaa9a8aab98cad4d31f0`

## Final release-lock candidate

- Release-lock precursor commit: `9918b2c`
- Recorded final `SOURCE_DATE_EPOCH`: `1788731058`
- Two clean builds from that exact commit: byte-identical
- Final wheel size: `1,248,102` bytes
- Final wheel SHA-256:
  `db13b03d697114c64375635e4564032afb9155998f53e6d6b9186e127c563246`
- Fresh installed SBE: `0.4.53` from `site-packages`
- Installed SPC: `0.11.1`
- `pip check`: no broken requirements
- Public `astrowoof-run-timeline-qa`: pass
- Real three-run installed CLI acceptance: pass with 138 accepted wrapper
  events, zero refused wrapper lines, and all expected cycle/allocation classes
- Provider calls, R2 access, and retained workspace access: zero

One final byte-identity confirmation from the documentation-complete release
lock remains before owner authorization to tag and publish.
