# Post-Sprint — Dynamic Chapter Subtitle Contract

## Context

The AstroWoof frontend added v0.4 support for authoring-owned dynamic chapter
registries. Main chapter headers use `title`, compact navigation uses
`short_title`, `emoji` participates in the visual language, `order` controls
display, and registry `id` supplies stable identity and anchors.

Static AstroWoof chapters also display one short explanatory line beneath the
chapter title. Dynamic Interdogpendence and Takeaways chapters therefore gained
the optional registry field `subtitle`:

```json
{
  "id": "self_and_horizon",
  "title": "Selfhood Meets the Open Road",
  "short_title": "Self + Horizon",
  "emoji": "🧭",
  "subtitle": "How independence and adventure become part of belonging.",
  "order": 1
}
```

## Contract

The final v0.4 deck contract treats `subtitle` as optional. Missing, `null`,
empty, or whitespace-only values are valid and render no subtitle. A present
non-null value must be a string. This preserves Bre and all previously generated
v0.4 decks.

Newly generated authoring workspaces apply a stronger production rule: every
new registry entry must include a nonempty subtitle. The author is asked for one
concise, warm explanatory sentence that tells the reader what the grouped cards
help them understand. It should not merely repeat the chapter title or describe
the schema.

## Pipeline behavior

- SBE's pass-6 theme assignment explicitly requests `subtitle` alongside
  `id`, `title`, `short_title`, `emoji`, and `order`.
- Opaque pass acceptance rejects a newly authored registry that omits or blanks
  the field.
- Assembly accepts and preserves optional subtitles while remaining compatible
  with legacy registries.
- Final validation accepts absent/null/empty/whitespace subtitles and rejects
  non-string values.
- Theme-group sparse polish exposes existing subtitles only when theme-group
  editing is explicitly enabled.
- Fake-provider fixtures generate subtitles, keeping zero-token workflow tests
  representative of the current authoring surface.

## Verification

The full repository suite passes: 101 tests.

Coverage includes:

- new authored registries contain subtitles;
- missing subtitles are rejected by current pass-6 acceptance;
- subtitles survive six-workspace assembly;
- legacy absence remains valid in the final deck contract;
- `null`, empty, and whitespace-only values remain valid;
- non-string subtitle values fail validation; and
- ordinary theme-group validation, balance, independence, and registry-ID
  checks remain unchanged.

This is a backward-compatible v0.4 contract extension and does not require a
schema-version increment.

## Live Ella observation and follow-up

The first real pass-6 test produced useful, compact subtitles between 9 and 15
words long. The Interdogpendence set described Ella's patterns directly and
varied its sentence movement naturally. The Takeaways set was semantically
sound but all four subtitles used the same meta-editorial architecture:

- `These cards show ...`
- `These cards gather ...`
- `These cards illuminate ...`
- `These cards trace ...`

This is acceptable content, but it makes separately authored chapter
descriptions feel more templated than necessary. In the next bounded authoring-
guidance pass, prefer subtitles that speak directly about the dog's pattern,
the practical territory, or the reader's organizing question. Vary sentence
architecture across the registry and avoid using `These cards ...` as the
default opening for every chapter. This should remain positive craft guidance,
not a brittle prohibition against an otherwise natural phrase or a hard lexical
rejection rule.

The same live test confirmed that subtitle authoring did not destabilize the
rest of pass 6. Opaque QA rejected an initial one-card chapter, the creative
retry produced balanced independent registries, final validation passed, and
whole-deck lint was clean. No mechanical-polish call was required.
