# Slice 4 — Completed Run Retention Hygiene

## Goal

Reduce completed-run disk usage without weakening resume safety before
completion or removing the evidence needed for cost, QA, retry, and editorial
audit afterward.

## Policy

Cleanup is explicit and terminal-state-only. The runner refuses any run whose
top-level state or subject state is not a successful delivery state.

Before planning deletion it verifies:

- `run.json` and complete subject records;
- final deck, assembly, validation, and lint reports;
- delivery ZIP integrity;
- every accepted pass workspace; and
- every source pass ZIP and its integrity.

Only reconstructable expanded copies are targets. Request/response logs, raw
Batch artifacts, authored-field payloads, QA reports, accounting, accepted
prose, and deliveries remain directly available.

## Interface

```powershell
python src/author_semantic_closure.py `
  --cleanup-completed-run C:\path\to\run `
  --cleanup-dry-run
```

Omit `--cleanup-dry-run` to execute and write `cleanup-report.json`.

## Verification

Focused tests cover:

- refusal of nonterminal state;
- ZIP and retained-artifact preconditions;
- dry-run nonmutation;
- exact conservative target selection;
- preservation of accepted prose, source archives, final artifacts, and
  request evidence;
- successful deletion; and
- idempotent zero-target rerun.

A dry run against the completed Ella subtitle test identified nine directories
and 1,471,698 reclaimable bytes. Execution removed exactly those nine targets.
An immediate second dry run reported zero targets and zero bytes, while all
accepted workspaces, source ZIPs, request/response records, accounting, final QA,
deck, and delivery artifacts remained present.

## Explicit boundary

Raw Batch JSONL evidence remains uncompressed and retained. If production volume
later makes that material dominant, a separate archive tier should define
checksums, lookup/index behavior, restoration, and lifecycle policy rather than
quietly broadening this command.
