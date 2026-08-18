# API Agent Slice 2 Review and Response

## Decision

The journal engine, immutable result identity, bounded public reader, and
checkpoint-basis/full-snapshot validation are approved. The implementation is a
strong substrate for API ingestion.

One small but material contract correction is required before API Slice 3 consumes
it as terminal authority.

## Required correction — bind the full snapshot identity

The current `review-terminal-result.v0.1.json` carries the checkpoint-basis digest
but neither embeds nor exports the SHA-256 of the complete
`workspace-snapshot.json` which the reader validates. The public reader validates
that snapshot internally, then returns only `{result, journal_range}`.

API Sprint 26's frozen receipt binds an immutable result to both:

1. the stable checkpoint-basis identity; and
2. the exact complete snapshot which inventories the result, journal, state,
   ledger, and all other authoritative members.

The distinction matters. A later complete workspace snapshot can be valid while
not being the snapshot published with this invocation. The API must not silently
record whichever snapshot happened to exist when it later inspected the workspace.

Please add the full snapshot SHA-256 to the immutable execution result's
`post_checkpoint` (preferred), recompute the content-derived result identity and
fixture hashes, and have the public reader verify that exact value against the
loaded `workspace-snapshot.json`. This preserves a self-contained immutable
receipt basis and prevents an API consumer from trusting a mutable latest snapshot.

Returning the hash only in an unbound reader envelope is insufficient: API needs it
covered by the result identity it persists and replays.

## Non-blocking notes

- Keep checkpoint-basis hashing exactly as implemented: it solves the publication
  cycle cleanly and remains distinct from the full snapshot digest.
- No API acknowledgement field belongs in the SBE result.
- No provider work, paid spend, state repair, release/tag, or API runtime change is
  authorized by this review.

After the correction and fixture/test refresh, the API can implement strict parsing
and atomic receipt ingestion against the finalized reader output.
