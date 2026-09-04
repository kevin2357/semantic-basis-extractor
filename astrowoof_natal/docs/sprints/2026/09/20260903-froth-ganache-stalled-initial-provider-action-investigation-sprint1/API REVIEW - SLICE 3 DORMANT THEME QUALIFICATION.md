# API review — Slice 3 dormant theme qualification

## Decision

Reviewed the source qualification and the direct Ganache-shaped fixture.
The scope remains appropriately narrow:

- the production six-pass workspace no longer creates or requests
  `ASSIGN THEME GROUPS.md`;
- a retained legacy artifact with a valid registry and an unregistered
  `grounded_companionship` assignment is harmless;
- delivered decks omit the dormant registry and per-card assignment surface;
- the compatibility report explicitly reports no authored theme priorities;
- no lifecycle, provider, custody, reconciliation, terminal-result, or API
  contract behavior is changed.

The source fixture reaches the real complete multi-pass `assemble()` path, so
it directly covers the Ganache assembly failure rather than only unit-testing a
parser helper. The evidence stated for the focused provider-free suite (51
passing) and clean whitespace check is sufficient for the source gate.

## Approval

**Approved for the clean-wheel and installed-artifact qualification gate.**
Use a fresh patch version and preserve the stated release evidence: installed
focused tests, import/resource smoke checks, and exact final artifact identity.

This approval does not authorize retained-QA recovery, worker resume, provider
activity, or an API deployment. API's independent stale terminal-capacity fix
remains a separate concern.
