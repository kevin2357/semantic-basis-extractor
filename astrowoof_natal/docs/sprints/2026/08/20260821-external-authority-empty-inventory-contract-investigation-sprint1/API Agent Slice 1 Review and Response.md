# API Agent Slice 1 Review and Response

Date: 2026-08-21
Disposition: approved to proceed with Slice 2

## Approved decisions

- Tighten lifecycle inspection v0.5 in place; do not introduce v0.6.
- Adopt both proposed command-conditional tables exactly.
- Reuse and enrich `lifecycle.branch_selected`, `external_authority.refused`, and
  `execution.failed`; do not add an event name/schema version.
- Typed events use counts and digests, while exact action IDs remain in validated
  lifecycle/request documents and redacted operational logs.
- Use the proposed closed, deterministically sorted failed-predicate vocabulary.
- Raise on internally contradictory constructed documents rather than disguising
  programming/persistence defects as truthful native refusals.

## Qualification requirements

- Schema and semantic validation both enforce capacity reason, local readiness,
  capacity `resume_not_before`, and branch `not_before` in addition to the other
  conditional fields.
- Preserve the distinction between unknown retained-incident cause and proven v0.5
  validation gaps.
- Diagnostic sink failure remains unable to affect returned bytes, native state,
  snapshots, authority, or provider behavior.
- Installed-wheel qualification uses packaged/public fixtures, not source-tree test
  helper imports.

