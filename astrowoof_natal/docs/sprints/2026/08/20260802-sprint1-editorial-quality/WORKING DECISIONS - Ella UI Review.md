# Working Decisions — Ella UI Review

**Status:** Historical decision inventory; promoted project decisions now live in `astrowoof-project`
**Started:** 2026-08-03  
**Source:** Ella long-summary/short-summary UI comparison and follow-up design review  
**Purpose:** Preserve every decision, principle, candidate direction, rejected
assumption, and open question that may affect future editorial, data, pipeline,
validation, or interface work.

> This document remains the detailed evidence and decision-recovery record for
> the Ella UI review. It is no longer the project-wide living authority.
> Promoted product principles, UX findings, dynamic-chapter decisions, and open
> questions are maintained in
> [`astrowoof-project`](https://github.com/kevin2357/astrowoof-project).
> SBE-specific implemented decisions remain authoritative in their dedicated
> component contracts and tests.

This document was intentionally broader than the sprint plan and captured the
complete state of agreement at the time. It now serves as historical evidence
so that the reasoning behind promoted decisions does not require reconstructing
conversation history.

## Status vocabulary

- **MUST:** hard product, semantic, or editorial contract.
- **SHOULD:** strong default; departure requires a concrete reason.
- **MAY:** supported option, not an expectation.
- **CANDIDATE:** promising direction not yet adopted for implementation.
- **OPEN:** unresolved and requiring design, evidence, or testing.
- **REJECTED:** considered assumption that should not guide future work.

## Evidence from the Ella UI review

- The Reading Companion materially changes the Complete WoofMap from a long
  linear report into a navigable reference experience.
- Ella's longer summaries generally had stronger standalone literary synthesis.
- Ella's shorter summaries generally produced a stronger Summary-section user
  experience and more immediate card theses.
- Both decks rendered without clipping, overlap, or an unusable card layout.
- The shorter-summary deck remained slightly taller overall because its five
  uneven theme groups introduced an additional chapter header and more partially
  occupied grid rows.
- Total page height therefore depends on chapter distribution and grid packing,
  not only prose length.
- The five-group deck appeared more subject-specific and semantically expressive
  even though it was marginally less space-efficient.
- An observed reading behavior emerged naturally: begin with None to understand
  an insight, open Light to learn the principal astrological basis, open Full to
  inspect complete support, then return to None for continued browsing.

## Accepted reading-model principles

### Canonical interpretation

- **MUST:** One dog has one coherent canonical interpretation.
- **MUST:** Variation in prose, audience, density, scope, or author does not
  create a different underlying dog.
- **MUST:** Every delivered view preserve subject identity, chart provenance,
  and the central meaning of retained claims.
- **SHOULD:** Creative variation should diversify expression while preserving
  characterization.

### Cards and navigability

- **MUST:** Cards are self-contained reading units, not arbitrary fragments of
  one continuous essay.
- **SHOULD:** Individual-card tractability, section distinction, and navigation
  matter more than raw full-page height.
- **SHOULD:** The Complete WoofMap should support selective browsing and return
  visits rather than assume one linear sitting.
- **MUST:** Semantic organization is authoritative over minor grid-packing or
  total-height efficiency.
- **SHOULD:** Presentation should accommodate meaningful uneven group sizes
  rather than force the semantic layer to manufacture visually convenient
  groupings.

### Independent reading dimensions

The following dimensions answer different user questions and must not be
collapsed conceptually:

- **Reading scope:** how much of the dog's portrait to consume.
- **Astrology density:** how much reasoning behind an insight to expose.
- **Audience:** which relationship and rhetorical purpose frames the prose.
- **Handler notes:** whether supporting practical guidance is visible.

### Audience and handler notes

- **MUST:** Handler, Direct-to-Dog, and Hybrid remain semantically consistent but
  rhetorically distinct.
- **MUST:** Audience is independent from astrology density.
- **MUST:** Handler notes are supporting guidance, not part of audience identity.
- **SHOULD:** Direct-to-Dog mode collapse handler notes by default while keeping
  them readily available locally and globally.

## Astrology-density ladder

- **MUST:** None, Light, and Full express the same central insight.
- **MUST:** Density changes explanatory depth, not the truth or subject of the
  card.
- **SHOULD:** None establish the behavioral or practical insight in ordinary
  language.
- **SHOULD:** Light retain that insight and reveal its principal astrological
  basis.
- **SHOULD:** Full retain that insight and expose the complete relevant chart
  support and interpretive interaction.
- **SHOULD:** Moving None → Light → Full feel like progressive disclosure of one
  card rather than three independent mini-essays.
- **MUST:** The rule that different claims are independent writing assignments
  must not be misapplied to density variants within one claim.

## Summary-section principles

- **MUST:** Summary remains a coordinated four-card, four-lens orientation to the
  dog as a whole.
- **MUST:** Only Summary may use the full selected and unselected chart basis as
  its direct authoring basis.
- **SHOULD:** Summary provide memorable retrieval handles before the detailed
  reading begins.
- **SHOULD:** Each summary card have one clear central thesis plus enough contrast
  or qualification to avoid flattening the dog into a slogan.
- **SHOULD:** Summary quality include synthesis, memorability, UI tractability,
  and fitness for its opening role—not standalone literary quality alone.
- **SHOULD:** Complete-reading summaries still behave like summaries even if a
  future Quick reading exists.
- **MUST NOT:** Universal hard word limits be inferred from the Ella comparison.
  Length targets remain soft and scope-, audience-, density-, and viewport-aware.

## Stable major-section model

- **Summary:** four full-chart overview lenses.
- **Big 3:** Sun, Moon, and Ascendant.
- **Core Dog:** planetary placements.
- **Finding Her Footing:** angles.
- **Training & Growth:** North Node and Part of Fortune.
- **Interdogpendence:** aspects and their interacting chart forces.
- **Takeaways:** synthetic claims and higher-order conclusions.

## Interdogpendence and Takeaways chapter contract

### Foundational distinction

- **MUST:** Interdogpendence and Takeaways receive independently planned chapter
  systems.
- **MUST:** Interdogpendence chapters organize relationships among chart
  influences, including reinforcement, tension, friction, regulation,
  amplification, and exchange.
- **MUST:** Takeaways chapters organize integrated conclusions about the dog,
  including recurring character patterns, lived behavioral themes, practical
  insights, and developmental meaning.
- **MUST:** No chapter title appear in both sections.
- **MUST:** The collective chapter systems feel like fundamentally different
  organizational approaches.
- **MUST NOT:** The plans be synonymous, lightly reworded, token-reordered, or
  structurally mirrored versions of one another.
- **MAY:** Both sections discuss the same underlying behavioral domain when the
  section-appropriate explanatory framing remains distinct.

### Chapter count and size

- **MUST:** In the current Complete WoofMap, each dynamic section use between
  three and five chapters.
- **SHOULD:** The chosen count reflect the number and semantic diversity of that
  section's claims rather than a fixed count used for every dog.
- **MUST:** Every dynamic chapter contain at least two claims.
- **SHOULD:** Groups be reasonably balanced when semantic coherence permits.
- **MUST NOT:** Exact numerical equality or small size differences override a
  tighter, clearer semantic organization.
- **MUST NOT:** Grid row completion be used as a hard authoring constraint.
- **MUST:** Deterministic QA reject a chapter plan when its largest group contains
  more than twice as many claims as its smallest group. This deliberately broad
  boundary permits ordinary unevenness such as 5/5/6/8/9 while rejecting
  visibly and editorially suspect distributions such as 2/2/2/10.
- **MUST:** A claim may not form a singleton dynamic chapter. If it remains in
  the section, it must be assigned to a semantically defensible chapter with at
  least one other claim.
- **OPEN:** A future Quick WoofMap with too few retained aspects or syntheses for
  this contract will need a scope-specific chapter rule or may omit the
  corresponding dynamic section.

### Cross-plan QA

- **MUST:** Deterministic QA reject exact cross-section title duplication after
  normalization for case, punctuation, whitespace, and equivalent separators.
- **SHOULD:** Deterministic QA catch obvious token-reordered duplicates where it
  can do so reliably.
- **MUST:** LLM planning guidance explicitly audit whether the two complete
  chapter systems represent foundationally different organizations.
- **MUST NOT:** A weak deterministic similarity check be treated as proof of
  semantic distinctness.
- **OPEN:** Whether cross-plan semantic review remains part of the pass-6
  authoring call or later gains a separate critic step.

## Chapter-title visual language

- **MUST:** Dynamic chapter titles participate in AstroWoof's established visual
  language: warm, trustworthy reading content presented inside cute, colorful,
  lightly playful application chrome.
- **MUST:** Every dynamic chapter receive a relevant emoji or small visual marker
  suitable for section headers and navigation.
- **SHOULD:** The emoji be meaningfully related to the chapter rather than chosen
  arbitrarily.
- **SHOULD:** Distinct chapters within a section use distinct markers when a
  suitable choice exists.
- **MAY:** Sparkles or similarly atmospheric symbols represent dreamy,
  nebulous, or otherwise difficult-to-literalize themes.
- **SHOULD:** Chapter titles use the shortest wording that preserves the actual
  organizing idea.
- **MUST NOT:** Semantic usefulness be sacrificed merely to avoid a natural line
  wrap.

## Candidate reading-scope architecture

**Status: CANDIDATE — strong direction, not yet an implementation commitment.**

- One WoofMap may expose a Quick WoofMap and a Complete WoofMap.
- Complete would establish the canonical authored portrait.
- Quick would be derived from Complete rather than independently interpreted.
- Every retained Quick card would preserve its Complete claim identity.
- Quick prose would preserve the Complete card's central meaning while reducing
  detail, imagery, and secondary qualifications.
- Quick would contain no independently invented claims or conclusions.
- Quick would reduce both claim coverage and prose depth.
- Omitted claims and derivation provenance would be inspectable.
- “Quick” and “Complete” are preferred scope names because “Full” is already an
  astrology-density term.
- Quick should preserve sufficient integrated and practical material to remain
  an AstroWoof reading rather than become a placement inventory.

### Open Quick/Complete decisions

- Whether Quick becomes a shipped product feature.
- Exact Quick card count and selection policy.
- Which personal placements, angles, points, and aspects remain mandatory.
- Whether Quick retains zero, one, or several synthesis claims.
- Scope-specific summary and ordinary-card length guidance.
- Semantic-equivalence and contradiction QA.
- Scope/version/provenance metadata.
- Whether Quick is generated during initial closure or asynchronously afterward.

## Candidate card-local astrology interaction

**Status: CANDIDATE — UI direction requiring testing.**

- The global density control should continue to establish a reading-wide default.
- A card-local “Show the astrology” / “Go deeper” interaction may allow temporary
  None → Light → Full exploration without changing the global default.
- This may be especially valuable on mobile.
- The card should remain spatially anchored while its reasoning expands.
- Aggregate, privacy-respecting interaction data could test whether progressive
  disclosure is a common behavior.

### Open interaction decisions

- Exact desktop and mobile controls.
- Whether local depth resets on navigation.
- Whether users can pin a local override.
- Whether experienced astrologers exhibit the reverse Full-first pattern.
- Whether Quick encourages later entry into Complete.

## Accepted dynamic-chapter data direction

- **MUST:** The artifact provide section-scoped theme-group registries for
  Interdogpendence and Takeaways rather than treating one title string as a
  global cross-section taxonomy.
- **MUST:** Every registry entry have a stable section-scoped ID, full editorial
  title, best abbreviated navigation label, emoji or visual marker, and explicit
  display order.
- **MUST:** Dynamic cards reference the stable registry identity owned by their
  section.
- **MUST:** Emoji remain separate data rather than being embedded in the semantic
  ID or title string.
- **MUST:** The frontend be free to select the full title or abbreviated label
  according to available space while preserving one chapter identity.
- **SHOULD:** Existing decks be migrated or adapted explicitly rather than relying
  on accidental interpretation of legacy shared `theme_group` strings.

### Registry shape to finalize during implementation

The expected direction is structurally equivalent to:

```json
{
  "theme_group_registry": {
    "interdogpendence": [
      {
        "id": "signals_and_learning",
        "title": "Signals, Learning, and Adaptable Intelligence",
        "short_title": "Signals & Learning",
        "emoji": "🧠",
        "order": 1
      }
    ],
    "takeaways": []
  }
}
```

The exact key names, schema version, and backward-compatible card-reference
shape remain implementation details, not open questions about the architecture.

## Resolved data-model questions

- **IMPLEMENTED:** Existing decks remain valid under the legacy card-level
  `theme_group` contract. New v0.4 decks use a top-level
  `theme_group_registry`; migration is not required merely for continued
  rendering or validation.
- **IMPLEMENTED:** Registry entries use `id`, `title`, `short_title`, `emoji`,
  `order`, and optional `subtitle`. Participating aspect and synthesis cards use
  `theme_group_id`.
- **IMPLEMENTED:** New-registry cards do not retain a derived legacy
  `theme_group`. Frontend legacy fallback remains a consumer compatibility path
  and is never mixed with registry resolution inside one section.

The durable implemented contract is documented in
`docs/post_extraction_authoring/AstroWoof Dynamic Chapter Registry Contract.md`.

## Rejected or superseded assumptions

- **REJECTED:** One universal summary length can satisfy every reading scope and
  user appetite.
- **REJECTED:** Five theme groups are inherently excessive.
- **REJECTED:** Theme groups should be forced into equal sizes for visual
  neatness.
- **REJECTED:** Chapter balance should override semantic organization.
- **REJECTED:** Ella's shorter-summary page height was a capture artifact.
- **REJECTED:** Interdogpendence and Takeaways should share one taxonomy.
- **REJECTED:** Exact string uniqueness alone proves two taxonomies are distinct.
- **REJECTED:** Passing deterministic QA proves the underlying product rule is
  correct.
- **REJECTED:** None, Light, and Full should be treated as unrelated writing
  assignments.
- **REJECTED:** The existence of a future Quick reading permits Complete summaries
  to stop functioning as summaries.

## Immediate current-sprint implications

- Add density-ladder semantic coherence to authoring guidance and tests.
- Split pass-6 aspect and synthesis chapter planning.
- Prohibit exact and conceptual cross-section chapter-plan duplication.
- Replace the synchronized global three-or-four/balance rule with independently
  validated three-to-five chapter plans, two claims minimum per chapter, and
  semantic coherence as the governing principle.
- Decide the minimum schema change needed for independent plans before coding.
- Include relevant emoji/visual-marker authoring in the dynamic chapter contract.
- Preserve concise summary discipline without introducing universal hard word
  limits.
- Live-test a fresh pass 6 and inspect both navigation and section rendering.
- Keep Quick/Complete generation and card-local density UI outside this sprint;
  preserve them as candidate architectures with explicit open questions.

## Documentation follow-through

After this working inventory is reviewed:

1. Preserve the Ella comparison as an immutable evidence/results report.
2. Promote accepted cross-sprint principles into a durable AstroWoof reading
   model and editorial-principles document.
3. Add stable decision IDs and statuses to an editorial decision register.
4. Move unresolved candidates into a structured research/experiments tracker.
5. Update the sprint plan with only the immediate implementation work.
6. Update implementation manuals, schemas, handoff packets, and validator docs
   only as their corresponding behavior is implemented.
