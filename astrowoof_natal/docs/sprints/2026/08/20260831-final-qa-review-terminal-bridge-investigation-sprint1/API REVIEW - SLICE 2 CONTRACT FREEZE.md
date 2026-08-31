# API review — Slice 2 contract freeze

## Decision

**Voof-paws 3 is approved.** The causal matrix correctly locates the defect in
native status/custody composition and constrained-dispatch fencing. API's
terminal-lifecycle refusal remains correct and must not be weakened.

## Frozen consumer rule

API may consume terminal closeout only from an exact invocation-returned sealed
terminal result and its joined inventory/receipt/snapshot evidence. It must not
infer terminal authority from `FINAL_QA_REQUIRES_REVIEW`, `FINAL_QA_WARN`, or
any other status label.

Conversely, a public lifecycle document that truthfully reports durable pending
provider custody remains reconciliation-only. API must not create a replacement
operation, reinterpret terminal bytes as continuation permission, or invent an
action denial.

## Confirmed precedence

The proposed ordering is correct:

1. ambiguity/contradiction fails closed;
2. durable provider custody is retrieval/reconciliation-only;
3. completed-but-unadopted evidence is local fan-in;
4. authorized/submitting ordinary work is nonterminal constrained dispatch;
5. prepared providerless work awaits exact authority; and
6. editorial review may become terminal only after every required custody and
   local-publication inventory is resolved.

`WAITING_FOR_RESPONSE` is acceptable as the native outer projection for durable
unresolved provider custody, provided the public inspection retains its exact
custody/timing facts. The label must not be used by consumers as a claim that
the provider is necessarily still running: a completed-but-unadopted result is
a distinct local-fan-in state in the matrix.

## Slice 3/4 guardrails

- The post-intent fence must execute after the intent is durably committed and
  before provider call-entry, under the native writer, with no provider I/O on
  refusal.
- `post_intent_lifecycle_contradiction` is the correct new typed reason. It is
  not an external checkpoint-change condition and must preserve refused-grant
  and replay semantics.
- The provider-free fixture must assert both the exact public lifecycle
  selection and absence/presence of a sealed terminal result. Testing only
  internal reducer fields would miss the bridge failure.
- The no-polish legitimate-review control and the providerless-authorized
  explicit-disposition case remain essential; neither may be accidentally
  collapsed into the Glimmer custody route.

No API schema expansion is requested by this freeze. SBE may proceed with the
provider-free production-path reproduction in Slice 3.
