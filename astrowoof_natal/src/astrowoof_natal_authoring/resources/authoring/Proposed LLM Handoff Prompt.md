# Proposed LLM Handoff Prompt v0.4.2

Edit the supplied AstroWoof projected natal authoring packet into the final
`natal.<subject>.cards.json` artifact.

Before writing, read and obey:

1. `AstroWoof Projected Natal Card Authoring Manual.md`
2. `AstroWoof Independent Card Writing Brief.md`
3. `LLM Card-by-Card Authoring Execution Protocol.md`
4. `LLM Editing Permissions and QA Checklist.md`
5. this prompt

The execution protocol is mandatory. Treat every card as an independent
writing assignment and complete one entire card before beginning the next.
Bulk field-by-field generation, sentence-frame substitution, global phrase
banks, and rotating humor or advice are prohibited.

The independent-card writing brief is the positive creative standard. Write 50
miniature essays about the same dog: consistent understanding, diverse
expression. The schema stores the writing; it must not determine the writing.

Do not use Python, JavaScript, templates, string interpolation, deterministic
transformations, or any other programmatic method to generate reader-facing
language. Tools may inspect evidence, maintain files, checkpoint, lint, and
validate only. Compose each editable prose field through fresh reasoning about
that exact card.

Use only the selected `cards` and their retained evidence when authoring the 50
ordinary claim cards. The top-level `unselected_claims` collection must not
leak into those selected cards.

The four top-level summary cards are the sole exception: they intentionally
summarize the complete natal chart and may use both selected and unselected
claims.

## Phase 0: understand the complete dog

Before authoring card 1, create the mandatory
`<subject>.whole-chart-authoring-portrait.json` described by the execution
protocol. Read the complete chart basis and synthesize the dog's overall
temperament, recurring motifs, tensions, behavioral rhythms, relationship
dynamics, strengths, growth edges, tone, and comic affordances with source
claim IDs.

Do not write any card prose until this portrait is complete. Use it to keep the
deck recognizably about one individual dog, but never turn portrait motifs into
fixed sentences appended across cards. Ordinary cards remain limited to their
own selected evidence.

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

- decode the canonical claim and retained evidence through the registry;
- define its unique editorial job in the private ledger;
- distinguish that job concretely from its two closest selected neighbors;
- identify its center of gravity, recognizable behavior, likely handler
  misreading, grounded surprise, memorable image, and claim-natural narrative
  angle;
- fill all handler, direct-to-dog, and hybrid headlines and bodies;
- fill all no-, light-, and full-astrology density branches;
- fill `dos` and `donts`;
- fill the card-level `funny_dog_quotes`, `imperative_dog_quotes`, and
  `applicable_canine_jokes` arrays;
- assign only strongly relevant registered context filters.

Humor belongs once at `card` level. Do not add humor fields inside astrology
density branches.

Every reader-facing line fails when it could fit five other claims after
changing only the dog's name or projected terms. Rewrite the complete line or
paragraph rather than disguising a repeated frame with a new opening.

Do not manufacture lexical uniqueness through subject names, claim quotations,
scene labels, priority numbers, or other variable slots. Do not attach one
subject-specific refrain to many cards. Forget previous cards' syntax; remember
their stories and avoid repeating them.

Scenes are optional. Use one only when it arises naturally from the evidence.
Never select scenes from a bank, assign them by card position, or prefix every
rendering with a scene.

A ledger entry fails when its unique job merely says "Explain X through scene
Y" or otherwise substitutes terms into a reusable meta-description. Concrete
scenes must be evidence-supported, not assigned from a rotating scene pool.

## Reader-facing language

Use `projected_term_registry` to understand compound terms, operators, signs,
aspects, Doghouses, and other vocabulary. Preserve the registry unchanged.

Do not expose raw registry labels in no-astrology prose. Never treat a
compound phrase as finished prose or as separate words to concatenate.

Reader-facing prose must not mention:

- selected or unselected claims;
- retained evidence;
- semantic profiles or systems;
- models, graphs, or graph processing;
- projection or projected readings;
- authoring, extraction, selection, or packet mechanics.

Do not emit scaffolding such as `unspecified pattern`, `whole personality`,
`mode mode`, or `recurring pattern pattern`.

## Voice and density

Handler explains what may be happening for the dog and helps the person
recognize it.

Direct-to-dog expresses the dog's imagined perspective using correct
second-person grammar and independently composed prose.

Hybrid describes the reciprocal dog-human interaction: what the dog and
person or environment contribute, and what rhythm, adjustment, or possibility
emerges. It must not be handler advice with pronouns changed, a generic
instruction plus "together," or a repeated "`<Dog>` brings X; you bring Y"
frame.

No-astrology prose translates the claim completely into recognizable dog life
without astrology, projection language, or raw registry labels.

Light astrology names the one or two most useful actual astrological sources
and promptly translates them into canine meaning. Saying "the WoofMap
suggests" is not sufficient.

Full astrology explains the retained planets, luminaries, angles, nodes,
signs, Doghouses, aspects, operators, geometry, and orb strength that matter
to the claim. It interprets them for a reader rather than reporting provenance.

## Context filters

Context filters are reader-navigation facets, not structural categories.
Assign a filter only when a reader deliberately choosing it would be satisfied
to see the card. An incidental or tangential connection is insufficient.

Empty arrays are editorially preferable to false retrieval promises when no
registered filter strongly fits. Multiple values are allowed only when each
independently passes the reader-expectation test.

Do not fill available slots, force exactly one value, target equal vocabulary
coverage, or assign most filters through broad interpretation. Record a
private justification for every value, then audit each filter's complete
result set after all cards are written.

## Theme groups

Every selected aspect and synthesis contains a `theme_group_id` placeholder,
and the deck contains independent structured registries for Interdogpendence
and Takeaways.

Read all selected aspects and plan three to five subject-specific
Interdogpendence chapters around relationship and interaction dynamics.
Independently read all selected syntheses and plan three to five Takeaways
chapters around integrated conclusions. Each chapter must contain at least two
claims, and the largest may contain no more than twice as many as the smallest.

The two taxonomies must be foundationally different. Do not repeat, reorder,
synonymize, or cosmetically reword one section's chapter titles for the other.
For every chapter provide stable `id`, reader-facing `title`, concise
`short_title`, relevant `emoji`, one concise explanatory `subtitle`, and
consecutive `order`; cards reference the stable ID. Do not add
`theme_group_id` to other claim types.

For each registry subtitle, orient the reader directly to the dog's shared
pattern, practical territory, or organizing question. Let the subtitles use
natural, varied sentence movement rather than repeating one meta-editorial
frame such as “These cards ...” across the section. Do not force superficial
difference when the clearest sentence happens to share an ordinary word.

## Summary cards

Populate `summary.card1` through `summary.card4`, including `dos`, `donts`,
card-level humor, and every voice/density headline and body.

These are the first cards shown to a reader. They provide a friendly,
memorable, primarily non-astrological overview through four fixed lenses:

1. Who the dog is: core personality, temperament, and identity.
2. How the dog lives: routines, comfort, home style, activity, and preferred
   environment.
3. What the dog needs: emotional support, enrichment, handling, and the most
   actionable guidance for thriving.
4. How the dog grows: learning, challenge, development, and opportunity.

For summaries only, read all selected cards, `unselected_claims`, whole-graph
analysis, and the registry. First create a private source outline for each
lens, then integrate those motifs into prose. Do not list registry terms or
write universal dog-care language with only the subject's name substituted.

Use supplied pronouns when present. When pronouns are absent, use the dog's
name and grammatically neutral constructions. Do not invent awkward labels
such as "You: Who They Are" or "`<Dog>` Together."

The Bre gold reference demonstrates warmth, depth, voice and density
differentiation, claim-specific humor, and four-lens summary behavior. It is
an editorial reference only. Do not copy Bre-specific facts, phrases, filters,
theme groups, or obsolete schema details.

## Persistent completion

Maintain the working deck, checkpoint, and detailed editorial ledger required
by the execution protocol. Resume from the first unfinished priority ID after
an interruption. Card 50 must receive the same care as card 1.

After every five cards, run the protocol's repetition and integrity audit.
Run `lint_astrowoof_editorial.py`, save the checkpoint audit artifact, and
correct errors and substantiated warnings before continuing automatically.
After all cards, review the complete deck for repeated openings, endings,
headline frames, advice, imagery, claim-type templates, and humor. Review every
hybrid body alone.

The linter is a backstop, not the writing objective. A zero-warning report does
not excuse name-swapped prose, slot-filled uniqueness, repeated semantic
stories, all-empty filters, or unreadable language.

Return one complete parseable JSON file plus the whole-chart authoring
portrait, completed authoring ledger, checkpoint audit files, final editorial
linter report, and validation report. Do not return samples, excerpts, or a
partial deck.

Run:

```text
python validate_astrowoof_editorial.py AUTHORING_PACKET EDITED_DECK \
  --phase authoring
```

Correct every error before delivery. A validator pass proves structural
integrity; it does not waive the protocol's editorial QA.

Later prose-only polish passes use the completed deck as baseline:

```text
python validate_astrowoof_editorial.py COMPLETED_BASELINE POLISHED_DECK \
  --phase polish
```

In polish phase, context filters, theme groups, and summaries remain locked
unless the user explicitly authorizes the corresponding override.
