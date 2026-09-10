# Slice 1 — Immutable First-Polish Authority Findings

## Outcome

Both first-polish actions have exact, structurally valid, API-readable authority
requests in their immutable checkpoints. Neither action has authorization,
provider custody, reported evidence, or denial evidence. Native should preserve
the awaiting-authority continuation. Instead, SBE converts that live request to
review posture in both runs.

The primary defect is SBE-owned at the first-polish spend-boundary /
terminal-review selection. API's Aldus action-inventory rejection is a correct
downstream guard against the contradictory terminal publication.

## Access and integrity

The owner authorized exactly one conditional HEAD and one bounded conditional
GET for each supplied coordinate. Both reads passed:

| Checkpoint | ETag | Bytes | Archive SHA-256 | Inventory SHA-256 |
| --- | --- | ---: | --- | --- |
| Ada generation 6 | `a1075ed1da92381e6ea22bc4f88f5865` | 4571726 | `3620eb4eb84b4fe31d60e81369dbec6f89a6897f5c0d0bf2f4fa996e912c955a` | `e0d38510f42dc956b5add027183638b4042b45bbbcab1c40bfb9d0e9b7494068` |
| Aldus generation 11 | `36ba8fba7ec94a27511df2cdcef1404e` | 4872013 | `55a93dc27e6146e8541b16a0cb66a0cd40f67fe07fd505e923253e5a0f3b4a14` | `36027a5134298b389d5a651249bcb26b9bc732c679b003723d8e9659c0925915` |

Offline validation found no unsafe or duplicate paths, matched the complete
declared member sets, and verified every archived member's byte size and hash.
The two HEAD and two GET allowances are exhausted. No listing, alternate read,
write, delete, provider operation, execution, recovery, or mutation occurred.

## Exact authority evidence

### Ada

- Run state: `AWAITING_SPEND_AUTHORIZATION`, revision 54.
- Action: `paid_67c8a2afd008a6fdf317c1b0`, state `PREPARED`, stage
  `polish`, route ending `:polish:001` for the exact subject.
- The ledger has no authorization, provider, or reported evidence.
- `spend-authorization-requests.json` contains exactly that action and a binding
  byte-for-value equal to the ledger binding at revision 54.
- The binding identifies canonical request
  `c1418a090dd94ed695ab7c600abead86fd0ba0eb53c314687e5511d7c13321f6`
  and its immutable request-payload artifact.
- Sealed result `nres_3b5ee9a244262af1e415e112` and receipt
  `nreceipt_83bab5d85dda4de42f748eaf` join by run, invocation, result,
  hashes, journal range, checkpoint basis, and snapshot.
- The v0.1 result includes the polish action ID and says
  `awaiting_external_authority` / `spend_authorization_required`.

This is not merely an outcome hint: the exact consumable request sidecar is
present and agrees with the ledger. API's released `prepared_actions` reader
accepts this schema, stage, action ID, request digest, prepared revision, and
positive commitment shape. The incorrect transition is the enclosing SBE
provider-reconciliation command returning `review_required` instead of
preserving the request for authority handling.

### Aldus

- Run state: `AWAITING_SPEND_AUTHORIZATION`, revision 78.
- Action: `paid_470896db6a2cf2312864dccd`, state `PREPARED`, stage
  `polish`, route ending `:polish:001` for the exact subject.
- The ledger has no authorization, provider, reported, or denial evidence.
- The request sidecar contains exactly that action and a binding equal to the
  ledger binding at revision 78. It identifies canonical request
  `16a23dc217d593dc40f40b21c0b3c5d10fbd6dda565400e07199f2fc453f0f3b`
  and its immutable request-payload artifact.
- Sealed v0.2 result `nres_e41bbf89a77e50f6b5c87a06` and native receipt
  `nreceipt_de8f55540f2b4ded4f9f899b` join exactly inside the checkpoint.
- Its terminal action binding digest
  `fe6347c6477d24651c315d5151731a31f333c0d77fc1a2843ae75f4aee87a1ea`
  recomputes from the same polish action and binding.
- Despite the live exact request and absence of denial evidence, the result
  projects the PREPARED action as `providerless_denial_only`, sets
  `custody_finality=providerless_denial_required`, forbids provider creation,
  and returns `review_required`.

That v0.2 projection is internally schema-valid but semantically premature.
The terminal-review contract deliberately maps every PREPARED/AUTHORIZED action
to providerless-denial custody; therefore the erroneous step is entering
terminal review while a valid first-polish authority request remains live.

## Ownership and causal classification

The earlier two-defect possibility narrows to one native selection defect with
two publication manifestations:

1. final QA legitimately prepares first polish and writes its exact request;
2. the paid-stage pause unwinds into terminal-review-enabled handling;
3. lifecycle inspection reports `retain_for_review` while the run is still
   awaiting spend authorization; and
4. SBE treats that review posture as permission to close rather than preserving
   the authority continuation.

Ada exposes the contradiction as a correct v0.1 awaiting-authority publication
followed by a closure-level review result. Aldus exposes it through a later v0.2
terminal projection of the still-PREPARED action. API then observes an expected
seven-to-eight local inventory mutation inside what SBE presents as terminal
review and rejects it.

No API grant/denial omission needs to be inferred: SBE closes the command before
API receives a stable authority disposition to service. No provider failure,
custody ambiguity, budget exhaustion, malformed request, or editorial terminal
decision is present.

## Narrow Slice 2 reproduction target

Build a provider-free fixture for:

`reported initial/retry inventory → final QA failed → first polish PREPARED +
exact request sidecar → AwaitingSpendAuthorization`

The required invariant is that a live, valid prepared polish request cannot be
converted to terminal review or providerless-denial custody merely because the
post-unwind lifecycle disposition is `retain_for_review`. The command must
return an actionable awaiting-authority outcome without mutating the action
inventory again.

Preserve genuine terminal review for an explicit denial, budget exhaustion,
attempt exhaustion, ambiguity, invalid finalization contract, or other existing
closed terminal evidence. Do not weaken API's terminal inventory guard.

## Artifacts

- `ada-generation-6-r2-read-receipt.v1.json`
- `aldus-generation-11-r2-read-receipt.v1.json`
- `ada-generation-6-selective-inspection.v1.json`
- `aldus-generation-11-selective-inspection.v1.json`
- `tools/slice1_selective_offline_inspection.py`

Slice 1 is complete and ready for API/owner review before provider-free Slice 2.
