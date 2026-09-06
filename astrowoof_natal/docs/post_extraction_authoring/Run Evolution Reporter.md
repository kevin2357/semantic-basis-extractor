# Run evolution reporter

## Purpose

`astrowoof-run-report` turns an exported worker log into a closed diagnostic
report and human-facing views. It is intended for incident
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

When the export also contains supported API wrapper execution events, `build`
additionally emits:

- `report.timeline.json`: the closed shared-time cohort projection; and
- `report.timeline.html`: a self-contained horizontal cohort swimlane.

Native-only logs retain the original four outputs. To require cohort evidence
and fail explicitly if it is unavailable, use:

```text
astrowoof-run-report timeline --input "cohort logs.txt" --output-dir cohort-report --display-timezone America/Denver
```

An existing timeline artifact can be rendered again without reparsing logs:

```text
astrowoof-run-report render --report cohort-report/report.timeline.json --format timeline-html --output cohort.html --display-timezone UTC
```

The HTML viewer works offline. Choose a run, filter lanes, change epoch density,
select a cell for source-line evidence, or use **No-progress only** to focus on
candidate windows.

The cohort viewer places every run on one absolute axis. It can highlight a
run, hide waits, highlight the existing no-progress candidates, and show exact
source/evidence details for each interval. Lease spans are labeled observed
execution allocations; neither they nor witnessed cross-run handoffs assert
global slot ownership or an SLA.

## Matrix model

Rows are stable semantic lanes: run, lifecycle selection, pass/attempt, paid
action, external authority, provider custody, reconciliation/adoption, local
work, checkpoint/publication, command handoff, and diagnostics. Columns are
semantic epochs produced by registered boundary events. Cells retain the last
directly observed posture and point back to exact line numbers and raw-line
digests.

The JSON stores sparse cell deltas rather than copying the entire matrix at
every epoch. Renderers reconstruct the display deterministically.

Current workers also emit three decision-evidence summaries:

- `native_stage_evidence_summary` appears in the local-work lane after an
  optional-stage attempt is durably classified;
- `native_validation_evidence_summary` appears in the local-work lane with
  report digests and closed code counts; and
- `native_publication_evidence_summary` appears in the checkpoint/publication
  lane with explicit outcome/cause and result/receipt identities.

The parser preserves these registered fields, including bounded comma/semicolon
code distributions. It never retains finding prose, prompts, payloads, or
arbitrary exception text.

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
astrowoof-run-timeline-qa
astrowoof-decision-evidence-observability-qa
```

All qualifications are provider-free and network-free. The first proves
deterministic four-format output, privacy-sentinel exclusion, closed receipt
validation, and no-progress detection. The timeline qualification proves the
public three-run CLI path, closed projection/receipt, shared handoff, incomplete
evidence, no-progress overlay, two deliveries plus one review, and zero provider
activity. The decision-evidence qualification proves the new stage,
validation, and publication summaries survive packaging and parsing, preserve
closed code counts, and cover the recent-investigation replay matrix. Neither
inspects an SBE native workspace.

## Evidence boundary

The matrix is built from SBE evidence. The optional cohort projection joins only
the approved diagnostic subset of API wrapper execution events and retains the
owner and canonical timestamp field on every boundary. API observations do not
become native truth, and native labels do not become scheduler authority.
Missing log evidence never proves an event did not occur.
