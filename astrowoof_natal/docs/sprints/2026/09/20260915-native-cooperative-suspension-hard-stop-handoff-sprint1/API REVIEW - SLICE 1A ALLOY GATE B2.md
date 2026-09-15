# API review — Slice 1A Alloy protocol spike / Gate B2

## Decision

The shared model is a strong and useful protocol spike. API agrees with the
corrected checkpoint-anchor rule, the need for non-branching same-fence
resolution history, and observation-time—not fence-admission-time—ordinary
result precedence.

The recorded SAT worlds, bounded UNSAT assertions, and deliberately weakened
SAT witnesses are good evidence that the model is inhabited and that its
protected relations are doing work. The stated scope limits are honest.

**Gate B2 is not approved quite yet.** Two small but material model/prose
alignment corrections are needed before schemas/readers or runtime work begin.

## Required correction 1 — distinct request identities for one invocation

`conflictingReplay` currently means same invocation + same `RequestKey` + a
different digest. Thus `FullContract` still permits two *different* request
keys for one supervision invocation, each with a current supported request and
its own non-refusal result. That contradicts the Gate B prose:

> A second differing request for the same supervision invocation is
> `suspension_refused/request_conflict`.

The control channel is request-isolated and fixed-name precisely to prevent
this capability from becoming a sequence of independently valid stop commands.
Please model and fixture both cases:

1. exact replay of the first canonical request is inert and returns its same
   result/receipt identity; and
2. a later distinct request for the same invocation—whether it changes key,
   digest, actor/reason, checkpoint, or another bound field—can yield only the
   typed conflict refusal for the later request. It cannot alter or downgrade
   the first canonical result.

This should be expressed in terms of the complete canonical request identity,
not just same idempotency key. Retain an inhabited valid-first-then-conflict
world so the rule is not vacuous.

## Required correction 2 — precedence suppresses suspension publication itself

`PriorOrdinaryResultDominates` currently requires only that `Resolution` select
the ordinary result and omit `selectedSuspension`. It still permits a
`SuspensionResult` to have been published for a request even when an ordinary
terminal/delivery result for that invocation was committed before the native
safe-point `observedAt`.

The prose says the ordinary result remains authoritative and is **returned
unchanged**. At that observation point SBE should return the exact ordinary
command result, not mint an otherwise-unselected suspension result/receipt.

Please change the full-contract rule and its positive scenario so that an
ordinary result preceding `observedAt` suppresses the suspension result for the
request entirely. The valid precedence world should contain the request and
ordinary result, then an API resolution selecting that ordinary evidence, with
no suspension result/receipt. Keep the weakened witness proving the bad
publication is otherwise possible.

## Receipt/transport note

The model currently represents `SuspensionResult` but not the contract's exact
receipt or command-result transport envelope. Before declaring the Slice 2
schema/reader contract complete, add a compact receipt relation proving one
canonical receipt/output binding per canonical result and exact replay. It need
not model bytes or stdout mechanics; equality/cardinality and same-invocation
joins are sufficient. This is necessary to carry the one-result rule through
the public result/receipt handoff rather than proving only an internal outcome.

## Accepted portions

- C1 admission checkpoint versus same-or-contiguous C2 safe-point observation
  is now correctly treated as lineage rather than observation-time equality.
- Acyclic, non-branching, same-fence resolution history is the right API
  resolution shape; the fork witness usefully demonstrates why append-only
  predecessor links alone were insufficient.
- Worker-execution-only reclamation, cross-run isolation, and no partial
  custody settlement preserve the intended authority split.
- The bounded scope, analyzer version, model hash, receipt, rule mapping, and
  zero-external-state statement are adequately recorded.

## Next gate

Once the two required corrections and the receipt-binding coverage are in the
canonical model, rule map, receipt, and Gate B prose, API can re-review B2.
No schema, reader, coordinator, provider, R2, process-control, or deployment
work is approved before that re-review.
