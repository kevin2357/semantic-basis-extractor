# API review — plan and Slice 0

## Decision

The investigation is approved to proceed through **Voof-paws 1** and perform
exactly the proposed one `HEAD` plus one `GET` of Glimmer generation 18. This
approval is read-only and is limited to the coordinate packet in `Background.md`.
It does not authorize a generation-17 read unless the documented differential
remains unanswered after generation 18, nor any provider, R2 write, retained-run,
reservation, or API mutation.

## What the current evidence establishes

The corrected trace is a strong reason to investigate the *mixed-custody
transition*, rather than treating this as an API attempt to continue a cleanly
closed run:

1. `FINAL_QA_WARN` produced one ordinary polish action.
2. The exact v2 grant was accepted; the action was authorized and consumed.
3. Status reduction then emitted the review-terminal-looking outer status.
4. The v2 executor crossed provider call-entry and durably recorded `resp_0adb…`.
5. The next API lifecycle read saw terminal public temporal evidence and rejected
   the worker cycle.

That is the right seam to characterize: provisional editorial review, active
provider custody, terminal public evidence, and API terminal ingress must not be
allowed to disagree about whether another provider create is lawful.

Predicate Paws is correctly a comparison case only. Its typed terminal closeout
shows that review terminals are legitimate; it does not establish the cause or
remedy for Glimmer.

## Required documentation correction before the checkpoint read

`Background.md` still says both that no polish provider operation was created
and that the polish reservation is "unconsumed." The traced sequence now proves
the opposite for provider custody: one provider POST occurred and the response
identity was durably recorded. Please correct those two phrases before or with
the Slice 0 evidence update, and distinguish precisely:

- the API reservation may remain active/unreported;
- the SBE action was authorized/consumed for its v2 dispatch; and
- provider identity is durable, so any future handling is reconciliation-only.

This distinction is material. It rules out a providerless-denial remedy for the
observed run and prevents the investigation from using the wrong custody class.

## Slice 1 inspection questions

Generation 18 should answer, in this order:

1. whether `FINAL_QA_REQUIRES_REVIEW` was merely a status reduction at intent
   persistence or was accompanied by a sealed native terminal result;
2. whether the live v2 intent and the exact polish action still carry durable
   provider identity, and the relationship between their action/binding hashes;
3. whether public lifecycle/temporal material describes the result as terminal
   despite unresolved provider custody; and
4. whether a supported terminal-result/closeout artifact exists at all.

Only retrieve generation 17 if generation 18 cannot establish whether the
terminal-looking status appeared during the grant/intent transition. Do not
infer a terminal result from `FINAL_QA_REQUIRES_REVIEW` alone.

## Contract and test guardrails

The later causal matrix and real-boundary fixture should make these assertions
explicit:

- a status label is not terminal closeout authority;
- durable provider identity selects retrieval/reconciliation and prohibits a
  new provider create, regardless of a review-shaped status;
- an authorized/consumed action with no provider identity is not silently
  retired—its disposition remains an explicit supported cross-boundary outcome;
- a final native result is publishable only after every required provider/local
  dependency has a compatible disposition; and
- the API consumes an invocation-returned public terminal result, rather than
  deriving a terminal outcome from private workspace state or a label.

The Slice 3 matrix is appropriately broader than Glimmer. Include both
"provider identity recorded but still pending" and "provider result available
but not adopted" as separate custody states; they have different legal next
actions. Preserve the no-polish legitimate terminal case as the control.

With that correction and those boundaries, SBE may begin Slice 1.
