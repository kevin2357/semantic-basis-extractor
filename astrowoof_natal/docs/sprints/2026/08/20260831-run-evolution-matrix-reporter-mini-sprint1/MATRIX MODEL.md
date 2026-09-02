# Run evolution matrix model

## Geometry

The canonical data is a rectangular matrix:

- **columns:** semantic epochs, not individual log lines or fixed wall-clock
  buckets;
- **rows:** stable entity/state lanes; and
- **cells:** the last directly observed fact for that lane during the epoch,
  plus change/error markers.

The UI may render the rectangle in a square card with scrolling or collapsed
lanes. The contract should not force N rows to equal N columns: a six-pass run
with 80 meaningful transitions is not made clearer by inventing 74 rows.

## Epoch boundaries

A new column is created when at least one high-value identity changes:

- native revision or snapshot/fingerprint;
- run status;
- lifecycle command/branch or capacity disposition;
- authority request/grant/intent identity;
- provider call entry or durable provider identity;
- reconciliation selection/result;
- pass attempt accepted/rejected/ambiguous;
- local-work consumption/refusal;
- terminal/native-result publication; or
- command exit.

Repeated fingerprints and summaries inside one unchanged epoch are counted and
linked but visually collapsed.

## Default lanes

1. Run status/revision
2. Lifecycle branch/capacity
3. Initial passes 1–6 (expandable into one lane each)
4. Retry/polish/critic/candidate attempts (dynamic action lanes)
5. External authority
6. Provider custody/I/O
7. Reconciliation and native adoption
8. Deterministic QA/local work
9. Snapshot/checkpoint/publication
10. Command/worker handoff
11. Warnings, refusals, and contradictions

## Cell vocabulary

- `●` directly observed and active
- `✓` directly observed complete/accepted
- `×` directly observed refused/rejected
- `?` ambiguous or contradictory
- `…` pending/waiting
- `↻` repeated semantic posture without proven progress
- `·` not applicable
- blank means not observed, never silently false

Every rendered cell links back to normalized event IDs/source line numbers.
Color is additive and never the sole carrier of meaning.

## Illustrative matrix from the supplied corpus

This is intentionally compressed and explanatory, not yet generated output:

| Lane / epoch | E1 retry pending | E2 retry adopted | E3 authoring done | E4 polish prepared | E5 authority | E6 provider pending | E7 reconcile | E8 local result |
|---|---|---|---|---|---|---|---|---|
| Run | WAITING r68 | AUTHORING r69 | ✓ COMPLETE r72 | AUTH r75 | AUTH r77 | WAITING r80 | WAITING r83–85 | WAITING |
| Pass 6 retry | … ambiguous | ✓ accepted | ✓ | · | · | · | · | · |
| Polish | · | · | prepared | ● attempt 1 | authorized | … `resp_055d…` | provider evidence | local work unresolved |
| Authority | · | · | · | request | request/grant | consumed | · | · |
| Provider custody | retry response | adopted | none | none | none | ● known ID | reconciliation | retained/unknown |
| Local work | fan-in due | consumed | assembly/QA | polish prepare | none | none | result handling | × `semantic_work_not_consumed` |
| Checkpoint | r68 | r69–72 | r73–75 | r76 | r77 | r80 | r83–85 | unchanged/failed progress |
| Diagnostic | · | · | · | · | · | · | · | review needed |

The matrix shows why a time-only chart is insufficient: the important story is
the changing custody and authority relationship, not simply elapsed minutes.
