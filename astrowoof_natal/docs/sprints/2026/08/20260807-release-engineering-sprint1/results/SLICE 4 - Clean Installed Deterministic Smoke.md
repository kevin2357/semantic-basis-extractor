# Slice 4 — Clean Installed Deterministic Smoke

## Result

Slice 4 passes and awaits gate approval. The exact Slice 3 candidate wheel was
installed without dependencies into a fresh CPython 3.12 virtual environment
under `C:\tmp`. Both the invoking directory and runtime module were outside the
checkout, and `--require-installed` rejected checkout fallback by contract.

Artifact SHA-256 remained
`799307597fb33e5717112e0c772983bca2dd78bd193b999a5286e4476f2b4ea4`.

## End-to-end smoke

The installed console command completed packaged projected-input extraction,
all six fake authoring passes, a forced rejection and fresh retry, a separate-
process resume, assembly, registry validation, final QA, delivery integrity,
snapshot validation, and safe cleanup.

The run reached `DELIVERY_COMPLETE` with 50 cards, four summaries, two attempts
for the deliberately rejected pass, five delivery members, matching delivery
manifest hashes, and 20 cleanup targets reclaiming 4,627,864 bytes.

## Exact input and identity boundary

The smoke records AGF 0.6 wheel SHA-256
`d1b357b1ec0e40faf7070b29e5c25d18e54c9507406518f26587aac46300aa95`
and SPC 0.10 wheel SHA-256
`60bd0f18d3b183d2f4c6375447f90881ab6c22c6138b8f9b8ffe69a246015150`.
Its deterministic identity-only derivation substitutes opaque UUID
`550e8400-e29b-41d4-a716-446655440000` for the historical fixture identity and
verifies it through contexts, claims and syntheses under packet provenance,
authoring state, deck, and delivery provenance.

The installed resource set contains 19 members with aggregate SHA-256
`439c8771fe7944ddb1b5b83465b7d2f76f252340624f1b85c85f9278fba55404`,
matching Slice 3 exactly.

## Installed spend and state seam

A second installed-only check prepared an exact initial-authoring action. It
persisted before returning `AWAITING_SPEND_AUTHORIZATION`, appeared in the
public pending-action view, accepted only its exact bound authorization, and
persisted `AUTHORIZED`. Execution deliberately stopped before provider
submission. A legacy paid state without a durable ledger failed closed.

The broader deterministic suite continues to distinguish waiting, warning,
review, hard budget, optional skip, ambiguity, authorization, and delivery
outcomes while preserving accepted evidence monotonically.

## Verification

- installed wheel smoke: pass;
- installed prepare/authorize/public/legacy seam: pass;
- repository suite: 141 passed;
- `git diff --check`: pass;
- live provider calls: zero.

No tag or publication occurred. Slice 5 requires separate explicit approval
for both live-provider work and a real non-illustrative spend policy; the
current sprint flag still forbids live provider work.
