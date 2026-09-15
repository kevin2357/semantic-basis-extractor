# Plan

## Slice 0 — Freeze provenance and map the join surface (complete)

- Bind each API/native/result/receipt identity to the exact checkpoint packet in `BACKGROUND.md`.
- Map every reader join that can produce `native_join_conflict` on ordinary terminal-review v0.2 evidence.
- Trace the producer and capture-consumer definitions of terminal
  `binding_sha256`. In particular, distinguish the closed terminal-action
  binding projection from the complete mutable ledger binding object.
- Record why delivery is a valid control: delivery capture does not consume
  terminal-review `action_dispositions`, whereas both failed witnesses do.
- Preserve the distinction between an unsupported/incomplete packet and a contradiction in otherwise sufficient evidence.

**Gate A:** freeze the finite candidate matrix before retained access. Do not
change source merely because static inspection suggests a digest-domain split.

Gate A passed. See `SLICE 0 - NATIVE JOIN SURFACE AND DIGEST DOMAIN.md`.

## Slice 1 — Bounded read-only witness comparison (complete)

- Perform the owner-authorized one conditional HEAD and one bounded GET per named object.
- Verify archive and inventory digests before extracting only relevant terminal evidence.
- For every pass and optional-stage action referenced by each terminal result,
  compare exactly three values:
  1. the sealed result disposition's `binding_sha256`;
  2. SHA-256 of the complete ledger `binding`; and
  3. SHA-256 of the producer's closed terminal-action binding projection.
- Also prove action-ID cardinality, result/receipt/checkpoint identity, state
  revision, checkpoint-basis digest, and optional initial-deck digest so a
  nearby contradiction is not hidden by the leading candidate.
- Compare the actual value(s) and provenance edges that disagree in witnesses A and B. No source listing or mutation.

**Gate B:** both archives and inventories match their pinned coordinates, and
the exact first failing join is established independently for each witness.

Gate B passed. See `SLICE 1 - EXACT RETAINED BINDING JOIN FINDING.md`.

## Slice 2 — Causal recommendation and provider-free reproduction (complete)

- State the exact causal conflict, ownership, and safe correction boundary.
- Build a provider-free reproduction using realistic complete ledger bindings,
  not reduced synthetic dictionaries, if the evidence establishes the shared
  digest-domain seam.
- Define the fail-closed regression matrix: exact projected binding succeeds;
  mutations to every contract-bound field, wrong action ID, duplicate action,
  missing disposition, and conflicting disposition fail. Extra ledger fields
  outside the sealed projection must not silently redefine the producer's
  digest contract.
- Recommend one shared canonical projection/digest implementation for producer
  and capture consumer; do not remove the join or substitute latest-result
  discovery.
- Do not implement or release a correction without a separate review gate.

**Review gate C:** pause after exact witness proof and provider-free
reproduction. Runtime implementation, versioning, package qualification,
release, deployment, and live witness require subsequent approval.

Gate C reached. See
`SLICE 2 - CAUSAL REPRODUCTION AND CORRECTION FENCE.md`. Investigation is
complete; API and owner approved the narrow correction.

## Slice 3 — Shared terminal projection and exact consumer joins (complete)

- Expose one canonical terminal-action binding projection/digest helper from
  the existing v0.2 contract implementation without changing its projected
  fields or any producer bytes.
- Use that helper for the producer, terminal-result validation, and both
  editorial-review disposition membership checks: initial pass attempts and
  optional-stage actions.
- Preserve the distinct complete-ledger binding digest already carried by
  editorial packet decisions. The correction must not substitute the terminal
  projection digest into packet content or alter successful-delivery bytes.
- Do not accept either digest opportunistically, rewrite historical results,
  or weaken action-ID/cardinality/duplicate/conflict checks.

Status: implemented within the approved boundary. Producer bytes and the
closed projection remain unchanged; packet decisions retain complete-binding
digests.

## Slice 4 — Provider-free regression and focused qualification (complete)

- Cover realistic complete bindings containing the four proven extra fields.
- Prove no-polish and multi-polish review captures reach canonical packet,
  projection, and artifact construction from producer-generated dispositions.
- Derive expected artifact counts and identities from each fixture's actual
  contributing actions and distinct deck inventory; do not hard-code the
  successful delivery control's eleven-row count.
- Prove every sealed projection field mutation plus missing, wrong, duplicate,
  and conflicting dispositions remains fail-closed.
- Prove extra non-contract ledger fields do not redefine terminal identity and
  successful-delivery packet bytes remain unchanged.
- Add any new test module to `test_suite_manifest.json`; prefer extending an
  existing classified module when that keeps the regression cohesive.

**Review gate D:** pause after implementation, focused tests, manifest check,
and diff review. Versioning, broad/package qualification, release, deployment,
and live witness remain separate gates.

Gate D reached. See
`SLICE 3-4 - SHARED DIGEST CORRECTION AND FOCUSED QUALIFICATION.md`.

## Slice 5 — Release-bound regression and package qualification (in progress)

- Freeze fresh distribution version `0.4.64` before release-bound testing.
- Retain the focused Python 3.11 coverage required by API review.
- Run the complete manifest-controlled repository suite on the maintained host
  interpreter.
- Commit the exact tested artifact source, build twice from clean committed
  source with one recorded `SOURCE_DATE_EPOCH`, and require byte identity.
- Inspect wheel contents and qualify the exact candidate from clean installed
  Python 3.11 and 3.12 environments, including release smoke, lifecycle smoke,
  editorial-review QA, and the feature-specific public runtime regressions.
- Record `no Alloy impact`: this correction aligns an existing exact digest
  join and changes no modeled chronology, authority, custody, selection,
  packet scope, or transition semantics.

**Review gate E:** pause with exact release-lock commit and wheel coordinates
for API consumer review and explicit owner tag/publication authorization.
