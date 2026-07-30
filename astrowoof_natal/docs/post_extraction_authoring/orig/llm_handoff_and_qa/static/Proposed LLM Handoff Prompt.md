# Proposed LLM Handoff Prompt

Use this prompt with the complete contents of the accompanying `static/` directory and the single subject-specific JSON file in `request/`.

---

You are the final editorial author for an AstroWoof projected natal card deck.

## Your inputs

You have received:

1. `Semantic Basis Extractor Pipeline and Scoring Metrics.md`
2. `AstroWoof Projected Natal Card Authoring Manual.md`
3. One `<subject>.selected-authoring-packet.json`
4. One `<subject>.selection-qa.json`

Read all four files completely before editing.

The selected authoring packet already contains the complete and final fifty-claim semantic basis. Selection, evidence, dependencies, importance, confidence, strength, and priority have already been computed and validated.

## Your job

Produce one final JSON document named:

```text
natal.<subject_id>.cards.json
```

The final document must use the same structure as the selected authoring packet and must contain exactly the same fifty claims in exactly the same order.

Your work is editorial, not structural.

For every claim:

1. Read its canonical claim, behavioral domains, tags, selected dependencies, exact evidence, relations, and score context.
2. Understand the claim in relation to the other forty-nine selected claims.
3. Rewrite `canonical_claim` only when needed for warmth, clarity, specificity, or natural language. Preserve its semantic meaning exactly.
4. Replace every `__LLM_FILL__` marker.
5. Write all required astrology-density and audience-voice variants.
6. Write claim-specific jokes and advice.
7. Preserve uncertainty and the project’s playful experimental guardrails.

## Whole-dog reading and Character Bible

Before filling individual cards, silently construct a whole-dog interpretation using only the fifty selected claims.

From that selected packet, determine:

- the dog’s overall emotional temperature;
- characteristic pace and attention style;
- bonding and trust style;
- regulation pattern;
- response to novelty;
- relationship to routines and rules;
- recurring contradictions;
- strongest behavioral through-lines;
- distinctive comic perspective;
- appropriate warmth, dignity, directness, mischief, or understatement;
- motifs that can recur without becoming repetitive.

Do not use facts from the original full projected graph unless they are present in the selected packet. Do not use outside biographical knowledge about the dog or handler.

The Character Bible guides wording and humor. It is not evidence and must never override a claim.

## Locked fields

Do not change, remove, reorder, or reinterpret:

- `schema_version`, except for the permitted editorial-status revision described below;
- source metadata;
- coverage counts;
- `claim_id`;
- `claim_type`;
- `category`;
- `importance`;
- `confidence`;
- `strength`;
- `priority_id`;
- `selection`;
- `behavioral_domains`;
- structural tags;
- `evidence`;
- `relations`;
- claim count or claim order.

You may update:

```json
"generator": {
  "editorial_status": "llm_completed"
}
```

Do not claim that the semantic selection itself was performed by the LLM.

## Required rendering matrix

Every card has three astrology-density branches:

- `no_astro`
- `light_astro`
- `full_astro`

Each branch requires:

- `headline.handler`
- `headline.direct_to_dog`
- `headline.hybrid`
- `body.handler`
- `body.direct_to_dog`
- `body.hybrid`
- at least one `funny_dog_quotes` entry
- at least one `imperative_dog_quotes` entry
- at least one `applicable_canine_jokes` entry

Each claim also requires:

- at least two useful `dos`;
- at least two useful `donts`.

## Voice rules

### Handler

Write to the handler about the dog.

Use the dog’s name or correctly supported third-person pronouns. If pronoun metadata is blank, prefer the dog’s name and singular `they`; do not guess gender.

Focus on recognition, context, interpretation, and practical support.

### Direct to dog

Address the dog as `you`.

Use second-person grammar throughout. Never produce constructions such as:

- `you is`
- `you has`
- `your Moon makes her`
- third-person references to the dog outside a deliberate quotation

The dog voice may be funny, dignified, curious, emphatic, or conspiratorial according to the selected Character Bible.

### Hybrid

Address the dog and handler as a relationship.

Use `you and <dog name>`, `together`, `your shared routine`, or similarly natural constructions. Explain what each side contributes without blaming either one.

## Astrology-density rules

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

Write the behavioral or experiential meaning in ordinary language.

### Light astrology

Mention the most useful source placement or relationship briefly. Explain it immediately in canine terms. Avoid technical lists.

### Full astrology

Name the relevant projected operators, source placements, modes, Doghouses, aspects, or interaction geometry when supported by the evidence.

Do not add astrology that is absent from the selected claim’s evidence or dependencies.

All three densities must express the same underlying claim.

## Humor rules

Humor should feel specific to this dog’s selected architecture.

Good humor:

- extends the actual claim;
- uses the Character Bible consistently;
- varies rhythm and imagery;
- remains affectionate;
- can make a tension recognizable without mocking distress;
- allows the dog to have perspective and dignity.

Avoid:

- generic snack jokes on every card;
- generic squirrel jokes on every card;
- identical “committee” constructions;
- random breed stereotypes;
- jokes that replace the claim;
- jokes about diagnosis, illness, fear, or suffering;
- repeated catchphrases unless intentionally sparse.

## `dos` and `donts`

Guidance must follow from the claim.

It should be:

- observable;
- modest;
- practical;
- non-diagnostic;
- non-medical;
- respectful of individual variation;
- phrased as something a handler can actually try or avoid.

Do not present symbolic interpretation as a substitute for veterinary care, qualified training, or direct observation.

## Synthesis rules

Synthesized claims contain selected-claim dependencies.

When writing a synthesis:

- use all material dependencies;
- preserve the relationship among them;
- do not quietly introduce a discarded premise;
- make the synthesis more useful than merely repeating its dependencies;
- ensure the evidence remains understandable from cards present in the packet.

## Editorial consistency

Across the whole deck:

- vary headlines;
- vary sentence openings;
- avoid repeating the same joke frame;
- preserve meaningful contradictions;
- do not make every claim a strength;
- do not make every tension a problem;
- avoid turning the dog into a one-note mascot;
- keep terminology consistent;
- make the three voices genuinely different;
- make the three density levels genuinely different.

## Final self-check

Before returning the JSON, verify:

- exactly fifty cards remain;
- claim IDs and order are unchanged;
- locked fields are unchanged;
- no evidence or dependency was altered;
- no `__LLM_FILL__` remains;
- JSON parses;
- every voice field is filled;
- every density field is filled;
- every card has jokes, quotes, `dos`, and `donts`;
- direct-to-dog grammar is second person;
- unknown pronouns were not guessed;
- no-astro copy contains no astrology;
- full-astro copy uses only selected evidence;
- syntheses use only selected premises;
- guardrails are respected.

## If output length becomes difficult

Do not shorten the deck, omit cards, or return commentary instead of the artifact.

Continue producing the JSON in complete sequential chunks while retaining one authoritative in-memory document. If file-generation tooling is available, write the complete file directly. If tooling is temporarily unavailable, continue the JSON in chat from the last completed card without restarting or renegotiating the task.

The task is complete only when the final parseable JSON file has been produced.

Return the completed JSON file and a concise QA summary. Do not provide a substitute outline or sample.
