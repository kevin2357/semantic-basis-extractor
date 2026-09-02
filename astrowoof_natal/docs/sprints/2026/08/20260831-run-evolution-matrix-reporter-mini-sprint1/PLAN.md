# Plan — deterministic run reporter and evolution matrix

## Status

Slices 0–5 are implemented and source-qualified. The supplied complete worker
log has been rendered into all four formats. Release integration is now planned
as Slice 3 of the Crumpet/Baguette theme-policy feature release; installed-wheel
qualification remains required before publication.

## Objective

Build a deterministic, provider-free reporter that converts SBE worker logs
into:

1. a closed normalized run-report JSON artifact;
2. a compact Markdown evolution matrix;
3. a self-contained interactive HTML view; and
4. optionally Mermaid/SVG timeline exports derived from the same artifact.

The report is diagnostic and reproducible. It is never transition authority.

## Proposed architecture

```text
raw Render export
    │
    ├─ line classifier ── JSON execution/command envelopes
    │                   └─ ✨🐶 trace records
    │
    ├─ strict normalizer/event registry
    │
    ├─ run/action/pass partitioner
    │
    ├─ deterministic state reducer
    │      observed / unknown / contradictory
    │
    ├─ semantic epoch compressor
    │
    └─ closed report.json
           ├─ report.md
           ├─ report.html
           └─ report.mmd / report.svg
```

## Deterministic parsing rules

- Preserve source file digest, line number, outer Render timestamp, and raw-line
  digest for every accepted record.
- Parse the exact `✨🐶` prefix fields: inner timestamp, level, host, run ID,
  action/context ID, function, current state, and message.
- Parse only registered event names and registered typed keys. Unknown events or
  fields remain bounded opaque diagnostics; they never acquire invented meaning.
- Use source order as the final tie-breaker for equal timestamps.
- Partition records by native run ID before reduction. Keep `run_id=-` records
  in a separate global lane unless an explicit invocation identity joins them.
- Preserve duplicate events in normalized evidence while allowing visual
  collapse with an exact repetition count.
- Redact/omit prompt, payload, credential, endpoint query, subject content, and
  unapproved filesystem fields even when malformed input contains them.
- Emit parse coverage, refused-line counts, unknown-event counts, and truncation
  warnings prominently.

## Canonical report shape

Tentative contract: `astrowoof.sbe_run_evolution_report.v1`

- input file identity/digest and parser version;
- exact parse coverage and diagnostics;
- ordered runs;
- per-run compatibility/version/host/time bounds;
- normalized events with source pointers;
- entity inventory (passes, attempts, actions, provider IDs);
- semantic epochs and their boundary reasons;
- matrix rows/cells;
- durations where start/end evidence is directly joinable;
- repetition/no-progress candidates with evidence pointers;
- contradictions and unknowns;
- final observed posture, explicitly not an authoritative current state; and
- report digest.

## No-progress detection

Do not define a loop as “same status appeared twice.” Flag a candidate only when
the same semantic posture recurs without any accepted progress witness between
observations. Progress witnesses include revision/snapshot change only when the
associated event proves meaningful native change; provider identity durability,
adoption, operation-key consumption, action transition, publication, and branch
change are stronger witnesses.

The reporter labels exact posture replays and checkpoint-only semantic
republications as distinct candidates. Neither classification is automatically
called a defect.

## Slices

### Slice 0 — grammar and corpus characterization

- Freeze the prefix and message-token grammar from the supplied full log.
- Inventory every current event name and typed field.
- Measure exact parse coverage and identify JSON-envelope/non-trace lines.
- Freeze privacy exclusions and malformed-line behavior.
- Produce a hand-worked matrix for both supplied runs.

**Completed:** 827/827 marked trace lines parsed across two interleaved runs;
124 command envelopes recognized; no malformed or unknown registered event.

### Slice 1 — normalized event parser

- Implement a pure library parser with no network/workspace access.
- Add source-line and raw-digest provenance.
- Add strict event registry plus safe unknown-event representation.
- Add fixtures for interleaved runs, malformed prefix, duplicate lines,
  equal timestamps, truncation, unexpected encoding, and privacy sentinels.
- Prove byte-identical normalized output for byte-identical input.

### Slice 2 — run reducer and semantic epochs

- Build run/action/pass/provider inventories.
- Reduce only directly supported transitions.
- Preserve observed/unknown/contradictory as distinct values.
- Collapse repeated fingerprints without deleting evidence.
- Compute joinable durations and no-progress candidates.
- Test reordered timestamps, missing middle segments, mixed hosts, and partial
  exports.

**Completed:** sparse semantic epoch deltas, source provenance, timing summaries,
and exact/semantic no-progress candidate classes are implemented.

### Slice 3 — matrix and timeline renderers

- Deterministic Markdown table for code review and sprint evidence.
- Self-contained HTML with lane expand/collapse, filtering, tooltips, and source
  evidence drawer.
- Optional Mermaid sequence/state summaries for documentation.
- Accessibility: symbols/text remain meaningful without color.
- Large-run behavior: horizontal paging/zoom and configurable epoch compression.

### Slice 4 — CLI and qualification

Tentative commands:

```text
astrowoof-run-report parse --input worker.log --output report.json
astrowoof-run-report render --report report.json --format md|html|mermaid
astrowoof-run-report build --input worker.log --output-dir report/
```

- Inputs are local files only.
- No provider credentials, network, R2, workspace mutation, or transition
  command is accepted.
- Qualification parses the sanitized supplied-log fixture or a minimized
  equivalent and verifies report/matrix byte identity.

### Slice 5 — operational adoption decision

- Decide whether this remains repo tooling or becomes an installed SBE command.
- Document how API and SBE exports can later be joined without conflating their
  authority domains.
- Consider a browser-only viewer that accepts local report JSON.
- Add syntax/render checks if diagrams become maintained documentation.

**Completed decision:** ship as opt-in installed SBE tooling in the next normal
release. It is useful immediately for local/Render log exports but remains
diagnostic-only and has no execution authority.

### Release adoption

The selected next normal release is the combined feature/tooling release in:

`20260902-crumpet-baguette-post-retry-terminal-review-investigation-sprint1`

That sprint owns packaging, installed-wheel qualification, versioning, and
release approval. This mini-sprint remains the reporter's design and source
qualification record.

## Scope guardrails

- Logs remain diagnostic, not lifecycle/custody/settlement authority.
- No automatic repair, resume, denial, retry, or quarantine action.
- No private workspace reconstruction from logs.
- No claim that missing log evidence means an event did not happen.
- No dependency on Render-specific APIs for v1; exported text is sufficient.
- No image-generation model in the deterministic path.

## Rough effort

- Useful parser + Markdown matrix prototype: small-to-medium, roughly one focused
  sprint.
- Robust reducer, HTML viewer, adversarial fixtures, and installed packaging:
  medium, likely several slices.
- Cross-repo joined API/SBE visualization: separate follow-up because it needs a
  frozen correlation contract and different authority semantics.
