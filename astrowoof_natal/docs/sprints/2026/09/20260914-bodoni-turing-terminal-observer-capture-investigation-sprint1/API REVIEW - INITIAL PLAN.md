# API review — initial plan

Reviewed the initial plan and approve its staged, read-only investigation shape.
The frozen fences, export-capping distinction, provider-free Slice 1, and separate
owner gates are all appropriate.

## Evidence update

The capped original `sbe-worker-terminal-observer-20260915-07.log` has now been
replaced with three unfiltered five-minute files covering the full original
window. Their line counts are 513, 356, and 326, respectively, so none reaches
Render's 1,000-line export cap. `BACKGROUND.md` contains the exact paths and
windows.

## One wording correction

Slice 1 should not call the observed failure an *expected* exception. The live
signature proves that `build_editorial_review_runtime_capture(...)` raised an
exception caught by the observer's deliberately broad local-capture catch set
(`EditorialReviewTransportError`, `OSError`, `ValueError`, `KeyError`, or
`TypeError`) and returned `branch=unavailable`. It does not yet classify that
exception as contractually expected or unexpected.

The absence of `capture failed` remains a separate telemetry fact. `_report_phase`
intentionally suppresses reporter exceptions, so a rejected/failed sink emission
is plausible; the completed event's absence is likewise an observability gap to
map, not evidence that the wrapper never returned.

Proceed with Slices 0--1. Do not request retained-workspace coordinates or start
runtime correction work until Review Gate A.
