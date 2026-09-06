# Plan — shared-time cohort swimlane reporter

## Status

Complete. SBE `0.4.52` was built and qualified from the exact release-lock
commit, published under immutable tag `astrowoof-natal-authoring-v0.4.52`, and
verified by fresh download. The separate test-output/parallelization sprint
remains intentionally outside this release.

## Objective

Extend the existing deterministic run evolution reporter with a reusable
horizontal swimlane that aligns every parsed run on one common time axis. The
new view should make cohort overlap, slot serialization, provider waits,
progressive peer latency, no-progress windows, and final outcomes quickly
legible while retaining exact provenance and diagnostic-only semantics.

The existing matrix, Markdown, Mermaid, parser, and report contract remain
supported. This is an additive cohort view.

## Core invariants

1. Every rendered interval is backed by exact accepted events and source
   pointers.
2. Interval end points are joined by closed pairing rules, never inferred from
   the next visually convenient event.
3. Missing or contradictory evidence is rendered as unknown/open, not silently
   classified as waiting or idle.
4. All lanes share the same absolute time domain and deterministic ordering.
5. Source order remains the tie-breaker for equal timestamps.
6. No-progress overlays reuse the existing detector and never become defect
   verdicts.
7. Color is secondary to text/pattern/shape labels.
8. The output remains self-contained, offline, provider-free, network-free,
   privacy-bounded, and non-authoritative.
9. Existing `report.json` v1 consumers and existing renderer outputs do not
   change shape accidentally.
10. API queue/allocation or capacity ownership is shown only when explicit
    approved API evidence exists; SBE observations alone do not manufacture it.

## Proposed interval taxonomy

The exact names are frozen in Slice 0, but characterization starts with:

| Interval class | Representative evidence | Meaning |
|---|---|---|
| deterministic work | job/command start and completion | local deterministic preparation |
| initial provider wave | initial-wave start/completion | active initial provider submission boundary |
| provider reconciliation | reconciliation cycle start/completion | retrieval/adoption cycle |
| external authority v2 | v2 invocation/fence/command completion | constrained ordinary-action dispatch |
| local native work | advertised local operation plus completed command | deterministic fan-in/finalization work |
| delivery validation | delivery command start/completion | final packaged-delivery validation |
| observed execution allocation | matching wrapper lease acquire/release | observed lease window, never global slot ownership |
| provider wait | validated pending/not-due decision boundaries | detached retained provider custody |
| queue/capacity wait | explicit defer/release and next claim boundaries | API-owned waiting, only when evidenced |
| terminal review | sealed typed review result/closeout evidence | native review conclusion, not inferred API policy |
| delivered | accepted delivery/publication evidence | observed delivery completion |
| contradiction/failure | typed refusal or failure boundary | observed exceptional outcome |
| unknown/open | unmatched, partial, or contradictory evidence | intentionally unclassified gap |

Adjacent intervals of the same class may be visually coalesced only if the
underlying evidence list and boundaries remain recoverable in the report.

## Slices and voof-paws points

### Slice 0 — characterize the real cohort and freeze interval grammar

- Feed the 2026-09-06 three-run structured-log cohort through the installed
  parser.
- Inventory the exact events available for command start/completion, defer,
  claim, reconciliation, v2 dispatch, delivery, review, and publication.
- Map the hand-built swimlane segments back to exact normalized events and
  source-line/digest evidence.
- Identify which visually useful waits are directly provable, merely bounded,
  or currently unknowable from SBE-only input.
- Freeze pairing precedence for nested or overlapping commands.
- Freeze behavior for equal timestamps, duplicate events, partial windows,
  unmatched starts/ends, clock reversal, and mixed legacy/structured logs.
- Decide whether the interval projection can be additive inside report v1 or
  requires a new closed report version. Prefer a new projection artifact if
  widening v1 would break exact-key consumers.

Deliverables:

- event-to-interval contract table;
- hand-verified three-run interval fixture;
- schema/version decision; and
- initial privacy and ambiguity matrix.

**Voof-paws 1:** review the interval grammar and evidence claims before schema
or reducer implementation.

**Completed:** characterized the 2026-09-06 three-run cohort, mapped every
displayed interval class to its actual evidence owner, and proved that the
current parser cannot derive the common-clock view from SBE structured records
alone. The required API execution-event adapter and conservative pairing rules
are frozen in `SLICE 0 - COHORT CHARACTERIZATION AND INTERVAL GRAMMAR.md`.

### Slice 1 — closed timeline projection contract

- Define the closed cohort-timeline schema and packaged reader/validator.
- Bind source report ID/digest, parser version, run identities, absolute bounds,
  timezone-display metadata, interval identities, exact evidence pointers, and
  projection digest.
- Keep canonical timestamps in UTC; timezone changes presentation only.
- Represent open/unknown/contradictory intervals explicitly.
- Define deterministic lane ordering and stable interval IDs.
- Carry per-run final observed posture with the existing explicit
  non-authoritative marker.
- Carry existing no-progress candidates by identity and evidence pointer rather
  than recomputing different semantics in the renderer.
- Add closed mutation tests for every authority-sensitive or provenance field.

**Voof-paws 2:** freeze the public diagnostic projection before rendering.

**Completed:** published the closed
`astrowoof.sbe_run_cohort_timeline.v1` schema, reader, and validator. The
contract preserves canonical and outer timestamps, source-line/raw-digest
provenance, evidence ownership, exact correlation identities, explicit
unknown/open/contradictory states, derived interval durations, non-authoritative
final postures, existing no-progress joins, and witnessed-not-SLA cross-run
handoffs. The existing run-evolution report v1 remains unchanged.

### Slice 2 — deterministic interval reducer

- Implement pure event-to-interval pairing over the existing normalized report.
- Keep active execution intervals distinct from the gaps between them.
- Classify waits only from supported defer/pending/not-due/claim evidence.
- Preserve nested command boundaries without double-counting wall-clock time.
- Detect and surface impossible overlaps or end-before-start evidence.
- Coalesce only presentation-equivalent adjacent spans while retaining all
  constituent evidence.
- Compute directly supported cohort observations such as active overlap,
  observed queue latency, due-time lateness, and terminal elapsed time.
- Never derive API resource authority from native labels.

**Completed:** implemented the pure mixed-evidence reducer over the exact log
bytes already bound by run-report v1. API wrapper evidence is adapted through a
closed event allowlist and remains explicitly API-owned; native SBE evidence
retains its own ownership. Pairing uses witnessed source order, exposes open,
orphaned, and clock-contradictory evidence rather than discarding it, derives
lease windows as observed allocations, and derives cross-run handoffs only from
chronologically adjacent completed SBE cycles on the same observed worker
instance. Handoffs are sorted by witnessed chronology with digest only as the
tie-breaker.

Tests:

- one-run and three-run cohorts;
- interleaved lines and equal timestamps;
- partial export beginning/ending mid-command;
- missing completion and orphan completion;
- duplicate/replayed log records;
- clock reversal and conflicting boundaries;
- legitimate partial-wave progress;
- existing exact and semantic no-progress candidates; and
- privacy sentinels in unknown fields and messages.

### Slice 3 — shared-axis interactive HTML renderer

- Add one self-contained horizontal swimlane view using the timeline projection.
- Use one lane per run and one absolute responsive axis.
- Directly label sufficiently wide segments; provide exact accessible detail for
  every segment.
- Support local run selection/highlighting, wait visibility, and no-progress
  highlighting without altering data.
- Distinguish active work, wait, review, delivered, failure, and unknown through
  both labels and visual encoding.
- Mark evidence gaps and partial-window edges honestly.
- Provide useful layouts at narrow, normal, and expanded desktop widths.
- Keep the first render useful without interaction and avoid remote assets.

The renderer must make the 2026-09-06 fairness rotation visually apparent
without embedding run-specific logic or names.

**Completed:** added a deterministic, self-contained renderer for the closed
timeline projection. It uses one absolute cohort domain, one lane per run,
direct interval labels, exact keyboard-accessible evidence details, optional run
highlighting, wait visibility, and existing no-progress highlighting. Open and
contradictory evidence remain visibly distinct. Display timezone changes labels
only and is validated independently from the canonical UTC artifact.

### Slice 4 — CLI and existing-output integration

Preferred CLI behavior:

```text
astrowoof-run-report build --input worker.log --output-dir report
astrowoof-run-report render --report report.json --format timeline-html
```

- Add `report.timeline.html` to `build` output, or document a better stable name.
- Preserve the four existing build outputs and their bytes unless an explicitly
  reviewed version change requires otherwise.
- Permit display timezone selection such as `America/Denver` without changing
  canonical UTC data or projection digest.
- Keep local-file-only operation and reject network URLs.
- Return typed, useful errors for an empty report or no timeline-capable events.
- Update package exports and console help.

**Completed:** added an explicit `timeline` command, `timeline-html` rendering,
and optional timeline output during ordinary `build`. Logs without timeline-
capable evidence retain exactly the original four output names. Timeline input
is local-file-only, display timezone is presentation-only, and the public JSON
reader remains the render boundary for existing artifacts.

### Slice 5 — provider-free qualification and playbook adoption

- Package a sanitized multi-run fixture modeled on the observed three-run
  cohort.
- Prove deterministic projection and byte-identical HTML output.
- Prove one review result and two delivered results on a common axis.
- Prove the observed 102 ms capacity rotation boundary without claiming global
  scheduler authority.
- Prove incomplete exports remain explicitly incomplete.
- Prove no-progress overlays point to the existing candidate evidence.
- Prove no prompts, payloads, generated content, credentials, arbitrary paths,
  or privacy sentinels enter any output.
- Run the installed CLI in a clean environment and open the produced HTML
  offline.
- Update `Run Evolution Reporter.md` and the Better Stack query playbook with a
  short cohort-timeline workflow.

**Voof-paws 3:** consumer/release review after installed qualification.

**Source qualification complete:** added a packaged console qualification that
runs the real public timeline CLI over a sanitized three-run cohort and validates
a closed deterministic receipt. It proves two delivered outcomes, one native
review outcome, the witnessed 102 ms handoff, an explicit open interval, one
existing no-progress candidate, deterministic projection/HTML digests, privacy
sentinel exclusion, and zero provider activity. Clean installed-wheel execution
remains part of release preparation.

### Slice 6 — release preparation, if packaging changed

If the feature changes the installed package:

- choose a fresh unreleased patch version before final regression testing;
- apply the repository release playbook and select focused versus broad tests
  according to the touched surface;
- build twice from the exact release-lock commit and prove byte identity;
- record wheel hash, source commit, epoch, installed qualification receipt, and
  test scope; and
- pause for explicit owner approval before immutable tag/publication.

If implementation remains docs/tooling outside the package, close the sprint
without manufacturing a release.

## Test strategy

The minimum focused set should include:

- current run-report parser/reducer/renderer tests;
- structured sparkle-log fixtures;
- timeline schema/reader mutation tests;
- three-run shared-axis golden fixture;
- incomplete/contradictory interval cases;
- existing no-progress cases;
- CLI build/render tests; and
- installed provider-free qualification.

Escalate to the broad suite if the normalized event model, report v1 schema,
shared parser, CLI build semantics, or package resources change across multiple
consumer surfaces.

## Expected result

The reporter retains its detailed semantic matrix for close inspection and adds
the cohort overview that operators currently lack:

- the matrix answers **what changed inside this run?**
- the swimlane answers **what were all runs doing at the same time?**

Together they should make qualification cohorts, fairness behavior, long waits,
unexpected serialization, and genuine no-progress windows much faster to
understand before any workspace download is considered.
