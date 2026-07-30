# AstroWoof Projected Natal Card Authoring Manual

**Status:** Detailed working specification for the AstroWoof projected natal card JSON, the claim-extraction workflow that produces it, and the writing system that turns projected natal evidence into audience-specific cards.

**Primary current example:** `Bre_cards_restored.json`

**Source framework basis:** the attached Woofmapping and operator-preservation documents, including `Operator_Preservation_Rules_V5_1_Woofmapping_Application_Rewrite.md`, `canine_projection_mapping_v0_2_nivek.md`, `canine_projection_mapping_v0_3_doghouses_transits.md`, `Woofmapped_Transit_Framework_v0.3_Hybrid_and_Lunar_Model.md`, and the Nivek projected-chart reading used as the detailed interpretive example.

---

## 1. What this document governs

This manual defines how AstroWoof converts a projected natal chart for a dog into a structured JSON document containing independently renderable cards. The JSON is not merely a storage container for cute copy, and it is not merely an export of astrological placements. It is the bridge between a projected semantic chart, a detailed whole-dog interpretation, a set of evidence-grounded claims, and the user-facing AstroWoof card interface.

The intended consumer is the AstroWoof application, especially its card and deck views. The interface may group cards into products such as Core Personality, Mind and Intelligence, Emotions and Inner World, Energy and Motivation, Strengths and Talents, Growth and Potential, Play and Adventure, Learning and Training, Communication, Social and Pack Life, Trust and Security, Stress and Resilience, and future health or wellness-oriented categories that remain carefully separated from medical claims. The card JSON therefore needs to support both semantic integrity and flexible presentation, because one underlying claim may appear in different decks, voices, astrology densities, audiences, and lengths without changing what that claim actually means.

The reference dashboard below illustrates the broader AstroWoof product context. It shows that AstroWoof is organized around dog profiles, chart-derived decks, user-selectable voice, astrology depth, and card layout, which means the data format must support those controls cleanly rather than baking one style into the source material. The current JSON is designed to make those interface choices possible while retaining the chart evidence needed for audit, revision, and future regeneration.

![AstroWoof dashboard reference](reference_astrowoof_dashboard.png)

The second reference image emphasizes the card-browser concept. The exact visual design may evolve, but the underlying architectural requirement remains stable: cards must be sortable, filterable, independently renderable, and traceable to the projected natal evidence that produced them. A future interface may display one sentence, one paragraph, a humorous quote, practical guidance, or explicit astrology, but each of those views should be understood as a rendering of the same grounded claim rather than as separate unrelated content.

![AstroWoof card browser reference](reference_astrowoof_card_browser.png)

---

## 2. The complete production pipeline

The production pipeline should be understood as a sequence of semantic compression and controlled rendering. It begins with the full projected natal graph, continues through a complete projected natal reading, extracts claims from that reading and graph, and only then produces compact card text. This order matters because writing cards before understanding the whole dog encourages generic jokes, repeated themes, missing tensions, and prose that sounds pleasant but is not anchored to the actual chart.

The canonical sequence is:

```text
exact natal source data
    ↓
projected natal graph
    ↓
complete projected natal reading
    ↓
dog identity / character bible
    ↓
claim extraction
    ↓
claim-level evidence retention
    ↓
multi-axis card rendering
    ↓
semantic QA
    ↓
editorial QA
    ↓
AstroWoof JSON
```

Each stage has a different responsibility, and no stage should quietly absorb the responsibilities of another. The projected natal graph provides structured source semantics, the complete reading explains how the system behaves as a whole, the character bible captures the distinctive identity and voice inferred from that system, claims isolate independently supportable propositions, and the renderer expresses each proposition for a specific audience and display context. The final JSON should preserve enough of every prior stage to make later editing and verification possible without reconstructing the entire process from memory.

This manual intentionally separates extraction from rendering. A claim can be correct while a particular headline is weak, and a headline can be delightful while the underlying claim is unsupported. Keeping those layers distinct allows AstroWoof to revise tone, humor, length, or audience without changing evidence, and it allows semantic reviewers to inspect operator preservation without being distracted by copywriting preferences.

---

## 3. Begin with a complete projected natal reading

The task should always begin with a complete natal interpretation of the dog before claims are extracted. The reading should be built from the complete projected chart rather than from isolated placements selected because they are easy, funny, or familiar. The Nivek example demonstrates the preferred depth because it interprets operators, modes, domains, relationships, tensions, and system-level architecture before compressing anything into cards.

The reading should first establish the canine Big Three. In the Woofmapped framework, the Sun is the enduring temperament and whole-dog organizing identity, the Moon is the comfort and regulation system, and the Rising sign is the first-response strategy or behavioral doorway. These three are not the entire chart, but they provide the first coherent answer to the questions “What kind of dog is this?”, “What helps this dog feel safe?”, and “How does this dog initially meet novelty, strangers, uncertainty, and the environment?”

After the Big Three, the reading should address the remaining projected planetary and angle operators in a consistent way. Mercury should be interpreted as scent-signal interpretation, cue decoding, environmental understanding, routine prediction, and other canine equivalents of interpretation rather than as human speech. Venus should be interpreted through valuation, preferred humans, preferred objects, reward style, affection style, and what the dog experiences as good, while Mars should be interpreted through pursuit, play, activation, defense, assertion, and directed action.

Jupiter should be read as expansion of the dog's world, optimism, permission, exploration radius, and confidence growth. Saturn should be read as limits, training structure, inhibition, routine, repeatability, responsibility, and the conditions under which rules become usable. Uranus, Neptune, and Pluto should preserve their deeper operators while being translated into canine-relevant domains such as novelty and disruption, atmospheric permeability and ambiguity, primal intensity, territory, hierarchy, trust, fear, compulsion, and transformation.

The reading should also address the angles as functional interfaces rather than decorative chart facts. The Ascendant describes the dog's behavioral doorway and first visible response, the Descendant describes the primary companion interface or counterpart style, the Midheaven describes visible pack function, and the IC describes the safe-den baseline or private security foundation. These angle interpretations are often especially useful for cards because they naturally correspond to observable patterns in introductions, household roles, attachment, and recovery.

The houses or Doghouses should be treated as domains in which operators act. The operator-preservation framework requires that the planet or point retain its functional role, the sign retain its mode or style, and the house retain its domain, rather than allowing any one element to replace the others. A Mercury placement therefore should not become “Gemini behavior” merely because the card sounds curious, and a house placement should not be treated as a personality trait without explaining what operator is acting there.

The complete reading must include relationships whenever the projected graph supplies them. Conjunction-like relationships may describe fusion or co-operation, squares may describe friction or competing demands, trines may describe easy flow, sextiles may describe available coordination channels, oppositions may describe polarity, and other relationship types should retain their declared projected semantics. If the projected graph contains no supported relationships, the reading and JSON should say so rather than inventing aspect-based cards from an unsupported assumption.

The reading should synthesize recurring architecture after interpreting atomic elements. This synthesis is where the author identifies major clusters, repeated modes, reinforced themes, tensions that recur across multiple systems, and practical patterns that are not reducible to a single placement. A synthesized statement such as “a secure den makes a bigger world possible” may emerge from the IC, Mercury, Jupiter, and Neptune acting together, but it should only become a claim when the contributing evidence is explicitly retained.

The complete read is also the source for emotional balance. A good natal reading does not describe every placement as a charming strength, and it does not describe every tension as a defect. It should explain how the same architecture can produce gifts, needs, stress expressions, development opportunities, and context-dependent behavior, because the cards will later need enough variety to avoid turning the dog into a one-note mascot.

A useful complete reading should answer at least the following questions in connected prose. It should explain the dog's overall temperament, comfort and regulation pattern, first-response style, information-processing pattern, bonding preferences, action and play pattern, adventure radius, relationship to rules and routines, response to novelty, atmospheric sensitivity, deep trust architecture, growth direction, instinctive fallback patterns, visible pack function, safe-den requirements, companion style, and the major ways these systems support or frustrate one another.

The reading should not be written as if it were a veterinary or behavioral diagnosis. AstroWoof is a playful experimental projection system, and the language should remain interpretive, probabilistic, and respectful of actual canine observation. Phrases such as “may,” “can,” “often,” “appears to,” “is likely to,” and “may be especially visible when” are generally preferable to claims of certainty, particularly when moving from symbolic structure to real-world behavior.

---

## 4. The complete reading as a Character Bible

The complete natal reading should produce an intermediate identity artifact that can be called the Character Bible. The Character Bible is not a fictional biography pasted on top of the dog, and it is not a license to invent random recurring jokes. It is a compact representation of the dog's distinctive emotional tone, perspective, behavioral style, recurring concerns, favored metaphors, humor potential, and interpersonal stance as inferred from the complete projected chart.

The Character Bible should describe how the dog seems to experience the world. One dog may feel like a cautious archivist of smells, another may feel like an exuberant neighborhood mayor, another may feel like a dignified guardian who takes routines seriously, and another may feel like a dreamy emotional barometer. These identity impressions should emerge from repeated chart architecture rather than from a single placement, breed stereotype, stock dog joke, or convenient writing gimmick.

The Character Bible is useful because card generation creates repetition pressure. Without a stable identity model, every curiosity claim becomes “sniffing,” every Saturn claim becomes “rules,” every Moon claim becomes “cuddles,” and every funny voice becomes interchangeable dog comedy. With a Character Bible, the same operator can be expressed through the dog's distinctive worldview while still preserving the claim's semantic center.

The Character Bible should include both stable identity traits and boundaries. It may describe the dog's likely warmth, confidence, observational style, pace, comic dignity, vulnerability, directness, curiosity, seriousness, or theatricality, but it should also say what the dog is not. A quietly observant dog should not suddenly sound like a hyperactive cartoon character unless the specific claim supports that contrast, and a dignified dog may still be funny without every line becoming regal parody.

For Bre, recurring motifs such as neighborhood intelligence, smell research, the Squirrel Council, careful observation, quietly competent supervision, meaningful routines, mild regality, warmth, and thoughtful participation can function as identity inspiration. Those motifs should not replace claim evidence, however, because a Squirrel Council joke under a comfort-regulation claim still needs to express comfort regulation rather than generic curiosity. The correct relationship is that the claim supplies the meaning while the Character Bible supplies the particular voice and imagery through which that meaning is expressed.

The Character Bible should be treated as reusable but revisable. It should remain stable enough to make the deck coherent, yet it should be updated when the complete reading reveals an overlooked subsystem or when editorial review shows that the current voice overemphasizes one theme. A Character Bible is therefore a controlled intermediate artifact, not a permanent personality verdict.

---

## 5. What a claim is in relation to the projected natal chart

A claim is the smallest independently defensible behavioral or experiential proposition that can be supported by the projected natal graph and the complete reading. It is more specific than a broad section theme, but more meaningful than a raw placement label. A claim should be capable of standing as the semantic center of one card while remaining traceable to one or more projected operators.

A placement itself is not automatically a claim. “Moon in Aries in Doghouse 1” is evidence, while “Bre may regulate more readily through immediate, body-led action than through forced stillness” is a claim derived from that evidence. The distinction matters because AstroWoof cards are designed to communicate interpretive meaning, not merely list astrological coordinates.

A claim is also not the same as a joke, headline, piece of advice, or narrative. “Professional Mood Sniffer” may be an excellent headline, but it is not a claim unless its underlying proposition is defined and evidenced. “Deploy emergency cuddle protocol” may be an entertaining quote, but it is only valid under a claim whose evidence genuinely concerns comfort, bonding, reassurance, or regulation.

Claims may be atomic or synthesized. An atomic claim is primarily derived from one projected placement, angle, orientation, or relationship, while a synthesized claim is derived from multiple pieces of evidence whose combined behavior supports a broader proposition. Synthesized claims are often the most useful and human-readable, but they are also the easiest place for interpretive drift, which is why their evidence arrays and relation fields must be especially explicit.

A good claim is narrow enough to audit and broad enough to render. “Bre's Moon is Aries” is too raw, while “Bre is curious, affectionate, brave, responsible, playful, and emotionally intelligent” is too broad to support as one coherent card. “Movement can be part of regulation” is appropriately scoped because it describes one pattern, can be supported by specific evidence, and can generate distinct handler, dog, hybrid, funny, and astrology-explicit renderings.

Claims should not duplicate one another merely because the same evidence can produce multiple phrasings. Two cards may share evidence when they isolate meaningfully different propositions, but the distinction must be explainable. For example, “Safety starts in motion” may focus on the Moon's regulation mechanism, while “Movement before calm” may synthesize Moon, Ascendant, and Mars into a broader sequence involving activation and settling.

Claims should also preserve uncertainty. Confidence and relevance scores describe the quality of the derivation, not the factual certainty of astrology as an empirical system. The prose should avoid converting a high internal projection score into an absolute behavioral assertion, because those scores measure fidelity within the projection framework rather than scientific validation.

---

## 6. What a claim is inside the JSON document

Within the JSON, a claim is represented by one complete card object. That object should include semantic metadata, evidence, relation data, practical guidance, and all user-facing renderings that belong to that claim. The object is deliberately self-contained so that cards can be sorted, edited, rendered, audited, or exported without losing the source proposition.

The current Bre example places user-facing content fields such as `handler`, `direct_to_dog`, `hybrid`, and the quote arrays alongside the claim metadata. It also retains a legacy or source `card` structure containing `no_astro`, `light_astro`, and `full_astro` renderings, which illustrates the desired multi-density concept even though the exact final nesting may be revised. The important rule is not one fixed nesting arrangement, but the permanent co-location of claim meaning, evidence, and rendered content.

A complete claim object should make five questions answerable without external guesswork. A reviewer should be able to determine what the claim says, why it exists, what evidence supports it, how it relates to other claims, and how it is presented to different audiences. If any of those questions requires reconstructing the original conversation or relying on memory, the object is incomplete.

The current JSON is listed as a working example rather than a perfect final schema. It demonstrates the key architectural commitment that evidence must remain with each claim, but it also contains evidence of the iterative process, including fields that overlap or preserve previous rendering stages. Future schema cleanup may normalize these structures, but cleanup must never remove provenance merely to make the file smaller or visually simpler.

---

## 7. Precise definition of every top-level JSON element

### 7.1 `schema_version`

The `schema_version` identifies the structural contract of the JSON document. It tells readers and software which fields, nesting conventions, and semantic expectations apply, and it should change when a backward-incompatible structural revision occurs. The value is not merely decorative metadata because future applications may need to migrate or validate documents created under earlier card schemas.

A schema version should be stable and explicit. Minor changes that add optional fields may justify a minor version increment, while changes that rename or reorganize required fields may justify a major increment. The current example uses `astrowoof.projected_natal_cards.v0.1`, which correctly communicates that the format is an early working contract rather than a frozen production standard.

### 7.2 `generator`

The `generator` object records the versions of the systems or manual processes that produced the document. It may identify the projection engine, projection profile, claim extractor, and card generator, which makes it possible to distinguish changes in source projection from changes in extraction or prose generation. This separation is essential for reproducibility because a card can change when the chart projection changes, when claim selection changes, or when only the writing style changes.

Generator metadata should be truthful. A manually reviewed or manually written stage should not be described as deterministic automation if it was not, and a prototype version should remain labeled as a prototype. The purpose is provenance, not prestige, so clarity is more important than presenting the process as more automated than it actually is.

### 7.3 `subject`

The `subject` object identifies the dog for whom the cards were generated. It should include a stable subject identifier, display name, subject type, pronoun data, breed when known and appropriate, birth datetime, and birth location when those fields are part of the authorized source data. Empty fields should remain empty or explicitly unknown rather than being guessed.

Pronouns deserve special attention because direct-to-dog and handler text may expose grammatical errors quickly. The renderer should rely on normalized pronoun fields where possible instead of performing naive string substitutions such as changing “Bre” to “you,” which can produce constructions like “you’s” or mismatched third-person verbs. A future schema may also include grammatical number and preferred handler terminology to make rendering safer.

### 7.4 `source`

The `source` object records the chart and projection material from which the cards were derived. It may include the source chart ID, source file, graph type, materialization type, projection ID, context ID, and source graph hash. These fields allow later reviewers to verify that the card deck corresponds to the intended chart and has not been silently regenerated from a different source.

The graph hash is particularly useful when the source file name remains unchanged across revisions. A file name alone does not prove semantic identity, while a hash can show that the underlying source graph changed. Source metadata should therefore be retained even when the end-user interface does not display it.

### 7.5 `coverage`

The `coverage` object explains what the source graph contained and what the generated card set could legitimately cover. It may include projected object counts, projected relationship counts, aspect-card counts, limitations, and guardrails. This is where the document should openly declare that unsupported relationship cards were not generated rather than hiding missing coverage.

Guardrails should state the epistemic and safety boundaries of the content. Appropriate examples include playful experimental projection, not veterinary advice, not behavioral diagnosis, and not empirically validated. These statements should guide both downstream presentation and future editorial decisions, particularly when cards concern stress, resilience, food, sleep, health, or training.

### 7.6 `statistics`

The `statistics` object summarizes the document's claims. It may include total claim count, counts by claim type, atomic or orientation claim counts, synthesized claim counts, and future QA coverage metrics. Statistics should always be recomputed after claims are added, removed, reordered, or merged, because stale counts create false confidence and make automated validation unreliable.

Future statistics should include evidence coverage. Useful fields may include the number of claims with evidence, number of claims missing evidence, number of synthesized claims with multiple evidence items, number of claims with completed semantic QA, and number of claims with completed editorial QA. These additions transform statistics from a simple inventory into a completion and integrity summary.

### 7.7 `categories`

The `categories` array lists the category vocabulary used by the document. Categories are broad organizational labels that support deck construction, browsing, filtering, and reporting, and they should not replace the more precise behavioral domains attached to each claim. A claim may belong to one primary category while touching several behavioral domains.

Category values should be controlled rather than improvised on every card. A controlled vocabulary makes the application predictable and prevents near-duplicates such as `core_trait`, `core_traits`, `personality`, and `core_personality` from fragmenting the same deck. Category changes should be treated as schema or taxonomy work rather than casual copy edits.

### 7.8 `behavioral_domains`

The top-level `behavioral_domains` array declares the available domain vocabulary used by claims. Domains are more granular than categories and describe the areas of canine life affected by a claim, such as comfort, attachment, communication, training, home, resources, play, curiosity, recovery, territory, trust, or vulnerability. These values support search, grouping, cross-deck reuse, and future recommendation systems.

The domain list should be grounded in the Woofmapped target architecture. It should not simply import human psychological categories without translation, and it should not use playful language where a stable semantic label is needed. Human-readable display labels can be generated separately while the stored domain identifiers remain consistent.

---

## 8. Precise definition of every claim-level element

### 8.1 `claim_id`

The `claim_id` is the stable machine-readable identifier for the claim. It should remain unchanged when headlines, narratives, jokes, or advice are edited, because those are renderings of the same proposition rather than new claims. A stable identifier allows relations, QA records, editorial histories, and application references to survive prose revisions.

Claim IDs should be descriptive, unique within the document, and deterministic whenever practical. Values such as `moon_regulation`, `sun_pack_role`, `motion_before_calm`, or `home_world_bridge` communicate the semantic center more clearly than sequence-only IDs. If a claim is materially redefined rather than merely rewritten, it should receive a new ID or an explicit migration record.

### 8.2 `claim_type`

The `claim_type` states how the claim was derived. Common values include `placement`, `angle`, `orientation`, `synthesized_theme`, `system_interaction`, and `tension`, and future schemas may add explicit relationship or developmental types. The type helps reviewers understand the expected evidence pattern and the amount of synthesis involved.

A `placement` claim should usually have one primary placement evidence item, while a `synthesized_theme` or `system_interaction` claim should usually have multiple pieces of evidence. A `tension` claim should preserve the conflicting systems or relationship that creates the tension rather than describing stress generically. The type should therefore match the derivation, not merely the tone of the card.

### 8.3 `category`

The claim-level `category` assigns the claim to a broad product or editorial grouping. It may be used to organize cards under angles, core traits, development, synthesized patterns, or future deck taxonomies. It should describe where the claim belongs in the content system rather than what astrological object produced it.

A category is usually singular even when a claim could appear in multiple decks. Cross-deck reuse should be handled through behavioral domains, tags, or an explicit deck-membership field rather than by duplicating the claim. This avoids semantic divergence between copies of the same proposition.

### 8.4 `canonical_claim`

The `canonical_claim` is the concise, audience-neutral statement naming the proposition. It should be understandable without the funny voice and should summarize the semantic center in language that remains stable across renderings. It is not required to contain astrological terminology, although it may if the schema chooses an astrology-explicit canonical layer.

A strong canonical claim is specific and generative. “Movement Can Be Part of Regulation” is stronger than “Active Dog” because it describes a relationship between action and regulation, and it is stronger than a paragraph because it remains easy to compare, rank, and reuse. The canonical claim should generally fit in one short line and should not attempt to include every nuance contained in the evidence.

### 8.5 `importance`

The `importance` score estimates how central the claim is to the dog's overall chart architecture or to the intended deck. It may be influenced by projected relevance, luminary or angle prominence, repeated reinforcement, centrality in the complete reading, or practical significance. Importance is primarily a ranking field and should not be confused with certainty or moral value.

Scores should be calibrated consistently within one generation process. A high score should indicate that the claim deserves prominent placement or frequent reuse, not that the behavior is guaranteed to occur. If ranking logic changes, the generator version should change or the scoring method should be documented.

### 8.6 `confidence`

The `confidence` score estimates confidence in the extraction or synthesis of the claim from the available projected evidence. It should reflect whether the semantic connection is direct, whether the evidence is complete, whether multiple systems converge, and whether the interpretation requires a larger inferential leap. Confidence does not establish empirical truth about astrology or the actual dog.

A direct placement claim may receive high internal confidence when the operator, mode, and domain combine cleanly. A broad synthesized claim may receive lower confidence even when it is useful, because it depends on integrating several sources and choosing one interpretation among plausible alternatives. Reviewers should be able to lower confidence without deleting a potentially valuable claim.

### 8.7 `strength`

The `strength` score estimates how strongly the pattern may express within the projected chart. It may reflect source prominence, repeated support, angularity, clustering, relationship density, or another declared metric. Strength is conceptually different from importance because a pattern may be strong but narrow, or important but expressed through subtle regulation rather than obvious behavior.

The score should be used carefully in user-facing products. It may help determine card ordering, emphasis, or whether a claim appears in a quick deck, but it should not be displayed as a scientific probability. The application should avoid implying that a score of `0.95` means a ninety-five percent chance of observed behavior.

### 8.8 `behavioral_domains`

The claim-level `behavioral_domains` array identifies the specific areas of canine life touched by the claim. A Moon regulation claim may include comfort, body state, attachment, and recovery, while a Mercury claim may include cue processing, scent ecology, communication, or home. These domains should reflect the actual claim rather than every domain loosely associated with the source planet.

Domains support reuse and discoverability. A claim can appear in a Core Personality deck and also be retrieved for Training or Trust because its domain metadata explains the overlap. Each domain should add meaningful retrieval value, so excessively broad domain lists should be avoided.

### 8.9 `tags`

The `tags` array contains concise descriptive labels for search, filtering, editorial navigation, and possible recommendation logic. Tags may capture recurring motifs, modes, behavioral qualities, or implementation-relevant distinctions that are too specific for the controlled domain taxonomy. They should remain short, normalized, and semantically useful.

Tags should not become a second uncontrolled claim narrative. Values such as `fast-regulation`, `resource-focus`, or `information-seeking` are useful because they describe compact facets, while long phrases or jokes belong in rendered content. A future validation step should identify duplicate spellings, singular-plural variants, and tags used only once without a clear reason.

### 8.10 `evidence`

The `evidence` array is the non-negotiable provenance record for the claim. Every claim must contain at least one evidence item, and synthesized claims should retain every material supporting item rather than only the most convenient one. Evidence is what allows reviewers to determine whether the prose preserves the projected operator or has drifted into generic characterization.

Evidence should remain attached to the claim throughout drafting, editing, merging, export, and QA. A prose-only intermediate file may be useful for a particular editor, but it must never become the authoritative source because order-based reconstruction is fragile and claim IDs alone may not preserve all derivational context. The authoritative document should always keep evidence and content together.

### 8.11 `relations`

The `relations` object records how the claim connects to other claims. Typical arrays include `reinforces`, `tensions_with`, and `related_claims`, each containing stable claim IDs rather than copied prose. These links allow the deck to represent a coherent system rather than a bag of independent personality statements.

`reinforces` should be used when another claim strengthens, repeats, or provides compatible support for the current proposition. `tensions_with` should be used when two valid claims create competing needs, pacing differences, or contextual friction, while `related_claims` can capture meaningful adjacency that is neither direct support nor tension. Relations should be derived from chart architecture or explicit synthesis, not added merely because two cards share a word.

### 8.12 `card`

The current example contains a nested `card` object with `no_astro`, `light_astro`, and `full_astro` variants. This field demonstrates the intended separation of astrology density from the semantic claim, and it preserves earlier renderer outputs that may still be valuable for comparison. The exact future name may change to `renderings`, but the concept should remain.

Each astrology-density branch may contain audience-specific headlines and bodies plus optional quotes or jokes. The branches should communicate the same claim at different levels of astrological explicitness, not introduce different interpretations. If the no-astro and full-astro branches would lead a reader to materially different conclusions, one or both renderings need revision.

### 8.13 `handler`

The top-level `handler` object is the primary user-facing rendering addressed to the human responsible for the dog. It usually contains `headline`, `body`, `narrative`, and `handler_advice`, and it should translate the claim into observably useful, respectful, non-diagnostic guidance. The handler rendering can acknowledge uncertainty while still being concrete enough to influence attention, routine, enrichment, training, expectations, or handling.

The handler rendering should not talk down to the reader or portray the dog as a problem to be fixed. It should explain what the pattern may look like, why it may make sense within the dog's architecture, and how the handler can respond constructively. Even when funny language is used elsewhere, the handler narrative should remain emotionally credible.

### 8.14 `direct_to_dog`

The `direct_to_dog` object addresses the dog in second person as a playful product voice. It may contain `headline`, `body`, `narrative`, and `dog_advice`, but it should still express the same underlying claim rather than becoming a random monologue. The voice can be whimsical because the human is the actual reader, yet the dog-directed framing should reinforce affection and recognition rather than ridicule.

The direct-to-dog renderer requires proper grammar and pronoun handling. It should be written intentionally in second person rather than generated by replacing the dog's name with “you,” because naive replacement creates errors such as “you builds,” “you’s,” or lingering third-person pronouns. A future renderer should use templates or grammatical generation rules that explicitly distinguish first, second, and third person.

### 8.15 `hybrid`

The `hybrid` object addresses the dog-handler pair as a shared system. It usually focuses on co-regulation, shared routines, mutual understanding, teamwork, or the way a handler can meet the dog's needs without erasing the dog's agency. It should not merely copy the handler text and add the phrase “together.”

A strong hybrid card explains the interaction between the claim and the relationship. For example, a curiosity claim may become a shared exploration ritual, while a comfort claim may become a mutual slowing-down practice. The hybrid voice is especially important for AstroWoof because many canine traits are expressed through attachment, environment, routine, handling, and relational context.

### 8.16 `headline`

A `headline` is the shortest user-facing expression of the claim within a particular audience or rendering branch. It should be memorable, specific, and faithful to the claim, and it may be straightforward or funny depending on the selected voice. It should not carry so much nuance that it becomes a sentence-length body paragraph.

The default target is three to eight words, with a soft maximum of approximately twelve words when a precise concept requires more space. Headlines should usually fit on one or two UI lines in a card layout. A headline that could apply to almost any dog, such as “A Special Friend,” should be rejected unless the body and claim make the distinction unusually clear.

### 8.17 `body`

The `body` is the compact explanatory text visible on a standard card. It should state the practical or experiential meaning of the claim in one or two sentences and should remain understandable without opening a longer narrative. The body is where the card earns its usefulness, because a headline alone is often too compressed to preserve operator meaning.

The default target is approximately twenty-five to sixty words, with shorter values acceptable for very simple cards and longer values reserved for complex synthesized claims. The body should not repeat the headline verbatim, and it should not introduce a second unsupported claim. Every sentence should be traceable to the canonical claim and evidence.

### 8.18 `narrative`

The `narrative` provides the richer card expansion. It should illustrate how the claim may appear in ordinary canine life, add context or emotional nuance, and make the dog's distinctive identity visible without drifting away from the claim. The narrative is the main place where the Character Bible can influence imagery, pacing, humor, and recurring worldbuilding.

The default target is approximately seventy-five to one hundred eighty words. A quick deck may omit or truncate it, while a full deck may allow two hundred to three hundred words for complicated tensions or system interactions. The narrative should remain one coherent expansion of the claim rather than becoming a miniature general natal report.

### 8.19 `handler_advice`

The `handler_advice` array contains concise actions, observations, or mindset adjustments for the human. Each item must follow directly from the claim and should help the handler respond to the described pattern rather than attempt to diagnose or correct the dog. Advice may concern routine, enrichment, cue clarity, pacing, environmental setup, recovery, choice, predictability, or shared ritual.

The default target is two to four items, with each item generally containing four to fourteen words. One item may be acceptable when the recommendation is uniquely clear, while more than four usually indicates that the claim is too broad or the advice is becoming a general training list. Advice should use actionable language without presenting medical, veterinary, or professional behavioral prescriptions.

### 8.20 `dog_advice`

The `dog_advice` array contains playful second-person suggestions addressed to the dog. It is primarily a tone and engagement device, but it must remain related to the claim and should not contradict the handler guidance. The advice can be humorous, affectionate, or mock-serious, yet it should still reinforce the dog's identity and the card's central meaning.

The default target is one to three items, with each item generally containing three to twelve words. These lines often work best as brief imperatives or permissions, such as “Take your time gathering clues” or “Show your human the interesting spots.” They should not all collapse into “trust your nose,” because repeated stock advice weakens both specificity and character.

### 8.21 `funny_dog_quotes`

The `funny_dog_quotes` array contains short lines written as if the dog were commenting on the claim. These quotes should derive their humor from the dog's chart-inferred identity and the claim's actual operator, not from generic dog behavior pasted into every card. A Moon-regulation quote, a Saturn-training quote, and a Mercury-investigation quote should feel meaningfully different even when all three sound like the same dog.

The default target is one to three items, with each item typically six to twenty words and rarely more than one sentence. One strong quote is better than three weak variants. Quotes should avoid humiliating the dog, trivializing fear or stress, or turning every serious pattern into a joke.

### 8.22 `imperative_dog_quotes`

The `imperative_dog_quotes` array contains mock instructions or demands voiced by the dog. It is especially useful for portraying the dog's agency, priorities, or comic seriousness, and it can make an abstract claim feel concrete. The imperative should reveal the claim, such as requesting a clear next step under a regulation claim or requesting additional investigation under a Mercury claim.

The default target is one to two items, with each item generally four to sixteen words. These lines should not merely repeat dog advice in a different tense, because their function is character expression rather than guidance. A good imperative sounds like this particular dog advocating for a need implied by this particular claim.

### 8.23 `applicable_canine_jokes`

The `applicable_canine_jokes` array contains third-person or narrator-style jokes related to the claim. These jokes can broaden the tone beyond the dog's direct voice and can support UI elements such as rotating footers, tooltips, or shareable snippets. They remain subordinate to the claim and should never be used as evidence.

The default target is one to three items, usually one sentence and approximately eight to twenty-four words. Jokes should be claim-specific enough that moving them to another card would noticeably weaken them. Reusable generic jokes may belong in a separate application-level joke library rather than inside a claim object.

### 8.24 `dos`

The `dos` array contains concise practical responses that align with the claim. Unlike audience-specific handler advice, these items function as normalized semantic guidance and may be used by future renderers, filters, or recommendation systems. They should remain grounded in the claim and should avoid overpromising outcomes.

The default target is two to four items, with each item generally three to ten words. Items should begin with a clear action verb when possible, such as “Offer a short movement reset” or “Reward voluntary release.” The array should not become a comprehensive care protocol.

### 8.25 `donts`

The `donts` array contains concise cautions about responses that may conflict with the claim. These items should explain what kinds of handling, pacing, assumption, or environmental pressure may make the pattern harder to navigate. They should not shame the handler or treat every imperfect response as harmful.

The default target is two to four items, with each item generally three to twelve words. A useful caution might distinguish urgency from bad intent, motion from refusal, observation from fear, or slow activation from low motivation. Each item should be specific enough to connect back to the claim.

---

## 9. Precise definition of every evidence element

### 9.1 `kind`

The evidence `kind` identifies what sort of source record supports the claim. Current examples use `projected_placement`, while future documents may include projected relationships, synthesized graph motifs, orientations, or other explicitly defined evidence types. The kind determines which additional fields are expected and how directly the item supports the claim.

Evidence kinds should remain literal and machine-readable. They should describe the source structure rather than the interpretation, because the interpretation belongs in the claim. A future validator should be able to reject an evidence item whose required fields do not match its declared kind.

### 9.2 `role`

The evidence `role` identifies whether the item is primary, supporting, contrasting, moderating, or otherwise functionally related to the claim. A primary item should be capable of explaining the claim's core, while supporting items add convergence, nuance, mechanism, or contextual structure. The role is particularly important for synthesized claims because not every contributing placement should be treated as equally responsible.

Roles should be assigned intentionally rather than by list order. If removing an item would destroy the basic claim, that item is probably primary, while an item that changes tone or expression without creating the proposition may be supporting. A future schema may allow more explicit roles such as `counterweight` or `trigger`, but those values should be controlled.

### 9.3 `source_object`

The `source_object` records the original astrological body, point, or angle. Examples include Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, North Node, South Node, Ascendant, Midheaven, IC, Descendant, Part of Fortune, or another supported source object. This field preserves traceability to the source chart.

The object name should follow a consistent vocabulary. Abbreviations such as `ASC`, `MC`, `IC`, and `DSC` may be acceptable when standardized, but mixed spellings should be avoided. User-facing renderers can expand or localize names without changing the stored identifier.

### 9.4 `source_sign`

The `source_sign` records the astrological sign associated with the evidence item. Within Woofmapping, the sign provides the mode or style through which the operator acts, such as immediate chase for Aries, nap-spot loyalty for Taurus, information sniffing for Gemini, pack-security focus for Cancer, or another declared canine mode. The sign should not be treated as an independent subsystem that replaces the source operator.

The source sign is part of evidence even when the no-astrology rendering never mentions it. It allows full-astrology output, semantic audit, and future regeneration from the same claim. The projected mode should be the primary canine-facing interpretation of the sign rather than an unexamined list of human personality adjectives.

### 9.5 `source_house`

The `source_house` records the original house or projected Doghouse number when applicable. It may be null for angles or evidence items whose domain is not represented by a numbered house. The house identifies where the operator acts and should remain distinct from the source object and sign.

A document must declare which house or Doghouse system was used. If the projection compresses several houses into one broader domain, that quotient or compression should be explicit rather than hidden. House evidence should never be inferred solely from a card category.

### 9.6 `projected_operator`

The `projected_operator` names the preserved functional role in canine space. Examples include `comfort_safety_regulation`, `pack_role_identity`, `scent_signal_interpretation`, `bonding_preference`, `chase_play_defense_drive`, `training_rule_structure`, `adventure_optimism`, or another operator defined by the projection profile. This field is one of the most important audit points because it states what must survive all later writing changes.

The projected operator should remain stable across voices and astrology densities. A funny renderer may make the operator entertaining, and a no-astrology renderer may hide its technical name, but neither may change it into a different function. Semantic QA should explicitly ask whether the prose still expresses the operator.

### 9.7 `projected_mode`

The `projected_mode` names the style in which the operator acts. It usually derives from the sign and may use values such as `immediate_chase_mode`, `nap_spot_loyalty_mode`, `information_sniffing_mode`, `pack_security_focus_mode`, `working_dog_seriousness_mode`, or another controlled projection-profile value. The mode adds behavioral texture without becoming the operator itself.

A common drift error occurs when writers preserve the mode but lose the operator. For example, an Aries Moon claim may become a generic boldness card because “immediate” was remembered while comfort regulation was forgotten. The evidence record prevents that error by keeping both fields visible.

### 9.8 `projected_domain`

The `projected_domain` names the canine life-domain in which the operator and mode are expressed. It may correspond to a Doghouse such as body and temperament, food and resources, smells and local data, den and home-base safety, play and zoomies, training and routine, companion bonds, trust and vulnerability, adventure territory, pack role, social group dynamics, or deep instinct. It may be null when the evidence concerns an angle or another non-house interface.

The domain should be specific enough to constrain interpretation. Mars in a resource domain should not automatically be rendered as generalized athletic energy, while Mercury in a home-safety domain should not become only neighborhood curiosity. Domain fidelity is one of the best protections against generic planet-sign writing.

### 9.9 `weight`

The `weight` records the relative contribution of the evidence item to the claim. A primary item may receive a value near one, while supporting items may receive smaller values that reflect their role in the synthesis. The weight should be understood as an internal derivational parameter rather than an empirical probability.

Weights should be calibrated within one extraction process. They may help rank supporting evidence, generate concise evidence summaries, or determine whether a synthesis is sufficiently grounded. A future validator may require that synthesized claims include at least one primary item and that supporting weights remain below the primary weight unless a documented reason exists.

### 9.10 `projection_relevance_score`

The `projection_relevance_score` estimates how directly the source evidence maps into the canine target domain under the chosen projection profile. A high score means the operator, mode, and domain have a strong and relatively direct canine interpretation, while a lower score may indicate a more speculative, compressed, or less central mapping. The score belongs to the projection process rather than the prose-writing process.

The score should influence caution and ranking, not invite false precision. A lower-relevance item may still be useful as supporting evidence, especially when multiple sources converge, but it should not silently become the sole basis for a confident claim. Reviewers should examine low-relevance primary evidence closely.

---

## 10. Writing axes: voice, astrology density, audience, and length

AstroWoof card writing is multidimensional. Voice, astrology density, audience, and length are separate choices, and the renderer should not assume that funny always means dog-directed, that maximal astrology always means long, or that handler voice must always be serious. Treating these axes independently gives the application far more flexibility and prevents a proliferation of unrelated card files.

A complete rendering matrix may be represented conceptually as:

```text
voice:
    normal
    funny

astrology density:
    none
    minimal
    maximal

audience:
    handler
    dog
    hybrid

length:
    quick
    standard
    expanded
```

Not every implementation must pre-generate all thirty-six combinations. The schema may store a smaller canonical set and generate additional views dynamically, but the writing specification should still define what each axis means. Any generated combination must preserve the same canonical claim and evidence.

---

## 11. Voice option: normal

Normal voice is clear, warm, observant, and emotionally credible. It should sound like a thoughtful description of the dog rather than a clinical assessment or a mystical proclamation. Normal voice may still contain charm and imagery, but its primary goal is recognition and practical understanding.

A normal handler rendering might say that Bre often notices emotional atmosphere and settles more easily when the household is calm. A normal dog rendering might tell Bre that she is good at noticing how everyone feels, while a normal hybrid rendering might emphasize that calm and reassurance move in both directions. All three remain grounded in the same claim even though their pronouns and relational focus differ.

Normal voice should be the semantic baseline used for QA. When a funny rendering is difficult to evaluate, reviewers should compare it to the normal rendering and canonical claim. If the humor cannot be explained as a stylistic transformation of the normal meaning, it has probably drifted.

---

## 12. Voice option: funny

Funny voice uses playful exaggeration, mock bureaucracy, dog logic, recurring identity motifs, and affectionate anthropomorphism. It should make the card enjoyable without making the claim less accurate. Humor is a rendering strategy, not a source of new evidence.

The funniest lines usually preserve the operator more strongly than generic dog jokes. A Mercury investigation claim can become “Please suspend judgment pending additional smells,” while a Saturn structure claim can become a household compliance memo, and a Moon regulation claim can become an emergency protocol for restoring equilibrium. These jokes work because the operator is still visible beneath the style.

Funny voice should be customized to the Character Bible. Bre may sound like a thoughtful investigator, assistant neighborhood manager, mild royal official, smell scientist, or concerned member of the Squirrel Council, while another dog may have a completely different comic identity. Reusing the same joke architecture for every dog would undermine the purpose of chart-derived uniqueness.

Humor should remain respectful. Fear, pain, medical concerns, severe stress, trauma, resource guarding, or potentially dangerous behavior should not be trivialized for a punchline. A light joke may coexist with a serious claim, but the card should never encourage the handler to dismiss observable distress.

---

## 13. Astrology density: none

The no-astrology option communicates the claim without naming planets, signs, houses, aspects, or technical projection operators. It should read as a self-contained behavioral insight while remaining fully traceable to evidence in the JSON. Removing terminology does not authorize removing mechanism or replacing the claim with a vague affirmation.

A no-astrology body for a Moon-in-Aries regulation claim might say that Bre often settles more easily after a brief, purposeful action than after being forced to remain still. The reader does not need to know the Moon, Aries, or the first Doghouse to understand the pattern. The evidence remains in the claim object so the simplified prose can still be audited.

No-astrology output is appropriate for users who want dog-centered guidance without learning astrology. It may also be useful for onboarding, quick cards, notifications, social sharing, or contexts where technical language would crowd the interface. It should never be described as evidence-free, because it is evidence-hidden rather than evidence-absent.

---

## 14. Astrology density: minimal

The minimal or friendly astrology option names the most relevant astrological factor in accessible language. It may mention an Aries Moon, Gemini Sun, Cancer IC, or a simple relationship between two placements, but it should avoid overwhelming the reader with every coordinate and technical operator name. The goal is to show why the interpretation exists while keeping the card readable.

A minimal rendering might say that an Aries Moon makes comfort active and body-led, or that a Gemini Sun makes pack identity curious and information-oriented. It can introduce the Doghouse in plain language when that domain is important, such as “in the home-and-safety Doghouse.” It should not list several placements unless the claim is genuinely synthesized from them.

Minimal astrology is often the best default product setting. It gives AstroWoof a distinct astrological identity while remaining approachable to users who do not know chart syntax. The interface may label this setting “Friendly,” “Light,” or another product term, but the data contract should preserve a clear semantic definition.

---

## 15. Astrology density: maximal

The maximal astrology option states the relevant placements, angles, houses or Doghouses, operators, modes, and relationships needed to explain the claim. It should be detailed enough for an astrology-literate reader to understand the derivation, but it should still be prose rather than a raw dump of the evidence array. Maximal astrology is explanatory density, not indiscriminate data volume.

A maximal synthesis might explain that Bre's Aries Moon in Doghouse 1 makes comfort regulation immediate and body-led, her Aries Ascendant gives the first-response interface a fast launch, and her Taurus Mars adds sustained physical follow-through around resources and embodied action. That explanation makes the “movement before calm” claim auditable in human language. It should not introduce unsupported aspects or reinterpret a placement beyond the declared projection profile.

Maximal astrology should remain readable and canine-centered. The purpose is not to revert to a conventional human natal interpretation, because the source has already been projected into canine architecture. Technical detail should clarify the Woofmapped operator, mode, and domain rather than replace them with generic sign descriptions.

---

## 16. Audience option: handler

Handler audience addresses the person responsible for understanding and caring for the dog. The text should help that person notice patterns, adjust expectations, support regulation, design enrichment, communicate more clearly, and appreciate the dog's distinctive style. It should avoid implying that the handler can control every expression of the chart.

Handler text should make observable behavior central. It may say what the pattern can look like, what conditions tend to help, what common misinterpretation to avoid, and what small response may be worth trying. The advice should remain proportionate to the claim and should not become professional medical or behavioral guidance.

The handler voice can be normal or funny, but even funny handler text should preserve usefulness. A mock incident report may be entertaining, yet the card should still tell the human that the dog is monitoring routine changes, seeking inclusion, or using observation before action. Humor should reward attention rather than replace it.

---

## 17. Audience option: dog

Dog audience addresses the dog directly in second person. The human reader understands that this is playful anthropomorphism, but the text should still feel affectionate, recognizable, and specific to the dog's chart-derived identity. It can grant the dog comic authority, dignity, agency, or a distinctive internal monologue.

Dog-directed text should avoid naive grammatical transformation. The renderer must deliberately write “you notice,” “you prefer,” and “your comfort system” rather than converting “Bre notices” into “you notices” or “Bre's” into “you's.” Pronoun and verb agreement should be included in automated QA.

The dog audience is particularly effective for humor and shareability, but it can also be tender. A direct-to-dog card may validate caution, celebrate curiosity, grant permission to rest, or recognize the dog's efforts to maintain pack harmony. The claim should remain visible beneath the affection.

---

## 18. Audience option: hybrid

Hybrid audience addresses the dog-handler relationship as a two-part system. It should explain how the dog's architecture and the human's response interact, especially around co-regulation, routine, trust, exploration, training, handling, and shared attention. Hybrid writing is not merely pluralized handler writing.

A hybrid curiosity card might say that a walk becomes richer when the dog investigates and the human joins the pace. A hybrid comfort card might say that reassurance moves in both directions and that a quiet ritual helps both participants settle. These renderings make the relational implications of the claim explicit.

Hybrid content is essential because canine behavior is embedded in environment and relationship. AstroWoof should not imply that every trait exists inside the dog independently of context. The hybrid voice helps the product remain compassionate and practical without collapsing into human-dog synastry, which is a separate evidence domain.

---

## 19. Length option: quick

Quick content is optimized for a small card, feed item, daily rotation, notification, or scan-heavy deck. It should usually contain a headline and one compact body sentence, with an optional quote or one advice item. Quick content must preserve the claim's core even when nuance is compressed.

The headline target is three to eight words, while the body target is approximately fifteen to thirty-five words. Advice or quote items should usually be three to twelve words. Quick content should not attempt to summarize every supporting evidence item.

Compression should be declared and controlled. A quick card is a quotient representation of a larger claim, and it may omit caveats or secondary mechanisms that remain available in standard or expanded views. It should not distort the claim merely to fit a visual tile.

---

## 20. Length option: standard

Standard content is the default card view. It should contain a headline, a compact body, a narrative paragraph, and a small amount of advice or supplemental humor. This length is intended to feel satisfying without becoming a full report.

The body target is approximately twenty-five to sixty words, while the narrative target is approximately seventy-five to one hundred eighty words. Advice arrays should contain two to four concise items, and quote or joke arrays should contain one to three strong items. The standard view should be able to stand alone while still inviting deeper astrology or evidence inspection.

Standard content is where the deck's coherence becomes most visible. Each card should sound like the same dog and product, but each claim should still contribute something distinct. Repetition review is therefore especially important at this length.

---

## 21. Length option: expanded

Expanded content is intended for detailed card views, report exports, educational modes, or readers who want the derivation and context. It may include two or more paragraphs, explicit astrology, a discussion of supportive and tension relationships, and more nuanced practical implications. Expanded content should still focus on one claim rather than reproducing the complete natal read.

The default target is approximately two hundred to five hundred words, with longer content allowed for major synthesized themes. The expansion should explain why the evidence supports the claim, how the pattern may vary by context, how it interacts with related claims, and what the handler should avoid overgeneralizing. It should not pad simple claims merely to satisfy a length setting.

Expanded writing is also a valuable QA artifact. When a concise card seems vague, an expanded derivation can reveal whether the claim is genuinely coherent or merely attractive phrasing. The expanded layer should therefore be generated before final compression for difficult synthesized claims.

---

## 22. Relationship between every rendered item and its claim

Every text field under a claim must express, illustrate, advise on, contextualize, or humorously transform that same claim. No field is a free-writing slot. A card may be varied in voice, audience, and density, but it should remain semantically recognizable as one proposition.

A useful test is the relocation test. If a quote, joke, advice item, or narrative could be moved to five unrelated cards without losing meaning, it is probably too generic. Generic material may still be charming, but it belongs in a separate application-level content pool rather than inside a claim-specific object.

A second test is the evidence-backtrace test. A reviewer should be able to point from each material sentence to the canonical claim and then to at least one evidence item. Not every adjective requires its own evidence record, but every behavioral assertion and every practical recommendation should be explainable through the claim.

A third test is the operator-preservation test. The renderer must preserve the source operator even when it changes surface language. Mercury may become smell investigation, cue reading, or neighborhood intelligence, but it should not become motivation; Saturn may become rules, delay, inhibition, or repeatability, but it should not become affection simply because the resulting card sounds warm.

A fourth test is the domain-preservation test. The card should retain where the operator acts. A Venus claim in a resource domain may concern favored objects, food, toys, and comfort preferences, while the same Venus operator in a companion domain may concern affection and preferred relational exchange. Generic planet writing fails this test because it ignores the projected domain.

A fifth test is the mode-preservation test. The card should retain how the operator acts without allowing the mode to take over the entire interpretation. Gemini can make an operator quick, sampling, and information-oriented, while Cancer can make it protective and home-focused, but the operator still determines what function is being performed. Good writing preserves all three layers.

---

## 23. Worked example: atomic placement claim

Consider a claim whose evidence is Moon in Aries in Doghouse 1, with projected operator `comfort_safety_regulation`, projected mode `immediate_chase_mode`, and projected domain `doghouse_1_body_temperament_presence`. The evidence says that the Moon's comfort and regulation function acts immediately and physically in the dog's body and visible temperament. The claim should therefore concern how safety, regulation, and body-led response interact.

A strong canonical claim is “Safety Starts in Motion.” A normal no-astrology handler body might say, “Bre often regulates by doing something rather than waiting quietly for feelings to pass, so a brief purposeful action may help settling become available.” A funny dog-directed line might say, “Please assign one clear emergency task before requesting inner peace.”

A weak rendering would say, “Bre is bold and loves adventure.” That text preserves an Aries stereotype but loses the Moon's comfort-regulation operator and the first-domain body context. The evidence array makes the mistake visible because the prose can be compared directly to the operator, mode, and domain.

A second weak rendering would say, “Bre needs lots of exercise.” That statement overreaches from a regulation mechanism to a broad physical prescription and may conflict with the dog's actual health, age, or daily needs. The correct card can suggest a brief structured movement reset without converting symbolic interpretation into universal exercise advice.

---

## 24. Worked example: synthesized claim

Consider “Movement Can Be Part of Regulation,” supported primarily by the Aries Moon and secondarily by the Aries Ascendant and Taurus Mars. The Moon supplies the comfort-regulation function, the Ascendant supports an immediate behavioral doorway, and Mars contributes steady embodied follow-through. The synthesis is not simply “this dog is energetic,” because the important pattern is the sequence through which action may make settling possible.

The evidence roles matter. The Moon should remain primary because the claim concerns regulation, while the Ascendant and Mars explain why regulation may begin quickly and continue physically. If Mars were treated as primary, the card might drift toward play drive or persistence rather than emotional settling.

A standard handler narrative might explain that forced stillness is not always the shortest path to calm and that one brief, familiar action can sometimes help the body organize before a settle cue. A hybrid rendering might emphasize that the human provides the structure while the dog supplies movement and feedback. A funny imperative might say, “Please authorize one meaningful task before initiating blanket mode.”

---

## 25. Worked example: system interaction claim

Consider “A Secure Den Makes a Bigger World Possible,” supported by the Cancer IC, Cancer Mercury in the home-and-safety domain, Jupiter in the play domain, and Neptune in the adventure domain. The claim describes an interaction between private security and outward exploration rather than a single placement. The evidence should therefore include the safe-den baseline as primary and the information, optimism, and atmospheric systems as supporting.

The handler rendering can explain that reliable home rituals may expand confidence rather than make the dog dependent. The dog rendering can celebrate returning to a known base after field research, while the hybrid rendering can frame exploration and homecoming as one shared rhythm. The funny voice may use “base camp,” “mission control,” or “den security clearance,” provided the underlying relationship remains visible.

A weak version would simply say, “Bre loves home and adventures.” That sentence lists two themes without explaining the system interaction. The stronger claim says that security enables expansion, which is the actual synthesis created by the evidence.

---

## 26. Worked example: tension claim

A tension claim should describe two valid systems that create friction, not label one side as wrong. For example, an immediate comfort-response system may conflict with a slower training-rule system, producing moments when the dog knows the routine but cannot access it comfortably at the same speed. The card should help the handler distinguish knowledge from readiness.

The evidence array should include both sides of the tension and any projected relationship that supports the conflict. The canonical claim might say, “Knowing the Rule Is Not Always the Same as Being Ready,” while the handler body explains that body state and learned structure can briefly fall out of sync. Practical guidance might recommend reducing cue load, restoring predictability, or allowing a short reset before repeating the rule.

The funny voice can still work if it respects the tension. A dog quote such as “I have received the memo, but my nervous system has requested an extension” preserves both rule awareness and temporary regulation difficulty. A generic joke about disobedience would undermine the claim and encourage the wrong interpretation.

---

## 27. Evidence preservation rule

Evidence preservation is mandatory. Every claim must retain the evidence items that justify its existence, and those items must remain attached throughout every production stage. A claim without evidence is not an AstroWoof projected natal claim; it is unsupported creative characterization.

The evidence should not be removed for editing convenience. Editors may work from a prose-focused view, but the authoritative source must preserve claim IDs, canonical meaning, evidence, relations, and renderings together. If a tool requires a flattened file, the flattening should be generated from the authoritative document and merged back by stable claim ID with validation rather than by unverified position alone.

Evidence should also remain visible during semantic QA. The reviewer should not approve prose merely because it sounds like the dog or matches the Character Bible. The question is whether this specific claim, under this specific evidence, has been rendered faithfully.

The current Bre restoration process demonstrated why this rule matters. The prose remained usable, but once metadata and evidence were separated, confidence in claim-card alignment depended on the assumption that order had not changed. Restoring by index worked as a recovery technique, but it should not become the normal workflow.

---

## 28. Human-readable evidence summaries

In addition to the machine-readable `evidence` array, future versions should include a compact human-readable evidence summary. This summary is not a replacement for structured evidence and should be generated from it. Its purpose is to help writers and reviewers understand the derivation quickly without manually decoding every nested field.

A useful structure might look like this:

```json
"evidence_summary": {
  "primary": [
    "Moon in Aries, Doghouse 1"
  ],
  "supporting": [
    "Aries Ascendant",
    "Mars in Taurus, Doghouse 2"
  ],
  "operator_summary": "Comfort regulation begins through immediate, body-led action.",
  "synthesis": "Brief structured motion may make settling easier."
}
```

The summary should remain concise and deterministic. It should not introduce interpretations absent from the structured evidence, and it should be regenerated whenever evidence changes. Human-readable summaries can dramatically reduce semantic drift during editing because the author sees the intended mechanism beside the prose.

---

## 29. Claim-level QA metadata

Future claim objects should include a QA block that records semantic and editorial review. The block should distinguish whether evidence has been reviewed, whether the projected operator is preserved, whether the domain and mode are preserved, whether audience grammar has been checked, whether advice remains proportionate, and whether the claim remains distinct from neighboring claims. These fields turn informal confidence into a visible completion state.

A possible structure is:

```json
"qa": {
  "evidence_reviewed": true,
  "operator_preserved": true,
  "mode_preserved": true,
  "domain_preserved": true,
  "audience_grammar_checked": true,
  "claim_distinctness_checked": true,
  "character_voice_checked": true,
  "editorial_status": "approved",
  "notes": ""
}
```

The QA block should not pretend that one automated check proves semantic validity. Some fields may be machine-validated, while others require human review, and the document should identify which is which. A future process may also include reviewer name, timestamp, generator version, and a revision reason.

---

## 30. Semantic QA process

Semantic QA begins by reading the canonical claim and its evidence before reading the rendered prose. The reviewer should identify the primary operator, mode, domain, supporting systems, and any relevant relationships. Only then should the reviewer evaluate whether each audience and astrology-density variant preserves the same meaning.

The reviewer should check for operator drift, mode takeover, domain loss, synthesis overreach, unsupported certainty, duplicated claims, generic advice, and contradictions between variants. A no-astrology rendering may omit terms, but it may not omit the central mechanism, while a maximal-astrology rendering may add explanation but may not add unsupported placements. Humor should be checked separately because it often hides drift behind charm.

Semantic QA should also compare the claim with the complete natal reading. An isolated card can be technically consistent with one placement while distorting the whole dog if it ignores a major counterweight or repeatedly overemphasizes one subsystem. The full reading provides the context needed to decide whether a card is accurate, incomplete but acceptable, or misleading.

---

## 31. Editorial QA process

Editorial QA begins after semantic QA. It checks clarity, grammar, pronoun consistency, tone, pacing, repetition, word length, UI fit, audience distinction, and quality of humor. Editorial changes should not alter the canonical claim or evidence without returning the card to semantic review.

Pronoun QA is especially important for direct-to-dog content. The current example contains artifacts created by naive substitution, which demonstrates why audience text should be generated independently rather than mechanically transformed. Automated checks should flag phrases such as “you’s,” second-person subjects with third-person verbs, and references that switch unexpectedly between “you,” “she,” and the dog's name.

Deck-level editorial QA should check repetition across cards. A recurring motif can strengthen identity, but repeated headlines, identical advice, interchangeable jokes, and constant emphasis on curiosity can flatten the deck. The goal is coherence without monotony.

---

## 32. Determinism and reproducibility

The generation process should preserve deterministic structure wherever practical. The same source graph and extraction rules should produce the same claim IDs, evidence associations, and canonical claims unless an explicitly versioned editorial or semantic change occurs. Deterministic structure makes later comparison and regression testing possible.

Rendered prose may allow controlled variation, especially in funny voice, but the system should record the renderer version and preserve stable semantic inputs. If randomized generation is used, a seed or equivalent reproducibility mechanism should be stored when feasible. The process should not claim determinism when only one unrepeatable generation was performed.

A future QA runner should compare claim inventories, evidence arrays, and canonical meanings across regenerations. Textual determinism may be tested separately from semantic determinism. A card can vary stylistically while still preserving the same claim, but that variation should be intentional and measurable.

---

## 33. Current example: `Bre_cards_restored.json`

`Bre_cards_restored.json` is the current working example for this specification. It contains twenty-six claim objects, each carrying user-facing handler, dog, and hybrid content alongside claim IDs, types, categories, canonical claims, ranking scores, behavioral domains, tags, evidence, relations, legacy astrology-density card variants, and practical dos and don'ts. It therefore demonstrates the core requirement that rendered content and provenance remain in the same authoritative object.

The example should be treated as instructive rather than perfect. It includes useful material from multiple production passes, but it also reveals areas for normalization, including duplicated rendering layers, stale or historically inherited structures, and grammatical artifacts in some direct-to-dog text. Those imperfections are valuable because they show exactly what the next schema and workflow should prevent.

The first claim illustrates a placement claim supported by Moon in Aries in Doghouse 1, with comfort regulation as operator, immediate chase as mode, and body-temperament presence as domain. The fourth claim illustrates a synthesized theme supported by Moon, Ascendant, and Mars evidence. Later claims illustrate angles, system interactions, multiple supporting sources, relation links, and practical guidance, making the file a useful benchmark for future authoring and validation.

The example is included in this package beside the manual. Future manuals should continue to name one concrete current example so that abstract rules remain tied to a real artifact. When a new canonical example supersedes Bre, the document should record the change rather than silently replacing the reference.

---

## 34. Recommended schema improvements approved for future work

The authoritative card object should permanently keep semantic evidence and rendered text together. This is the most important process improvement because it eliminates order-based restoration and preserves auditability during every edit. Prose-only exports may exist as temporary views, but they should never become the canonical source.

A human-readable `evidence_summary` should be added beside the structured evidence array. This makes the operator, primary source, supporting sources, and synthesis visible to authors at a glance. The summary should be generated from structured evidence so that the two cannot drift independently.

A claim-level `qa` object should be added. It should track evidence review, operator preservation, mode preservation, domain preservation, audience grammar, character voice, distinctness, editorial status, and notes. This turns the authoring process into an inspectable workflow rather than a sequence of undocumented judgments.

Claim extraction and prose rendering should be separate stages. The complete reading should first produce canonical claims and evidence, and only approved claims should enter the writing stage. This separation allows the same claim set to support multiple voices, audiences, lengths, and astrology densities without semantic duplication.

The Character Bible should be an explicit intermediate artifact. It should summarize the dog's distinctive identity, tone, worldview, recurring motifs, emotional style, and boundaries as inferred from the complete natal read. Renderers should consult it for uniqueness while semantic QA ensures that character flavor never replaces evidence.

Completion-log coverage should be added at the document level. The statistics or QA summary should report claim count, evidence coverage, missing evidence, number of synthesized claims, number of claims with semantic QA, number with editorial QA, and any known limitations. A deck should not be described as complete when these fields reveal unfinished work.

Development-stage metadata should be clearly labeled or removed from production exports. Prototype extractor versions, manual-generation notes, temporary merge fields, and deprecated rendering branches may be useful during development, but production artifacts should distinguish active contract fields from historical scaffolding. Removing clutter is acceptable only after provenance and migration needs are satisfied.

The schema should include explicit grammar-safe audience rendering rather than relying on substitution. Pronouns, possessives, verb forms, and subject references should be generated from structured grammatical data. Automated validation should flag common audience-conversion errors before release.

The process should prefer stable claim IDs over positional alignment. Index-based merging can remain an emergency recovery technique when two files are known to preserve order, but normal editing should merge by claim ID and should verify that the full claim inventory matches. Any unmatched or duplicated IDs should stop the merge rather than silently dropping data.

---

## 35. What not to do

Do not begin by writing a stack of cute cards from the raw placement list. That approach produces plausible dog content but loses system architecture, underrepresents tensions, and encourages repeated stereotypes. The complete read must precede claim extraction and rendering.

Do not treat the Character Bible as evidence. It is a synthesis and voice guide derived from the complete reading, but a specific card still needs claim-level evidence. A line that sounds exactly like Bre can still be semantically wrong for the claim under which it appears.

Do not remove evidence after the prose is approved. Approval can later be challenged, cards may be reordered, and future editors may need to understand why a line exists. Evidence is part of the product's integrity, not temporary development scaffolding.

Do not interpret signs as free-floating personalities. Signs provide modes, planets and points provide operators, houses or Doghouses provide domains, and relationships describe interactions. Collapsing those roles creates operator drift.

Do not generate direct-to-dog text through blind replacement. Second-person writing requires intentional grammar, and the tone should be designed for the dog audience from the start. The same warning applies to hybrid text, which needs relational framing rather than a simple pronoun change.

Do not make medical, veterinary, diagnostic, or empirically validated claims. AstroWoof may discuss symbolic themes related to comfort, stress, sleep, food, routine, or resilience, but it must preserve its stated guardrails. Actual concerning behavior or health symptoms belong with qualified professionals.

---

## 36. Minimum acceptance criteria for a completed natal card JSON

A completed document must identify the source chart, projection profile, subject, schema version, generator versions, coverage, limitations, and claim statistics. It must contain a complete set of claims derived from a comprehensive projected natal reading rather than a convenience sample of placements. Every claim must include a stable ID, canonical claim, type, evidence, domains, and user-facing renderings.

Every claim must have at least one evidence item, and synthesized claims must retain all material supporting evidence. Every rendering must remain faithful to the same canonical proposition across audience, astrology density, voice, and length. Every advice item, quote, and joke must relate specifically to its parent claim.

The document must pass structural validation, semantic QA, audience grammar QA, and deck-level repetition review. Counts and completion metadata must be current. Known limitations must be stated rather than hidden.

The final artifact should be usable by the application without requiring the original chat conversation. A future developer or editor should be able to understand the card, its evidence, its voice, and its intended presentation by reading the JSON and this manual. That self-sufficiency is the practical definition of a successful interchange format.

---

## 37. Authoring execution and persistence

The detailed working method is now specified by `LLM Card-by-Card Authoring
Execution Protocol.md`. That protocol is normative for LLM authoring.

The central rule is that each card is an individual writing assignment. The
author completes one card's semantic decoding, unique editorial job, voices,
astrology densities, practical guidance, humor, filters, QA, ledger entry, and
checkpoint before beginning the next card. Processing a whole deck by field or
substituting projected terms into shared sentence frames is not acceptable
authoring.

Authoritative work belongs in a parseable working JSON file accompanied by a
checkpoint and editorial ledger. When execution tooling or a response window
ends, the author saves and validates those files, then resumes at the first
unfinished priority ID. Chat-only drafting is not a substitute for updating
the authoritative artifact.

The ledger records the decoded semantic brief, unique editorial job, voice
jobs, astrological sources, filter reasoning, humor premise, distinctive
imagery, and overlap warnings for every card. This makes semantic and
editorial decisions auditable rather than merely proving that fields are
nonempty.

---

## 38. Anti-template and voice acceptance standard

A reader-facing line fails when it could describe five unrelated claims after
changing only the dog's name or projected term. A new introductory clause does
not repair an unchanged sentence template; the paragraph must be rewritten as
a complete unit.

Handler, direct-to-dog, and hybrid are different editorial functions:

- handler helps a person recognize what may be happening for the dog;
- direct-to-dog gives the dog an affectionate, dignified second-person
  perspective;
- hybrid describes the reciprocal situation created by dog and person
  together.

Hybrid reciprocity does not require repeatedly writing "`<Dog>` brings X; you
bring Y." It may appear as a shared ritual, if/then interaction, complementary
roles, mutual adjustment, progression over several beats, or an invitation to
notice the dog's next choice. Across the deck, hybrid prose must vary naturally
and remain identifiable as relationship-centered even without its label.

No-astrology prose must decode internal vocabulary completely. Light astrology
must name and interpret one or two useful actual astrological sources. Full
astrology must explain the retained components and their relationship without
discussing claim selection, evidence packets, semantic models, graphs, or
authoring mechanics.

Practical guidance must describe what support looks like in the claim's actual
situation. Humor begins with a claim-specific comic premise and must not be
rotated from a global bank. Paperwork, protocols, fine print, departments,
snacks, treats, and squirrels may appear rarely when uniquely appropriate but
must not become production-line language.

Whole-deck acceptance includes repetition audits of openings, endings,
headline structures, advice, imagery, hybrid constructions, and humor
mechanisms. Structural validator success is necessary but does not establish
editorial quality.

---

## 39. Remaining future work

Additional future work includes deeper deterministic editorial linting,
card-ID migration rules, controlled vocabularies, application rendering
contracts, release packaging, and versioned example fixtures. These should
continue to evolve from observed production failures and successful decks
rather than speculative rules alone.

---

## 40. Whole-chart understanding before card authoring

The author must form an integrated understanding of the subject before writing
the first card. This is not merely the Summary-card step. A complete natal
portrait establishes the recurring motifs, tensions, counterweights,
behavioral sequences, relationship dynamics, strengths, growth edges, tone,
and uncertainties that make the deck belong to one individual dog.

The portrait is private authoring context and retains supporting claim IDs. It
may use the complete chart basis, including unselected claims. Ordinary cards
remain constrained to their own selected evidence: the portrait guides
interpretive emphasis and voice but does not authorize unsupported facts.

A whole-chart portrait must not become a phrase bank. Appending one
subject-specific refrain to many unrelated cards creates the appearance of
individuality while flattening the deck internally. Each card must express the
subject through the exact way its own claim participates in the larger
portrait.

---

## 41. Tool boundary and inspectable audit gates

Deterministic tools may read and preserve evidence, manipulate JSON, maintain
checkpoints, calculate repetition, lint language, and run structural
validation. They may not generate reader-facing prose through templates,
interpolation, phrase rotation, or claim-type renderers.

After every five cards, the author saves an editorial audit artifact containing
the deterministic linter report and a manual disposition of its warnings. The
single subject request continues automatically after corrections; no user
round trip is required. These gates make internal progress inspectable without
turning one dog into many separately billed authoring requests.

The final audit covers every reader-facing field, including Summary cards,
advice, and humor, and compares all subjects in a multi-subject request.
