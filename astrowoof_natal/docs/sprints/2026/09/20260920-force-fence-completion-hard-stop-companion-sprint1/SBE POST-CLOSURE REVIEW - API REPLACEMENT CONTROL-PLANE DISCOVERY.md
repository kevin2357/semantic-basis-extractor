# SBE post-closure review — API replacement control-plane discovery

## Decision

API's Slice 3B discovery is correct: platform replacement cannot be qualified
by validating a caller-supplied dictionary. It needs a durable evidence
protocol before it can release the fenced target's allocation.

**No new SBE wheel producer is currently indicated.** The missing facts are
worker-control-plane facts owned by the API worker parent and the platform
adapter, not facts that a single SBE subprocess can observe authoritatively.

## Why this is API-worker-owned

The SBE native process can attest only its own exact safe point and its own
closed result/receipt/request chain. It cannot establish any of the following:

- the complete set of other children launched by the API worker;
- that the worker will admit no new child after a replacement fence;
- that an API worker boot has retired or does not overlap a new boot; or
- that a Render operation/restart corresponds to the target fence and has
  produced a new serving worker.

Having SBE emit fields for those claims would only reflect unverified API
inputs back to API. That would add format without adding authority.

## Minimal provider-free next boundary

The API worker lifecycle protocol should provide immutable or transactionally
locked receipts for:

1. **Worker boot record:** a fresh boot identity published before any child can
   launch, with retirement state that rejects later artifacts from that boot.
2. **No-new-child fence:** a worker-scoped admission state set before the
   pre-replacement inventory and consulted by every child-launch path.
3. **Authoritative child ledger:** parent-maintained launch, exact PID, exit,
   and classification records for every child of that boot—not inference from
   historical SBE supervision rows.
4. **Collateral disposition:** each inventoried non-target child has an exact
   safe recovery record or an explicit refusal; an unclassified member blocks
   replacement finality.
5. **Platform replacement receipt:** the exact control operation, old-boot
   retirement/no-overlap readback, and independent new-boot readback bind to
   the target fence and worker role.

These can be designed and qualified provider-free using an injected platform
adapter and deterministic worker-runtime fixtures. The eventual live Render
operation is a later operational gate, not a prerequisite for proving the
state machine.

## SBE boundary preserved

The existing SBE v1 suspension result remains useful for an individual child
that reaches a cooperative safe point, but it is neither required nor
sufficient for platform replacement. No SBE schema change, source change,
wheel build, provider call, R2 access, or live mutation is requested by this
review. Reopen native work only if the API worker lifecycle protocol identifies
a concrete missing per-child safe-stop or closed-reader fact.
