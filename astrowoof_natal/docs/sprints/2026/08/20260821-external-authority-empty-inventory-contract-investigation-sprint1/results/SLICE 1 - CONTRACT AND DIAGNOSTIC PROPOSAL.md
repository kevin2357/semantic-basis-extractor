# Slice 1 — Contract and Diagnostic Proposal

Date: 2026-08-21
Status: complete; awaiting joint SBE/API approval

## Decision summary

- Correct lifecycle inspection v0.5 in place.
- Make every API external-authority predicate an explicit native invariant.
- Require nonempty IDs conditionally for `await_external_authority` only.
- Preserve empty IDs for `command=none` typed refusal.
- Keep valid request, typed refusal, and constructed-document failure as three
  machine-distinguishable outcomes.
- Add conditional JSON Schema rules to v0.5 while retaining cross-object equality in
  semantic validation.
- Reuse existing typed event names and enrich bounded safe payloads.
- Emit predicate-level validation diagnostics before raising, without changing
  native state or provider behavior.

The complete proposal and API questions are recorded in
`LIFECYCLE EXTERNAL AUTHORITY INVARIANT PROPOSAL.md`.

## Gate

Slice 1 implementation is intentionally limited to documentation and contract
design. Schema/runtime changes remain withheld pending API approval.

