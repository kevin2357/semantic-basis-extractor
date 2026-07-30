# LLM Editing Permissions and QA Checklist

## Purpose

This file defines the boundary between the deterministic Semantic Basis Extractor and the LLM editorial pass.

The selected authoring packet is authoritative for claim identity, selection, evidence, dependencies, and scores. The LLM is an editor and renderer, not a second selector.

## Locked fields

The LLM must preserve:

- card count and order;
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
- source and coverage metadata.

The LLM may update `generator.editorial_status` from `awaiting_llm` to `llm_completed`.

## Editable fields

The LLM may edit:

- `canonical_claim`, provided meaning does not change;
- all strings marked `__LLM_FILL__`;
- `dos`;
- `donts`.

## Required checks before return

- Exactly fifty cards.
- Same ordered claim-ID list as input.
- No locked-field changes.
- No `__LLM_FILL__` strings.
- Every density contains all three voices.
- Every voice contains a headline and body.
- Every density contains at least one funny quote, imperative quote, and canine joke.
- Every card contains at least two `dos` and two `donts`.
- Direct-to-dog copy consistently uses second person.
- Handler copy consistently discusses the dog for the handler.
- Hybrid copy discusses dog and handler together.
- No-astrology prose contains no astrological terminology.
- Full-astrology prose introduces no unselected evidence.
- Unknown gender, breed, pronouns, birth details, and biography are not invented.
- Syntheses use only their selected dependency claims.
- Guardrails are preserved.
- Output parses as JSON.

## Semantic review questions

For each card:

1. Does the prose still express the canonical claim?
2. Can every material statement be traced to its evidence or selected dependencies?
3. Does the joke express the claim rather than merely decorate it?
4. Do the practical suggestions follow from the claim?
5. Does the card duplicate another card’s semantic job?
6. Do the three densities remain interpretations of one proposition?
7. Are tensions presented as context-dependent patterns rather than defects?

## Prohibited shortcuts

- Do not delete difficult cards.
- Do not collapse the three voices into identical text.
- Do not copy light-astrology prose into no-astrology fields.
- Do not substitute generic dog jokes for missing interpretation.
- Do not silently repair selection by adding chart facts.
- Do not use outside information about the subject.
- Do not return a sample, outline, or partial deck as the finished artifact.
