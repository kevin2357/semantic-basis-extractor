# Slice 3C — Pass-attempt contract correction

## Outcome

The provider-free contract now represents initial attempts and creative retries
as the same pre-assembly species of pass materialization. It does not invent a
whole-deck transition before a whole deck exists.

The corrected v3 surface proves this chronology:

1. exactly six attempt-1 decisions exist, one per released pass;
2. an initial attempt may be accepted or rejected;
3. a rejected initial attempt carries no `accepted_workspace_*` fields;
4. a creative retry names the exact rejected predecessor decision, attempt,
   acceptance outcome, and QA-report digest for the same released pass;
5. exactly one accepted winner is selected for each of the six released passes;
6. the assembly bridge binds those six winners and the assembled deck; and
7. only polish, critic, and candidate decisions use whole-deck transitions.

The positive fixture deliberately contains a rejected pass-1 initial attempt
followed by an accepted pass-1 retry. Its assembly bridge selects the retry and
the accepted initial attempt for each other pass.

## Executable evidence

- Decision, packet, projection, transport, and semantic-contract resources
  advance together to v3.
- Both packaged fixtures are regenerated from the corrected builder.
- The rehashed mutation campaign expands from 29 to 36 cases, adding rejected
  initial false-acceptance, retry relation/predecessor/QA/pass mismatches, and
  superseded/duplicated assembly-winner cases.
- Focused provider-free suite: 23 passed, with one expected optional
  `jsonschema` skip.
- The v3 Alloy model has an inhabited two-packet world (`SAT`) and models the
  rejected-initial/accepted-retry/six-winner bridge explicitly. Its response
  uniqueness check found no bounded counterexample (`UNSAT`). Two broader,
  redundant reachability checks were stopped after prolonged solving rather
  than represented as proof; their corresponding executable invariants pass.

## Side-effect boundary

No provider, network, R2, API, database, retained-workspace, runtime-builder,
packaging, release, or deployment operation occurred.

## Gate

Pause for API review of v3 before resuming Slice 3 runtime construction.
