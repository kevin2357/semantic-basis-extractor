# Slice 1δ.1 — Alloy counterexample campaign and adoption decision

## Result

The bounded campaign passed and Alloy earned retention as an **optional
developer design check**. It is not a production dependency, runtime validator,
CI requirement, or release gate.

The complete contract admits an ordinary accepted packet and an editorial
closeout packet in the same finite world. Within that same exact scope, all ten
full-contract assertions produced no counterexample. Deliberately removing each
targeted structural rule produced a counterexample, as did both forbidden
eligibility policies based on artifact completeness or API observation.

This is the requested Voof-paws 1δ. Slice 1ε has not started.

## Exact evidence identity

- Model: `tools/editorial_review_counterexamples_v1.als`
- Model SHA-256:
  `56d0a3a7b1101889d5df83a1aa398900af6fb4cc89a8c3c258de1841004c43cb`
- Stable machine-readable receipt:
  `alloy-counterexample-receipt.v1.json`
- Receipt SHA-256:
  `b1f2ae0736195baab86e988dc4382772ddf801dca633a3151d3b00bb6b5fa38e`
- Tool: Alloy Analyzer CLI `6.2.0`
- Distribution SHA-256:
  `7379feeb56f5ea77ae20340b051436d05aab014eb1800786bb792a40fed5a576`
- Solver: CLI-default `sat4j`
- Repeat per command: `1`

Raw Alloy instances remain private under explicitly named
`.tmp-editorial-review-alloy-slice1delta1-command*` directories. They include
tool-generated timestamps/durations and are not claimed byte-deterministic.

## Exact finite scope

Every campaign command used exactly:

- 2 packets: one accepted and one editorial closeout;
- 16 decisions: six initial and two post-initial per packet;
- 2 terminal selections;
- 2 findings;
- 4 validations, with both terminal-owned and decision-owned witnesses;
- 22 packet/member projections;
- 4 actions, 4 bindings, and 4 Responses;
- 2 artifact observations and 2 packet-scoped artifact identities; and
- 2 API observations.

Deck and payload-digest universes were bounded above by 12 each. The topology
requires selected deck objects to differ across packets while sharing a payload
digest, and requires at least one used deck in each packet to have no artifact
observation.

These are bounded results. They do not prove Python behavior, canonical JSON,
cryptography, compression, byte limits, arbitrary history sizes, or any
unmodeled route.

## Satisfiability before universal-looking checks

`run FullContract` returned `SAT` after correcting an initially impossible
artifact scope. The first campaign scope demanded six observed artifacts while
also requiring missing packet-local artifacts; given the finite deck topology,
those requirements could not coexist. Reducing the exact artifact count to two
made the intended accepted/closeout world inhabitable.

This correction is important evidence in its own right: the campaign did not
accept vacuously successful assertions over an empty contract world.

## Full-contract assertion results

All ten checks returned `UNSAT`, meaning no counterexample was found within the
recorded scope:

| Protected relation | Check |
| --- | --- |
| selection must be reachable from its declared decision or assembly origin | `FullSelectionReachability` |
| adopted candidates become output; non-adoption preserves input | `FullAdoptionOutput` |
| post-initial input/output continuity | `FullContinuity` |
| action, binding, and Response uniqueness by decision | `FullResponseUniqueness` |
| finding ownership remains packet-local | `FullFindingOwnership` |
| validation ownership is closed and discriminated | `FullValidationOwnership` |
| projection/member ownership remains packet-local | `FullProjectionRelation` |
| artifact identity is packet-scoped and unique | `FullArtifactIdentity` |
| missing optional artifacts remain permitted | `FullArtifactAbsence` |
| API observations do not define native eligibility | `FullObservationNonAuthority` |

## Deliberately weakened rules

Each weakened-rule run returned `SAT` and therefore exhibited the requested bad
world:

- unreachable or falsely owned terminal selection;
- adoption/output disagreement;
- broken post-initial deck continuity;
- action/binding/Response reuse;
- orphaned or cross-packet finding ownership;
- missing, dual, or cross-packet validation ownership;
- cross-packet or incomplete projection membership;
- duplicate or non-packet-scoped artifact identity;
- packet eligibility controlled by complete artifact observation; and
- packet eligibility controlled by API observation.

The last two are especially useful boundary checks: optional evidence capture
and downstream observation cannot silently become native transition authority.

## Contract clarifications earned by the spike

The two Alloy slices forced five useful clarifications:

1. artifact absence must be packet-local, not merely globally witnessed;
2. adopted/non-adopted candidates must be distinct where the witness claims a
   changed candidate;
3. accepted decision-owned selection and closeout assembly-owned selection are
   separate relationships;
4. terminal-owned validation does not substitute for a real decision-owned
   validation witness; and
5. every assertion campaign must first prove its complete finite world is
   satisfiable at the same scope.

These clarify the adopted prose without replacing it. The prose contracts
remain authoritative, and any future contract change must update prose first,
then the model and executable validator.

## Adoption decision

Retain Alloy as an optional, pinned developer aid for relationship-heavy
contract changes. Its strongest value is rapid counterexample discovery before
schema/Python implementation. Do not require it for ordinary runtime work,
packaging, CI, or release qualification unless a later sprint independently
justifies that operational cost.

The required Slice 1ε semantic validator stack remains the executable contract
and mutation-test boundary. No provider, R2, Better Stack, API, database,
workspace-state, or release operation occurred in this slice.
