# API Voof-paws 2 review — closed cohort timeline contract

## Decision

The separate, closed diagnostic projection is aligned with the API/SBE
boundary. The source/report joins, boundary provenance, explicit
non-authoritative final posture, duration recomputation, and
`witness_only_not_sla` handoff fence are all the right shape.

Please make the two narrow corrections below, then Slice 2 is approved.

## Required corrections

1. **Bind evidence family to canonical timestamp field mechanically.** The
   narrative freezes native SBE at `message.timestamp` and API wrapper evidence
   at `message.observed_at`, but the validator currently permits either allowed
   field for either family. Require exactly:

   - `native_sbe` → `message.timestamp`; and
   - `api_worker_wrapper` → `message.observed_at`.

   This prevents an adapter or future fixture from quietly placing wrapper
   evidence on the native clock (or vice versa) while retaining a superficially
   valid `clock_relation`.

2. **Order observed handoffs by witnessed chronology, with identity only as a
   tie-breaker.** The validator presently orders them lexicographically by
   opaque `handoff_id`. The contract says these are ordered cohort facts, and
   renderers will consume them as a temporal sequence. Require ordering by the
   source/destination boundary time (or a derived explicit chronological key),
   then stable handoff identity for ties. Do not turn a digest's accidental
   lexical ordering into presentation semantics.

## Confirmation after correction

With those two mechanical fences in the schema, reader/validator, and mutation
tests, API approves Slice 2's adapter/reducer work. The projection remains
diagnostic only: it may show observed API-wrapper allocation windows and native
events together, but it cannot establish global capacity ownership, native
terminal posture from wrapper failure, or any lifecycle/settlement authority.
