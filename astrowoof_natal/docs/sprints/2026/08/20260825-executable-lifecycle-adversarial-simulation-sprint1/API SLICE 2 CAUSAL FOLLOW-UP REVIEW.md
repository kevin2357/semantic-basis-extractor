# API Slice 2 Causal Follow-Up Review

Status: joint vertical slice is **not yet complete**. This review supersedes the
earlier provisional joint-result wording only as to the remaining production-path
gate.

## Finding

The installed SBE half is sound and the API companion test correctly proves that
the public v0.7 inspection validates and maps to the currently implemented API
cycle result. It does not yet prove the complete production causal path from that
result to queue closeout and capacity release.

The companion test used real API queue and capacity services, but performed
`queue.fail(...)` and `capacity.release(...)` directly after inspecting the
mapped result. That bypasses `SbeReadingWorker`'s actual `TERMINAL_CLOSED`
branch.

More significantly, running that branch as it exists would reveal a real
contract incompatibility, not merely a missing assertion:

- SBE's fixed fixture truthfully declares `selected_command = none` and
  `capacity_disposition = retain_for_review`.
- That is nonterminal native lifecycle evidence; the fixture has no sealed native
  terminal transition to ingest.
- API currently maps `retain_for_review` to `TERMINAL_CLOSED`.
- A production worker configured with `SbeNativeTerminalIngress` must ingest a
  sealed native terminal record before it fails the job/releases capacity. It
  therefore cannot lawfully close this fixture through the normal terminal path.

The earlier API test omitted terminal ingress, which made the direct closure look
successful but cannot qualify deployed behavior. The retained-slot historical
counterexample is still valid; the corrected successor must not be invented by an
API-only terminalization.

## API disposition decision

API accepts the SBE review's first alternative: `retain_for_review` is
deliberately nonterminal, so it requires an explicit API-owned nonterminal review
disposition. This is an API worker/scheduler correction; no SBE contract change is
requested for the fixed v0.7 inspection.

The new path must release scheduling capacity without claiming or requiring sealed
native-terminal ingestion, preserve the review/native custody needed for an
operator-owned completion path, and be replay-safe. It must not reuse
`TERMINAL_CLOSED`. The present implicit shape—nonterminal
`retain_for_review` mapped to `TERMINAL_CLOSED`—is invalid. Retaining capacity is
also not acceptable, because the Muffin counterexample is exactly a continuously
eligible second run being starved by that retained slot.

## API follow-up once resolved

API will replace the manual closure with a test that drives the production
`SbeReadingWorker` using real queue and capacity services, asserts the explicit
nonterminal review path and absence of terminal ingress, and then proves the
second run becomes claimable. The test will
continue to use the installed SBE package only and no provider/retained-QA
activity.

No provider, network, spend, deployment, or retained-QA access occurred in this
review.
