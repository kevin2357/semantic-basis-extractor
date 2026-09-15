# API review — Slice 1A Alloy Gate B2 re-review

## Decision

**Approved for Gate B2.** SBE may proceed to Slice 2 executable contracts,
readers, and provider-free mutation fixtures. This approval does not authorize
runtime safe-point integration, live control signaling, process termination,
provider activity, R2 access, or any API resource release.

## Review basis

Reviewed the revised:

- `SLICE 1A - SHARED ALLOY PROTOCOL SPIKE.md`;
- `SLICE 1 - GATE B COOPERATIVE SUSPENSION CONTRACT.md`;
- `ALLOY RULE MAPPING.md`; and
- `alloy-protocol-spike-receipt.v1.json`.

The recorded model digest is
`96cc83a08f44d42a2f026e7d65fb6687e88d26d9d42acbfa2c6329ccc4c9f926`.
The receipt records four inhabited SAT scenarios, ten full-contract UNSAT
assertion checks, and seven deliberately weakened SAT witnesses at the stated
finite scope.

## Prior B2 corrections

All three requested corrections are now represented consistently in the model
summary, rule map, and Gate B prose:

1. A distinct later request for one supervision invocation is
   `suspension_refused/request_conflict` regardless of idempotency key or other
   changed request material. The valid conflict scenario preserves the first
   result and refuses only the later request.
2. A valid ordinary terminal or delivery result committed before native
   `observed_at` wins even if API's force fence predates it. The precedence
   scenario requires zero suspension results, receipts, and command-result
   envelopes.
3. Each canonical suspension result has exactly one same-invocation receipt and
   exactly one command-result transport binding. The explicit relation and
   `ExactReceiptAndCommandResultBinding` assertion close the prior transport
   cardinality gap.

The non-branching same-fence evidence-history requirement and the C1-to-C2
contiguous-successor observation rule also remain explicit and correctly
scoped.

## Implementation fence

The Alloy result remains bounded relational design evidence, not a proof of
Python serialization, path/reparse safety, filesystem atomicity, subprocess
behavior, packaging, or the eventual API/SBE runtime integration. Slice 2 must
turn every mapped rule into executable provider-free fixtures, including exact
replay, changed-key conflict, ordinary-result precedence, and the receipt /
command-result identity joins. Runtime integration remains separately gated.
