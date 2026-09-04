# Slice 1 — exact Providence result and receipt certification

## Decision

Providence's retained generation-12 checkpoint certifies the leading diagnosis.
The exact sealed artifact is a valid `astrowoof.native_execution_result.v0.2`
review result with canonical v0.1 publication receipt and aggregate
`custody_finality=providerless_denial_required`.

This is not a provider-custody, ambiguity, publication-integrity, or native
vocabulary defect. It is the already-identified missing API settlement boundary
for one providerless prepared action. Nothing in this investigation authorizes
settlement of Providence itself.

## Frozen access identity

- API coordinate packet SHA-256:
  `99170231609c2f4db616192b3ea98a3b71e9faf4dd97afe2e58b84204f153d37`
- Local closed access-manifest SHA-256:
  `be9f80b0e5cacdeff27dcd1df01819444f23507fe474ea338995e84846769d2d`
- Object key: `v1/checkpoint/64f3af2fbe3544cdbbecc1f96bbfb792`
- Checkpoint: `ec4a5b25-9e1a-4198-835f-6d2e07ebd0be`, generation 12
- Observed ETag: `960638104dd5ee838d7e507dafd5b43b`
- Archive bytes: `4812961`
- Archive SHA-256:
  `7c00e29b1df99ed6d31630d4114bd7d1dfbf49af21b516e39842658a2f26d5f8`
- Inventory SHA-256:
  `d2cd49c9f0ac006746af78122a7e75693c01890bef91a5973beca5d4fe71101d`
- Execution-time access-receipt SHA-256 (LF serialization):
  `572f30e561e2bbcca7d5cc7c90fc00760c5ce2b04ba6b85c0492f0791b4b43d2`
- Repository evidence-copy SHA-256 (working-tree CRLF serialization):
  `b1eda5e0330c8118f9dbdc0b1c77bca35bca3b375188d36a3250fa87eff511e5`

The authorized budget was consumed exactly once: one `HEAD`, one conditional
`GET`, zero listings, writes, deletes, provider calls, workspace executions, or
workspace mutations. All later inspection used only the downloaded local
archive.

## Archive and retained-evidence validation

The archive passed all of the following checks:

- no absolute, traversal, duplicate, or symlink members;
- the archive's 980 entries exactly match the checkpoint manifest inventory;
- every declared member byte count and SHA-256 matches;
- the canonical member inventory recomputes the frozen inventory SHA-256;
- `workspace-snapshot.json` hashes to
  `3b1b0834887d506c62ac20ce954d1585136c12b5c66150743441a065a79ab4cf`;
- the retained checkpoint basis recomputes
  `49d2f35c74d61c2c7f526fe7d39b5bfe3207cc6c4741af64f04efcd1c4fe6046`;
- all 90 native journal records have valid content identities, sequence, and
  predecessor links; and
- result journal range 85–90 contains six contiguous records and recomputes
  `6912239d007f1a0b0ee4b8987ceb4435010b00fcd6a3fe2448c05ded8e83acf4`.

The coordinate packet honestly carried a null checkpoint-basis digest because
API had not persisted it. The retained canonical receipt supplies the exact
digest, and it joins the result, revision-79 post-checkpoint, and retained basis.
No value was inferred or invented.

## Exact public result

- Schema: `astrowoof.native_execution_result.v0.2`
- Invocation: `ninv_7440ab2c75754ac3a5fb35f0`
- Result: `nres_0f3d3b6a3cc256db4b7a9c1b`
- Result SHA-256:
  `0f3d3b6a3cc256db4b7a9c1b13a5159b202e2b030aa9c9c7f66a7a711ab70ebc`
- Receipt: `nreceipt_2b0e8df6e0278a32ff245d61`
- Receipt SHA-256:
  `2b0e8df6e0278a32ff245d61aa3aa241045cf7d6a27ff0bf2476636181abbafa`
- Outcome: `review_required`
- Cause: `native_lifecycle_review_required`
- Finality: `providerless_denial_required`
- New provider create permitted: `false`
- Native state revision: 79
- Action-inventory SHA-256:
  `2aaf9f0075763e9e611fb7b9f9e78358f567e3ba43cf7597b6f44877793d5306`

The released/current Python validators accept both the result and the exact
result/receipt join. The result index ends with this exact result ID.

## Complete custody derivation

The retained `run.json` contains exactly eight paid actions. Re-running SBE's
production `build_terminal_action_dispositions()` against that ledger produces
the sealed result's ordered `action_dispositions` byte-for-byte at the semantic
JSON level:

- ordinals 1–6: initial authoring, `REPORTED`, consumed and reported, durable
  provider identities, `terminally_accounted`;
- ordinal 7: creative retry, `REPORTED`, consumed and reported, durable provider
  identity, `terminally_accounted`; and
- ordinal 8: polish action `paid_f5a73dc0325db8a8aedafe05`, `PREPARED`, no
  provider identity, no consumption/report, `providerless_denial_only`.

Therefore:

- `providerless_denial_action_ids` is exactly
  `["paid_f5a73dc0325db8a8aedafe05"]`;
- `reconciliation_action_ids` is exactly `[]`;
- there is no ambiguous or retained provider custody; and
- final closeout is not yet authorized because the prepared action is not
  terminally accounted.

## Journal chronology

The bounded result range confirms the relevant native sequence:

1. sequences 85–86 record completion and usage for the creative-retry provider
   operation;
2. sequence 87 records preparation of the polish action;
3. sequence 88 starts the terminal-review invocation;
4. sequence 89 records the native `review_required` transition; and
5. sequence 90 closes that invocation with the same cause and outcome.

This supports the result's public meaning: SBE did not dispatch polish, did not
discard it, and did not claim final custody. It sealed the exact providerless
action for a supported denial settlement that API does not yet implement.

## Classification and ownership

The Slice 1 decision matrix resolves to:

> Valid result; providerless-denial action; no provider custody → missing
> supported denial settlement → API implementation and joint qualification.

SBE already owns the action/custody derivation, public result, canonical receipt,
and providerless-denial native transition. API owns durable intake of the
precursor, its settlement intent/idempotency, capacity/lease policy, invocation,
successor ingestion, and final API closeout. SBE must not assert those API-global
facts.

## Privacy and non-authority boundary

Only checkpoint/snapshot/journal metadata, the named result and receipt, result
index, checkpoint basis, and paid-action ledger identities needed for the exact
join were inspected. No prompts or generated deck content were emitted into
sprint evidence. This document is diagnosis and contract evidence, not recovery
or settlement authority.

## Gate

Voof-paws 2 is ready. Before fixture/runtime work, API should confirm that this
exact artifact certification does not alter the already-frozen settlement owner
or ordering and approve the provider-free eight-action qualification boundary.
