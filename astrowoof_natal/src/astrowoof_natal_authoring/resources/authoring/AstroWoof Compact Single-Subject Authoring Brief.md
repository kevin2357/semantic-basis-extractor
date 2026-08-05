# AstroWoof Compact Single-Subject Authoring Brief v0.4.3

## The assignment

Turn the supplied selected authoring packet into one complete
`natal.<subject>.cards.json` deck.

Approach this as sustained editorial work on one JSON artifact. Understand the
dog, write the cards sequentially, review the finished deck, validate it, and
deliver it. Do not turn the assignment into a project-management simulation.

The packet's existing structure is authoritative. Preserve locked data and
edit only the prose and organizational placeholders described below.

## Understand the complete dog first

Before composing card prose, read:

- the whole-graph analysis;
- all 50 selected cards and their evidence;
- `unselected_claims`;
- the projected-term registry.

Form an integrated understanding of the dog's temperament, recurring motifs,
tensions, behavioral rhythms, relationships, strengths, growth edges, and
comic possibilities. This understanding should keep the dog recognizable
throughout the deck.

Ordinary cards may assert only what their selected claim and retained evidence
support. Unselected claims may inform the overall portrait and the four
Summary cards, but must not leak unsupported facts into ordinary cards.

You may plan privately. No separate portrait, ledger, audit, or checkpoint
artifact is required unless work is actually interrupted.

## Write 50 independent miniature essays

Treat each selected card as a fresh writing assignment, not the next row in a
schema-completion operation.

Before writing a card, determine privately:

- what the claim is really about;
- its center of gravity;
- a behavior a handler could recognize;
- the most likely misunderstanding;
- a grounded surprise or useful reframing;
- the memorable idea or image that belongs to this claim;
- how it differs from nearby cards;
- the narrative approach best qualified to reveal it.

Then complete that card before beginning the next. Keep the characterization
consistent while allowing pacing, imagery, sentence structure, humor, and
narrative viewpoint to vary naturally.

Behavior should ordinarily precede explanation. Scenes are optional and must
arise from the evidence, never from a rotating scene bank. Different words
that tell the same lesson still count as repetition.

Shuffled-card test: ten random cards should feel like ten distinct creative
starting points about the same dog, not one essay divided into fields.

## Reader-facing language

Decode compound terms and operators through `projected_term_registry`. Do not
expose graph labels or convert registry keys into spaced title case.

Never mention:

- selected or unselected claims;
- retained evidence or retained relationships;
- canonical claims;
- semantic profiles, systems, graphs, or projection;
- extraction, selection, packets, models, or authoring mechanics.

Translate internal labels such as `behavioral doorway`, `primary companion
interface`, `safe-den baseline`, or `visible pack function` into natural
astrology and recognizable canine behavior.

Do not invent biography, breed traits, diagnoses, medical claims, or facts not
supported by the packet.

## Voice

Handler helps a person recognize what may be happening for the dog and respond
constructively.

Direct-to-dog addresses the dog as `you`, offers perspective and dignity, and
must be composed independently rather than converted from handler prose.

Hybrid reveals the reciprocal dog-human situation: what happens between them,
how each response changes the other, and what shared rhythm or possibility
emerges. It is not handler advice with pronouns changed. Avoid repeatedly
using “the dog brings X; the person brings Y; together Z happens.”

Audience changes purpose, not grammar. Do not impose one sentence template on
each voice.

## Astrology density

All three densities express the same underlying insight.

No astrology contains no planets, signs, aspects, houses, Doghouses, angles,
nodes, graph terminology, or raw registry labels. It translates the claim
fully into dog life.

Light astrology names the one or two most useful actual astrological sources
and promptly interprets their canine meaning.

Full astrology explains the relevant planets, luminaries, angles, nodes,
signs, Doghouses, aspects, geometry, and orb strength. It remains a natal
interpretation, not a provenance report.

## Advice and humor

Every `do` and `dont` must follow from the exact claim and describe something
observable or usable. Generic patience, consistency, space, or enrichment is
insufficient without explaining what it looks like here.

Humor occurs once at card level. Build it from what is funny about this exact
behavior or tension. Audit comic worlds as well as exact wording: policies,
contracts, departments, paperwork, treats, squirrels, and similar motifs must
not become a deck-wide default.

## Filters and chapters

Assign a context filter only when a reader deliberately choosing that filter
would be satisfied to see the card. Tangential relevance is insufficient.
Empty arrays are preferable to false retrieval promises, but an almost
entirely empty deck requires reconsideration.

Assign `theme_group_id` only to selected aspects and syntheses. Plan aspects
and syntheses independently in their section-scoped registries. Each section
requires three to five subject-specific chapters, at least two claims per
chapter, and no more than a 2:1 largest-to-smallest size ratio. The two
taxonomies must be foundationally different and may not reuse chapter titles.
Each registry entry provides stable `id`, full `title`, compact `short_title`,
relevant `emoji`, one concise explanatory `subtitle`, and consecutive `order`.
Write subtitles as direct reader orientation to the dog's pattern, practical
territory, or organizing question. Vary sentence movement across the registry;
do not make every entry a meta-description beginning with “These cards ...”.
This is craft guidance, not a phrase ban: use the most natural sentence for each
chapter rather than forcing either repetition or artificial difference.
Do not add `theme_group_id` to placements.

## Four Summary cards

Write the summaries after understanding the full chart. Summaries alone may
use selected and unselected material.

1. Who the dog is: personality, temperament, and identity.
2. How the dog lives: routines, comfort, activity, home style, and environment.
3. What the dog needs: emotional support, handling, enrichment, and practical
   guidance.
4. How the dog grows: learning, challenge, development, and opportunity.

They are the user's friendly, non-astrology-first introduction to the dog.
Integrate motifs into a memorable portrait instead of listing chart terms.

## Preserve and populate

Preserve exactly:

- card count, order, IDs, and claim types;
- categories, scores, selection metadata, behavioral domains, and tags;
- evidence and relations;
- top-level subject, source, coverage, registries, and filter vocabulary;
- `unselected_claims`;
- `projected_term_registry`.

Populate:

- both structured chapter registries and every selected aspect and synthesis
  `theme_group_id`;
- selected-card context filters;
- all handler, direct-to-dog, and hybrid headlines and bodies;
- all no-, light-, and full-astrology branches;
- selected-card `dos`, `donts`, and card-level humor;
- every editorial field in `summary.card1` through `summary.card4`.

Remove every `__LLM_FILL__` placeholder.

## Finish the artifact

After writing all cards and summaries:

1. read the deck as a collection;
2. remove repeated semantic stories, openings, endings, headline frames,
   advice, imagery, hybrid constructions, and humor mechanisms;
3. verify voices and astrology densities remain distinct;
4. review filters and theme groups as user-facing collections;
5. run `lint_astrowoof_editorial.py` and correct substantiated findings;
6. run:

```text
python validate_astrowoof_editorial.py AUTHORING_PACKET EDITED_DECK \
  --phase authoring
```

7. correct every validation error;
8. return the complete parseable `natal.<subject>.cards.json`, plus the final
   linter and validation reports when available.

A linter or validator pass is not a substitute for editorial judgment.

If an actual execution interruption occurs, save the valid partially edited
deck and identify the exact next unfinished priority ID. Checkpointing is a
recovery behavior, not the normal unit of authorship.
