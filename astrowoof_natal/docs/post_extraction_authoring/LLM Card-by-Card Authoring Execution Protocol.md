# LLM Card-by-Card Authoring Execution Protocol v0.4.2

This protocol governs the working method used to turn one AstroWoof selected
authoring packet into a finished deck. It is mandatory. The authoring manual
defines the editorial standard; the handoff prompt defines the deliverable;
this document defines how to complete the work without collapsing into
template substitution.

`AstroWoof Independent Card Writing Brief.md` defines the positive creative
method and is mandatory alongside this protocol.

## 1. Governing rule

Each card is an individual writing assignment, not one row in a bulk
text-generation operation.

Process selected cards strictly in `priority_id` order. Complete every editable
field and the card-level QA for the current card before beginning any field of
the next card.

Never write all headlines first, all handler bodies second, all jokes third, or
otherwise process the deck by field. Never create a global phrase pool,
headline bank, advice bank, quote bank, joke bank, or reusable collection of
sentence frames.

Scripts and deterministic transformations may inspect, copy, merge, save,
checkpoint, lint, and validate artifacts. They must never generate, paraphrase,
expand, rotate, or slot-fill reader-facing prose. Every headline, body, `do`,
`dont`, quote, joke, and summary paragraph must be composed through a fresh
language-model reasoning step for its exact editorial job.

## 2. Persistent working state

For subject `<subject>`, create and maintain:

1. `natal.<subject>.cards.working.json`
2. `<subject>.authoring-checkpoint.json`
3. `<subject>.authoring-ledger.json`

The working JSON is authoritative. Save valid JSON after each completed card.

The checkpoint records at least:

```json
{
  "task": "astrowoof_card_authoring",
  "subject": "<subject>",
  "phase": "selected_cards",
  "last_completed_priority_id": 0,
  "next_priority_id": 1,
  "completed_claim_ids": [],
  "remaining_claim_ids": [],
  "status": "in_progress"
}
```

For every completed claim, the private ledger records:

- `priority_id` and `claim_id`;
- canonical claim;
- one-sentence decoded semantic brief;
- center of gravity;
- recognizable behavior;
- likely handler misreading;
- grounded surprise;
- memorable image;
- chosen narrative angle and why it fits;
- semantic-story overlap check;
- the card's unique editorial job;
- the two closest neighboring claim IDs and a concrete explanation of how this
  card's reader value differs from each;
- a concrete behavioral scene or observable expression;
- the distinct job of handler, direct-to-dog, and hybrid prose;
- astrological sources chosen for light and full density;
- filter assignments and a short justification for each;
- humor premise and comic mechanism;
- humor lines;
- headline structures and distinctive imagery;
- overlap warnings and card-level QA status.

The unique editorial job must be a content distinction, not a reusable frame
such as "Explain X through scene Y without collapsing it into neighboring
claims." The behavioral scene must be supported by the claim; never assign a
scene from a rotating pool merely to manufacture specificity.

The ledger is working material, not website content.

## 3. Startup, resume, and time limits

At the beginning of an authoring session:

1. inspect the working deck, checkpoint, and ledger;
2. resume at `next_priority_id` when they exist;
3. do not restart completed cards;
4. do not shorten later cards because the task is long;
5. continue automatically without asking for permission after each batch.

If an execution or response limit approaches:

1. finish the current card;
2. save and parse the working deck, checkpoint, and ledger;
3. record the next unfinished priority ID;
4. resume from that ID in the next execution window.

Do not keep authoritative work only in conversation memory.

## 4. Phase 0: complete natal portrait

Before writing any card, read the complete subject basis:

- whole-graph analysis;
- all 50 selected cards and their evidence;
- all `unselected_claims`;
- all four projected contexts;
- the complete projected-term registry.

Create `<subject>.whole-chart-authoring-portrait.json`. This private,
non-reader-facing artifact must contain:

- a concise integrated portrait of the dog's temperament;
- eight to twelve major recurring motifs;
- important tensions, counterweights, and apparent contradictions;
- characteristic behavioral rhythms and likely sequences;
- relationship and handler-dog dynamics;
- learning, regulation, play, trust, communication, pack, and adventure themes;
- likely strengths and growth edges;
- distinctions between superficially similar motifs;
- tone, warmth, comic affordances, and imagery appropriate to this subject;
- factual cautions and uncertainties;
- source claim IDs supporting each statement.

Do not write card prose during Phase 0. The portrait must synthesize rather than
list registry terms, and every statement must remain traceable to the complete
chart basis.

Use the portrait as a governing context for all later cards. It helps each card
sound like the same individual dog without appending one fixed subject-specific
sentence to many cards. A portrait motif may guide a card only when that card's
selected evidence independently supports it. `unselected_claims` may shape the
overall understanding and Summary cards but must never leak unsupported facts
into ordinary selected cards.

Before card 1, compare the portrait with the Bre gold reference for depth and
integration only. Do not borrow Bre's facts, phrases, humor, or voice.

## 5. One-card procedure

For the current card only:

1. Read the canonical claim.
2. Read its complete retained evidence and relations.
3. Read every selected dependency.
4. Look up every compound projected term, operator, sign, Doghouse, aspect, and
   other relevant entry in `projected_term_registry`.
5. Write a private one-sentence semantic brief in natural behavioral language.
6. Answer every private planning question in the independent-card writing
   brief.
7. Define the card's center of gravity and unique editorial job.
8. Choose the narrative angle because it best reveals this claim; never rotate
   angles by index or claim type.
9. State how this job differs from the two most semantically adjacent selected
   claims, naming their claim IDs and the behavioral distinction.
10. Compare that job with all completed ledger entries and the whole-chart
   portrait.
11. Choose a concrete dog-life expression or relational scene only when the
    evidence naturally supports one. Scenes are optional and never drawn from
    a bank.
12. Set aside previous cards' syntax while retaining their semantic stories in
    memory.
13. Write all handler renderings.
14. Write all direct-to-dog renderings independently.
15. Write all hybrid renderings as reciprocal dog-human interactions.
16. Write specific `dos` and `donts`.
17. Design one claim-specific humor set.
18. Assign only strongly relevant context filters and record why.
19. Run card-level QA.
20. Save the card, ledger, and checkpoint.
21. Only then begin the next priority ID.

The private semantic brief must decode the claim. It must not merely replace
underscores with spaces or concatenate registry labels.

## 6. Universal anti-template test

Every reader-facing line fails when it could fit five other claims after
changing only the dog's name or projected terms.

Every card also fails when it tells the same semantic story as several other
cards using different words. Lexical uniqueness is not editorial independence.

Reject and rewrite prose when:

- a projected term is inserted into a reusable sentence frame;
- the practical recommendation would apply equally to almost any dog;
- a headline merely announces that a pattern exists;
- a joke survives unchanged when moved to an unrelated claim;
- hybrid prose is handler advice with the dog's name or the word "together"
  added;
- light astrology merely says "the WoofMap suggests";
- full astrology discusses a selected claim, evidence packet, model, semantic
  profile, or authoring process instead of interpreting astrology.

Changing an opening clause does not repair an underlying repeated structure.
Rewrite the paragraph as a complete unit.

## 7. Voice contracts

### 6.1 Handler

Handler prose addresses the person and describes the dog in the third person.
It helps the person recognize what may be happening, understand the context,
and respond constructively.

The tone is warm, observant, specific, useful, and nonjudgmental. Guidance may
appear naturally, but the body must not become a disguised list of commands.

### 6.2 Direct to dog

Direct-to-dog prose addresses the dog as `you`. Write it independently rather
than converting handler copy by pronoun substitution.

Give the dog perspective and dignity. Do not put handler instructions,
technical process language, or constant treat jokes in the dog's mouth.

### 6.3 Hybrid

Hybrid is a relationship-centered voice with its own function. It describes
the reciprocal interaction created by the dog and person together.

A hybrid rendering contains, explicitly or implicitly:

1. something the dog brings, signals, needs, initiates, or does;
2. something the person, environment, or relationship contributes;
3. the rhythm, adjustment, consequence, or next possibility created between
   them.

Reciprocity does not require mechanically naming both contributions. Natural
hybrid forms include:

- a shared activity or ritual;
- an observation about what happens between dog and person;
- an if/then interaction;
- complementary roles;
- a moment of mutual adjustment;
- a two- or three-beat progression;
- a relationship outcome that develops over time;
- an invitation to notice the dog's next choice.

Do not repeatedly use forms such as:

- "`<Dog>` brings X; you bring Y";
- "`<Dog>`'s response tells you";
- "`<Dog>`'s next move shows you";
- "`<Dog>`'s job is X; your job is Y";
- generic advice followed by "together."

Across each set of 50 hybrid bodies at a density:

- no more than 20 percent may begin with the dog's name or possessive name;
- no more than 20 percent may begin with an imperative;
- "`<Dog>` brings/supplies/contributes" may appear no more than five times;
- "you bring/supply/contribute" may appear no more than five times;
- "tells you" and "shows you" feedback endings may appear no more than five
  times in total.

These are ceilings, not target quotas. Review hybrid bodies alone as a deck. A
reader should recognize hybrid mode without seeing its label.

## 8. Astrology-density contracts

All densities express the same semantic claim.

### 7.1 No astrology

Use no planets, signs, houses, Doghouses, aspects, nodes, angles, projection
terminology, graph terminology, or raw registry labels. Translate the claim
fully into recognizable behavior, temperament, relationship, and ordinary
dog-life situations.

### 7.2 Light astrology

Name the one or two most useful actual astrological sources retained in the
claim's evidence, then translate them promptly into canine meaning. Do not list
the evidence chain or substitute the phrase "WoofMap" for astrological
interpretation.

### 7.3 Full astrology

Explain the relevant planets, luminaries, angles, nodes, signs, Doghouses,
aspects, geometry, operators, and orb strength that are present in retained
evidence. Explain how the components combine while still writing for a reader.

Do not dump provenance or discuss claim selection, evidence retention,
semantic profiles, models, graphs, or projection mechanics.

## 9. Internal term translation

Use `projected_term_registry` actively. Treat each registered compound as a
semantic unit with long description, facets, operator guidance, and output
guidance—not as a bag of English words.

Do not expose internal terms in ordinary prose by changing underscores to
spaces. For example, do not write:

> The dog's primary companion interface is activated.

Write the decoded behavior:

> A change in the social terms may make the dog check the relationship itself
> before deciding what to do next.

Never use `unspecified pattern`, `whole personality`, `recurring pattern
pattern`, `mode mode`, or similar extraction scaffolding as finished prose.

## 10. Practical guidance

Each `do` and `dont` must follow from the exact claim and describe something
observable or usable. Prefer recognizable moments involving greetings, walks,
thresholds, toys, meals, visitors, training, rest, search games, transitions,
favorite people, household activity, recovery, or changes of plan when
supported.

Generic "be patient," "stay consistent," "give space," and "provide an outlet"
language fails unless the item specifies what patience, consistency, space, or
an outlet looks like in this claim's situation.

Do not turn symbolic interpretation into diagnosis or rigid prescription.

## 11. Humor

Each claim receives one stable card-level humor set:

- one `funny_dog_quote`;
- one `imperative_dog_quote`;
- one `applicable_canine_joke`.

Before writing it:

1. state privately what is funny about this exact behavior or tension;
2. choose a comic mechanism;
3. inspect the ledger for recent mechanisms and images;
4. reject the first generic joke if it could fit five other cards;
5. write a replacement grounded in this claim.

Possible mechanisms include reversal, understatement, overstatement, a tiny
scene, mock dialogue, physical comedy, dignified self-justification,
affectionate contradiction, unexpected specificity, household observation,
timing, status mismatch, and literal canine logic.

Never rotate lines, assign jokes by index, or substitute a projected term into
a stock frame. Avoid defaulting to paperwork, departments, protocols, fine
print, committees, snacks, treats, or squirrels. These may appear rarely when
uniquely appropriate but must not become production-line language.

## 12. Five-card checkpoint gates

After every five completed cards:

1. parse the complete working JSON;
2. confirm card count, order, and locked fields;
3. reconcile completed IDs with the checkpoint;
4. run `lint_astrowoof_editorial.py` against the working deck;
5. write `<subject>.checkpoint-N-editorial-audit.json` containing the linter
   report plus a manual review of every warning;
6. scan exact duplicate sentences and humor;
7. inspect repeated openings, endings, headline structures, advice, imagery,
   comic mechanisms, and claim-type-correlated sentence frames;
8. compare the five new ledger jobs with adjacent claims and reject generic
   "Explain X through scene Y" distinctions;
9. compare the five new cards semantically: repeated lessons, emotional arcs,
   behavioral sequences, tensions, and practical conclusions count as
   repetition even when wording differs;
10. apply the shuffled-card test from the independent writing brief;
11. correct all errors and every substantiated warning before continuing;
12. save all working files and the externally inspectable audit artifact.

Do not stop merely because a checkpoint was reached and do not wait for user
approval. The audit gate is internal to the single subject request but must be
saved for later inspection.

## 13. Theme groups and filters

Read the full selected aspect set before finalizing aspect `theme_group`
labels, and independently read the full selected synthesis set before
finalizing synthesis labels. Discover subject-specific chapters; do not reuse
a fixed generic taxonomy across subjects. Approximate balance is a secondary
constraint, not the source of group meaning.

Context filters are retrieval promises. Assign a value only when a reader
choosing that filter would be satisfied to see the card. Record a brief
justification per assignment. Do not fill available slots, target equal
coverage, or force a match merely to avoid an empty array.

After all cards are authored, review every filter's result set as a collection
and remove tangential matches.

## 14. Summary-card phase

Summary cards are authored only after the agent understands the complete
subject. They may use selected cards, `unselected_claims`, whole-graph
analysis, and the projected-term registry.

For each of the four fixed lenses, first create a private source outline naming
the distinct selected and unselected motifs that support it. Then write an
integrated portrait rather than a list of registry terms:

1. Who the dog is
2. How the dog lives
3. What the dog needs
4. How the dog grows

The four summaries must differ materially from summaries written for another
subject. Universal dog-care prose with only the name changed fails.

When pronouns are absent, use the dog's name and grammatically neutral
constructions. Do not manufacture labels such as "You: Who They Are" or
"`<Dog>` Together."

## 15. Global final pass

After all 50 cards and four summaries are complete:

1. read the deck in priority order;
2. review each thematic cluster for distinct editorial jobs;
3. remove repeated headline structures and body openings;
4. remove repeated advice, imagery, and humor mechanisms;
5. verify direct-to-dog grammar;
6. read every hybrid body alone and correct one-way or templated entries;
7. verify no-astro contains neither astrology nor internal registry language;
8. verify light and full astrology use retained actual astrological evidence;
9. audit filters as user-facing result sets;
10. audit aspect and synthesis chapters for semantic coherence;
11. compare summaries against other subjects in the same batch for name-swap
    boilerplate;
12. confirm locked data and the registry remain unchanged;
13. run the editorial linter over all reader-facing fields and correct
    substantiated warnings;
14. when multiple subjects share a request, run the linter's cross-subject
    audit across complete decks, including summaries, advice, and humor;
15. run the official validator and correct every error;
16. save the final deck, whole-chart portrait, completed ledger, checkpoint
    audits, linter report, and validation report.

Schema validation proves structural safety, not editorial quality. Completion
requires both.
