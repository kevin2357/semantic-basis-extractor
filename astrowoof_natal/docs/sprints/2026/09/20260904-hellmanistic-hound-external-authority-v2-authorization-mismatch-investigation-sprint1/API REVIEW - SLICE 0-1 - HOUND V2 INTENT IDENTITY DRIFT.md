# API review — Slice 0–1 — Hound v2 intent identity drift

**Disposition:** Approved to proceed to the joint-resolution packet. The
investigation has identified a narrow native/CLI seam, not a malformed API
grant, a digest-domain mismatch, or a provider failure.

## What the evidence establishes

The supplied, non-authoritative SBE trace is sufficient to establish chronology
when read alongside the frozen API authority packet:

1. Hound's newly selected v2 request/grant passed the public fence
   (`external_authority.fence_validated`).
2. The retained predecessor action was already `REPORTED`, had no provider
   custody, but still had a live `PROVIDER_PENDING` dispatch intent carrying
   predecessor identities.
3. Intent revalidation correctly rejected the successor at the first native
   conflict with `action_state_or_custody_mismatch`.
4. The current CLI then treats that specific refusal as deferrable and calls
   dispatch with the successor identities. Dispatch correctly detects that
   those identities do not match the retained predecessor intent and raises
   the later, less-specific `authorization_mismatch` before payload resolution
   or provider creation.

The provider-free public-CLI characterization is especially useful: it proves
the ordering and proves the no-provider-I/O property without reconstructing
API private state. The various trace digest values must remain documented by
their own schema domains; none is evidence of a generic "hash mismatch."

## Joint repair boundary

The repair should be expressed as two exact rules.

1. **Retire an obsolete native intent during authoritative native response
   reconciliation**, only when the exact intent's action has durably adopted
   completed/reportable evidence and has neither provider custody nor ambiguity.
   Retirement and the completed-result adoption must live in the same native
   writer/snapshot boundary. It is not an API-directed deletion and must never
   erase an intent with live custody, ambiguous submission, or incomplete
   evidence.
2. **Fail closed at the CLI boundary while such an intent remains.** A caught
   `action_state_or_custody_mismatch` must not fall through to a dispatch with
   a different request/grant identity. Return a typed deferred/refusal result
   that says the stale intent is unresolved, with zero payload resolution and
   zero provider create. This is not permission for SBE to mint a replacement
   request or for API to infer a replacement grant.

Once reconciliation has retired the eligible predecessor, the next lifecycle
inspection may expose the exact successor request normally. API can then make
its ordinary, separately audited decision from that exact public request; it
does not need a special recovery-only grant path.

## Required Slice 2 tests and disclosures

- A completed/reported, custody-free predecessor is retired atomically with
  response adoption; a subsequently fresh successor can commit and dispatch
  only through its own exact request/grant.
- A predecessor with live provider custody, ambiguity, or incomplete completed
  evidence is retained; successor dispatch is not attempted.
- The existing public CLI regression changes from characterizing the erroneous
  dispatch to asserting that it cannot occur. Keep the separate current-
  behavior characterization until the repair test replaces it deliberately.
- Verify no payload resolution/provider create in every unresolved-intent case.
- State compatibility explicitly: no API private-state reconstruction, no
  synthetic authority, no retained-QA mutation, and no active-run recovery is
  implied by this sprint.

The frozen API-side investigation and unfiltered diagnostic export remain
available for corroboration only. They do not authorize any retained-QA or
provider operation.

## Review of the implemented repair candidate — correction required

The reconciliation-side retirement boundary and the provider-free no-dispatch
regression align with the approved disposition. One adjustment is required
before qualification/release preparation.

`action_state_or_custody_mismatch` is an error *family*, not exclusive proof of
an obsolete completed intent. The same reason code is also used for, among
other things, unavailable ledger state, a consumed authorization, action state
that is not providerless `PREPARED`, invalid dispatch cursor, and a member that
is not durably `SUBMITTING`. The CLI must emit
`completed_intent_retirement_required` only after it independently establishes
the exact narrow predicate:

- one retained v2 intent exists;
- its exact ordered inventory is fully `REPORTED` with complete response
  evidence;
- it has no provider custody or ambiguity; and
- its request/grant identities differ from the presented, otherwise valid
  successor authority.

Every other `action_state_or_custody_mismatch` must retain its original typed
refusal/exception path. Otherwise an unrelated custody or integrity failure
could be mislabeled as a benign reconciliation delay, obscuring a condition
that API must handle as a genuine failure.

Please add a negative regression covering at least one non-retirement member of
that family (for example, a consumed authorization or non-`PREPARED` action),
asserting that it cannot produce the v4/v5 retirement result. With that
narrowing, the public v4/v5 result is approved: API should treat only that
exact result as a no-I/O refusal, schedule/await fresh inspection rather than
implicitly retrying or regranting, and preserve all other refusal semantics.

## Re-review — approved for qualification and release preparation

The implementation now uses the strict retirement proof on an isolated native
state copy before emitting the v4/v5 result. That correctly limits
`completed_intent_retirement_required` to a different, fully reported,
custody-free, unambiguous, retirement-eligible intent. The new live-intent /
non-`PREPARED` regression also demonstrates that another member of the broad
`action_state_or_custody_mismatch` family retains its original exception and
does not create an output result.

The new command-result v4 / dispatch-result v5 schema pair is therefore
approved for qualification and release preparation. API intake work remains a
separate companion task: accept this exact closed result as a no-I/O refusal,
then return to ordinary fresh-inspection scheduling without implicit regrant,
retry, or provider dispatch.

## Release-candidate review — technically approved

The `0.4.45` candidate evidence is sufficient for SBE tag/publication:

- the controlled builds are byte-identical and the candidate SHA-256 is
  recorded;
- the focused repair suite and installed-wheel qualification are provider-free;
- installed v4/v5 schema readers resolve the packaged public contracts; and
- the patch remains confined to ordinary-v2 completed-intent retirement and
  typed no-I/O refusal.

This approval does **not** make a QA rollout complete by itself. API currently
needs companion intake support for the exact command-result v4 /
provider-dispatch v5 pair. Until that is deployed, API must continue to fail
closed on an unknown result rather than treating it as success, retrying, or
creating provider work. Once SBE is released, API can implement and test that
closed-result intake before a jointly compatible fleet deployment.
