# Proposed LLM Editorial Rewrite Prompt v2

You are performing a complete editorial rewrite of an AstroWoof projected natal card deck.

The existing edited JSON passed structural validation but failed editorial review. Its prose is repetitive, procedural, abstract, overly technical, and dominated by internal projection terminology. Treat every existing editable string as a negative example. Rewrite editable content from scratch rather than polishing or paraphrasing it.

## Files and authority order

Read all supplied files completely.

When instructions conflict, use this authority order:

1. The current selected authoring packet for locked claims, evidence, dependencies, scores, and card order.
2. `natal.bre.cards_true_gold_examples.json` for approved editorial quality.
3. The current authoring manual and editing-permissions checklist.
4. The legacy 26-card Bre file for partial semantic inspiration only.
5. The failed first-run prose only as a negative example.

`natal.bre.cards_true_gold_examples.json` is authoritative for:

- claim concreteness;
- semantic synthesis;
- approximate lengths;
- handler voice;
- direct-to-dog voice;
- hybrid voice;
- astrology-density differentiation;
- claim-specific humor;
- practical `dos` and `donts`.

Do not mechanically copy its jokes, headlines, or sentence structures.

The legacy 26-card Bre file is useful only for:

- the scope of some canonical claims;
- short no-astrology semantic explanations;
- examples of concrete guidance;
- possible interpretations of a few compound claims.

Do not imitate the legacy file’s:

- voice implementation;
- direct-to-dog grammar;
- repeated headlines;
- identical light/full astrology fields;
- repeated humor;
- pronoun assumptions.

## Required result

Produce one complete parseable JSON file named:

```text
natal.bre.cards.json
```

The output must contain exactly the same fifty claims in exactly the same order as the selected authoring packet.

## Locked fields

Do not add, remove, reorder, or alter:

- `claim_id`;
- `claim_type`;
- `category`;
- `importance`;
- `confidence`;
- `strength`;
- `priority_id`;
- `selection`;
- `behavioral_domains`;
- `tags`;
- `evidence`;
- `relations`;
- source metadata;
- coverage metadata;
- claim count.

You may update `generator.editorial_status` to `llm_completed`.

You may rewrite:

- `canonical_claim`, while preserving supported meaning;
- every headline and body;
- funny quotes;
- imperative quotes;
- applicable canine jokes;
- `dos`;
- `donts`.

## Work in internal passes

Do not write all fields in one undifferentiated pass.

### Pass 1: Build the Character Bible

Using only the fifty selected claims, determine:

- Bre’s emotional temperature;
- attention and information style;
- bonding and trust style;
- response to novelty;
- regulation pattern;
- relationship to rules and routines;
- characteristic pace;
- strongest tensions and contradictions;
- recurring strengths;
- likely comic perspective;
- motifs worth using sparingly;
- tones or caricatures that would misrepresent Bre.

Do not import information from discarded graph records or outside biography.

### Pass 2: Repair the semantic briefs

Review all fifty `canonical_claim` values before writing cards.

Rewrite any claim that merely reports graph recurrence or exposes an internal label.

Unacceptable:

> Several systems repeatedly participate in safe-den baseline.

Acceptable:

> A Dependable Home Base Makes Exploration Easier.

Every synthesized claim must answer:

> What becomes newly understandable when these selected premises are considered together?

If a synthesis does not add a concrete behavioral, experiential, relational, or practical proposition, rewrite it until it does.

### Pass 3: Make a deck map

Assign each claim one distinct editorial job.

Identify:

- claims that establish identity;
- regulation claims;
- relationship and trust claims;
- training and routine claims;
- play and adventure claims;
- tensions;
- gifts;
- developmental claims;
- subtle supporting claims.

Note overlapping claims and decide how each card will differ. Do not let several cards become differently worded versions of the same lesson.

### Pass 4: Author in batches

Write no more than ten cards per internal batch.

After each batch, check:

- evidence fidelity;
- voice differentiation;
- density differentiation;
- practical specificity;
- headline variety;
- joke-frame variety;
- overlap with completed cards.

Continue automatically until all fifty are complete. Do not ask the user to prompt each batch.

### Pass 5: Global editorial rewrite

Read the completed deck as one work.

Remove:

- repeated sentence openings;
- repeated headline structures;
- repeated joke premises;
- repeated disclaimers;
- generic advice;
- internal system vocabulary;
- cards that sound interchangeable.

Make the deck feel like one coherent portrait of Bre without turning Bre into a one-note character.

### Pass 6: Final QA and assembly

Assemble the authoritative JSON and run every structural and editorial check before returning it.

## Prohibited user-facing language

Do not expose generation or pipeline terminology in card prose.

Ban these phrases and close variants:

- selected evidence;
- selected dependencies;
- selected projected evidence;
- source operator;
- source record;
- projected evidence;
- semantic architecture;
- architecture is rendered;
- technical appendix;
- whole-chart pattern;
- recurring whole-dog theme;
- full-astro mode;
- paperwork;
- case file;
- clipboard;
- operational procedure;
- this pattern to recognize;
- symbolic lens;
- source for this card.

Projected terms such as `primary_companion_interface`, `behavioral_friction`, `developable_coordination`, `comfort_safety_regulation`, and `odd_behavior_needing_adjustment` are internal semantic labels. Translate them into lived dog behavior. Do not merely remove underscores or capitalize them.

## Length targets

Use the gold examples as the primary calibration.

- Headlines: generally 2–7 words.
- No-astrology bodies: generally 18–40 words.
- Light-astrology bodies: generally 25–50 words.
- Full-astrology bodies: generally 40–75 words.
- Direct-to-dog bodies: usually 1–3 concise sentences.
- Quotes and jokes: usually 8–24 words.
- Each `do` or `dont`: one concrete action or mismatch.

Do not make full astrology longer merely by listing every evidence record.

## Voice requirements

### Handler

Write to the person caring for Bre.

The handler voice should be:

- warm;
- observant;
- specific;
- nonjudgmental;
- practically useful;
- alert to context.

Describe what the handler might notice and what may help.

### Direct to dog

Address Bre as `you`.

Use correct second-person grammar throughout:

- `you are`;
- `you have`;
- `you regulate`;
- `your`.

Never write:

- `you is`;
- `you has`;
- `you regulates`;
- third-person references to Bre unless they appear inside an intentional quoted joke.

The dog voice should be concise and possess perspective. It may be witty, dignified, curious, dry, emphatic, or conspiratorial according to the Character Bible. It should not explain the generation process to a dog.

### Hybrid

Describe Bre and the handler working with the claim together.

Use natural constructions such as:

- `you and Bre`;
- `together`;
- `your shared routine`;
- `give Bre... then notice together...`.

Explain what each side contributes. Do not blame either participant.

The three voices must perform different jobs, not paraphrase one paragraph.

## Astrology-density requirements

All three densities must express the same claim.

### No astrology

Do not mention:

- planets;
- signs;
- houses or Doghouses;
- aspects;
- nodes;
- angles;
- chart geometry;
- projection terminology.

Write observable or experiential meaning in ordinary language.

### Light astrology

Name the one or two most useful placements or relationships. Translate them immediately into canine terms. Do not list the entire evidence chain.

### Full astrology

Explain the relevant operator, mode, Doghouse, aspect, or relationship geometry in natural prose.

Use only selected evidence and dependencies. Choose the details that explain the claim; do not dump provenance.

Light and full astrology must not be identical.

## Humor requirements

Humor must arise from the specific claim and Bre’s Character Bible.

Good humor:

- reveals the claim from Bre’s imagined perspective;
- preserves Bre’s dignity;
- varies rhythm and premise;
- is affectionate rather than belittling;
- makes a tension recognizable without mocking fear or distress.

Do not reuse production-line joke frames involving:

- paperwork;
- case files;
- clipboards;
- committees;
- footnotes;
- operational procedures;
- filing everything as important dog business;
- snacks or squirrels as the default punchline.

Snacks or squirrels may appear rarely when genuinely suited to the claim.

No exact joke may repeat. No joke frame should dominate the deck.

## Practical-guidance requirements

Every card needs at least two specific `dos` and two specific `donts`; three each is preferable when evidence supports them.

Good:

> Pause at the doorway and let Bre look before cueing forward.

Weak:

> Support the underlying needs with practical choices.

Good:

> Keep the cue and reward criterion consistent across household members.

Weak:

> Notice what works.

Guidance must be:

- observable;
- actionable;
- modest;
- evidence-related;
- nonmedical;
- non-diagnostic;
- respectful of actual canine observation.

Keep broad epistemic disclaimers at deck level. Do not waste repeated card-level guidance slots saying that astrology is not a diagnosis.

## Evidence and synthesis discipline

Every material statement must be supported by:

- that card’s locked evidence;
- or one of its selected dependency claims.

Do not introduce facts from the discarded graph.

A synthesis must:

- use every material dependency;
- explain the relationship among them;
- add insight beyond repeating them;
- remain understandable from cards included in the packet.

## Final rejection checks

Do not return the file until all checks pass:

- exactly fifty cards;
- original claim order;
- locked fields unchanged;
- no placeholders;
- valid JSON;
- every required voice filled;
- every density filled;
- direct-to-dog grammar is second person;
- unknown biographical details are not invented;
- no-astrology fields contain no astrology;
- light and full astrology are meaningfully different;
- full astrology uses only selected evidence;
- syntheses use only selected premises;
- headlines are varied;
- no dominant boilerplate phrase;
- no dominant joke frame;
- advice is claim-specific;
- internal projection labels have been translated;
- no user-facing process narration remains.

If file-writing tools are available, write the complete result directly. If output limits require internal batching, continue automatically and assemble one final authoritative file. Do not return a sample, an outline, or a partial deck.

Return:

1. the completed `natal.bre.cards.json`;
2. a concise QA summary reporting structural validation, repetition review, voice review, density review, and semantic review.
