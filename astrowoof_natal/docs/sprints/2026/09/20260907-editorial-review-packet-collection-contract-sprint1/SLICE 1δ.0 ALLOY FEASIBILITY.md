# Slice 1δ.0 — Alloy tooling, scope, and translation feasibility

## Result

Feasible. A pinned portable Alloy distribution runs locally without installing
system Java or adding a Python/package/runtime dependency. The content-free
two-packet model parses, produces both ordinary terminal worlds, and checks
three representative assertions successfully within its exact recorded scope.

This is a voof-paws, not authorization to begin the counterexample campaign.

## Tool identity

- Tool: Alloy Analyzer CLI
- Version: `6.2.0`
- Distribution: official `alloy-6.2.0-windows-amd64.zip`
- Download SHA-256:
  `7379feeb56f5ea77ae20340b051436d05aab014eb1800786bb792a40fed5a576`
- Local-only location: `C:\tmp\alloy-6.2.0-windows-amd64`
- System Java before/after: absent; the portable distribution supplies its own
  runtime.
- Production/package dependency change: none.

The official CLI identified itself as `6.2.0` and exposed `commands` and `exec`
subcommands. The downloaded archive and extracted executable are tooling only
and are not part of the repository or release artifact.

## Model identity

- Model: `tools/editorial_review_contract_v1.als`
- Model SHA-256:
  `cea9de10087a66f4affb9989e08aeab245e9f4a11992d83b7223c6860f7c9b71`
- Solver: Alloy CLI default `sat4j`
- Symmetry setting: CLI default `20`
- Repeat: `1`
- Private raw CLI output:
  `.tmp-editorial-review-alloy-slice1delta0/`

The raw Alloy receipt contains local timestamps and durations and is therefore
not claimed byte-deterministic. This evidence document records the stable model,
scope, command outcome, and identities instead.

## Exact finite scope

Every command used:

- exactly 2 packets: one accepted and one editorial closeout;
- exactly 16 decisions: 8 per packet;
- exactly 6 initial-pass plus 2 post-initial decisions per packet;
- exactly 2 terminal selections;
- exactly 2 findings;
- exactly 4 validations, including terminal-owned validation in both packets;
- exactly 22 projections;
- up to 12 decks and 12 payload-digest atoms;
- exactly 4 actions, 4 bindings, and 4 Responses;
- at most 6 artifact observations, while requiring at least one used deck per
  packet to have no artifact observation; and
- exactly 2 API observations.

The model additionally requires distinct selected deck objects across packets
with equal payload-digest atoms. This proves cross-packet payload equality is
different from packet-scoped artifact-wrapper identity.

These are bounded results. They are not universal proofs of Python code,
serialization, larger histories, or unmodeled topology.

## Satisfiability before assertion checks

`validTwoPacketWorld` returned `SAT`.

The satisfying scope contains:

- an accepted packet whose first post-initial candidate is materialized,
  distinct from input, and adopted;
- a later materialized candidate that is not adopted;
- an editorial-closeout packet with a non-materialized attempt followed by a
  distinct materialized but non-adopted candidate;
- accepted selected/delivered equality and closeout with no delivered deck;
- terminal-owned validations;
- decision-owned validations;
- accepted selection owned by the exact post-initial decision and editorial
  closeout selection owned by assembly evidence;
- multiple post-initial provider action/binding/Response joins;
- repeated cross-packet deck payload equality; and
- deliberately absent artifact observations.

This guards against vacuous assertion success caused by an inconsistent model.

## First assertion results

| Command | Result | Meaning within recorded scope |
| --- | --- | --- |
| `check NoResponseReuse` | `UNSAT` | no counterexample to unique Response ownership |
| `check SelectedDeckReachable` | `UNSAT` | no counterexample to terminal selection equaling final native output |
| `check ProjectionStaysInPacket` | `UNSAT` | no cross-packet projection/member counterexample |

For Alloy `check`, `UNSAT` means no counterexample exists within the selected
finite scope. It is not a universal production proof.

## Modeling corrections made during feasibility

The feasibility and API review cycle revealed four weak or ambiguous witness
definitions before the counterexample gate was recorded:

1. artifact absence could have selected a deck used by the other packet;
2. an adopted candidate could equal its input and satisfy transition equality
   without visibly representing a changed candidate.
3. terminal selection ownership was not distinguished between a decision-owned
   accepted result and an assembly-owned editorial closeout result; and
4. the model did not require a genuine decision-owned validation witness in
   addition to terminal-owned validation.

The model now defines packet-local `usedDecks`, requires absent artifacts from
that set, requires the accepted adopted candidate (and closeout's later
non-adopted candidate) to differ from input, explicitly models decision versus
assembly selection origins, and witnesses both validation-owner classes. This
is early evidence that even a small relational model can expose
specification-quality weaknesses distinct from runtime tests.

## Feasibility assessment

- Tooling viability: **yes**, with a portable pinned local tool.
- Faithful relational mapping: **yes**, for the chosen semantic spine.
- Production dependency risk: **none at this stage**.
- Hidden-specification risk: manageable only if the rule mapping remains
  one-to-one and prose changes precede model changes.
- Evidence value so far: positive but preliminary; it caught two weak witness
  formulations, not yet a missing production invariant.

Recommendation: proceed to Slice 1δ.1 after voof-paws approval. Run the bounded
counterexample campaign, then decide whether Alloy earns retention as an
optional developer check. Required Slice 1ε remains independent.

## Commands

```text
alloy.exe version
alloy.exe commands <model>
alloy.exe exec -f -c * -t json -o <private-output> <model>
```

No provider, network (after the explicit official tool download), R2, Better
Stack, API, database, workspace-state, or release operation occurred.
