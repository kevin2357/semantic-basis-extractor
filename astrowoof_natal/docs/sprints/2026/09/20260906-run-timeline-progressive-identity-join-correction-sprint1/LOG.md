# Log — run timeline progressive identity join correction

## 2026-09-06

- Created the corrective sprint from the first real post-release cohort run.
- Confirmed 1,825 native structured log events, 107 native execution events,
  and 193 API wrapper candidates in the retained export.
- Confirmed deployed `sbe.cycle.started` and `worker.lease.acquired` events omit
  `native_run_id`, while matching completions/releases supply it.
- Confirmed the released adapter rejects those starts and uses an unnecessarily
  strict native-inclusive pairing key.
- Changed wrapper admission to permit an absent native identity while retaining
  strict API run identity.
- Added a bijective API/native mapping pass and enriched only events whose API
  run has an expressly witnessed native identity.
- Removed redundant native identity from wrapper pair keys.
- Added production-shaped positive coverage plus unresolved and contradictory
  mapping negatives.
- Focused timeline/reporter suite passed: 40 tests, one expected optional-schema
  skip. `git diff --check` reported no whitespace errors.
- Regenerated the complete three-run cohort. Accepted wrapper records increased
  from 66 to 138, refused records fell from 72 to zero, and unpaired API markers
  fell from 51 to 19.
- Froze release version `0.4.53` before release-bound testing and regenerated
  the version-bound providerless-denial fixture digest.
- Expanded focused gate passed: 52 tests with four expected optional-dependency
  skips. The broad/full suite was deliberately not run under the focused-patch
  provision of the maintainer release playbook.
- Committed/pushed artifact source as `0c183f7`.
- Built twice from clean exports of `0c183f7` with
  `SOURCE_DATE_EPOCH=1788730669`; both wheels were 1,248,102 bytes with SHA-256
  `78db0fae4f7858b831a0c036cb3bf693a9f9bd38cceafb2b0a729cedc22a5f04`.
- Installed that exact wheel outside the checkout with SPC `0.11.1`; `pip
  check`, packaged-resource inspection, public timeline QA, and the real-cohort
  CLI acceptance all passed.
- Committed the first release-lock record as `9918b2c`, then rebuilt twice from
  that exact commit with recorded final epoch `1788731058`. Both final wheels
  were 1,248,102 bytes with SHA-256
  `db13b03d697114c64375635e4564032afb9155998f53e6d6b9186e127c563246`.
- Repeated clean installed qualification from that final candidate; SBE
  `0.4.53`, SPC `0.11.1`, `pip check`, public QA, and real-cohort acceptance all
  passed.
