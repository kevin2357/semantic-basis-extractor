# Background — editorial-review packet collection contract

## Why this sprint exists

The editorial-quality calibration sprint began as research: replay a historical
cohort, show exact before/after evidence to humans and an independent model, and
reconsider standards originally chosen from a small manual sample.

Its five-run reconstruction also answered early questions for API Sprint 87's
proposed Better Stack corpus. It established realistic lineage cardinality,
candidate/finding relationships, query shapes, and byte sizes. That overlap was
useful during discovery, but the tracks now diverge:

- calibration asks which editorial decisions are sound; and
- collection asks how SBE can publish a closed, non-authoritative evidence
  packet for API to observe after eligible terminal settlement.

This sprint owns only the SBE collection-contract implementation. The original
calibration sprint retains human/model judgments and editorial-policy work.

## Companion work

API companion:

`C:\dev\github\astrowoof-api\docs\sprints\2026\09\20260907-editorial-review-evidence-retention-companion-sprint87`

Research source:

`astrowoof_natal/docs/sprints/2026/09/20260906-editorial-quality-standards-calibration-sprint1`

The API plan defines four broad slices: joint contract/boundary inventory,
provider-free fixtures, narrow runtime implementation, and joint provider-free
end-to-end qualification. The SBE plan expands those into smaller native-owned
gates and names the corresponding API slice at each step.

## Evidence already available

The calibration sprint provides five exactly reconstructed lineages—four
review-required/failed examples and one successful-delivery control—containing
39 ordered decisions and eight materialized polish transitions. It also provides
deterministic packet sizes, three disposable query representations, and a
private blinded-review surface.

Private authored content remains outside Git. Those research packets are schema
inputs, not public contract fixtures or transition authority.

## Frozen safety boundary

- The corpus is selective, exploratory, and best-effort—not an operational
  ledger, reporting source, representative sample, lifecycle input, or recovery
  source.
- SBE owns canonical editorial facts and packet bytes. API may transport them
  opaquely only after authoritative terminal persistence succeeds.
- Initial eligibility is limited to reader-validated ordinary live-exact
  successful delivery and normal editorial terminal closeout.
- Batch, bounded, mixed custody, recovery, interrupted, repair, compatibility,
  unsupported, ambiguous, unknown-version, and exotic routes are excluded.
- Construction binds the exact sealed native result returned by the invocation;
  generic/latest-result discovery grants no eligibility.
- Construction is all-or-none. Missing, inconsistent, unsupported, or oversize
  evidence yields a small typed non-authoritative status and no packet bytes/ID.
- No packet, status, transport result, Better Stack row, or query can change
  native/API state, retain capacity, authorize work, retry, or reopen a run.
- Raw prompts and provider responses are separate content decisions. A retained
  provider envelope stays opaque hashed evidence, not native editorial meaning.

## Slice 0-alpha decision

The joint huddle selected two deliberately separate observational products:

- one atomic hybrid editorial request containing compact complete editorial
  semantics plus bounded decision/finding/validation projections; and
- one artifact-source batch containing independently wrapped complete deck
  objects and exact joined provider responses.

The editorial request is all-or-none. Artifact records are independently useful
and partial best-effort availability is allowed. Both sources share stable
native packet/object correlations while API observation correlations remain
separately owned in the transport envelope. Neither source has authority.

Exact schemas, projection fields, deck roles, byte/count ceilings, and semantic
invariants remain for this sprint's contract freeze; the broad content/query
decision is no longer open.
