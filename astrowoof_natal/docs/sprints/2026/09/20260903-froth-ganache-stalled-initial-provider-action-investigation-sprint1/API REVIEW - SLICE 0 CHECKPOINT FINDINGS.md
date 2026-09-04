# API review — Slice 0 checkpoint findings

## Decision

Approved to begin Slice 1's narrow contract/ownership work. The bounded reads
and access receipt satisfy the API coordinate packet: exactly two named objects
were read, archive and inventory identities match, and no provider, workspace,
or retained-run mutation occurred.

## Confirmed split

The two runs are not one shared provider-custody defect.

### Froth

The archive establishes a coherent generation-7, five-reported/one-waiting
initial wave and a `provider_pending` result. Its `resume_not_before` was
21:16:06Z; later provider completion is an observation outside this frozen
archive. Given the trace's absence of any later Froth invocation, SBE had no
opportunity to read or adopt that completion.

Treat Froth as an API scheduling/worker-dispatch investigation after a valid
SBE release. Do not add an SBE retry, create, or receipt-repair mechanism for
it. API will separately join the due-time scheduling rows, queue eligibility,
and worker selection/claim evidence to locate the missing post-due invocation.

### Ganache

The archive establishes the pre-completion provider-pending generation; the
later trace then establishes completed-result retrieval, local adoption, and a
deterministic `AssemblyContractError` before any successor checkpoint or sealed
result publication. That is sufficient to investigate the reconciliation
finalization boundary.

Slice 1 should specify a typed, invocation-bound native terminal/review result
for this exact post-custody deterministic finalization failure. The result must
bind the consumed action identity, pre/post snapshot identity, and closure of
the provider action inventory. API must then consume that typed result before
falling back to subprocess-status classification; it must not treat an absent
stdout payload as generic retryable dependency failure where an exact sealed
result is available.

## Tightening requests for Slice 1

1. Keep `AssemblyContractError` scoped to deterministic finalization contract
   invalidity after exact provider-result adoption. Do not broadly convert
   arbitrary reconciliation exceptions into terminal review.
2. State explicitly whether the resulting native outcome is `review_required`
   or `terminal_failure`, with a stable cause code such as
   `finalization_contract_invalid`; API needs that distinction to choose the
   durable run disposition.
3. Preserve the existing no-create/no-provider-I/O guarantee for the
   reproduction. The fixture must prove the same retry no longer occurs under
   replay.
4. Do not make SBE responsible for Froth's missed due-time dispatch. Its
   existing `release_until_due` posture is correct on the evidence available.

No SBE release is implied yet; first freeze the exact public result/ingress
contract and demonstrate it provider-free.
