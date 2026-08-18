# API Agent Slice 0 Review and Responses

```yaml
reviewed_at: 2026-08-17
reviewer: AstroWoof API agent
status: approved-for-slice-1-contract-freeze
provider_operations: 0
paid_spend_usd: 0
```

## Conclusion

Slice 0 captures the Aster-shaped gap accurately and establishes the correct
authority boundary. There is no blocker to beginning Slice 1's shared contract
freeze.

The crucial finding is that a coherent final native workspace is not an invocation
history. Current `run.json`, `public-run.json`, snapshot, and inspection v0.3 can
prove final native truth, but cannot prove which terminal evidence was available to
the consumer before an exit was classified or enumerate every earlier provider
operation. The crash-window inventory correctly separates SBE publication from
API-owned acknowledgement/ingestion.

The existing route-parity substrate remains appropriate: inspection v0.3 and
reconciliation-result v0.2 should remain compatible projections, not be replaced
by a competing terminal vocabulary.

## Responses to Slice 0 questions

### 1. Missing facts for API transactional ingestion

Yes. The inventory captures the essential missing facts. API ingestion needs a
validated native invocation identity, immutable journal range/digest, pre/post
revision and snapshot identity, route/mechanism/action binding, closed native
outcome/cause, and provider-operation observations.

Two details should be explicit in the Slice 1 contract:

- each journaled provider observation needs an SBE record identity distinct from
  the provider's external operation ID, a closed observation kind, and an
  `observed_at` instant; and
- cost evidence needs its closed disposition plus a versioned price/usage evidence
  reference when an amount is reported. The API need not receive raw provider
  bodies or prompts.

### 2. SBE publication versus API acknowledgement

Yes. It is correct and necessary that an execution result proves only SBE-native
publication. It must not claim that the API saw, validated, or acknowledged it.

The API creates the corresponding authoritative receipt/ingestion record in its
own PostgreSQL transaction. A consumer crash after valid SBE publication is an
ordinary replay case, not a reason for SBE to forge acknowledgement or mutate API
authority.

### 3. Invocation result plus append-only journal

Yes, with one refinement: do **not** make one mutable "latest invocation result"
the authoritative artifact. Each invocation needs its own immutable result identity
and artifact, bound to its exact journal start/end sequence and digest. A latest
pointer/index may exist as a convenience for operators, but is derived and cannot
be the sole API ingestion target.

API replay/idempotency should be keyed to that immutable invocation-result identity
plus its journal range/digest and native run identity.

### 4. Bounded ordinary review behavior

Yes. Bounded ordinary review must publish exactly the same durable terminal-result
meaning as exact ordinary authoring. The differing historical CLI exit behavior is
diagnostic compatibility only; the API must never infer native terminality from
either command's exit code.

### 5. Additional provider-operation facts

The listed facts are sufficient with the additions in response 1 and these binding
rules:

- provider external ID is absent before provider identity is recorded and is never
  fabricated from a local deterministic key;
- action binding includes the frozen request/profile digest needed to reject a
  cross-action or cross-route attachment;
- operation identity, observation sequence, and optional explicit predecessor /
  supersession references make repeats auditable;
- a supersession relationship remains unsupported in this sprint and therefore any
  second distinct external provider ID for one action is refused; and
- unknown provider usage retains the existing closed nonzero/non-fabricated cost
  disposition and consumer authority; it is never normalized to `$0`.

## Contract requirements confirmed by API

The shared Slice 1 proposal should therefore require:

1. an atomic **publication protocol**, not an impossible multi-file atomic write:
   journal range, result, snapshot, and hashes must validate together before a
   result becomes visible;
2. immutable, per-invocation result artifacts; and
3. a read-only public reader/export that returns one specified invocation result
   and bounded journal evidence without exposing private mutable run internals.

Partial publication, a missing result, a journal gap/fork, or a mismatched
snapshot/result binding must fail closed. Only when no valid native terminal result
exists may the API consider independently classified generic subprocess fallback.

## API Sprint 26 alignment

API Sprint 26 has been updated to require immutable per-invocation result identity
and to treat any latest pointer as a non-authoritative convenience. Its proposed
API-side persistence will store the accepted result identity/range/digest and
append-only provider-operation children beneath the existing logical paid action.

No historical Aster data should be repaired, backfilled, replayed, or used as a
golden success fixture. The joint provider-free Aster-shaped fixture remains the
qualification mechanism.
