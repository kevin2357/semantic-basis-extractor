# API review — Slice 1 Ganache terminal-review contract

## Decision

Approved for Slice 2 provider-free reproduction.

The proposed bridge is properly narrow: it applies only after exact result
adoption and complete provider-custody closure, and only to the deterministic
`AssemblyContractError`. Reusing the existing v0.2 native result, receipt, and
terminal-review command-result envelope avoids needless schema proliferation.

## API ingress agreement

`review_required` with `finalization_contract_invalid` is the correct native
outcome. API will treat the invocation-bound terminal-review command result as
the primary ingress evidence and validate its exact sealed result/receipt join
before considering process exit status. Exit `2` alone is not authorization to
terminalize or retry.

The API companion investigation has separately established that Ganache's
attempt-limit failure retained an active capacity allocation and starved Froth.
That is API capacity cleanup work, independent of this SBE terminal-review
bridge. The SBE bridge must not attempt to compensate for queue fairness or
capacity release.

## Slice 2 guardrails

1. Demonstrate that the positive fixture has closed action custody before the
   assembly error; do not derive closure from the error itself.
2. Assert the terminal-review envelope is emitted before exit `2`, and that
   replay returns the same identifiers/digests without provider I/O.
3. Keep the mixed-custody fixture as a custody-first non-seal case. The noted
   existing expectation mismatch should be corrected or isolated as stated;
   it is not evidence that this bridge should supersede retained provider
   custody.
4. Do not broaden to Batch, bounded routes, ordinary initial admission, or
   Froth's API-owned scheduling path.

No retained-run recovery, provider action, or release is authorized by this
approval.
