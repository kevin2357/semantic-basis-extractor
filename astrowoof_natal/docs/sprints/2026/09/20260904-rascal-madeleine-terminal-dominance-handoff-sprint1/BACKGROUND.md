# Background — Rascal/Madeleine terminal-dominance handoff

## Trigger

Fresh QA cohort on native `0.4.45` passed the difficult early pipeline:

- Rascal Rugelach, API run `ca4f7886-8b14-4507-8cd2-95d71ac07462`, native run
  `c6a9c8bcd0a25029ab5451160e1eda18c4fc9746b6902d2cb92c5772d2692f1e`.
- Marauding Madeleine, API run `98d2819f-4807-4f13-9b73-9bc8e8d2e1f5`, native
  run `064c17a411af2df9670372d1e6d1cf71880d2f1c0d5d92b0682e3da751696965`.

Both completed six initial authoring actions, correctly reconciled all six
provider responses, prepared/submitted/adopted one polish action, and reached
a native terminal conclusion. The failure is in the terminal handoff surface,
not the provider, retry, custody, or polish-adoption seams.

## Frozen trace facts

Rascal’s SBE trace establishes:

1. polish response was joined to its exact optional-stage consumer;
2. lint passed with zero warnings;
3. delivery package was constructed;
4. native status became `DELIVERY_COMPLETE` and a sealed native publication
   reported `outcome=delivery_complete`;
5. while still `DELIVERY_COMPLETE`, SBE prepared a `qualitative_critic` action
   and selected `await_external_authority` for that action.

Madeleine’s trace establishes:

1. polish response was joined to its exact consumer;
2. final validation failed and lint passed;
3. native status became `FINAL_QA_FAILED` and publication reported
   `outcome=review_required`;
4. the surrounding provider-cycle result still advertised local progress,
   leading a later API job to re-enter a lifecycle that was already terminal.

The later API failures (`SBE temporal lifecycle is terminal`) are therefore
secondary symptoms. API will add its own strict terminal fence, but must not
invent successful delivery from conflicting native state.

## Required native contract

Once a terminal native conclusion has been committed, it dominates all later
optional-stage selection and authority preparation in that cycle:

- no qualitative critic/candidate or other new provider action may be prepared;
- no external-authority request may be emitted;
- the emitted cycle result must unambiguously identify the exact sealed result
  and terminal outcome;
- completed delivery must use the normal delivery handoff; editorial terminal
  review must use the normal terminal-review handoff;
- malformed or conflicting terminal evidence remains a typed refusal.

## Scope / guardrails

- Provider-free source/packaged tests only; no provider, R2, API, QA, or
  retained-run mutation is authorized.
- Do not change editorial product policy or retroactively recover these runs.
- Preserve qualitative-stage behavior before a terminal conclusion. This is
  terminal dominance, not a broad disablement of qualitative review.
- Coordinate the minimum public result metadata API needs for the companion
  API Sprint 76 queue fence.
