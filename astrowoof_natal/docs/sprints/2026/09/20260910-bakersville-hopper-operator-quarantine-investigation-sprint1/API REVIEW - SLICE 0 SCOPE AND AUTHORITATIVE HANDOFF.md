# API review — Slice 0 scope and authoritative handoff

## Review decision

Approved to proceed with Slice 0 as an investigation-first, provider-free
reconstruction of the *nice* assessed-quarantine path, alongside a separately
reported reconstruction of Baskerville's prior ordinary-lifecycle stall.

The separation is essential. The observed
`disposition_assessment_unavailable` refusal proves neither Baskerville's
native custody class nor the cause of the earlier stuck state. Conversely, a
future permitted quarantine would contain local API scheduling but would not
explain the missing terminal settlement.

The Plan's statement that no live quarantine execution is authorized needs a
small historical clarification: one owner-authorized, exact live request was
already submitted at `2026-09-10T19:27:22.727Z`. It was a single bounded
assessment exercise, not a successful quarantine. No repeat execution,
workspace read, provider operation, or runtime mutation is authorized by this
review.

## Exact observed assessment refusal

| field | value |
| --- | --- |
| API run | `2b93ee92-643b-47bf-a029-6db8b9df698f` |
| SBE-authoring job | `957784cb-fa7e-45e5-bf58-860802be9a40` |
| native run | `06d84cec0934accdd28c43cc72e282d39091e2fc8d8e4ba96c58eccc349236d3` |
| operator request | `02de1a55-b137-499d-9fb4-c327a7fe3116` |
| operator request state | `refused` |
| refusal code | `disposition_assessment_unavailable` |
| quarantine/capacity release | neither applied |

The operator runner job that admitted the request was
`job-dahg9aijnfac738qpui0`, succeeded from `19:27:38Z` to `19:27:54Z`.
The refusal was recorded at `2026-09-10 19:27:54.175995+00`.

## API-side Track B observations

These are authoritative API/DB observations and per-run SBE worker-log facts,
not a common-cause conclusion:

1. API's latest persisted native receipt for Baskerville is
   `nres_8da3f79e8b070bbb256ee664`, recorded at
   `2026-09-10 19:07:48.005267+00`: `provider_reconciliation`,
   `awaiting_external_authority`, cause
   `spend_authorization_required`, post-state revision `57`.
2. The SBE worker subsequently logged the same native run at revision `64` in
   `FINAL_QA_FAILED`, then emitted native result
   `nres_659e7fcaa7463bfc74ff19d2` with outcome `review_required` and cause
   `final_qa_requires_review` at approximately `19:09:05Z`.
3. Thus there is an exact, material native-to-API receipt-ingestion/settlement
   gap between the last persisted API receipt (revision 57) and later native
   terminal evidence (revision 64). Slice 0 Track B should locate the first
   boundary at which that successor failed to become an API receipt/closeout;
   it must not treat the later operator assessment refusal as proof that this
   is the same transport failure.
4. Hopper's SBE job
   `b4ff5c9a-8949-4e82-9c4c-60be1f093cf9` has been eligible since
   `2026-09-10 19:05:28.392154+00` (`retry_wait`, attempt 3) with six
   `provider_created` initial actions and zero reported actions. Its last SBE
   trace recorded six provider-local dependencies and released its own lease.
   The lack of later reconciliation is therefore an undispatched-job problem,
   not evidence that six providers necessarily failed to answer.

## Requested Slice 0 refinements

- In Track A's failure matrix, distinguish a valid SBE assessment that API
  rejects from failure before any bounded stdout exists. Record the exact
  subprocess output provenance and parser rejection details for both.
- In Track B, treat the revision-57-to-64 discontinuity as a named hypothesis
  boundary and report it independently of any assessment fixture result.
- The provider-free `permitted` fixture and restored-subprocess proof are the
  right first gate. Do not request live Baskerville R2 access until that
  baseline tells us precisely which missing artifact would discriminate the
  failure.

