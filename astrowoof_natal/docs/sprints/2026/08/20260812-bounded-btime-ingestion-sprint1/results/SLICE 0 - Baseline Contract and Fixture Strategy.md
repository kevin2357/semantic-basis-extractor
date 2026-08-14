# Slice 0 - Baseline Contract and Fixture Strategy

## Result

Gate 0 freezes the pre-refactor exact-Natal behavior, the bounded upstream intake
boundary, fixture custody, and the names of the new bounded contracts. No production
pipeline code changed in this slice.

The machine-readable companion is `slice0-baseline-contracts.json`. Hashes in that
file are lowercase SHA-256. Structured SBE values use canonical JSON with sorted
keys, compact separators, UTF-8, and `ensure_ascii=false` before hashing.

## Exact-Natal baseline

The released default is named `legacy_atomic.v1`. A fresh Bre replay produced 103
candidates, selected exactly 50, rejected 53, and passed extractor QA. Candidate,
selected-portfolio, packet, and QA identities are frozen in the companion file.

The source release smoke also passed through `DELIVERY_COMPLETE` with 50 cards, four
summaries, matching delivery hashes, and the frozen 30-resource aggregate identity.
This is the semantic boundary Slice 1 must preserve while moving exact rules behind
a policy seam. Path-bearing or otherwise operational smoke fields are deliberately
not treated as semantic identities.

## Sanitized repository-scale fixture

SBE adopts SPC 0.11.0's sanitized
`tests/fixtures/agf/bounded_natal_v1_tiny.json` as the source fixture. SPC remains its
custodian; SBE records its hash and generates the four projected artifacts through
SPC's public `semantic_projection.bounded_cli`. Generated artifacts are not yet
vendored because the bounded dependency and intake adapter land in Slice 3.

The generated four-context family passes SPC's official schemas and
`validate_parallel_bounded_contexts()`. It has two object correspondences and one
relationship correspondence. This small family is the fast positive contract
fixture. Slice 3 may package either the minimized projected family or a deterministic
derivation helper, but its recorded semantic identities must remain stable.

## Full-scale fixture custody

The supplied 27 MB expanded family remains external. Git retains only its archive
hash, compact metrics, and semantic validation identities. It is the controlled
full-scale qualification case: AGF 0.8.1, SPC 0.11.0, 106 objects, 1,520
relationships, 43 projected terms per context, and 1,544 evidence records. Both
official schema validation and parallel-context validation passed.

Requalification requires the exact archive hash recorded in the companion file,
an isolated SPC 0.11.0 runtime, validation of each of the four artifacts against
`projected_bounded_semantic_graph.v1`, and a passing specialized parallel-family
report. The archive must not be copied into the repository or into release wheels.

## Frozen bounded names

The seven names in `reserved_contract_names` are reserved for this sprint. A later
slice may add a numeric contract version alongside the string schema identity, but
must not silently reuse a name for incompatible bytes. These are separate from the
legacy exact packet and card schemas.

## Compatibility qualification

SPC 0.11.0 officially publishes and runtime-validates the bounded graph contract,
schemas, four contexts, and specialized validators. The supplied AGF 0.8.1 output
passes that exact runtime boundary. SPC's prose compatibility table currently names
AGF 0.8.0 rather than 0.8.1, so SBE records a documentation qualification gap:
runtime evidence supports the supplied 0.8.1 artifact, but SBE will not claim that
SPC's published compatibility prose already names 0.8.1. Slice 3 must pin exact
supported releases and state this distinction explicitly.

## Gate decision

Verification completed on 2026-08-14:

- focused baseline tests: 3 passed;
- full repository suite: 218 passed in 145.319 seconds;
- source release smoke: passed;
- freshly built, isolated, offline-installed wheel smoke with
  `--require-installed`: passed;
- SPC 0.11.0 official schema and parallel-family checks: passed for the sanitized
  and supplied full-scale families; and
- `git diff --check`: passed (Git emitted only the repository's expected Windows
  line-ending notices).

Gate 0 is ready for review. Production refactoring remains paused until approval.
