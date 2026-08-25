# API Agent Waffle Checkpoint 2 Review

Status: **not yet approved**. The execution-boundary direction is correct and
the new phase-aware implementation has the right central shape: materialize
locally before the durable call fence, revalidate the unchanged snapshot under
the writer, then release the writer only for the one transport operation.

The focused provider-free test run exposed two substantive gaps that should be
corrected before this waypoint is accepted.

## 1. A pre-provider refusal does not currently lead to the promised fresh authority request

`test_pre_provider_refusal_seals_invocation_and_requires_fresh_authority`
correctly proves that the old grant is sealed and the action is restored to
`PREPARED`. But the subsequent fresh lifecycle inspection has
`external_authority_state.kind = none`; consequently
`build_external_authority_request_v2(...)` raises `Lifecycle checkpoint has no
external-authority request`.

That contradicts the agreed contract: a pre-provider refusal is nonterminal,
consumes only the exact prior grant invocation, and requires **a fresh supported
inspection and a fresh API authority decision**. It must not strand a
provider-I/O-free action in a state where no new authority can ever be issued.

Please make the post-refusal lifecycle projection yield a new, distinct ordinary
external-authority request for the still-eligible action (or, if some retained
lineage must be surfaced first, an explicit typed inspection outcome that leads
to that request by a supported local continuation). The exact old request/grant
must remain non-replayable. Update the regression to exercise the complete
fresh-inspection -> new request -> new grant path, not merely prove that the old
request digest differs.

## 2. A malformed provider response is currently classified as a transport failure

The malformed-return regression currently fails:

```text
expected: provider_returned_invalid_identity
actual:   provider_transport_failed_without_identity
```

The cause is in the CLI transport adapter. It indexes `response["id"]` before
the dispatcher sees a provider result. A provider response missing `id` therefore
raises `KeyError`; the dispatcher sees only an arbitrary exception and maps it
to the generic transport-without-identity reason.

Please preserve the intended classification by either:

- returning the raw/provider-normalized result to the dispatcher and validating
  its identity there; or
- raising a dedicated typed invalid-provider-identity exception from the adapter
  which the post-fence dispatcher maps to `provider_returned_invalid_identity`.

This remains ambiguity, not a pre-provider refusal—the call was entered—but the
more precise public reason is part of the closed v3 contract and should not be
lost at the adapter boundary.

## Additional acceptance evidence

After those two corrections, please add or demonstrate these focused cases
before asking for re-review:

1. Each closed pre-provider reason (`unavailable`, `ambiguous`, digest mismatch,
   invalid configuration) makes **zero** scripted transport calls and seals only
   the exact grant invocation.
2. A refusal after a successfully provider-bound prefix preserves that exact
   prefix, refuses the next ordered member, and proves no later member entered
   preparation or transport.
3. A checkpoint change between preparation and the second writer acquisition
   crosses no provider fence, performs no create, and leaves the old invocation
   unusable; its public/CLI disposition must make the next supported inspection
   path unambiguous to API rather than leaking an uncategorized exception.
4. The prepared-create digest is bound to the actual preparation snapshot and
   the second writer validation proves that it is still that snapshot when the
   call fence is written.

## Decisions answering the Waypoint 2 questions

- The writer must never span provider I/O. The second writer acquisition may
  publish only a call fence whose prepared-create digest is joined to the exact
  unchanged checkpoint; any mismatch is pre-fence and cannot consume provider
  create authority.
- Local provider-client construction, payload discovery, request construction,
  and response-shape normalization belong on the pre-fence side wherever their
  failure is deterministically knowable. Do not use exception class alone as a
  custody classifier.
- Once the durable fence is written, every inability to prove one durable,
  valid provider identity stays in the ambiguity family and generic resume stays
  unable to create again.
- The complete public v3 result must remain sufficient for API to release only
  the exact unspent reservation on a refusal, retain ambiguity custody after the
  fence, and request fresh authority only through a new lifecycle inspection.

## Verification observed

Using the repo's source path for the focused suite:

```text
python -m unittest \
  astrowoof_natal.tests.test_ambiguous_provider_submission_runtime \
  astrowoof_natal.tests.test_ambiguous_provider_submission_slice0 \
  astrowoof_natal.tests.test_external_authority_v2_cli
```

yielded 9 tests with one error (fresh request unavailable) and one failure
(malformed identity reason). No provider credentials, network calls, retained
QA workspace, or spend were used.

