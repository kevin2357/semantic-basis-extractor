# Slice 0 — Paired checkpoint findings

## Decision summary

Crumpet and Baguette did not expose a broken provider lifecycle, missing retry
adoption, stale pass transition, or malformed terminal publication. They
independently exhausted all three allowed attempts for pass 6 because the
authoring pass gate treats theme-group coverage and balance as hard rejection
conditions.

This is intended behavior under the current code contract. Whether it remains
the intended product policy is the Slice 1 decision.

## Protected-access evidence

The two frozen generation-17 checkpoint objects were each read with exactly one
HEAD and one conditional GET. Both matched their frozen:

- object key and ETag;
- archive byte count and SHA-256;
- checkpoint generation and inventory digest; and
- API run, job, checkpoint, and native-run identities.

Both archives passed path traversal, duplicate-member, symlink, inventory, file
digest, and workspace-snapshot validation during offline restore.

Remote totals: two HEADs, two GETs, zero lists, zero writes, and zero deletes.
No provider operation or retained workspace mutation occurred.

## Native pass truth

Both workspaces have the same structural outcome:

- passes 1–5 are `PASS_QA_ACCEPTED` at attempt 1 with accepted workspaces;
- pass 6 has three `PASS_QA_REJECTED` attempts;
- pass 6 has no accepted attempt or accepted workspace;
- the containing pass is `FAILED_REQUIRES_REVIEW`; and
- finalization therefore correctly emits
  `finalization_deferred reason=authoring_passes_incomplete`.

The two reported creative-retry actions join exactly to pass 6 attempts 2 and
3. Both retries have durable provider response IDs, complete retry-attempt
evidence, and persisted QA reports. This rules out the leading transition-seam
hypotheses from the pre-sprint huddle.

## Exact rejection facts

| Run | Attempt 1 | Attempt 2 | Attempt 3 |
| --- | --- | --- | --- |
| Crumpet | `theme_group_coverage` twice; 33 claims | `theme_group_balance`; 14 claims | `theme_group_coverage`; 19 claims |
| Baguette | `theme_group_coverage` twice; 33 claims | `theme_group_coverage`; 19 claims | `theme_group_coverage`; 19 claims |

No non-theme-group issue code appears in any of the six rejected attempts.
The duplicate attempt-1 coverage code represents the two theme-group sections,
not duplicated retry lineage.

## Source-level predicate

`pass_acceptance.theme_group_plan_issues()` rejects a pass when either:

1. the set of assigned theme-group IDs differs from the registered IDs for a
   section (`theme_group_coverage`); or
2. any registered group has fewer than two claims, or the largest group is more
   than twice the smallest (`theme_group_balance`).

`pass_acceptance.main()` appends those issues to the authoring pass gate and
returns rejection exit 2. `closure.author_one_pass()` persists
`PASS_QA_REJECTED`; after the third attempt it sets the pass to
`FAILED_REQUIRES_REVIEW`. `finalize_subjects()` then correctly defers because
not every pass is `PASS_QA_ACCEPTED`.

The transition chain is internally coherent from provider report through
terminal publication.

## Terminal publication join

For both runs, the offline validator proved:

- native-result v0.2 schema/content identity;
- publication-receipt content identity;
- bounded journal range and closing record;
- retained snapshot and checkpoint-basis digests;
- logical workspace identity across current/retained evidence;
- native run identity;
- exact eight-action ledger inventory and binding digests; and
- final custody with all actions `REPORTED` and
  `new_provider_create_permitted=false`.

The sealed results are truthful terminal-review publications for the native
state that exists.

## Classification

- Provider/reconciliation defect: **not observed**.
- Retry-adoption defect: **not observed**.
- Pass-state transition defect: **not observed**.
- Terminal-result publication defect: **not observed**.
- Current hard-gate cause: **theme-group coverage/balance only**.
- Product-policy question: **open for Slice 1**.

Given the owner's earlier product context—that theme-group filtering is not yet
implemented and the static taxonomy remains provisional—the current hard gate
is likely disproportionate even though its implementation behaved correctly.
That policy judgment should be made explicitly rather than disguised as a
state-machine repair.
