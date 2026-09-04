# Slice 2 — provider-free eight-action settlement qualification

## Decision

The Providence-shaped settlement boundary now has a public, packaged,
provider-free qualification. It exercises the existing native contracts without
changing lifecycle, custody, denial, closeout, or provider runtime semantics.

The qualification proves the full native sequence:

1. seven actions are already terminally accounted;
2. one exact providerless `PREPARED` polish action remains;
3. SBE seals a v0.2 precursor with
   `custody_finality=providerless_denial_required`;
4. wrong action, wrong binding, and stale observation refuse before mutation;
5. the exact denial applies once with zero provider I/O;
6. exact replay is inert and changed replay authority refuses without mutation;
7. a cryptographically contiguous v0.2 successor derives
   `custody_finality=final`; and
8. lifecycle reinspection and closeout are terminal only after that final
   successor exists.

This remains qualification evidence, not API settlement authority and not a
simulation of API leases, reservations, capacity, persistence, or cleanup.

## Public/package surface

Added:

- module `astrowoof_natal_authoring.providerless_denial_qa`;
- CLI `astrowoof-providerless-denial-qa`;
- strict semantic receipt
  `astrowoof.providerless_denial_settlement_qualification.v1`;
- invocation-specific identity receipt
  `astrowoof.providerless_denial_settlement_qualification.v2`;
- packaged v1 and v2 schemas;
- packaged release-normalized v1 fixture; and
- public readers, runners, and Python validators.

The v1 receipt is deterministic across fresh temporary workspaces. The v2
receipt additionally carries the exact precursor and successor result, receipt,
snapshot, checkpoint-basis, action-inventory, denial-request, action-binding,
denial-artifact, and denial-snapshot digests for its invocation.

The packaged fixture's semantic receipt SHA-256 is:

`b4ceec6078f9fda5d6d8cf1d8f7ed90e8e18289a2533473332be4bf68b79be92`

## Fixture shape

- Route family: `exact_natal`
- Provider mechanism: `response`
- Paid-action count: 8
- Terminally-accounted actions: 7
- Providerless-denial action:
  `paid_000000000000000000000108`
- Stage: `polish`
- Provider creates performed: 0
- Provider retrievals performed: 0
- Provider transports performed: 0

The seven historical fixture actions carry provider/report/consumption evidence
solely to establish terminal accounting. The zero counters describe I/O
performed by the qualification, not the fixture's historical facts.

## Precursor assertions

The precursor is a strictly validated v0.2 result and canonical v0.1 receipt:

- outcome `review_required`;
- cause `native_lifecycle_review_required`;
- finality `providerless_denial_required`;
- denial inventory contains exactly the polish action;
- reconciliation inventory is empty; and
- `new_provider_create_permitted=false`.

The precursor is explicitly not final-closeout authority and remains byte-for-
byte semantically readable after denial and successor publication.

## Denial and refusal assertions

The exact request uses
`astrowoof.provider_negative_authorization_request.v0.1`. The applied result
uses `astrowoof.provider_negative_authorization_result.v0.2`, names the exact
action and binding, returns `DENIED_PROVIDERLESS`, and performs no provider I/O.

Before the valid denial, the same checkpoint proves:

| Mutation | Outcome | Workspace mutation |
| --- | --- | --- |
| unknown action ID | `immutable_binding_mismatch` | none |
| changed request binding | `immutable_binding_mismatch` | none |
| stale observed revision | `stale_observation` | none |

After application:

| Replay | Outcome | Workspace mutation |
| --- | --- | --- |
| exact same request | `idempotent_replay` | none |
| changed authority reference | `native_state_inconsistent` | none |

## Successor assertions

The successor is another strictly validated v0.2 result and canonical receipt:

- outcome remains the native editorial `review_required` conclusion;
- all eight action dispositions are terminally accounted;
- finality is exactly `final`;
- denial and reconciliation inventories are empty;
- provider creation remains forbidden; and
- its journal range starts exactly one sequence after the precursor range ends.

This preserves the important distinction: final custody does not erase the
editorial review outcome, while editorial review alone did not authorize final
closeout before custody became final.

## Verification

- New focused qualification module: 7 tests passed, 2 expected optional
  `jsonschema` skips in the lean interpreter.
- Qualification plus adjacent terminal-review/lifecycle contracts: 39 tests
  passed, 2 expected optional-schema skips.
- Source CLI produced and Python-validated the detailed v2 receipt.
- No R2, retained QA, provider, API database, deployment, or live settlement
  activity occurred in Slice 2.

## Gate

Voof-paws 3 is ready. API should ingest the packaged semantic fixture and review
the detailed identity surface before SBE performs installed-wheel qualification
or any release preparation. Runtime ownership remains API; no live Providence
settlement is approved.
