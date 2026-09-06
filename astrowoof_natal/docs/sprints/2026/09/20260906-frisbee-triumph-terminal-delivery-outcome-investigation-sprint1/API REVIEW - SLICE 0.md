# API review — Slice 0

## Decision

Approved. The evidence is sufficient to classify Triumph as an API terminal-
disposition mapper defect. No SBE runtime change, retained-checkpoint inspection,
or provider-free SBE reproduction is warranted for this incident.

## Cross-boundary conclusion

The exported trace proves the exact native sequence: provider response retrieval,
polish adoption, validation and lint success, delivery packaging, sealed
`delivery_complete` result/receipt, and terminal closeout. The API then accepted
generation 9 and emitted its own non-retryable
`native.terminal.delivery_complete` worker failure.

API source contains the corresponding split: sealed-terminal result readers already
map exact `delivery_complete` evidence to `DELIVERY_ACCEPTED`, but the generic
inspection helper maps an `execution_capacity_disposition=terminal` inspection to
`TERMINAL_CLOSED` without preserving the exact sealed terminal outcome. The worker
then correctly treats `TERMINAL_CLOSED` as a failed closeout. The fault is therefore
an API consumer-path inconsistency, not an SBE publication defect.

Frisbee must remain a separate outcome. Its eight reported actions and mixed
polish acceptance lead to ordinary `FINAL_QA_REQUIRES_REVIEW`; it does not support
generalizing the Triumph correction beyond exact delivery-publication evidence.

## API follow-up constraints

The API correction should add a provider-free regression for the affected generic
reconciliation/inspection route and prove all of the following:

1. exact sealed `delivery_complete` ingress reaches API's successful delivery path;
2. review-required, terminal-failure, and retained-provider-custody outcomes retain
   their existing non-success semantics;
3. result/receipt identity, generation, idempotency, and capacity-release behavior
   remain exact.

SBE may close this investigation as native-side resolved. No SBE release is needed
for the API fix.
