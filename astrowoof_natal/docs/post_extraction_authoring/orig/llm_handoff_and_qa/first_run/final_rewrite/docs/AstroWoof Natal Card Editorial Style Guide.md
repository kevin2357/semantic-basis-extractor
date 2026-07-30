# AstroWoof Natal Card Editorial Style Guide

## 1. Purpose

This guide defines the editorial standard for AstroWoof natal-card datasets. It is intended for human writers, LLM editing agents, pipeline authors, and validators responsible for turning selected projected-chart claims into warm, useful, entertaining card copy.

The source artifact already contains the semantic and astrological substance. Editorial work should make that substance readable and engaging without changing its meaning, evidence, selection, or structure.

The finished deck should feel as if it were written by a perceptive person who understands dogs, astrology, and the small negotiations that make up life between a dog and a human. It should not sound like:

- a graph-processing report;
- a clinical behavior assessment;
- a generic horoscope;
- a list of training commands;
- a comedy generator obsessed with treats;
- or a template populated with different nouns.

The central editorial challenge is controlled variation. Every card must remain structurally dependable while sounding individually observed.

## 2. The Reader Experience

A good AstroWoof card gives the reader four things:

1. **Recognition:** “Yes, I can picture my dog doing that.”
2. **Interpretation:** “That behavior may make sense in this larger pattern.”
3. **Relationship value:** “I understand how I can meet or work with it.”
4. **Delight:** “This sounds like a real dog, and it made me smile.”

Not every sentence must provide all four. The card as a whole should.

Interpretations are tendencies and useful possibilities, not diagnoses or guaranteed predictions. Use language such as:

- may;
- can;
- often;
- may be more likely when;
- can work best when;
- may find it easier to;
- one useful possibility is.

Do not weaken every sentence with excessive qualification, but never present symbolic interpretation as proven clinical fact.

## 3. Source Fidelity and Artifact Integrity

Editorial work operates on an already-selected claim packet. It must not silently alter the semantic basis.

### 3.1 Locked content

Unless a task explicitly authorizes structural changes, preserve:

- schema version;
- generator metadata;
- subject identity;
- source metadata;
- coverage and statistics;
- categories and behavioral domains;
- whole-graph analysis;
- claim count and card order;
- `priority_id`;
- `claim_id`;
- `claim_type`;
- canonical claim;
- importance, confidence, and strength;
- selection metadata;
- tags;
- evidence;
- relations;
- all other validator-designated locked fields.

Editorial fields may generally include:

- headlines;
- bodies;
- dos;
- don’ts;
- funny dog quotes;
- imperative dog quotes;
- applicable canine jokes.

The current schema and validator are authoritative if their field list differs.

### 3.2 Projected term registry

Every artifact derived from a completed semantic-projection artifact must retain its complete `projected_term_registry`.

The registry is not optional metadata. It is the semantic decoder for compound projected vocabulary. It may include definitions for:

- projected concepts;
- operators;
- signs;
- houses or Doghouses;
- aspects;
- angles;
- other projection-specific terms.

When multiple compatible projected artifacts are combined, merge their registries and deduplicate identical entries. Preserve every term needed to decode the resulting artifact.

The final card dataset should carry the registry as a top-level object. Do not:

- omit it because the prose appears self-explanatory;
- summarize it;
- regenerate it from memory;
- move it inside an individual card;
- retain only the entries that the editor happened to mention.

### 3.3 Subject metadata and pronouns

Populate subject metadata before editorial generation whenever possible. Pronoun information should include:

- subject pronoun;
- object pronoun;
- possessive adjective;
- possessive pronoun;
- reflexive pronoun.

For example:

```json
{
  "gender": "female",
  "pronouns": {
    "subject": "she",
    "object": "her",
    "possessive_adjective": "her",
    "possessive_pronoun": "hers",
    "reflexive": "herself"
  }
}
```

Blank pronoun metadata creates a predictable failure mode: an editor may replace every pronoun with the dog’s name, producing sentences such as “Bre knows what Bre values” or malformed phrases such as “Bre body.” Do not solve missing metadata through mechanical name repetition.

In prose, establish the subject with the dog’s name, then use natural pronouns where clarity permits.

## 4. Overall Voice

AstroWoof should sound:

- warm but not sentimental;
- intelligent but not academic;
- observant but not diagnostic;
- playful but not frivolous;
- practical but not bossy;
- astrological but not mystical filler;
- specific but not biographically inventive.

Prefer concrete dog-life settings:

- greetings and visitors;
- walks and thresholds;
- toys, food, and valued objects;
- search games and scent trails;
- household changes;
- rest and retreat;
- training sequences;
- transitions between activities;
- excitement and settling;
- favorite people;
- jobs, helping, watching, and supervising;
- exploration and check-ins.

Do not invent unsupported facts about breed, medical history, trauma, prior behavior, household membership, or specific events.

### 4.1 Warmth through observation

Warmth works best when it arises from recognizable detail:

> A small success can become a full victory lap when everyone notices.

It works less well when asserted abstractly:

> Bre is a wonderful and loving soul with a special gift.

The first line lets the reader recognize the dog. The second could apply to almost any pet.

### 4.2 Analytical vocabulary

Technical language belongs primarily in full-astrology copy. Even there, translate it into lived meaning.

Use words such as `system`, `interface`, `activation`, `inhibition`, `coordination`, and `regulation` sparingly. Repetition makes the deck sound like a systems-analysis document.

When appropriate, prefer:

- settle;
- recover;
- find her footing;
- get comfortable again;
- work through the first reaction;
- return to the routine;
- pause;
- reset;
- gather herself;
- come back to the task.

“Regulation” is useful and should not be banned, but it should not become the default word for every change in state.

## 5. The Three Audience Voices

The three voices are different editorial products built from the same claim. They must not be created through pronoun substitution.

## 5.1 Handler voice

Handler voice addresses the human and describes the dog in the third person.

Its job is to help the person:

- recognize a tendency;
- understand what may be happening;
- distinguish similar-looking motivations;
- respond thoughtfully.

Example:

> Bre may approach quickly while taking the terms of one-to-one connection more seriously. A fast greeting does not automatically mean unlimited closeness; initiative and relationship comfort can run on different clocks.

Handler voice may include practical implications, but it should not read like a command sequence. It is primarily interpretive.

Avoid:

- describing the source graph or derivation;
- repeating the dog’s name where a pronoun is natural;
- turning every paragraph into “Bre may X. Therefore, you should Y”;
- clinical certainty;
- generic advice detached from the claim.

## 5.2 Direct-to-dog voice

Direct-to-dog voice addresses the dog as `you`.

It should sound like an affectionate, intelligent reading spoken to the dog:

> You like discovery with a little flair. When trying something new feels playful and you get to show what you can do, courage has room to grow.

It must not be handler copy with `Bre` mechanically replaced by `you`. Recompose the thought from the dog’s point of view.

Direct-to-dog voice should:

- respect the dog as an active subject;
- make motivations feel intelligible;
- maintain warmth and personality;
- remain readable to the human who is actually consuming it.

Do not:

- make the dog sound stupid;
- make every thought about snacks;
- place dense technical astrology in a joke-like dog monologue;
- use baby talk;
- imply human levels of abstract deliberation in otherwise literal prose.

## 5.3 Hybrid voice

Hybrid voice describes the dog–human relationship in motion.

It is not merely handler voice with more second-person language. It should show how the dog, the person, and the situation shape one another.

A successful hybrid card usually contains, explicitly or implicitly:

1. something the dog contributes or experiences;
2. something the person, environment, or relationship makes possible;
3. a resulting rhythm, adjustment, or next possibility.

This does **not** mean those elements should be labeled.

Strong hybrid examples:

> A quick hello does not have to become a long interaction. Pausing after Bre’s first approach gives the relationship room to settle into a pace that feels mutual instead of assuming the opening move decided everything.

> The first burst does not have to be the final behavior. If you let Bre orient before offering the actual working cue, excitement has a better chance of becoming purposeful action instead of being corrected mid-launch.

> The more reliably Bre’s private retreat remains available, the more freely she can choose to rejoin the household. A safe place works best when no one turns it into another social obligation.

### 5.3.1 Useful hybrid shapes

Vary the form:

- a shared activity or ritual;
- an observation about what happens between dog and person;
- an if/then interaction;
- a progression across two or three beats;
- a moment of mutual adjustment;
- an invitation to notice without demanding a specific response;
- a relationship outcome that develops over time;
- a practical arrangement that protects both connection and autonomy.

Hybrid does not always need an explicit `you`. A sentence may still be relational when it describes how human-created conditions affect the dog:

> Keeping one familiar resting place available can make a changing household easier for Bre to explore.

### 5.3.2 The role-assignment failure mode

Avoid turning hybrid voice into a systems diagram:

> Bre brings the fast first move; you bring reciprocal pacing. Her response tells you whether balance is available.

This is conceptually reciprocal but stylistically mechanical. Across a deck it quickly becomes:

> Bre brings X; you bring Y; her response tells you Z.

Do not hide this template by attaching introductory phrases:

> During a greeting, Bre brings X...

> When the household changes, Bre brings Y...

That changes the opening statistics without changing the writing.

Use `brings`, `supplies`, and `contributes` only when they are the most natural verbs for the particular sentence. Do not use them as field labels.

### 5.3.3 Hybrid range

The person should not always be the rule-giver while the dog reacts. Depending on the claim, the dog may:

- initiate;
- invite;
- interrupt;
- investigate;
- set the pace;
- make a preference visible;
- request distance;
- restore play;
- lead the pair toward useful information.

The human may:

- support;
- notice;
- answer;
- join;
- clarify;
- redirect;
- protect space;
- wait;
- refrain from crowding the moment.

Some hybrid cards may lean toward practical guidance, while others are more observational. That variation is healthy. Forcing explicit reciprocity into every card merely creates another template.

## 6. Astrology Density

Astrology density controls how explicitly the card names and explains its astrological basis. It does not change the underlying claim.

## 6.1 No astrology

No-astrology copy translates the claim completely into temperament, behavior, relationship, and ordinary dog life.

It must not mention:

- planets or luminaries;
- signs;
- houses or Doghouses;
- angles;
- aspects;
- astrology itself.

Example:

> Once Bre decides something matters, momentum may become part of the experience. A warning before transitions and a meaningful next target can make it easier to leave one valued thing without turning the handoff into a contest.

No-astrology copy is not “astrology with the nouns removed.” It should stand independently as natural prose.

## 6.2 Light astrology

Light-astrology copy names the most useful placement, aspect, or configuration, then moves quickly into interpretation.

Example:

> Mars in Taurus can give persistence to pursuit and play. Transitions usually go better when Bre can see what comes next, especially when the next step has enough value to receive momentum already in motion.

Do not enumerate every supporting placement. Choose the configuration most useful to the reader.

## 6.3 Full astrology

Full-astrology copy explains the relevant components, their relationship, and their application.

Example:

> Mars in Taurus in the second Doghouse ties drive to valued resources and sustained commitment. Rather than abruptly cutting off a target Bre has invested in, a clear transition toward another worthwhile action gives that staying power somewhere constructive to go.

Full astrology may include:

- planetary or angular function;
- sign style;
- house or Doghouse domain;
- aspect type;
- orb strength when relevant;
- how the components modify one another.

It should still read like an interpretation, not a database traversal. Avoid:

- “this selected claim”;
- “the selected relationships”;
- “in this deck”;
- “the synthesis rests on”;
- “the source material says”;
- “the semantic system”;
- “the projected graph”;
- “architecture” as a label for the dog or document.

Registry vocabulary may be used when it adds precision or AstroWoof flavor. Decode it accurately, but do not dump definitions or mechanically concatenate compound phrases.

## 6.4 Density does not govern humor

Do not make dog quotes increasingly astrological as density rises. A dog joke does not need to mention Saturn because the body does.

Humor, dos, and don’ts should generally remain stable across density variants for the same claim unless the schema explicitly requires otherwise.

## 7. Headlines

Headlines should be:

- concise;
- memorable;
- specific to the claim;
- appropriate to voice and density;
- distinct without becoming cryptic.

Handler headlines often name the recognizable pattern:

> Favorites Can Complicate the Rule

Direct-to-dog headlines can sound more personal:

> You Notice the Reward System

Hybrid headlines can imply a shared arrangement:

> Rewards That Keep Their Meaning

Avoid generating a deck through repeated headline formulas such as:

- `Let [planet] [verb]`;
- `Build [noun] Through [planet]`;
- `Together, [verb] [noun]`;
- `[planet] Wants [generic outcome]`.

Some repetition is natural. The audit should focus on whether neighboring headlines feel interchangeable.

## 8. Dos and Don’ts

Dos and don’ts convert interpretation into useful options. They should be concrete enough that the reader can picture the action.

Good:

> Keep one retreat area consistently available and low-demand.

> Deliver the promised reward promptly when the stated criterion is met.

> Let Bre pause after a bold moment before increasing the challenge.

Weak:

> Be patient.

> Stay consistent.

> Give her space.

Generic advice becomes useful only when tied to a situation, signal, or purpose.

Dos and don’ts should:

- follow from the card’s claim;
- preserve the dog’s agency;
- avoid presenting one interpretation as a mandatory training doctrine;
- distinguish between related cards;
- avoid promising behavioral outcomes.

Do not make every `dont` grammatically begin with “Don’t” if the container already labels it as a don’t, though this is a stylistic preference rather than a schema error.

## 9. Humor and Dog Voice

Humor should make the card feel more alive after the interpretation already makes sense.

Each claim may include:

- a funny dog quote;
- an imperative dog quote;
- an applicable canine joke.

The humor set should remain stable across the claim’s three astrology densities. This preserves claim identity and prevents astrology density from producing bizarre technical dog jokes.

Strong humor is:

- short;
- claim-specific;
- affectionate;
- observant;
- varied in premise and rhythm.

Examples:

> “I remember the routine. My feet have submitted an urgent amendment.”

> “This corner is not wasted space. It is essential canine infrastructure.”

> “I understand the rule. I am now evaluating whether the compensation package reflects current market conditions.”

Avoid:

- making every joke about treats;
- repeating the same “human, do this” construction;
- putting technical astrology in the dog’s mouth;
- making the dog incompetent;
- using humor to carry essential meaning;
- forcing a punchline into a serious or sensitive interpretation.

A useful deck-level test is whether the humor lines sound like 50 observations from one recognizable comic world rather than one sentence template with swapped nouns.

## 10. Derived and Synthesized Claims

Synthesized claims are appropriate in a final AstroWoof card set when they help tell a richer, more coherent story.

A synthesized claim may combine:

- repeated motifs;
- multiple placements;
- aspect patterns;
- angular relationships;
- convergent themes;
- meaningful tensions or divergences;
- strong-orb configurations;
- relationships traversed through the source graph.

The synthesis must remain grounded in evidence retained in the card packet. The final prose should present the interpretation, not the mechanics of constructing it.

Bad:

> This synthesis combines three selected systems from the projected graph.

Better:

> Bre’s stickiest moments may happen when two things both matter a lot—trust and information, reward and rules, closeness and space.

The supporting evidence remains available structurally. It does not need to intrude into reader-facing copy.

## 11. Common Failure Modes

### 11.1 Pronoun substitution

**Symptom:** “Bre knows what Bre values.”

**Cause:** Blank metadata or mechanical avoidance of pronouns.

**Prevention:** Populate pronouns upstream and copyedit sentences individually.

### 11.2 Reciprocal template

**Symptom:** “Bre brings X; you bring Y; her response tells you Z.”

**Cause:** Treating hybrid requirements as serialized fields.

**Prevention:** Recompose each hybrid paragraph around a real interaction.

### 11.3 Template camouflage

**Symptom:** “During a transition, Bre brings X…”

**Cause:** Adding varied openings to unchanged templated sentences.

**Prevention:** Rewrite the complete paragraph rather than its first clause.

### 11.4 Process leakage

**Symptom:** “In the selected deck…” or “This synthesis rests on…”

**Cause:** The editor narrates its own reasoning process.

**Prevention:** Make derivation invisible in human-facing prose.

### 11.5 Technical dog jokes

**Symptom:** The dog speaks about aspect geometry or semantic operators.

**Cause:** Astrology density is incorrectly applied to humor.

**Prevention:** Keep humor stable and doglike across densities.

### 11.6 Generic canine filler

**Symptom:** Every card mentions treats, walks, patience, consistency, or unconditional love.

**Cause:** Dog flavor is added independently of the claim.

**Prevention:** Select examples from the claim’s actual behavioral domain.

### 11.7 Late-deck collapse

**Symptom:** Early cards are rich while later cards become shorter and repetitive.

**Cause:** Context, time, or tool pressure leads the agent to rush.

**Prevention:** Use a ledger and checkpoint workflow.

### 11.8 Endless broad rewrites

**Symptom:** A nearly finished deck repeatedly acquires new defects.

**Cause:** Broad prompts such as “make everything warmer and more varied.”

**Prevention:** Once the deck is sound, switch to exact, surgical corrections.

## 12. Editorial Workflow

## 12.1 Before writing

1. Parse and validate the input artifact.
2. Confirm the intended dog and pronouns.
3. Confirm the card count and order.
4. Confirm the projected term registry is present.
5. Identify locked and editable fields.
6. Read the whole selected packet before editing individual cards.
7. Note major motifs so related cards can be differentiated rather than repeated.

## 12.2 Card-by-card writing

For each claim:

1. Read the canonical claim, selection reasoning, evidence, and relations.
2. Identify the card’s unique contribution to the deck.
3. Draft the three voice variants separately.
4. Draft the three astrology densities at their proper technical levels.
5. Write concrete dos and don’ts.
6. Add claim-specific humor.
7. Check the card for unsupported invention.
8. Record the completed `priority_id`.

Do not create direct-to-dog or hybrid copy by replacing pronouns in handler copy.

## 12.3 Ledger and checkpoint strategy

For long editing runs, maintain a durable ledger:

- completed priority IDs;
- current priority ID;
- validation status;
- location of the latest parseable checkpoint.

If the execution environment times out or loses file tooling:

1. Preserve completed work in a valid artifact.
2. Record the last completed card.
3. Resume at the next unfinished card.
4. Do not restart the deck.
5. Do not shorten later cards.
6. Reassemble and validate the complete artifact when all cards are finished.

The recovery instruction should be simple:

> Resume from the first unfinished priority ID using the saved ledger and checkpoint. Continue until all cards are complete, assembled, and validated.

## 12.4 Revision strategy

Use broad revision only while the deck has broad defects.

Once the deck has:

- correct voices;
- good density separation;
- varied prose;
- stable humor;
- complete metadata;
- and valid structure;

stop requesting global rewrites.

Move to a surgical list:

- card ID;
- field;
- exact defect;
- narrowly defined correction.

This protects successful writing from collateral changes.

## 13. Whole-Deck QA

Card-level validation is necessary but insufficient. A deck can contain 50 individually acceptable cards and still sound repetitive as a collection.

### 13.1 Structural checks

Confirm:

- valid JSON;
- expected card count;
- unchanged priority IDs and ordering;
- unchanged locked fields;
- complete evidence and relations;
- complete projected term registry;
- populated subject pronouns;
- no placeholders;
- every editorial field present;
- validator pass with no unresolved errors or warnings.

### 13.2 Voice checks

For a representative sample, remove the voice labels and ask:

- Is handler still identifiable as third-person interpretation?
- Is direct-to-dog clearly spoken to the dog?
- Is hybrid clearly about the relationship or shared situation?

If hybrid could be relabeled handler without anyone noticing, it needs more relational content.

### 13.3 Density checks

Confirm:

- no astrology contains no explicit astrology terms;
- light astrology names only the useful configuration;
- full astrology explains components without narrating graph mechanics;
- all densities preserve the same underlying claim.

### 13.4 Repetition checks

Search and manually inspect:

- repeated opening words and phrases;
- repeated final-sentence formulas;
- `Bre brings`;
- `Bre supplies`;
- `Bre contributes`;
- `you bring`;
- `you supply`;
- `you contribute`;
- `tells you`;
- `shows you`;
- repeated headline frames;
- repeated advice;
- repeated joke premises;
- repeated uses of `system`, `interface`, `regulation`, and similar analytical vocabulary.

These are audit signals, not automatic errors. Natural repetition is acceptable; visible templating is not.

### 13.5 Name and pronoun checks

Search for:

- lowercase versions of the dog’s name;
- multiple uses of the dog’s name within one short sentence;
- malformed possessives;
- object positions incorrectly filled by the name;
- pronouns inconsistent with metadata;
- ambiguous pronouns.

Every match should be read in context. Do not perform blind global replacement.

### 13.6 Thematic differentiation

Related cards should make distinct contributions. Clarify differences such as:

- initiating versus sustaining;
- excitement versus recovery;
- confidence versus impulsivity;
- home security versus social attachment;
- preference versus resource defense;
- training structure versus visible duty;
- exploration versus information gathering;
- connection versus surveillance;
- retreat versus avoidance.

### 13.7 Humor checks

Confirm:

- one stable humor set per claim across densities;
- the expected number of unique humor sets;
- no technical astrology in dog quotes;
- no excessive treat dependence;
- no repeated punchline template;
- humor does not contradict the interpretation.

## 14. Acceptance Standard

A deck is ready when:

- it is structurally valid;
- the semantic basis is preserved;
- the registry is complete;
- all three voices are distinct;
- all three astrology densities are correct;
- hybrid prose is relational without becoming formulaic;
- pronouns are natural and metadata-supported;
- cards are warm, specific, and useful;
- humor is varied and claim-grounded;
- no authoring mechanics leak into reader-facing prose;
- the deck remains engaging when read sequentially rather than only card by card.

Perfection should not be pursued through endless regeneration. When remaining concerns are isolated matters of taste, preserve the successful baseline and make only targeted edits.

## 15. Compact Agent Brief

The following can be used as a short reminder after an agent has already received the full guide:

> Preserve all locked semantic fields, evidence, relations, ordering, subject metadata, and the complete projected term registry. Write warm, specific dog-life prose in three genuinely distinct voices: handler interprets the dog, direct-to-dog speaks respectfully to the dog, and hybrid shows the dog–human relationship in motion. Scale astrology from none, to one useful named configuration, to a full but readable explanation. Do not narrate graph construction, use mechanical reciprocity templates, replace pronouns with repeated names, or make humor increasingly technical. Keep humor stable per claim, make dos and don’ts concrete, audit the whole deck for repetition, and switch to surgical edits once the deck is sound.
