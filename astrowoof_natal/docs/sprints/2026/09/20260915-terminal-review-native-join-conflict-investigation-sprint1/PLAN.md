# Plan

## Slice 0 — Freeze provenance and map the join surface (active)

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

## Slice 1 — Bounded read-only witness comparison

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

## Slice 2 — Causal recommendation and provider-free reproduction

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
