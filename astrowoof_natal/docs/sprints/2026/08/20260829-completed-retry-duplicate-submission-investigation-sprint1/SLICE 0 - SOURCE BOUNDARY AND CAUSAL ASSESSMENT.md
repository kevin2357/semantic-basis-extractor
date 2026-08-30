# Slice 0 — source boundary and causal assessment

## Production boundary map

1. `closure.main()` restores the exact workspace and captures v0.7 local work.
2. Generic `--spend-authorization` applies authorization and saves native state.
3. `author_pending_passes()` reaches `SpendController.before_submit()`.
4. `before_submit()` validates retry lineage, moves the action to `SUBMITTING`,
   and persists `run.json` before provider I/O.
5. `provider_created()` persists a returned identity immediately in worker scratch.
6. Provider completion settles the action and authoring continues locally.
7. On ordinary completion, `checkpoint_spend_boundary()` calls
   `commit_local_work_progress()`.
8. The retained mixed predecessor remains an advertised semantic operation, so the
   commit raises `ordinary_resume did not consume advertised local work`.
9. That `ValueError` is outside the spend-boundary's closed handoff exceptions;
   no native execution result is published for API ingestion.
10. API restores the last accepted R2 checkpoint, where the successor is still
    `PREPARED`, and repeats steps 2–8.

Local `persist_state()` calls before and after provider I/O are valuable native
scratch durability, but they are not an API-retained checkpoint/result boundary.
An ephemeral-worker loss/retry therefore discards them when no invocation result is
adopted.

## Hypothesis disposition

| Hypothesis | Disposition |
| --- | --- |
| Stale whole-state save overwrote the first identity | Not supported by generation 11; it predates the identity. No later retained native bytes exist to prove an overwrite. |
| Completed result plus unconsumed fan-in caused command failure and unsafe re-entry | Supported. Retained mixed state and provider-free reproducer reach this exact refusal. |
| Native dispatcher failed to revalidate durable provider custody | Not the direct retained-state defect: the restored successor genuinely has no provider custody. The missing protection is a durable cross-worker call-entry fence for the invocation. |
| API failed to ingest correct sealed post-provider evidence | Supported as absence: no sealed post-action result exists to ingest. That is distinct from rejecting a valid result. |
| Retry identity was recreated incorrectly | Not supported: attempt 3 has one stable native action/binding in generation 11 and both live observations name it. |

## General correction direction for contract review

Do not fix this by suppressing `semantic_work_not_consumed`, selecting one provider
response, or special-casing Marmalade. The general direction should ensure:

- all create-capable ordinary action sets use a constrained request/grant/intent
  boundary whose `CALL_ENTERED` fact is captured before slow provider I/O;
- generic ordinary resume cannot create provider work for an action lacking that
  boundary;
- a post-provider local-progress contradiction publishes or preserves a typed,
  non-create-capable custody/review result rather than escaping as an untyped
  command failure;
- API does not restore/reinvoke create-capable work after a command failure unless
  the current validated SBE inspection provides fresh authority eligibility;
- the already duplicated historical action remains review-only until a separately
  reviewed recovery policy exists.

Those are proposed review topics, not Slice 0 implementation decisions.
