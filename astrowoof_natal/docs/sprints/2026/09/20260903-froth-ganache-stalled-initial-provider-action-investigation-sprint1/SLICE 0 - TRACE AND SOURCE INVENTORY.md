# Slice 0 — trace and source inventory

## Scope

This record uses only the supplied worker trace and the checked-out source. It
does not claim retained-workspace truth and did not access R2, provider APIs, or
either native run.

## Ganache: source-backed failure path

The trace establishes this sequence for native run `41e69b…c84720d1f`:

1. Five initial actions were `REPORTED`; one action,
   `paid_d5b51ca74b5892acba11fada`, remained provider-bound.
2. At `22:09:18Z`, its durable response
   `resp_01c1992ef4b35dda006a99e187865c87d09b5cbf8eb10c67f3` was retrieved
   with provider status `completed`.
3. Reconciliation selected one ordinary local continuation, accepted pass 3,
   and entered finalization.
4. `assemble_subject()` called `assembly.assemble()`, which parsed
   `ASSIGN THEME GROUPS.md` and raised because Story 8 referenced unregistered
   `interdogpendence` chapter `grounded_companionship`.
5. The API reconciliation command received no stdout JSON and converted that
   operationally visible failure to retryable `sbe.dependency.command_failed`.

The checked-out source confirms two distinct boundaries:

- `assembly.py` still has an active structural theme-group join: when the
  assignment file exists, it requires valid registries, every referenced
  chapter ID, compatible section/card kind, and complete multi-pass coverage.
  The 0.4.41 dormant policy removed pass-acceptance evaluation, but did **not**
  make assembly ignore this historical artifact.
- `closure.main()` has a newer `AssemblyContractError` handler that seals
  `finalization_contract_invalid` for its ordinary-authoring path. The trace
  instead entered `reconcile_authoring_provider_cycle()`; its exact
  reconciliation helper catches only spend/custody exceptions around
  `finalize_subjects()` and re-raises `AssemblyContractError`. Thus the
  terminal-review fence is not shared by the reconciliation path.

This is a precise candidate defect: deterministic finalization-contract errors
with final custody are sealed on one command path but escape as generic retry
failures on another. Retained checkpoint evidence must confirm the final-custody
assertion before it becomes a repair conclusion.

## Froth: trace posture

For native run `ea2267…ea892b78`, the last relevant trace shows one retained
initial provider action, no local dependency, and an SBE
`release_until_due` / `detached_provider_pending` publication. This is the
expected no-create posture while an action is not due. The trace cannot prove
whether its current native inventory still agrees with API's provider-created
row, so no SBE defect is assigned.

## Exact evidence needed for checkpoint joins

Request an API-created immutable coordinate packet containing, for each run:

1. latest accepted checkpoint object ID/key, ETag/version, byte size, archive
   SHA-256, inventory SHA-256, generation, and restore logical root;
2. any separately stored result-index/sealed-result/receipt object identity and
   digest; and
3. explicit authorization for one `HEAD` and one `GET` for each named object.

The packet should contain no credentials, signed URLs, prompts, generated deck
content, or API-private admission/lease data.
