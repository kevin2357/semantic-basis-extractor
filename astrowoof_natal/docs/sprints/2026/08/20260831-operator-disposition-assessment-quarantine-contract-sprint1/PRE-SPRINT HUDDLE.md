# Pre-sprint huddle — operator disposition assessment

## Understanding

API needs a public SBE answer to a deliberately narrow operator question:

> Can this exact native checkpoint be removed from ordinary API scheduling and
> have only its local API lease/capacity released, while every native/provider/
> spend/workspace obligation remains preserved?

That is not terminalization, cancellation, denial, recovery, reconciliation,
or native mutation. It is snapshot-bound inspection plus a closed custody
classification.

## Existing foundation

SBE already exposes most required native facts through lifecycle v0.5–v0.8,
temporal lifecycle, provider-custody inventories, local-work inventories,
retry-lineage inspection, terminal-result availability/readers, and operator
retirement assessment. The new contract should join and reduce those supported
facts; it must not read private `run.json` meaning into a parallel taxonomy.

The likely implementation is therefore small:

- one closed schema;
- one strict Python validator that does not depend on optional `jsonschema`;
- one snapshot-validating reader/builder;
- one package resource/fixture matrix;
- one provider-free CLI/qualification receipt; and
- root-level exports and consumer handoff documentation.

## Main semantic risk

The classification must be precedence-driven rather than status-name-driven.
At minimum:

1. contradictory or unsupported evidence fails closed;
2. ambiguous submission outranks every apparently calmer state;
3. durable provider identity/custody outranks prepared authority, local work,
   or terminal-looking status;
4. completed-but-unadopted evidence remains native fan-in work, never synthetic
   completion;
5. unresolved providerless authority remains visible and cannot be silently
   discarded;
6. sealed terminal is valid only when its exact result/receipt/checkpoint join
   and remaining custody assertions support it; and
7. provider-free quiescence is proven from explicit negatives, not inferred
   from an empty list or friendly status label.

## Release posture

If implementation remains a pure read-only projection with no lifecycle,
reconciliation, provider, mutation, or scheduling behavior change, this is a
credible lean patch release:

- focused schema/semantic/fixture matrix;
- affected lifecycle/result-reader tests;
- isolated installed-wheel CLI qualification;
- package/resource/export smoke;
- deterministic wheel rebuild and dependency check;
- explicit documentation that the full runtime suite was not run.

Any discovered need to change lifecycle production semantics, native mutation,
or provider custody handling immediately disqualifies the fasty-patchy path and
requires a broader gate.
