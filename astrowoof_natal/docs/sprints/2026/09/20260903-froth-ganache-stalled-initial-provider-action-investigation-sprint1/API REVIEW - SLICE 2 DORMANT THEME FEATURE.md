# API review — Slice 2 dormant theme feature

## Decision

The revised Slice 2 direction is correct. Ganache's observed failure was a
legacy `ASSIGN THEME GROUPS.md` artifact participating in final assembly even
though theme groups are a dormant, unimplemented filtering feature. Removing
that feature from production pass-six generation, assembly validity, delivery,
and output is the right correction. It is preferable to teaching API to turn a
valid deck into a terminal-review refusal merely because obsolete retained
compatibility data is malformed.

The scope remains SBE-only. It changes no provider custody, lifecycle routing,
reconciliation authority, or API result contract. The prior proposed
terminal-review bridge should remain withdrawn.

## One requested test refinement

Please make the retained-artifact fixture use one Ganache-shaped *structured*
invalidity in addition to, or instead of, opaque malformed text: for example,
a syntactically field-shaped `theme_group.interdogpendence.<priority>` entry
whose value is an unknown chapter such as `grounded_companionship`.

Opaque text proves that assembly no longer parses the file. The structured
unknown-reference case directly proves the historical failure cannot recur if
a legacy workspace retains the same category of stale assignment data.
Keep the assertions already described:

- successful complete six-pass assembly;
- no theme registry or per-card assignment in the delivered deck;
- no placeholder leakage; and
- an explicit empty compatibility `authored_theme_group_priority_ids` value.

## Approval boundary

## Re-review

The requested refinement is incorporated correctly. The fixture now renders a
structurally valid historical assignment artifact and changes one exact
Interdogpendence value to the unregistered `grounded_companionship` chapter.
That directly covers Ganache's failure shape while proving assembly neither
parses nor validates the dormant artifact. It also verifies that production
pass six does not generate or request it.

**Approved:** SBE may proceed to its provider-free qualification/review slice.
No API change, worker resume, provider activity, retained-run recovery, or
release approval is implied by this review.
