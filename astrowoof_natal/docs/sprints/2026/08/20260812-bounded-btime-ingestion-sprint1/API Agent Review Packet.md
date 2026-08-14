# API Agent Review Packet - Bounded Natal Candidate

Status: ready for AstroWoof API review. This review is required before SBE release
recommendation. The candidate is not tagged or published.

## Candidate identity

- SBE candidate: 0.4.0
- Wheel SHA-256: `4fb7a114ae4866475778d36b677d170499a5558e0f1a854aeb88616b9c6c8c84`
- AGF: 0.8.1, SHA-256
  `860c48793318c82c986b32664cd0f3fe97c4b1e02fb1e489561bc395c8b5a3ed`
- SPC: 0.11.0, SHA-256
  `82290df44fe5697e87df2e27eb0aa4bab3b7954c66ce988efda0962964e1366d`

## Requested API review

Please review and respond on these integration points:

1. `astrowoof-run-bounded-natal` create/resume arguments, public JSON state, and
   exit code `3` for waiting, budget exhaustion, or ambiguous submission.
2. Exact prepared-action authorization binding and the retained API ownership of
   cross-run transactional reservations, quotas, circuit breakers, entitlements,
   billing reconciliation, and publication policy.
3. Durable provider-ID reconciliation: restart performs GET-only polling; an
   interrupted submission without a durable identity remains ambiguous and
   fail-closed. Deterministic keys are not represented as provider idempotency.
4. Stable logical absolute workspace restoration, complete snapshot validation,
   quiescence inspection, and closeout requirements before worker scratch removal.
5. Bounded delivery/schema/provenance consumption and whether the sanitized sample
   contains the identifiers and evidence-scope separation needed by API/frontend.
6. The explicit rejection of `service_level=batch` until a real bounded Batch
   submission adapter exists.
7. Event vocabulary: bounded route/admission/basis/selection/compilation events
   supplement the shared lifecycle/provider/spend events. Confirm that API logging
   can treat them as non-authoritative observations without requiring extra
   release-blocking event types.
8. The editorial-only provider response boundary: SBE reattaches immutable claim
   authority, evidence provenance, subject, registry, and term identities and
   rejects identity-set drift.
9. Exact pin/hash instructions and the proposed 0.4.0 compatibility boundary.

## Installed qualification

The final candidate was rebuilt after provider-schema hardening. Two builds are
byte-identical, all 274 source tests pass, and the exact final wheel passed Linux
`pip check`, installed lifecycle/release smoke, full-scale bounded delivery,
complete snapshot inventory, quiescence inspection, and closeout with exact AGF
0.8.1/SPC 0.11.0.

Please return blocking corrections, non-blocking follow-ups, and an explicit
consumer-contract acceptance/rejection. SBE will reconcile the response before
requesting product-owner Gate 9 approval.
