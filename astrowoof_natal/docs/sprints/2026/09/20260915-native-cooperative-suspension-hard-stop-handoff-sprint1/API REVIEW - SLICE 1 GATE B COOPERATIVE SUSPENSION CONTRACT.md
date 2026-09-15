# API review — Slice 1 Gate B cooperative-suspension contract

## Decision

The proposed v1 shape is sound and is the right deliberately constrained
starting point: exact interactive ordinary-v2 dispatch and reconciliation only,
with an API-owned force fence, a launch-bound request channel, cooperative SBE
safe points, and resource-specific later API resolution. It does not blur an
ordinary authority revocation into process death, provider cancellation, or
semantic settlement.

API supports proceeding to Gate B after the clarification below is incorporated.
This is not runtime authorization; the joint Gate B and the shared Alloy spike
remain required before contract-reader or coordinator implementation.

## What is especially well fenced

- The four-document split keeps API supervision identity, API request authority,
  SBE native fact publication, and the transport handoff distinct.
- The request-isolated, outside-workspace control root prevents relocated
  assessment authority from becoming execution/control authority.
- The exact route limit avoids pretending that initial fan-out, Batch, bounded,
  or legacy provider loops have the same stopping semantics.
- The provider-boundary and local-work vocabularies preserve ambiguity rather
  than turning a possible create or unadopted completed response into a clean
  stop.
- Ordinary terminal/delivery-result precedence and append-only resolution are
  necessary: a later containment request must not rewrite an already committed
  native result.
- The resource matrix correctly permits only API worker-execution reclamation
  after an exact envelope-bound child exit; it keeps run allocation and all
  provider/spend/workspace/native custody behind separate evidence-bound policy.

## Required Gate B clarification — checkpoint basis is an admission anchor, not
an observation-time equality gate

`checkpoint_basis_sha256` should record the exact checkpoint API observed while
atomically admitting the force fence and publishing the request. It must bind
the request to that admission fact, but SBE must **not** require it to equal the
latest checkpoint when the child later reaches a valid serialized safe point.

That equality would reject a safe and expected sequence:

```text
API admits fence at checkpoint C1
  -> already-authorized native work reaches a protected boundary and persists C2
  -> SBE observes the request at the next safe point
```

For the exact same envelope/job/attempt/lease/native-run lineage, SBE may honor
the request at C2 and must bind both facts in its result: the request's
admission checkpoint C1 and the exact observed/post-publication checkpoint C2.
The result must prove that C2 is a valid successor in the same authoritative
lineage. A missing, contradictory, forked, or non-successor checkpoint remains
`suspension_refused` or the applicable ambiguity outcome; it never gains a
synthetic successor.

This preserves the audit value of API's admission-time observation without
making cooperative containment spuriously unusable whenever normal in-flight
work checkpoints before the next safe point.

## Small implementation-facing additions to retain in the prose/fixtures

1. Specify the exact child handoff for the envelope path and control-root path
   (dedicated ordered CLI arguments are preferable). The envelope digest alone
   cannot tell the child which immutable file to open. Fixture coverage should
   include argument/path substitution and a byte-valid envelope at the wrong
   canonical location.
2. For `suspension_deferred`, require the result to say whether the child will
   continue only until a named next safe-point, exit after publishing that
   result, or await a separate API action. API must never infer process exit or
   release from a deferred result. The grace deadline is an observation deadline
   only, not an instruction to fabricate a stop.
3. Keep malformed/conflicting/unsupported control input fail-closed with
   respect to **new** native/provider work. Where a refusal cannot safely be
   published, the only truthful downstream state is API's existing fenced,
   ambiguous posture; no ordinary retry or reconciliation path may be selected
   merely because a suspension request was rejected.
4. Provider-free fixtures should include the C1-to-C2 successor case above,
   plus a fork/non-successor case, to make the lineage rule executable rather
   than implicit prose.

## Gate B API position

With the checkpoint-lineage correction and the listed fixture obligations,
API is aligned on the contract direction and ready to review the canonical
Alloy protocol spike. SBE remains the publisher of narrow native facts only;
API remains sole owner of force-fence admission, process observation, worker
execution reclamation, and every future settlement/release decision.
