# API review — Slice 1 mixed-custody findings

## Decision

**Voof-paws 2 is approved.** Generation 18 is sufficient; do not retrieve
generation 17. The evidence establishes a native mixed-custody contradiction,
not an API misreading of a valid terminal handoff.

The API must retain its strict refusal to treat public terminal lifecycle bytes
as provider-continuable. The correction belongs on the native producer side:
SBE must publish a coherent nonterminal provider-custody projection until that
custody is reconciled and a genuine terminal result is sealed.

## Confirmed causal distinction

Generation 18 joins all required facts at revision 104:

- `FINAL_QA_REQUIRES_REVIEW` is the outer status;
- the polish action is authorized, consumed, provider-bound, unreported, and
  awaiting first retrieval;
- the live v2 intent is `PROVIDER_PENDING` with exactly the same provider ID;
- retrieval count is zero; and
- no sealed Glimmer terminal-review result exists.

That makes the required precedence unambiguous: durable ordinary-provider
custody outranks a provisional final-QA review finding for public scheduling and
terminal publication. A status label cannot substitute for terminal closeout
authority.

## Slice 2 contract freeze requirements

Please freeze the following without inventing any API-side custody inference:

1. While a durable ordinary-provider operation remains unresolved, public
   lifecycle must expose a reconciliation-compatible nonterminal disposition;
   it must not expose a terminal disposition merely because final QA currently
   warns/requires review.
2. A terminal public result is authoritative only when its exact inventory has
   no unresolved provider identity, call-entry ambiguity, or required native
   publication work.
3. The v2 executor must revalidate its just-persisted state before provider
   call-entry. If the checkpoint contradicts the intent, it must fail before
   POST and leave a typed, replay-safe result—not create provider work from a
   terminal-shaped checkpoint.
4. Existing durable provider identity remains strictly retrieval/reconciliation
   only. Neither SBE nor API may use this correction to create a replacement
   operation or silently retire Glimmer's already-bound polish action.
5. A providerless authorized action is a separate case: any retirement/denial
   remains an explicit API-authorized/native-supported outcome, never a side
   effect of status reduction.

The causal matrix should separately prove the two ordinary paths:

- final QA warning + **no** active polish custody can lead to a legitimate
  review-terminal result; and
- final QA warning + active polish provider custody remains nonterminal and
  reconciliation-capable until a later supported disposition is reached.

Please keep the absence of a sealed native result as a first-class check in the
API-facing artifact/fixture. That prevents a future consumer from inferring
terminality from `FINAL_QA_REQUIRES_REVIEW` alone.

SBE may proceed to Slice 2.
