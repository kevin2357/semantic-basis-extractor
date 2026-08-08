# Slice 0 — Baseline and Release-Coordinate Audit

## Result

Slice 0 audit work is complete and awaiting gate approval. No package metadata,
runtime code, wheel, tag, or published release was changed.

## Source baseline

- Pre-sprint runtime baseline: `4ea2e17` (`Minimize provider data and validate
  run snapshots`).
- Planning scaffold commit: `edb6c93`.
- Predecessor tag: `astrowoof-natal-authoring-v0.1.0`.
- Predecessor tag commit: `8fdad164b151c87f77dfc416f6efb754cf00fd7b`.
- Current package metadata remains `0.1.0`; no version change has begun.
- Current Python floor remains `>=3.11`; the local qualification interpreter
  is CPython 3.12.13.

Since the predecessor release, the component gained opaque source identity,
provider-spend authorization, run schema v0.9, provider disclosure
minimization, durable exact-path snapshots, evidence-scope provenance, tests,
and consumer/release documentation. The committed diff from the v0.1 tag to
the planning baseline is 32 files, 2,571 insertions, and 76 deletions.

## Version recommendation

Recommend distribution version `0.2.0` and annotated tag
`astrowoof-natal-authoring-v0.2.0`.

This is a minor-version increment within the pre-1.0 series because it adds
substantial new consumer contracts and operational capabilities. It also
changes paid-run resume compatibility: pre-v0.9 OpenAI run state fails closed
because spend and snapshot evidence cannot be reconstructed. A `0.1.x` patch
would understate that integration impact.

The recommendation is not yet approved. `pyproject.toml`, package fallback
version, release directories, and tag names remain unchanged until the Slice 0
gate is approved.

## Proposed exact compatibility tuple

### Upstream artifacts

- Astrology Graph Foundry `0.6.0`
  - tag: `astrology-graph-foundry-v0.6.0`
  - tag/qualified commit: `e36284af0f04e7380113ab141731e18f378ea2dc`
  - wheel: `astrology_graph_foundry-0.6.0-py3-none-any.whl`
  - SHA-256: `d1b357b1ec0e40faf7070b29e5c25d18e54c9507406518f26587aac46300aa95`
  - canonical graph contract: `canonical_astrology_graph` `1.3.0`
- Semantic Projection Core `0.10.0`
  - tag: `semantic-projection-core-v0.10.0`
  - tag commit: `68f11c56ff1ad26873958cf955b7f3699895e870`
  - qualified artifact commit recorded by its release manifest:
    `caa4e3c5243b226d914b8c36ca5dcbeaeb885232`
  - wheel: `semantic_projection_core-0.10.0-py3-none-any.whl`
  - SHA-256: `60bd0f18d3b183d2f4c6375447f90881ab6c22c6138b8f9b8ffe69a246015150`
  - projection engine: `0.10.0`

### SPC semantic resources

- profile: `woofmapped_astrology.v0@0.1.0`;
- general context: `woofmapped.doghouse.general.v0@0.1.0`;
- direct-to-dog context: `woofmapped.dog_direct.v1@1.0.0`;
- handler context: `woofmapped.handler_guidance.v1@1.0.0`;
- hybrid context: `woofmapped.hybrid_horoscope.v1@1.0.0`; and
- projected registry:
  `woofmapped_astrology.projected_terms@0.1.0`.

### SBE/Closure candidate boundary

- proposed distribution: `astrowoof-natal-authoring==0.2.0`;
- Python: `>=3.11`, with CPython 3.12.13 as the reproducible-build and primary
  local qualification interpreter;
- input contract: `astrowoof.projected_natal_input.v0.1`;
- subject params: `astrowoof.subject_params.v0.1`;
- operator state: `astrowoof.semantic_closure_run.v0.9`;
- provider ledger/authorization/reconciliation: v0.1 contracts;
- provider disclosure: `astrowoof.provider_disclosure.v0.1`;
- workspace snapshot: `astrowoof.semantic_closure_snapshot.v0.1`;
- delivery manifest: `astrowoof.natal_delivery_manifest.v0.1`; and
- price book: `openai-public-2026-08-07.v1`.

The intended OpenAI routing set is Terra for initial/fixed and creative-retry
authoring, and Luna for polish, critic, and qualitative candidate, unless the
approved generation profile explicitly selects another price-book-supported
route. Actual dollar ceilings must be supplied and authorized by the consumer;
this sprint does not define default allocations.

## Audit findings

1. The source implementation and focused tests accept one common non-empty
   opaque source identity across all four contexts and reject mixed identities.
2. The packaged Bre smoke fixture still declares historical `natal:bre` source
   identity. It proves SPC 0.10 and canonical graph 1.3 compatibility, but does
   not prove the AGF 0.6 opaque/UUID identity path required for this release.
3. Slice 1 must use exact pinned-wheel output or a derived immutable release
   fixture carrying a UUID-style identity, and assert that identity through
   claims, syntheses, authoring state, delivery provenance, and installed smoke.
4. Existing package metadata is intentionally still v0.1.0. Updating it before
   this gate would make the audit alter the candidate it is meant to define.
5. v0.1.0 remains immutable at its tag. Main-branch retrospective/publication
   records do not move or rewrite that tag.
6. The release playbook and contract catalog already enumerate the new spend,
   disclosure, snapshot, provenance, and state qualification requirements.
7. No current release tag conflicts with the proposed v0.2.0 tag.

## Gate recommendation

Approve:

1. target distribution version `0.2.0`;
2. target tag `astrowoof-natal-authoring-v0.2.0`;
3. the exact AGF/SPC artifacts and semantic-resource tuple above;
4. CPython 3.12.13 as the reproducible-build interpreter while retaining the
   declared `>=3.11` package floor; and
5. Slice 1 creation of exact opaque-identity compatibility evidence from the
   pinned upstream artifact boundary.

After approval, update the plan's release coordinates and begin Slice 1. Do
not yet update package metadata; that remains scheduled for Slice 3 after the
contract/safety gates.

## Verification

- predecessor annotated tag resolved locally: pass;
- upstream tags, versions, manifests, and published checksums inspected: pass;
- current contract catalog parsed and audited: pass;
- release playbook audited: pass;
- working diff whitespace check: pass;
- wheel build, installed smoke, live provider call, tag, and publication: not
  performed by design.
