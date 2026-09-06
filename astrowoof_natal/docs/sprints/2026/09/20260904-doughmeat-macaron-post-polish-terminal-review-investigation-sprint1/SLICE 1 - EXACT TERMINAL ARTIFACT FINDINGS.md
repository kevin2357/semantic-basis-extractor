# Slice 1 — Exact terminal artifact findings

## Access boundary

The owner authorized the exact operations described by
`API SLICE 0 REVIEW AND IMMUTABLE COORDINATES.md`. SBE froze separate local
access manifests, then issued one conditional HEAD and one GET for each named
generation-11 archive. The pinned ETag/provider version, byte size, archive
SHA-256, and safe archive-member constraints all passed.

Observed operation totals:

| Operation | Count |
| --- | ---: |
| Conditional HEAD | 2 |
| GET | 2 |
| Bucket/object listing | 0 |
| R2 write/delete | 0 |
| Provider I/O | 0 |
| Execution/recovery/mutation | 0 |

## Publication joins

Each restored archive contains the exact expected native result, publication
receipt, checkpoint-basis record, and workspace-snapshot record. Their public
run, invocation, result, receipt, native revision, checkpoint-basis, and
snapshot identities agree with the API coordinate packet.

Both results are:

- `outcome = review_required`;
- `cause_code = final_qa_requires_review`;
- `command_kind = provider_reconciliation`;
- bound to all eight paid actions and all eight durable provider response IDs;
- published by SBE `0.4.49` with no remaining provider custody.

## Doughmeat

Doughmeat followed the ordinary two-polish exhaustion path:

| State | Lint findings | Acceptance |
| --- | ---: | --- |
| Initial assembled deck | 3 | rejected for polish |
| Polish attempt 1 | 2 | `POLISH_ACCEPTED` |
| Polish attempt 2 | 1 | `POLISH_ACCEPTED` |

The final structural validator passed. The sole surviving lint finding is
`repeated_opening`: the opening `"you do not"` remains in six
`no_astro.body.direct_to_dog` fields. The result therefore represents genuine
editorial exhaustion, not failed polish adoption or stale evidence.

## Macaron

Macaron's first polish was accepted, but the resulting deck retained five lint
warnings. Its deterministic acceptance report rejected the deck for:

- `cross_card_exact_duplicate`: three duplicate groups; and
- `multi_field_opening_template`: two dominant opening groups.

The most pronounced template finding is `"lady macaron may"` across 37
`no_astro.body.handler` fields. Structural validation passed.

The second provider response was retrieved and reached the stage-specific
consumer, but the sparse edit repeated the exact field
`cards.17.card.no_astro.body.handler`. Native state records attempt 2 as:

- `state = POLISH_ERROR`;
- `error.type = ValueError`; and
- `error.message = Sparse polish repeats field: cards.17.card.no_astro.body.handler`.

Because the sparse edit failed before producing a candidate deck, the absence of
attempt-002 lint and validation reports is expected. It is not an evidence-loss
or checkpoint-publication defect.

## Disposition

The checkpoint evidence confirms the Slice 0 interpretation and closes the
investigation. Both runs exhausted the configured two polish attempts while
retaining real editorial defects. No SBE runtime change, API companion change,
or release is warranted.
