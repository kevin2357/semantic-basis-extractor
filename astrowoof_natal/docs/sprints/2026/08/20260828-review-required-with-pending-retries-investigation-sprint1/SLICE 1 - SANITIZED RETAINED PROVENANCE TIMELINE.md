# Slice 1 — sanitized retained provenance timeline

## Outcome

The two retained workspaces show the same lineage defect pattern. Neither proves
an editorial terminal review or exhausted retries. Both are nonterminal,
`AWAITING_SPEND_AUTHORIZATION` workspaces whose last sealed native transition is
`provider_pending`.

The later API `native.review.requires_review` result is directly explained by the
v0.7 post-fan-in inspection rule that maps the presence of any authorized,
providerless native action to `retain_for_review`. The API then maps that
nonterminal capacity disposition to its durable failure reason. This is a safety
review projection, not evidence that SBE reached `FINAL_QA_REQUIRES_REVIEW`.

## Shared retained topology

For both runs:

1. Passes 1–5 accepted their first attempts.
2. Pass 6 attempt 1 failed the authoring-pass gate with closed issue code
   `theme_group_coverage`.
3. An early attempt-2 creative-retry action gained a durable provider identity
   and remains `WAITING`.
4. A later, distinct attempt-2 action was created, completed, reported, and also
   failed `theme_group_coverage`.
5. An attempt-3 action was prepared and authorized but never entered provider I/O.
6. A second attempt-3 action was prepared. It is the action referenced by the
   pass attempt, remains unapproved, and has the same request digest as the
   reported attempt-2 action—not the authorized attempt-3 action.
7. The retained run contains three pass attempts, but attempt 3 has not run QA;
   `max_attempts=3` is therefore not exhausted by completed editorial attempts.

The duplicated route identities and differing request digests prove that action
counts alone were misleading. Each run contains two native actions for attempt 2
and two native actions for attempt 3.

## Pippin von Waffle

- Native run: `8fcce2334d4e717595cafe5af18bb6ee5d097270da362a6783a5fab2f5a8bb79`.
- Retained revision/status: 88 / `AWAITING_SPEND_AUTHORIZATION`.
- Pass 6:
  - attempt 1: `paid_515c95af47adc2c87c72c192`, QA rejected;
  - early attempt 2: `paid_d3a5e09f09f5c64716ccac42`, provider ID durable,
    ledger `WAITING`, absent from the final pass-attempt pointer;
  - reported attempt 2: `paid_b22c4c30626fa24636e1f74f`, QA rejected;
  - authorized attempt 3: `paid_dce132aa80a57e21f92fcb94`, providerless;
  - current prepared attempt 3: `paid_387fa13b80e7a5b7acad9c96`, referenced by
    the pass and awaiting authority.
- Journal chronology:
  - 06:12:51–06:12:55Z: early attempt-2 action authorized, consumed, entered,
    received provider identity, and became pending;
  - 06:15:43Z: later attempt-2 action prepared;
  - 06:16:06–06:16:08Z: later attempt-2 action authorized, entered, and received
    a different provider identity;
  - 06:18:35Z: later attempt-2 provider result completed/reported;
  - 06:18:36Z: attempt-3 action prepared;
  - 06:19:06Z: that action authorized, then a second attempt-3 action prepared;
  - 06:19:08Z: last retained transition remained `provider_pending`.

Provenance: `run.json` SHA
`9ff55f17a1243e0e07cbe0171cce5bcb65ba540a2feadf8b544dc7ea3a9f85ca`;
`native-transition-journal.jsonl` SHA
`c7ac1b256d779e2c34d42a1b809eb63ad898f815693409e0c9f9e03e88f91ebb`;
attempt-1/2 gate report SHAs `647d2621d21f81a0bd07a2d58afeca964cad5e73bb88fb534b2bab9338010b78`
and `c89a3d3fc46e98db78c8cc9d70f711dcd27e94e2689378a8c25b68e0699d503b`.
Evidence class: direct. Confidence: high.

## Duchess Crumpet

- Native run: `d436f2a008656d16bb8f1efbdb11342278ed808ad88acba3fdafef087d230268`.
- Retained revision/status: 89 / `AWAITING_SPEND_AUTHORIZATION`.
- Pass 6:
  - attempt 1: `paid_c019f259dbb595c12540a1f1`, QA rejected;
  - early attempt 2: `paid_14eebbbb1f47f7c682849334`, provider ID durable,
    ledger `WAITING`, absent from the final pass-attempt pointer;
  - reported attempt 2: `paid_849986497f19b4ffb84a34f9`, QA rejected;
  - authorized attempt 3: `paid_e85cd8a7ca4c65670899b2be`, providerless;
  - current prepared attempt 3: `paid_f20ea3978b41e01418dbf0a1`, referenced by
    the pass and awaiting authority.
- Journal chronology:
  - 06:14:35–06:14:38Z: early attempt-2 action authorized, entered, received a
    provider identity, and became pending;
  - 06:20:07Z: later attempt-2 action prepared;
  - 06:20:31–06:20:32Z: later attempt-2 action entered and received a different
    provider identity;
  - 06:23:02Z: later attempt-2 provider result completed/reported;
  - 06:23:03Z: attempt-3 action prepared;
  - 06:23:30Z: that action authorized, then a second attempt-3 action prepared;
  - 06:23:33Z: last retained transition remained `provider_pending`.

Provenance: `run.json` SHA
`fd52a54c92ee136a987223d7393fc0b7b5e4d3a6a4bdd3b2d5000bba3c4bb323`;
`native-transition-journal.jsonl` SHA
`c58c4a06709929df9ece065913c26e28ea2130e6700aa8c7ef3008a74e551f43`;
attempt-1/2 gate report SHAs `a7913ed2a93f0d8c052696f77549a60054be9fcea46ef3a37ab42c0ebb87c9ee`
and `2e648cd6da45b4401643e200f8b787548e98525aa7e6f013e9a9afd71984c1f3`.
Evidence class: direct. Confidence: high.

## Path-identity discrepancy

The API inspection authority expected logical roots based on API run IDs. The
native snapshots instead bind worker-workspace UUID roots. All archive and member
hashes validated, and both native run IDs matched, but the roots do not.

This is a distinct API/checkpoint metadata contract discrepancy. It did not alter
the locally inspected bytes and should not be silently normalized in a recovery
path. Evidence class: contradictory. Confidence: high.

## Causal classification at Voof-paws 2

- **Editorial review was valid/exhausted:** disproved for the retained checkpoint.
  Attempt 3 had no QA result and the run was not in a terminal review status.
- **Retry lineage/fan-in defect:** strongly supported. Duplicate action lineages
  exist for the same pass/attempt, and the current attempt-3 pointer does not join
  the already-authorized attempt-3 binding.
- **Custody projection defect:** supported. A nonterminal mixed-custody workspace
  is collapsed to `retain_for_review` solely by authorized-providerless presence,
  masking retained provider custody in the selected branch.
- **Historical terminal cause:** the API review result is explainable as the
  public inspection/mapping result; no native terminal result exists in the
  retained snapshot.

Overall confidence: high for retained lineage and branch-selection cause;
medium-high for the precise runtime sequence that created duplicate bindings,
which Slice 2 must reproduce through supported provider-free boundaries.
