# Run evolution reporter

## Purpose

`astrowoof-run-report` turns an exported SBE worker log into one closed
diagnostic report and three human-facing views. It is intended for incident
review, run comparison, and spotting likely no-progress cycles without opening
a native workspace.

It never resumes, repairs, retrieves, authorizes, denies, or mutates a run. A
report is not lifecycle, custody, settlement, or terminal authority.

## Build a report

```text
astrowoof-run-report build --input "sbe logs.txt" --output-dir run-report
```

The output directory contains:

- `report.json`: canonical diagnostic artifact;
- `report.html`: self-contained interactive matrix;
- `report.md`: review-friendly sampled matrix; and
- `report.mmd`: compact Mermaid sequence source.

The HTML viewer works offline. Choose a run, filter lanes, change epoch density,
select a cell for source-line evidence, or use **No-progress only** to focus on
candidate windows.

## Matrix model

Rows are stable semantic lanes: run, lifecycle selection, pass/attempt, paid
action, external authority, provider custody, reconciliation/adoption, local
work, checkpoint/publication, command handoff, and diagnostics. Columns are
semantic epochs produced by registered boundary events. Cells retain the last
directly observed posture and point back to exact line numbers and raw-line
digests.

The JSON stores sparse cell deltas rather than copying the entire matrix at
every epoch. Renderers reconstruct the display deterministically.

## No-progress candidates

The detector does not equate a repeated status with a loop. It requires:

1. the same semantic lifecycle posture;
2. at least one completed command boundary between observations; and
3. no stronger progress witness between them.

It distinguishes:

- `candidate_exact_no_progress_cycle`: checkpoint identity and semantic posture
  both recur; and
- `candidate_semantic_republication_cycle`: checkpoint/revision changes but the
  same semantic work selection recurs without a stronger progress witness.

Both are review prompts, not defect verdicts. Partial log windows can omit the
event that would disprove a candidate.

## Privacy and provenance

Only registered safe fields are retained. Prompt, payload, credentials, subject
content, endpoint queries, arbitrary paths, and unknown values are not copied.
Every parsed line retains its source line and SHA-256; the report binds the
source-file digest, parser version, coverage, and report digest.

## Qualification

```text
astrowoof-run-report-qa
```

The qualification is provider-free and network-free. It proves deterministic
four-format output, privacy-sentinel exclusion, closed receipt validation, and
no-progress detection. It does not inspect an SBE native workspace.

## Known boundary

This first version parses SBE worker logs only. A joined API/SBE view should be a
separate contract because API queue/custody truth and SBE native truth have
different owners. Missing log evidence never proves an event did not occur.
