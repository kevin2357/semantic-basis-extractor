# Proposed LLM Handoff Prompt v0.3

Edit the supplied AstroWoof projected natal authoring packet into the final
`natal.<subject>.cards.json` artifact.

Use only the selected `cards` and their retained evidence when authoring the 50
ordinary claim cards. The top-level `unselected_claims` collection must not
leak into those selected cards.

The four top-level summary cards are the sole exception: they intentionally
summarize the complete natal chart and may use both selected and unselected
claims.

## Preserve exactly

Do not change:

- claim count or order;
- claim IDs or types;
- `categories`;
- importance, confidence, strength, or selection metadata;
- behavioral domains or tags;
- evidence or relations;
- top-level subject, source, coverage, category registry, behavioral-domain
  registry, or context-filter vocabulary;
- `unselected_claims`;
- `projected_term_registry`.

## Populate selected claims

For every selected claim:

- fill all handler, direct-to-dog, and hybrid headlines and bodies;
- fill all no-, light-, and full-astrology density branches;
- fill `dos` and `donts`;
- fill the card-level `funny_dog_quotes`, `imperative_dog_quotes`, and
  `applicable_canine_jokes` arrays;
- assign at least one relevant registered `context_filter_groups.high_level`
  value;
- assign at least one relevant registered `context_filter_groups.detail_level`
  value.

Context filters are reader-navigation facets, not restatements of structural
`categories`. Assign a filter when the claim is strongly related enough that a
reader who deliberately filtered the deck to that subject would reasonably
expect to see the card. The filter need not be the claim's sole or primary
focus, but an incidental or tangential reference is insufficient.

Multiple assignments are allowed when each independently passes that test.
Do not assign most or all filters merely because a broad interpretation could
connect the claim to them.

Humor belongs once at `card` level. Do not add humor fields inside astrology
density branches.

## Assign theme groups

Every selected aspect and selected synthesized claim contains:

```json
"theme_group": "__LLM_FILL__"
```

Replace it with a concise, nonempty chapter label. The website already
organizes claims into major sections such as Big Three, placements, angles,
nodes, aspects, and syntheses. `theme_group` supplies the chapter level within
the aspect and synthesis sections.

Organize the selected aspects into three or four approximately equal-sized
chapters whose members share a recognizable theme. Independently organize the
selected syntheses into three or four approximately equal-sized chapters.
Choose subject-appropriate labels after reading the complete selected set.
Exact equality is not required, but avoid one giant miscellaneous group, a
single-card group, or a unique label per claim unless an unavoidable count
edge case makes one necessary.

Aspect and synthesis chapters may coincidentally use the same label, but group
each major section independently rather than using one combined size quota.

Do not add `theme_group` to placement claims.

## Author the four summary cards

Populate `summary.card1` through `summary.card4`, including:

- `dos`;
- `donts`;
- the three card-level humor arrays;
- all voice and astrology-density headline/body combinations.

These are the first cards a reader sees when opening a WoofMap. They should
provide a friendly, memorable, primarily non-astrological overview before the
reader enters the full deck. Their four fixed lenses are:

1. **🐶 Who She Is** — Core personality: the at-a-glance account of temperament
   and identity.
2. **🏡 How She Lives** — Daily lifestyle and the dog's natural way of moving
   through the world: home style, routines, comfort, and preferred environment.
3. **❤️ What She Needs** — Emotional needs, support, enrichment, handling, and
   the most actionable guidance for helping the dog thrive.
4. **🌱 How She Grows** — Development, learning, challenges, opportunity, and
   how the dog's potential unfolds over time.

Use the subject's actual pronouns in labels and prose rather than mechanically
using “She.”

For summary cards only, read the entire chart basis: all selected `cards`, all
`unselected_claims`, whole-graph analysis, and the projected-term registry.
Compress that complete understanding through the four lenses. Do not mention
claim selection, unselected status, graph processing, or evidence mechanics in
reader-facing prose.

The supplied Bre gold reference demonstrates the desired warmth, scope,
density, voice differentiation, and four-lens summary behavior. Use it as an
editorial reference only. Do not copy Bre-specific facts, phrases, filter
assignments, or obsolete schema details into another subject's deck.

## Registry use

Use `projected_term_registry` to decode compound projected terms, operators,
signs, aspects, and Doghouse vocabulary. Preserve the registry unchanged.

## Completion

Work through all 50 claims and four summary cards using a durable priority-ID
ledger. If interrupted, resume at the first unfinished field rather than
restarting or shortening later cards.

Return one complete parseable JSON file. Run
`validate_astrowoof_editorial.py` against the original authoring packet and
correct every error before delivery:

```text
python validate_astrowoof_editorial.py AUTHORING_PACKET EDITED_DECK \
  --phase authoring
```

Later prose-only polish passes must use the completed deck as both the baseline
contract and the source of locked organizational fields:

```text
python validate_astrowoof_editorial.py COMPLETED_BASELINE POLISHED_DECK \
  --phase polish
```

In polish phase, context filters, theme groups, and summaries remain locked
unless the user explicitly requested changes and the corresponding
`--allow-...-edits` option is supplied.
