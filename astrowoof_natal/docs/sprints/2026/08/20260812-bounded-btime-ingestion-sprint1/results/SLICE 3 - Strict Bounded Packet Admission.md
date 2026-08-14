# Slice 3 - Strict Bounded Packet Admission

## Result

SBE now has a separate, provider-free bounded-Natal admission route. It pins
`semantic-projection-core==0.11.0` and exposes
`astrowoof-admit-bounded-natal`. Exact extraction explicitly rejects bounded
artifacts rather than inferring that their superficially similar rows are exact.

Admission requires the official `projected_bounded_semantic_graph.v1` contract,
numeric version `1.0.0`, exact four-context set and versions, bounded profile,
ontology, SPC runtime and semantic-resource identities, supported upstream AGF
contracts, opaque source identity, shared source artifact, anti-precision
capabilities and limitations, registry closure, correspondence structure, and
certainty-invariant epistemic material. Each artifact passes SPC's official schema
validator and the family passes `validate_parallel_bounded_contexts()`.

Failures carry stable status classes (`invalid`, `unsupported`, or `mixed`) and
codes. Successful admission emits `astrowoof.bounded_natal.input_admission.v1` plus
a minimized `bounded_input.admitted` event containing hashes, contract identities,
contexts, and counts only. It contains no subject ID, birth data, coordinates,
location evidence, paths, prompts, or provider payloads. Provider operation count
is always zero.

## Qualification

- Sanitized SPC fixture: passed; 2 objects, 1 relationship, 6 projected terms.
- Supplied AGF 0.8.1/SPC 0.11.0 archive: passed; 106 objects, 1,520 relationships,
  43 projected terms; the frozen epistemic and structural hashes matched Slice 0.
- Source, registry, runtime-resource, correspondence, capability, and evidence
  mutations: rejected by SBE or SPC.
- Reversed source order: identical admission summary.
- Exact loader supplied the valid bounded family: explicitly rejected.
- Local focused admission/policy tests: 13 passed.
- Full suite: 234 passed in 166.492 seconds.
- Fresh offline-installed wheel default release smoke: passed.
- Fresh wheel installed into the qualified Linux SPC 0.11 image; packaged bounded
  admission CLI: passed.
- `git diff --check`: passed after correcting Slice 2's trailing blank line, with
  only expected Windows line-ending notices.

## Gate status

Gate 3 is ready for review. No bounded candidate scoring or authoring has begun.
