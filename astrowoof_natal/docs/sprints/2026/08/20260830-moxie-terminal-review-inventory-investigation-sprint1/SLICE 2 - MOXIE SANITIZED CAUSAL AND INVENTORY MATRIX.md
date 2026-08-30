# Slice 2 — Moxie sanitized causal and inventory matrix

## Decision summary

Generation 11 proves a native ordering seam rather than an ambiguous inventory
count:

1. retry attempt 2 (`paid_5769…`) completed provider retrieval;
2. ordinary local continuation began from that completed evidence;
3. the continuation durably prepared retry attempt 3 (`paid_95b6…`);
4. no public lifecycle/external-authority request for retry 3 was published;
5. the local-work progress fence observed that retry-2's completed evidence had
   not been consumed from the ledger-level local-work inventory; and
6. SBE sealed a valid eight-row terminal-review result and receipt with
   `review_required / local_work_progress_contradiction`.

The eight-row result is truthful complete-native-ledger evidence. It is not a
seven-row API subset, and the providerless retry-3 row must not be inferred away
or denied by API. This slice does not yet assign corrective ownership.

## Exact retained chronology

| Order | Retained native evidence | Revision/time | Meaning |
|---|---|---|---|
| 1 | Journal sequence 55 | revision 29, `2026-08-30T18:46:36Z` | Retry attempt 2 action `paid_5769…` is prepared. |
| 2 | Journal sequences 71–75 | revisions 56–58, `18:47:58Z`–`18:48:01Z` | Retry 2 is authorized and consumed; provider submission starts; provider identity is durably recorded; custody becomes pending. |
| 3 | Reconciliation cycle 59 | revision 58, `18:48:57Z` | One GET observes retry 2 still pending. A sealed seven-action provider-pending result follows at revision 59. |
| 4 | Reconciliation cycle 60 | revision 59, `18:51:02Z` | One GET observes retry 2 completed and records local continuation for pass 6. A sealed seven-action provider-pending result follows at revision 65. |
| 5 | Journal sequence 82 | revision 67, `18:51:34.076900Z` | Ordinary continuation prepares retry attempt 3 action `paid_95b6…`. It is providerless and `PREPARED`. |
| 6 | Journal sequences 83–85 | revision 69, beginning `18:51:35.422091Z` | SBE starts the terminal invocation, transitions to review, and closes it as `review_required / local_work_progress_contradiction`. |
| 7 | Result and receipt | revision 69 | Result `nres_b68e…` and receipt `nreceipt_5306…` seal all eight native ledger rows. |

The gap between retry-3 preparation and terminal invocation is approximately
1.35 seconds. The retained result index and journal contain no intervening
lifecycle/external-authority publication for retry 3. Earlier public results
contain seven actions: revision 55 `awaiting_external_authority`, followed by
revision 59 and revision 65 `provider_pending`. The next public result is the
eight-row terminal review at revision 69.

## Pass, ledger, and public-evidence matrix

| Evidence surface | Retry attempt 2 (`paid_5769…`) | Retry attempt 3 (`paid_95b6…`) |
|---|---|---|
| Pass record | `AMBIGUOUS_PROVIDER_SUBMISSION`; unfinished; no provider metadata on the pass attempt | `AWAITING_SPEND_AUTHORIZATION`; unfinished; providerless |
| Spend ledger | `WAITING`; durable provider ID; authorization consumed; last reconciliation outcome `completed` | `PREPARED`; no provider ID; no consumption |
| v0.7 local-work derivation | Completed ledger evidence makes retry 2 the source of `provider_result_fan_in_and_retry_evaluation` | Not a source operation; it is newly prepared during that operation |
| API authoritative action set | Present as the seventh API action | Absent |
| Terminal-review v0.2 | Reconciliation-only custody | Providerless-denial-only custody |
| Provider creation permitted by this evidence | No | No—no public request/grant was published or admitted |

The shared request SHA between attempts 2 and 3 does not merge their authority.
They have distinct attempt numbers, action IDs, and action bindings.

## Production-boundary reconstruction

The retained ordering matches the current production boundary:

1. Before `--resume`, `inspect_post_fan_in_lifecycle()` selects
   `ordinary_resume` from the completed retry-2 ledger evidence and freezes that
   lifecycle as `prior_local_lifecycle`.
2. `author_one_pass()` reads the pass record. Because attempt 2 is recorded as
   `AMBIGUOUS_PROVIDER_SUBMISSION`, it is not one of the states treated as an
   interrupted resumable attempt. The function advances to attempt 3.
3. Spend authorization is unavailable, so the ordinary continuation prepares
   `paid_95b6…` and returns with `AWAITING_SPEND_AUTHORIZATION`.
4. On unwind, `checkpoint_spend_boundary()` calls `seal_local_progress()`.
5. `commit_local_work_progress()` re-inspects native truth under the writer. Its
   local-work operation is derived from ledger actions whose reconciliation
   outcome remains `completed`. Retry 2 therefore remains advertised under the
   same basis-independent operation key.
6. The progress fence correctly refuses to call that consumption and invokes
   the contradiction publisher. The publisher seals the complete eight-row
   v0.2 terminal-review result before exit 2.

This is not evidence that the progress fence malfunctioned: it detected exactly
what its contract says it detects. The unresolved design/ownership question is
why the completed provider result was not adopted into the pass-level attempt
before retry 3 was prepared, and whether retry preparation should ever become
durable before that consumption is proven.

## Public authority and evidence limits

- There is no retained public v2 authority request for `paid_95b6…`.
- Consequently API had no supported basis to admit, grant, dispatch, deny, or
  persist that action.
- The exact terminal result and receipt are nevertheless valid native evidence;
  strict API refusal of an eight-versus-seven join was correct.
- The detailed outer subprocess stdout/stderr and API ingestion trace were not
  retained. This limits claims about what API logged or attempted after exit 2,
  but it does not weaken the journal-proven native ordering above.
- No claim depends on prompt or generated-content inspection.

## Candidate correction classes for Voof-paws 3

The evidence supports review of two closely related seams, without choosing one
yet:

1. **Native fan-in adoption ordering:** completed ledger evidence should be
   adopted into pass/attempt truth before a successor retry can be prepared.
2. **Native publication ordering:** if successor preparation is legitimate, a
   public request/admission boundary must exist before downstream consumers can
   be required to join that action; a terminal result cannot be the first public
   evidence API sees for it.

Any correction must preserve:

- complete-native-ledger terminal review;
- strict API action/binding/provider joins;
- reconciliation-only custody for retry 2;
- no provider creation for retry 3 without fresh public authority; and
- immutable result/receipt history.

## Activity statement

This reconstruction used only the already downloaded, hash-validated local
copy of generation 11 and current source. It performed no additional R2 access,
provider I/O, resume, reconciliation, repair, denial, publication, API mutation,
or retained-workspace mutation.
