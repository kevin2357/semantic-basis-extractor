# Slice 0 — Preliminary source boundary map

## Status and evidentiary limit

This is source interpretation from SBE main at `fd1652f`; it is not yet a retained
workspace diagnosis. Exact line numbers may move during the sprint. Conclusions
remain provisional until joined to snapshot-validated incident bytes and API rows.

## Relevant production sequence

1. `closure.main()` captures a v0.7 local-work inspection before an ordinary resume.
   It retains that prior document only when the selected command is
   `ordinary_resume`.
2. `author_pending_passes()` resumes incomplete pass attempts through
   `author_one_pass()` and a `SpendController` bound to the in-memory run state.
3. `SpendController.before_submit()` persists preparation, requires exact external
   authorization, changes the action to `SUBMITTING`, and persists call-entry intent
   before provider I/O.
4. `provider_created()` records and persists the returned provider identity
   immediately. Existing conflicting identities become ambiguity rather than a
   permitted overwrite.
5. Provider reconciliation can persist response evidence and mark reconciliation
   timing `completed` while leaving successful actions in provider custody for the
   ordinary local fan-in path.
6. On ordinary resume, `OpenAIResponsesProvider.author()` reuses a persisted
   `openai-background-response.json` identity when present and consumes reconciled
   response evidence before attempting any POST.
7. `SpendController.settle_active()` changes the active action to `REPORTED` and
   persists usage/cost evidence. Pass response, repair, QA, acceptance/rejection,
   and a successor retry may then mutate local semantic state.
8. At the paid-stage boundary, `seal_local_progress()` calls
   `commit_local_work_progress()`. That function reloads and snapshot-validates the
   workspace, recomputes current local work, and refuses
   `semantic_work_not_consumed` when the prior semantic operation is still
   advertised.

## Safety properties already visible in source

- An in-memory action in `SUBMITTING`, `PROVIDER_ID_RECORDED`, or `WAITING` is not
  intentionally create-replayable.
- A persisted background-response marker is supposed to route the provider adapter
  to GET/local reconciled evidence, not POST.
- A conflicting second identity passed to the same in-memory action is supposed to
  become ambiguity.
- `commit_local_work_progress()` runs only after the paid-stage body unwinds and is
  designed to refuse a semantic no-op.

Those properties make the incident especially important: two provider IDs imply
that some later invocation did not observe or did not honor the durable custody
facts that the first invocation believed it had persisted.

## High-value failure windows for retained evidence

### A. Native bytes advanced but no API-adoptable checkpoint/result followed

Provider identity/completion may be durable in worker scratch while a subsequent
`semantic_work_not_consumed` exception prevents the invocation's normal sealed
result/publication boundary. If API restores an older R2 generation on retry, the
next worker may legitimately not see the scratch-only provider identity. The retained
archive chain and command-result intake history must prove or refute this window.

### B. Provider marker or attempt join absent from the restored checkpoint

Even with ledger identity, `OpenAIResponsesProvider.author()` chooses its retrieval
path from the attempt-local background marker. A changed attempt selection, missing
marker, mismatched restore, or action/pass join defect could expose the create path.
The retained attempt metadata, marker, retry key, and binding must be compared.

### C. Stale whole-state publication

Multiple persistence points operate on the shared in-memory state while helper
paths reload state for validation. A later save of stale state could theoretically
erase a provider mutation. Revisions, journal projection, snapshot generations, and
the exact state object used by each boundary must be reconstructed before claiming
this occurred.

### D. Correct native refusal, unsafe API reinvocation

The API row remained `authorized` without a provider operation ID. That proves API
non-convergence, but not by itself that API caused native duplicate permission. The
exact SBE result/receipt/envelope presented after each command and the API intake
decision are required.

## Questions the retained checkpoint must answer

- Which provider identity, if either, is present in the active R2 checkpoint?
- Does the affected ledger action contain provider, consumption, reported, and
  reconciliation evidence, and at what revision?
- Does the affected pass attempt point to that same action and provider marker?
- Is `openai-background-response.json` present and snapshot-declared at the expected
  attempt root?
- Which semantic local-work operation remained unconsumed?
- Was a native result/receipt published before each nonzero exit?
- Did the active checkpoint regress, supersede, or omit a generation containing the
  first provider identity?
- Was the second create driven by the same immutable request/grant/binding or by a
  recreated lineage?

## Preliminary confidence

- **High:** the API action row and native events did not converge.
- **High:** `semantic_work_not_consumed` is a real native safety refusal rather than
  proof that provider completion never occurred.
- **Medium:** a checkpoint/publication gap after provider durability is a plausible
  route to duplicate creation.
- **Low pending retained bytes:** stale overwrite, missing marker, attempt-lineage
  recreation, or API-only reinvocation as the specific root cause.
