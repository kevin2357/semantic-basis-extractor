# Slice 1 — Contract and Integration Qualification

## Result

Slice 1 implementation and deterministic qualification pass. The result is
awaiting gate review and commit.

Opaque caller-owned identity now participates in the packaged release smoke.
The deterministic fixture uses
`550e8400-e29b-41d4-a716-446655440000` as the shared source identity across all
four SPC contexts while retaining `bre` as the package routing subject.

## Exact upstream evidence

The published artifacts were downloaded through their GitHub releases and
independently hashed:

- AGF 0.6.0 wheel:
  `d1b357b1ec0e40faf7070b29e5c25d18e54c9507406518f26587aac46300aa95`;
- SPC 0.10.0 wheel:
  `60bd0f18d3b183d2f4c6375447f90881ab6c22c6138b8f9b8ffe69a246015150`.

AGF's preserved cross-repository qualification proves its caller-owned opaque
identity reaches SPC unchanged. Its runtime source is identical between the
qualified live commit and final tag; the intervening tag diff contains only
sprint evidence. SPC's release manifest fixes engine/profile/context/registry
versions and the wheel above.

The local platform could not repeat AGF's Swiss-Ephemeris live calculation:
the qualified dependency has no CPython 3.12 Windows wheel and native build
tools are absent. We did not substitute an unqualified astronomy runtime or
claim a fresh AGF calculation. Instead, the SBE fixture derivation changes only
the three explicit `source_identity` carriers in the packaged SPC 0.10
projected fixture. Projected records, scores, registry, graph reference, and
semantic content remain unchanged. The derivation is machine-recorded in the
smoke report.

## Identity propagation

The smoke verifies:

1. all four projected contexts carry the same UUID identity;
2. SBE accepts the UUID independently of routing subject `bre`;
3. the authoring packet retains that identity;
4. all 50 selected claims and every synthesis retain evidence under that
   packet-level source identity;
5. the assembled deck retains the source identity;
6. operator input provenance records the declared UUID; and
7. delivery provenance independently records the UUID.

This preserves the intended model: source identity is authoritative deck-level
provenance rather than duplicated into every claim as a second identity field.
Claim and synthesis evidence remains linked beneath that source declaration.

## Registry, evidence, and state qualification

- Projected-term registry merge/preservation tests pass.
- Extractor closure still requires exactly 50 selected claims with evidence and
  preserves rejected candidates for broader synthesis.
- Delivery provenance separately labels claim-local selected evidence and
  broader summary/whole-dog synthesis evidence.
- Forced pass rejection, cumulative retry, and accepted-state resume remain
  monotonic.
- One matrix test now proves eight distinct outcomes: provider waiting,
  awaiting spend authorization, hard budget exhaustion, ambiguous submission,
  final review, final failure, delivery with warnings, and clean delivery.

## Snapshot concurrency finding

Full-suite execution exposed a real race in whole-directory snapshot hashing:
one concurrent author worker could attest while another was creating its
response workspace. Worker state saves remain atomic, but only the coordinator
now writes the complete snapshot after workers quiesce. A crash before that
point leaves a manifest mismatch and fails closed. The focused reproduction and
full suite pass after this correction; the durable workspace documentation now
states the concurrency boundary.

## Verification

- published AGF/SPC artifact download and SHA-256: pass;
- focused release-contract tests: 12 passed;
- source-tree UUID end-to-end smoke: pass;
- final smoke status: `DELIVERY_COMPLETE`;
- cards/summaries: 50 / 4;
- delivery integrity and manifest hashes: pass;
- snapshot cleanup: pass;
- complete repository suite: 136 passed;
- `git diff --check`: pass.

The exact clean-installed-wheel smoke remains scheduled for Slice 4 after the
candidate artifact is built. No OpenAI call, package version change, wheel
build, tag, or publication occurred in Slice 1.
