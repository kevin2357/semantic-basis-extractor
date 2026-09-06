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

