# API review — Slice 3 relocation capability fence

## Decision

**Approved for the stated read-only relocation boundary.** This is compatible
with API Sprint 90's authority-bound assessment intake and does not broaden
that sprint into native suspension or executable-workspace authority.

## What the review confirms

- Relocation authority remains exclusive to the dedicated read-only assessment
  reader. API cannot accidentally provide it to resume, reconciliation,
  local-work, publication, retirement, or snapshot-write surfaces because
  those public signatures do not accept it.
- The matrix's byte-for-byte before/after assertions cover the API-host threat:
  a request-isolated restored copy must not become executable merely because
  its checkpoint and relocation authority are valid.
- The new publication ordering is the right narrow correction. Checking the
  durable `stable_logical_absolute_path` invariant before any snapshot/journal/
  result/receipt mutation closes the relocated-copy write seam while retaining
  post-refresh full snapshot validation for an authoritative workspace.
- The retirement result is appropriately a non-eligibility refusal, not an
  implied native stop, capacity release, provider settlement, or custody
  conclusion.
- The new provider-free fixture reaches every listed executable/mutating class
  without provider access and is registered in the maintained suite manifest.

## API integration boundary

API will consume only `read_relocated_operator_disposition_assessment` and the
closed pair validator through the authority-bound wrapper. Its own writer
re-locks the exact checkpoint, generation, archive/inventory digests,
compatibility identity, and logical restore root before it performs the
separate API-local quarantine fence/capacity release.

This review does **not** approve any SBE native suspension, forced termination,
provider reconciliation, resume, retirement, or other workspace mutation from
a relocated copy.

## Remaining release gate

The final cross-package gate must use the released installed wheel with API's
real isolated checkpoint restore shape and `force=False` in-process logging.
It should prove the relocated reader is available, produces the closed wrapper,
and that API's existing writer accepts only the exact bound result. The current
source-level capability fence is necessary but does not replace that installed-
wheel consumer qualification.
