# Review-required while creative retries remain

## Status

Investigation-only record. No implementation, provider work, retained-run
mutation, deployment, or release is authorized by this document.

## Question

The 2026-08-28 QA cohort ended with `native.review.requires_review` while each
run still had creative-retry authority in mixed custody states. Determine
whether this is a correct editorial/state-machine outcome, an incorrect retry
selection/fan-in outcome, or an interaction with the broken terminal-handoff
path documented in the companion sprint
`20260828-terminal-review-closeout-handoff-sprint1`.

The answer must be based on the exact native workspace state, retry policy, and
public lifecycle semantics—not action counts alone.

## Observed state

Both Pippin von Waffle (`fbe8ada6-511d-469f-a9b6-31fe15835138`) and Duchess
Crumpet (`40783a32-e326-4605-8503-de8838152fc0`) have:

- six reported initial actions;
- one creative retry reported with actual cost;
- one creative retry provider-created with a durable OpenAI response identity
  but no completed provider observation in the API ledger; and
- one subsequent creative retry authorized but never provider-created.

Both SBE workers then emitted `native.review.requires_review`. Pippin did so at
`2026-08-28T06:20:03.396Z`; Duchess at `2026-08-28T06:24:28.929Z`.

## Why count-based reasoning is insufficient

`max_attempts=3` means a pass may have an initial attempt plus up to two
creative retries. It does not require every run to consume every possible retry
before a different pass or final QA can produce a review-required disposition.
The observed three creative-retry action rows can also belong to different pass
lineages. Therefore the investigation must recover each action's pass/attempt
lineage and the actual rejection/final-QA reason.

## Questions to resolve

1. Which pass(es), attempt numbers, and QA reports produced the two completed
   creative-retry outcomes and the review-required status?
2. Did any pass exhaust its allowed attempts, receive a fatal validation
   outcome, or reach final QA review? Record the exact reason and evidence.
3. Why was the later authorized retry prepared: a valid independent pass,
   an expected next retry, stale pending work, or an invalid successor?
4. At the terminal decision point, why did SBE project
   `provider_local_dependency_count=0` while the API still had a
   provider-created retry? Is this merely unreported terminal evidence, or a
   substantive disagreement about provider custody?
5. Are the transition and retry-selection rules documented/tested such that an
   API operator can distinguish a normal review-required run from a broken
   terminal handoff without parsing private workspace files?

## Desired outcome

Produce a concise provenance timeline and a public-contract assessment. If the
review branch is valid, document that fact and add a regression fixture for a
review-required result with mixed retry custody. If invalid, identify the
smallest ownership-correct correction and its companion API contract needs.
