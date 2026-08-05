# Slice 4 — Provenance Implementation

## Result

Slice 4 passed. Every new authoring run now carries a deterministic provenance
record from projected inputs through packaged delivery, while preserving a
strict distinction between observed declarations and unavailable information.

## Provenance contract

Canonical schema: `astrowoof.natal_authoring_provenance.v0.1`.

The operator run records:

- distribution version, Python version and implementation, and platform class;
- every packaged runtime resource with bytes and SHA-256;
- an ordered aggregate resource-set SHA-256;
- every projected context and optional params artifact with bytes and SHA-256;
- allowlisted AGF/SPC declarations present in each projected graph;
- the complete authoring profile;
- provider and service level;
- observed models and attempt count;
- final validation and lint report identities and hashes; and
- completed delivery ZIP identity and hash.

The delivery manifest carries a compact standalone subset: runtime identity,
resource-set identity, complete provenance for that subject's four inputs,
authoring profile, and hashes for the deck and three final reports.

## Upstream evidence policy

The harvester reads only declared fields from `metadata`, `source_identity`,
`source_graph_ref`, `target_ontology`, and `audit`. It does not derive or guess
engine versions, graph versions, source hashes, context versions, registry
versions, or projection identities.

For the Bre fixture, the source explicitly reported:

- SPC projection engine: `0.10.0`;
- projection profile: `woofmapped_astrology.v0` version `0.1.0`;
- canonical source graph: `canonical_astrology_graph` version `1.3.0`;
- source graph hash: `4d1b19c312c8f44ed258b496`; and
- distinct projection/context/audit identities for all four contexts.

Older run-state migrations mark input provenance
`unavailable_from_legacy_run`. Current resource/runtime identity is recorded,
but historical creation-time inputs are not reconstructed.

## Integrity model

Delivery-manifest entries hash the four artifacts that precede the manifest.
The completed ZIP is then hashed into operator state. The manifest does not
attempt to contain its own ZIP digest, avoiding a recursive checksum.

Resource aggregation hashes the ordered tuple of each resource path and its
content digest. This makes the authoring guidance/reference set independently
identifiable even when the distribution version remains unchanged during a
development candidate.

## Verification

Focused provenance tests: 4 passed.

Complete repository suite: 115 passed.

Token-free end-to-end proof:

- run status: `DELIVERY_COMPLETE`;
- projected input contexts: 4;
- input digests: valid SHA-256;
- packaged resource count: 15;
- aggregate resource digest: valid SHA-256;
- final QA reports recorded: validation and lint;
- delivery ZIP digest: valid SHA-256;
- manifest artifact hashes independently recalculated: all matched.
