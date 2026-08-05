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
