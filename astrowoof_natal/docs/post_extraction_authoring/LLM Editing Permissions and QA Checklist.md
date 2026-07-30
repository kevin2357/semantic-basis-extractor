# LLM Editing Permissions and QA Checklist v0.3

## Editable

- Selected-claim `theme_group` where the extractor supplied a placeholder
- Selected-claim `context_filter_groups.high_level`
- Selected-claim `context_filter_groups.detail_level`
- Selected-claim `dos` and `donts`
- Selected-claim card-level humor arrays
- Selected-claim headline and body voice maps at all three astrology densities
- All editorial fields within `summary.card1` through `summary.card4`

## Locked

- Selected claim membership and ordering
- IDs, claim types, and `categories`
- Scores and selection metadata
- Behavioral domains and tags
- Evidence and relations
- Top-level subject, source, coverage, category registry, behavioral-domain
  registry, and context-filter vocabulary
- `unselected_claims`
- `projected_term_registry`

## Required final checks

- Exactly 50 selected cards
- No `__LLM_FILL__` placeholders
- Every selected aspect and synthesis has a nonempty `theme_group`
- No placement has an added `theme_group`
- Every claim has at least one valid high-level and one valid detail-level
  context filter
- All filter values occur in the registered vocabulary at the matching level
- Humor occurs at card level and never inside density branches
- All four summary cards are complete
- `unselected_claims` is byte-for-structure equivalent to the request packet
- `projected_term_registry` is unchanged
- No-astrology prose contains no explicit astrology
- Handler, direct-to-dog, and hybrid voices are complete
- At least two dos and two donts exist for each selected and summary card
- The deterministic editorial validator passes
