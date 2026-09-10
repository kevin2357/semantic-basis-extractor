# API Review — Slice 2 Provider-Free Reproduction

## Decision

Approved. The provider-free fixture isolates the same semantic contradiction
seen in Ada and Aldus: a structurally valid, exact live first-polish authority
request exists, while post-fan-in selection converts the reason that polish was
elected (`FINAL_QA_FAILED`) into terminal-review dominance before API can
consume the request.

This is native scheduling/selection ownership. API must retain its strict
consumer checks: it may grant or deny an exact request, but it must not infer a
request from a terminal result or relax its terminal action-inventory guard.

## Approved Slice 3 fence

Implement the correction at the narrow post-spend-boundary selection seam.
When unwinding `AwaitingSpendAuthorization`, do **not** publish terminal review
if the exact workspace state proves one live, externally eligible optional
continuation. The implementation must require all of the following rather than
relying on a subject status alone:

1. one exact `PREPARED` ordinary-v2 optional-stage ledger action with no
   authorization, provider, reported usage, denial, or ambiguous-submission
   evidence;
2. an exact matching persisted request-sidecar action and binding;
3. the matching stored optional-stage consumer attempt is still eligible
   (the reproduction's first-polish `SUBMITTED` attempt); and
4. no higher-precedence closed terminal predicate for that same action or
   subject.

Under that conjunction, the command must publish the ordinary
awaiting-external-authority handoff and preserve the live request for API. A
final-QA failure is provisional in this precise circumstance; it is not itself
a denial or terminal-review cause.

All other closed predicates remain dominant: explicit providerless denial,
attempt/budget exhaustion, ambiguous submission, invalid finalization
contract, committed terminal result/transition, contradictory evidence, and
an editorial terminal outcome with no elected continuation. Missing,
non-exact, stale, or contradictory request/consumer evidence must fail closed
to the existing review posture rather than inventing a continuation.

Do not broaden this correction to Batch, bounded, mixed-custody, recovery, or
other optional routes without a separately demonstrated common seam. Add
provider-free regression cells for both the fixed first-polish route and the
protected closed-terminal controls above.
