# API review — Slice 2 executable contracts

## Decision

**Voof-paws C is held for one narrow cardinality correction.** The closed
readers, route vocabulary, root identity checks, C1/C2 lineage checks,
invocation-wide request conflict classifier, result/receipt/command joins, and
provider-free scope fence are all aligned with Gate B/B2. No runtime work is
authorized until the one-result-per-request executable invariant below is
closed.

## Confirmed strengths

- The result / receipt circular-digest correction follows the established
  result-then-receipt-then-command-envelope ordering and is the right fix; a
  result must not preclaim a later receipt digest.
- `ordinary_result_preceded_observation=true` correctly refuses suspension
  result validation, preserving the rule that a prior ordinary result produces
  no suspension result, receipt, or command envelope.
- The request reader enforces exact launch-envelope joins and the replay
  classifier makes any distinct later request for an invocation a conflict,
  including a changed idempotency key.
- C1 equality or a direct C2 successor, root disjointness, and receipt/command
  identity joins are all explicit and provider-free.

## Required C correction — bundle must enforce one result per request

`validate_suspension_fixture_bundle()` currently records `seen_results` and
`seen_receipts`, but not `request_id` / `request_sha256`. Consequently it
accepts two coherently re-sealed distinct results, receipts, and command
envelopes for the *same* exact request. That violates the B2 rule that one
request has at most one canonical semantic result and exact replay returns the
same result/receipt identities.

I confirmed the gap provider-free by constructing a second, correctly rebinding
`provider_boundary_ambiguous` result/receipt/command envelope for the same
request and envelope. The current bundle reader accepted it.

Please make the bundle maintain an exact request-to-result/receipt/command
binding (or reject a duplicate request identity outright), and add a mutation
test proving that a same-request/different-result package is refused even when
all result, receipt, and command digests have been recomputed. Preserve the
existing exact-replay rule: a repeated observation may return the same already
published identities, but it cannot append a second bundle result.

Once that focused correction and test are in place, API expects to approve C
without reopening the already-aligned contract surface.
