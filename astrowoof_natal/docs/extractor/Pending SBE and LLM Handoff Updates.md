# Pending SBE and LLM Handoff Updates

> **Status: historical/superseded checklist.** The extractor work below was
> completed in the v0.3 update. Later authoring work replaced the shared
> free-text `theme_group` design with the v0.4 section-scoped
> `theme_group_registry` and card `theme_group_id` contract. Do not use this
> file as current implementation guidance.
>
> Current authorities are:
>
> - [`Semantic Basis Extractor Pipeline and Scoring Metrics.md`](Semantic%20Basis%20Extractor%20Pipeline%20and%20Scoring%20Metrics.md)
>   for extraction, selection, and packet construction;
> - [`../post_extraction_authoring/AstroWoof Dynamic Chapter Registry Contract.md`](../post_extraction_authoring/AstroWoof%20Dynamic%20Chapter%20Registry%20Contract.md)
>   for aspect/synthesis chapter organization;
> - [`../post_extraction_authoring/Runtime Contracts.md`](../post_extraction_authoring/Runtime%20Contracts.md)
>   for the released input, state, provenance, and delivery boundary; and
> - [`../post_extraction_authoring/Semantic Closure Runner.md`](../post_extraction_authoring/Semantic%20Closure%20Runner.md)
>   for current authoring orchestration and QA behavior.

This document records the schema and workflow changes requested during the
earlier AstroWoof card-artifact restructuring. It is retained as implementation
history and as evidence for the acceptance criteria that led to v0.3.

## Semantic Basis Extractor update pass

**Implementation status:** Completed in the v0.3 extractor update. Retained
below as the governing acceptance checklist.

Update the SBE-generated card artifact and its validator/schema expectations as follows:

- Hoist `funny_dog_quotes`, `imperative_dog_quotes`, and `applicable_canine_jokes` to the claim’s `card` level. They should be siblings of `no_astro`, `light_astro`, and `full_astro`, not repeated inside every astrology-density object.
- Replace the singular claim field `category: string` with `categories: string[]`.
- Emit a one-element `categories` array for claims that currently have one category.
- Assign Sun and Moon placement claims to `["big3_core_traits"]` instead of `["core_traits"]`.
- Assign the Ascendant placement claim to both its existing angle category and the Big Three category: `["angles", "big3_core_traits"]`.
- Add `big3_core_traits` to the artifact’s top-level category registry.
- Add a `theme_group: string` field beside `categories` on every selected
  aspect and selected synthesized claim. Emit `__LLM_FILL__` in the authoring
  packet; selected placement claims do not receive this field.
- Update schemas, examples, prompt contracts, locked-field lists, and validation rules to use `categories`.
- Validate that all claim categories exist in the top-level category registry.
- Validate that `categories` is a nonempty array of unique strings.
- Validate that the three card-level humor arrays exist and that obsolete density-level humor fields are absent.
- Preserve the complete top-level `projected_term_registry`.
- Preserve any unselected claims in an `unselected_claims` field parallel to `claims`; this must include at a minimum any unselected primitive or aspect, but should also include if possible any unselected synthetic claims, including stronger versions of syntheses that were selected that have additional support from unselected aspects
- Assume the per-subject input can consist of multiple files which need to be merged
- Assume that an input package could contain projected graphs for several subjects
- Output a `summary` key for the authoring LLM to fill in; example provided

## LLM handoff update pass

Update the LLM authoring packet, handoff prompt, examples, ledger/checkpoint instructions, and editorial validator as follows:

- Provide the allowed top-level `context_filter_groups` vocabulary to the editor.
- Require the editor to assign relevant filters to every claim at:
  - `context_filter_groups.high_level`
  - `context_filter_groups.detail_level`
- Require the editor to assign a flexible chapter category in `theme_group` for
  every selected aspect and selected synthesized claim. Theme groups are
  editorial chapter labels rather than structural categories: the LLM may
  create subject-appropriate labels that group related aspects and syntheses
  into a coherent reading sequence.
- Leave `theme_group` empty in the SBE authoring packet for the LLM to fill,
  require a nonempty string after authoring, and do not require `theme_group`
  on selected placement claims.
- Require assignments to use only names registered for the matching level.
- Permit multiple relevant assignments, but discourage indiscriminate assignment to most or all filters.
- Instruct the editor to treat filters as reader-navigation facets, not as
  restatements of the claim’s structural `categories`: assign a filter only
  when a user choosing that filter would reasonably expect the claim, not for
  a tangential connection.
- Require the editor to author all four top-level `summary` cards.
- Explain that each summary card has the same editorial structure as a normal claim’s `card` object:
  - card-level humor arrays;
  - `no_astro`, `light_astro`, and `full_astro`;
  - handler, direct-to-dog, and hybrid headlines and bodies.
- Define the four summary cards as Who She Is, How She Lives, What She Needs,
  and How She Grows, using the subject's actual pronouns.
- Author summaries from the complete chart basis, including unselected claims;
  summaries are the only prose surface authorized to use unselected material.
- Update handoff examples and gold examples to show humor only once at card level.
- Lock populated context-filter assignments, theme groups, and summary content
  during later polish passes unless the requested task explicitly includes
  them.
- Validate that no summary field remains blank after the LLM authoring pass.
- Validate that all four summary cards follow the normal voice, density, humor, and placeholder rules.

## Current filter vocabulary

### High level

- Personality
- Learning
- Play
- Adventure
- Communication
- Trust
- Training
- Pack

### Detail level

- Core Personality
- Mind & Intelligence
- Emotions & Inner World
- Energy & Motivation
- Strengths & Talents
- Growth & Potential
- Play & Adventure
- Learning & Training
- Communication
- Social & Pack Life
- Trust & Security
- Stress & Resilience
