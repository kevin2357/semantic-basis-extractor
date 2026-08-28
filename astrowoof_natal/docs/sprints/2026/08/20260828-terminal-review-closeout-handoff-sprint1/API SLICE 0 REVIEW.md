# API Slice 0 review — terminal review closeout handoff

Date: 2026-08-28  
Status: approved with the contract refinements below. Slice 1 may begin.

## Assessment

The corrected causal finding is stronger and more useful than the original
publication-order hypothesis. The provider-free public-command reproduction
demonstrates that the native exact-interactive command can seal and publish a
review-required result before exit 2. The retained QA evidence therefore cannot
by itself establish that SBE failed to write that result; it establishes that the
API never ingested one. Separating those claims is correct.

The API source finding is also decisive: the ordinary-resume route must not
reduce a later `retain_for_review` inspection to a bare failed job before it has
looked for the result produced by the native invocation. That explains the
authoritative state exactly: earlier provider-pending receipts survive, while
the run/job become failed and active custody remains unresolved.

## Responses to the Slice 0 questions

### 1. Missing PostgreSQL receipt versus absent workspace receipt

Agreed. Until the exact retained workspace is read, a missing API receipt proves
only missing API ingestion. It cannot prove missing SBE publication. The API
incident and companion documents should be adjusted to use that narrower claim.

### 2. Immediate ordinary-resume ingestion

Agreed, with one precision: API should ingest the *exact sealed result produced
by the invocation it just ran*, not naively discover "the latest" result in a
mutable directory. The process/result handoff needs an invocation/result/receipt
identity that is snapshot- and journal-bound; the API validates and ingests that
identity before interpreting exit code, later inspection, or worker closeout.

This should apply to every ordinary resume result, including nonterminal
`provider_pending`; terminal review is the release-blocking incident because it
currently exposes a nonzero exit and a review branch. A later inspection remains
a diagnostic/recovery input, not the first authoritative result transport for a
successful invocation.

### 3. Closed mixed-custody result version

Agreed. A fresh closed result/version is required. The API must not join v0.1's
independent action-ID and provider-operation lists, nor reconstruct a terminal
inventory from API action rows or private `run.json`.

The new per-action projection should be ordered and include native action ID,
full public binding or digest, native action state, custody class, provider
identity/evidence class, accounting/consumption class, and terminal disposition.
An aggregate digest must bind that exact order and join the result, snapshot,
checkpoint, journal range, and receipt. `unknown`, `none`, and `zero` remain
distinct.

### 4. Editorial terminality with provider reconciliation

Agreed in principle, but the contract must name two separate concepts:

1. **Editorial terminality:** no more authoring, retry, polish, critic, or new
   provider creation is permitted after `review_required`.
2. **Custody finality:** every existing paid action is reported/settled, denied
   through a supported providerless-denial result, or retained under a
   reconciliation-only provider identity.

`review_required` may be editorially terminal before custody is final. In that
case, the API must not represent the outer run as a fully closed generic
`failed` state that strands custody. It should expose typed
review-required-with-retained-custody status and allow only reconciliation/denial
continuations. Once custody is final, the API can close resources and present the
terminal product outcome. This avoids both reopening authoring and pretending an
unreconciled submitted action is harmless.

## Slice 1 requirements worth making explicit

- Add a result/receipt field that names whether custody is final and, if not,
  the closed reconciliation-only continuation inventory.
- State that `new_provider_create_permitted=false` for every review-required
  successor—even after reconciliation.
- Define the exact invocation-to-result handoff surface API will consume. A
  result index scan alone is insufficient when a run can have historical sealed
  results.
- Include a provider-free fixture where a review outcome coexists with one
  reported action, one durable submitted identity, and one providerless
  authorized action. The fixture must prove no new create and a strict
  per-action join.
- The published result itself is not API authorization to release a providerless
  reservation; it only lets API select the existing exact denial operation.

## Retained QA workspace inspection

The API agent sees no meaningful privacy or spend objection to a narrowly scoped
read-only inspection of Pippin and Duchess. This is a QA database/cohort with
manufactured inputs; the key unresolved factual question is whether the sealed
review result exists in each native result namespace and, if it does, what exact
invocation/result/receipt identity it carries.

If the owner authorizes it, SBE should perform one controlled evidence pass:

1. ensure no worker is actively resuming either run;
2. retrieve/read only their retained workspace artifacts and result indexes;
3. hash and record the accessed artifact identities plus the exact result and
   receipt validation outcome;
4. do not invoke provider create/retrieval, reconciliation, resume, repair,
   deletion, or any workspace write; and
5. report only sanitized identifiers, state/result/receipt/journal metadata—no
   prompts or generated dog content in the sprint evidence.

That read-only check is the fastest way to distinguish a native publication gap
from an API ingestion gap. It should be recorded as a separate explicitly
authorized evidence action, not silently folded into implementation.
