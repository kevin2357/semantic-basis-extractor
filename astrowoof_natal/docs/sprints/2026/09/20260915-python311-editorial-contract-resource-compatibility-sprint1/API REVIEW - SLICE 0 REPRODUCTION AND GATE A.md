# API review — Slice 0 reproduction and Gate A

## Decision

Slice 0 is approved.  SBE may proceed with Slice 1's narrow correction to
`editorial_review_contracts._resource_bytes()` and its Python 3.11/3.12
regression coverage.

## Evidence assessment

The reproduction establishes causation, not merely correlation:

- the live call shape raises `TypeError` on the actual declared minimum runtime
  (CPython 3.11.15) and succeeds on 3.12.14;
- chained traversal selects byte-identical semantic-contract content on both
  versions (11,604 bytes, SHA-256
  `306fcf0e55c56f5fe48b18eaced64dbb3338ab783a5722a801f7759af96e52e5`);
- missing and malformed resources retain their existing failure classes; and
- the exact boundary matches both independent Render witnesses after every
  native capture phase through packet validation had already succeeded.

The proposed chained traversal is therefore a compatibility restoration, not
a change to selected evidence, packet content, status semantics, or ownership.

## Scope ruling

Keep this release focused on the live
`editorial_review_contracts._resource_bytes()` defect.  The ten explicit and
one starred latent multi-component calls are real Python 3.11 compatibility
risks, but none were implicated by the live witnesses.  Do not broaden this
hot correction silently.  Open a separately reviewed compatibility-sweep
follow-up that classifies each caller's production versus qualification role,
adds its own real-resource coverage, and then applies the same byte-preserving
form only where proven.

`resource_access.py` deserves early priority in that follow-up because it is a
generic accessor; nevertheless, its reach is exactly why it should not be
changed under this narrowly evidenced release without caller coverage.

## Gate B expectations

For the candidate wheel, retain the planned public delivery and terminal-review
capture qualifications on a real Python 3.11 installed wheel, the Python 3.12
contrast, package-byte checks, and source/API consumer gate.  No API, Alloy,
schema, lifecycle, custody, transport, or Better Stack change is required.
