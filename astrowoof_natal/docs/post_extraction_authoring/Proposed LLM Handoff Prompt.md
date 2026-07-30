# Proposed LLM Handoff Prompt v0.3

Edit the supplied AstroWoof projected natal authoring packet into the final
`natal.<subject>.cards.json` artifact.

Use only the selected `cards` and their retained evidence when authoring card
copy. The top-level `unselected_claims` collection is preservation and audit
material. Do not import its facts, evidence, or broader synthesis support into
selected cards or summaries.

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

Humor belongs once at `card` level. Do not add humor fields inside astrology
density branches.

## Assign theme groups

Every selected aspect and selected synthesized claim contains:

```json
"theme_group": "__LLM_FILL__"
```

Replace it with a concise, nonempty chapter label. Theme groups are flexible
subject-specific editorial groupings, not controlled structural categories.
Use the same label for aspects and syntheses that belong in the same meaningful
chapter of the reading. Prefer a small coherent set of useful chapter names
over a unique label for every claim.

Do not add `theme_group` to placement claims.

## Author the four summary cards

Populate `summary.card1` through `summary.card4`, including:

- `dos`;
- `donts`;
- the three card-level humor arrays;
- all voice and astrology-density headline/body combinations.

Give the four cards distinct jobs:

1. whole-dog personality overview;
2. emotional, relational, and security pattern;
3. learning, motivation, play, and growth pattern;
4. practical life-together overview integrating strengths and tensions.

Summaries may synthesize selected cards but may not use unselected claims.

## Registry use

Use `projected_term_registry` to decode compound projected terms, operators,
signs, aspects, and Doghouse vocabulary. Preserve the registry unchanged.

## Completion

Work through all 50 claims and four summary cards using a durable priority-ID
ledger. If interrupted, resume at the first unfinished field rather than
restarting or shortening later cards.

Return one complete parseable JSON file. Run
`validate_astrowoof_editorial.py` against the original authoring packet and
correct every error before delivery.
