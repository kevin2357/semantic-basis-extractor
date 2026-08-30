# API Voof-paws 4 review — lifecycle v0.8 contract freeze

## Decision

**Approve the contract direction; hold Slice 4 runtime mutation for the two
corrections below.** They are narrow contract completion work, not a request to
change the retry-reentry or custody-precedence design.

The key design decision is correct: logical attempt identity is precisely
native-run/route-family/stage/pass/attempt, while request, binding, action,
mechanism, provider identity, and pass-attempt pointer are evidence attached to
that identity. This closes the original “changed request means a new attempt”
escape hatch. The split between forward-dispatch refusal and retrieval-only
reconciliation is also correct.

## Required correction 1 — exact retry-lineage ↔ lifecycle inventory joins

`validate_lifecycle_inspection_v08()` currently validates the v0.7 document and
the retry inventory independently, but it does not join their action evidence.
The Slice 3 test itself demonstrates the gap: it constructs lineage action IDs
`paid_000…001`/`paid_000…002`, while the materialized v0.7 custody action has a
different action ID; the v0.8 validator still accepts the document as a valid
reconciliation selection.

Before mutation work:

1. Every retry-lineage action must join exactly one v0.7 checkpoint
   `action_inventory` record by `action_id`.
2. The joined record must agree on the logical attempt coordinates available on
   both sides (at least stage, pass, attempt, route/route-family mapping and
   request identity), and the provider ID/mechanism must agree whenever the
   lineage record carries them.
3. Every retry-stage action in the checkpoint action inventory must appear once
   in the lineage inventory; absence, duplication, or contradictory action
   membership is a closed conflict/refusal.
4. A custodial retry action selected for reconciliation must be present in that
   joined lineage inventory, with the same provider operation identity. The
   already-v0.7-valid `due_action_ids` selection remains SBE-owned; this adds
   the missing evidence join, it does not ask API to select members.

The contract currently validates only that due IDs are a subset of custody. That
is necessary but insufficient: otherwise a separate, invented lineage record
can make `reconciliation_permitted=true` without describing the actual retained
provider action.

Please add positive and mutation tests for a custody action omitted from
lineage, a lineage action absent from the checkpoint inventory, a mismatched
provider operation ID, and the current fabricated-ID scenario.

## Required correction 2 — package the full v0.8 lifecycle public surface

The newly packaged `retry-lineage-contracts.v1.schema.json` validates the
inventory only. API Slice 2 needs a supported reader/schema for the complete
`astrowoof.authoring_lifecycle_inspection.v0.8` document, including its v0.7
basis/temporal-decision extension and the retry-lineage binding.

Please provide a root-level public reader such as
`read_lifecycle_inspection_v08_schema()` (or a clearly named equivalent), the
packaged schema resource, and an example/fixture document. `validate_…v08` is
already a good root-level Python semantic validator, but API must not reverse
engineer the v0.7-plus extension shape from source.

The schema need not duplicate all semantic/digest checks; those can remain in
the strict Python validator. It does need to define the closed public document
shape and link the inventory schema/version explicitly.

## Clarification requested while correcting

For a post-custody lineage conflict, expose a closed typed conflict reason in
the v0.8 public lifecycle result (or explicitly make the lineage inventory's
closed `reason_codes` the authoritative machine-readable classification). The
API will not infer “this review was caused by a lineage contradiction” from a
state-name string. This is a small documentation/schema decision, not a request
for an additional state machine.

## API adoption boundary

Once those corrections land, the API will consume the packaged v0.8
reader/validator and preserve the exact SBE-selected command. It will reject a
contradictory document before queue failure/capacity release; it will neither
reconstruct retry lineage nor select reconciliation members.

No API provider, queue, retained-workspace, deployment, or configuration action
was taken during this review.
