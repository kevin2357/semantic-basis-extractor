# Frisbee/Hype Prepared-Polish Authority-Request Investigation

## Status and boundary

Investigation only. Do not perform provider access, R2 listing/writes, retained
workspace mutation, reconciliation, resumption, recovery, deployment, release,
or API database mutation from this sprint until a later owner-authorized slice
explicitly permits it.

## Reproduced QA cohort

The fresh QA cohort below ran with SBE 0.4.48 and SPC 0.11.1 after the full
release-pair/provider-free qualification passed.

| Pup | API reading | API run | Native run |
| --- | --- | --- | --- |
| Frisbee Fortuna `9253cf1b` | `7298852d-9e89-4e24-b0fc-50295a2a0619` | `f69eceb5-73b4-4f10-828c-22da6a35cba8` | `6d6fe16a151d3cbddcd03e569b0c217eaccf1304adb9e6822aa6247dbea0a890` |
| Hype Hellman `a30a02bd` | `267a224f-73d2-4794-aad2-da6f3531ecee` | `e663f477-c551-4694-8ccc-21de46422b79` | `0041e6240151ba8ba2299efed3f7d40bdb9f196230ff048f57fd0fabb891a677` |

Both completed deterministic work, created and reconciled six initial provider
actions, and reached `AUTHORING_COMPLETE` without a creative retry. Final QA
reported zero validation errors but lint findings (Frisbee 6, Hype 3). Each
workspace prepared exactly one polish action, then entered
`AWAITING_SPEND_AUTHORIZATION`.

The key common SBE trace facts are:

- `action_states=PREPARED:1,REPORTED:6`;
- `action_stages=authoring_initial:6,polish:1`;
- no provider custody and one local dependency;
- `execution_branch=none`, reason `native_review_or_ambiguity`;
- `request_present=false` despite the prepared polish action; and
- native publication `awaiting_external_authority`, immediately followed by
  semantic closure `review_required`.

API records subsequently show both authoring jobs failed non-retryably with
`native.review.requires_review`. Capacity and leases are released, and no polish
action exists as a persisted API paid-action row. The two retained runs are not
to be revived during this investigation.

## Log evidence

An API agent exported the unfiltered SBE worker logs for the full hour around
the cohort, in four bounded chunks:

- `C:\\tmp\\astrowoof-sbe-polish-authority-20260904\\sbe-worker-00-2320-2335Z.log`
- `C:\\tmp\\astrowoof-sbe-polish-authority-20260904\\sbe-worker-01-2335-2350Z.log`
- `C:\\tmp\\astrowoof-sbe-polish-authority-20260904\\sbe-worker-02-2350-0005Z.log`
- `C:\\tmp\\astrowoof-sbe-polish-authority-20260904\\sbe-worker-03-0005-0020Z.log`

Window: `2026-09-04T23:20:46Z` through `2026-09-05T00:20:46Z`.

These are non-authoritative diagnostic evidence. They must be cross-checked
against a bounded retained-checkpoint read if a source-level fact is not already
proved by the logs and public fixtures.

## Investigation questions

1. For an ordinary-v2 optional polish stage, what exact condition should cause
   lifecycle inspection to surface an `external_authority_request`?
2. Is a prepared optional action without that request an implementation gap,
   an intentionally typed refusal, or a defect in the public lifecycle projection?
3. Does the reader have enough evidence to expose one exact request without
   widening authority to any other prepared/ambiguous action?
4. Can SBE package provider-free witnesses for both the positive prepared-polish
   request and the requestless fail-closed alternative, so API can consume the
   exact installed-wheel evidence?
