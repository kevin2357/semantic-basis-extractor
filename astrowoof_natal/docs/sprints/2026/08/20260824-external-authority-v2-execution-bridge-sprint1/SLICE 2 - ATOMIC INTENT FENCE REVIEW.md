# Slice 2 — Atomic Intent Fence Review

Date: 2026-08-24
Status: implementation complete; API review requested before Slice 3 provider dispatch

## Outcome

SBE now has a native writer-fenced operation that converts one exact validated
v0.6 ordinary-action request, one exact v2 aggregate grant, and the complete
ordered ordinary authorization documents into one durable dispatch-intent
checkpoint. It performs no provider I/O.

The checkpoint contains the exact request and grant identities, lexical action
inventory, authorization-document digests, API decision identity, and a closed
`INTENT_COMMITTED` state. Every selected ledger action is authorized, consumed,
and marked `SUBMITTING` in the same candidate `run.json` write.

## Atomic publication claim

The native guarantee is deliberately filesystem-realistic:

- before `persist_state`, failure leaves authoritative workspace bytes unchanged;
- after `run.json` replacement but before snapshot replacement, the workspace is
  snapshot-invalid and therefore cannot resume;
- after snapshot publication and validation, the complete aggregate unit is
  authoritative;
- there is no state in which a valid snapshot exposes only some selected members,
  authorization without intent, or intent without the exact grant.

This is an atomic publication protocol, not a claim that two filesystem files can
be replaced in one indivisible operating-system operation.

## Validation and refusal order

Under the native single-writer fence SBE:

1. validates the complete restored snapshot and logical root;
2. resolves the complete requested inventory;
3. checks provider identity, ambiguity, consumption, and native action state;
4. reconstructs a fresh v0.6 inspection at the request observation;
5. joins the v2 request exactly to the current inspection/basis;
6. validates the v2 grant and every full ordinary authorization document;
7. creates the full candidate state; and
8. persists and revalidates the complete snapshot.

Provider evidence and ambiguity take precedence over a generic stale-basis
classification. Other closed implementation refusals are:

- `snapshot_invalid`;
- `stale_checkpoint_basis`;
- `member_inventory_mismatch`;
- `authorization_mismatch`;
- `action_state_or_custody_mismatch`;
- `unsupported_contract`; and
- `exact_replay` when an otherwise dispatchable state already contains the same
  intent (the ordinary post-commit state is normally more safely classified as
  `provider_submission_ambiguous` because all actions are `SUBMITTING`).

## Public result

Successful intent publication returns the strict closed
`astrowoof.external_authority_intent_result.v2` artifact. It binds:

- result digest and outcome;
- native run ID;
- request and grant digests;
- lexical ordered action IDs;
- pre/post native state revisions;
- complete post-snapshot digest; and
- `provider_io_performed: false`.

The packaged JSON Schema and Python validator independently enforce this shape.
No result is returned for a refused or interrupted checkpoint.

## Failure-injection evidence

Focused tests prove:

- failure immediately before persistence is byte-identically nonmutating;
- interruption after state persistence but before snapshot publication leaves one
  complete intent unit behind an invalid snapshot, never a resumable partial unit;
- stale grant or changed binding causes no mutation;
- newly appeared provider identity or ambiguity is classified before staleness;
- replay does not publish a second checkpoint; and
- result mutations, digest changes, noncanonical IDs, and side-effect claims fail
  strict validation.

Focused Slice 0–2 and temporal-lifecycle run: **40 tests passed** with JSON Schema
enabled. `git diff --check` is clean apart from Git's existing Windows line-ending
notices.

Provider calls, retrievals, credentials, network activity, spend, and retained-QA
workspace access: **0**.

## Slice 3 review questions

1. Does the intent checkpoint bind enough exact evidence for API audit while
   leaving API-global reservation/capacity facts outside SBE?
2. Is the snapshot-invalid interruption posture acceptable as the honest
   irreducible filesystem boundary?
3. Is provider-safety precedence over stale/replay classification correct?
4. May Slice 3 proceed with provider dispatch outside the writer and per-identity
   durability/reconciliation-only result handling?
