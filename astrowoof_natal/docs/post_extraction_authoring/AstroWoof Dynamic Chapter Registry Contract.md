# AstroWoof Dynamic Chapter Registry Contract

> **Authority:** This is the implementation-level producer contract for SBE and
> Semantic Closure. The cross-system consumer summary is maintained in the
> [`astrowoof-project` authored natal deck contract](https://github.com/kevin2357/astrowoof-project/blob/main/docs/contracts/Authored%20Natal%20Deck%20Contract.md).
> Changes affecting API or frontend consumption must be reconciled with that
> project contract; detailed generation and validation behavior remains owned
> here.

## Scope

This document defines the implemented dynamic chapter contract for AstroWoof
projected natal-card artifacts using schema version
`astrowoof.projected_natal_cards.authoring_packet.v0.4`.

Dynamic chapters organize two editorially different sections:

- `interdogpendence` groups selected aspects by interacting drives, systems,
  tensions, and channels;
- `takeaways` groups selected syntheses by conclusions, recurring patterns,
  practical lessons, and developmental implications.

The sections are planned independently. They must not mirror one shared
taxonomy, and no exact or trivially reordered chapter title may occur in both.

## Top-level registry

New v0.4 artifacts contain:

```json
{
  "theme_group_registry": {
    "interdogpendence": [
      {
        "id": "spark_and_settle",
        "title": "Spark, Then Settle",
        "short_title": "Spark & Settle",
        "emoji": "⚡",
        "order": 1,
        "subtitle": "How surprise, momentum, and regulation negotiate a workable rhythm."
      }
    ],
    "takeaways": []
  }
}
```

Both section keys are required under the new contract. Each section contains
three to five entries and is ordered by the explicit integer `order` field.

## Registry entries

- `id` is a stable lower-snake-case identifier used by cards and anchors.
- `title` is the full chapter heading shown in the reading.
- `short_title` is the compact navigation label.
- `emoji` is a relevant visual marker and part of AstroWoof's friendly chrome
  language.
- `order` is a unique, consecutive positive integer within its section.
- `subtitle` is an optional final-artifact string. New authoring requires a
  nonempty value; legacy or migrated artifacts may omit it or use null/blank,
  in which case the UI renders no subtitle and no empty spacing.

Titles should be semantically useful before they are short. Navigation labels
should be the best concise rendering of the same chapter, not a different
taxonomy. Subtitles should orient the reader directly to the dog's pattern or
the chapter's practical territory rather than merely announcing that “these
cards” discuss a topic.

## Card references

Every selected aspect and synthesis carries one `theme_group_id` whose value is
registered in its own section. Placements, angles, Big Three cards, nodes, and
Part of Fortune do not gain this field.

The new contract does not also emit the legacy free-text `theme_group` field.
Consumers resolve the registry once per section and use `theme_group_id` for
group membership, stable identity, order, and navigation anchors.

## Group-count and balance rules

Each registered chapter must be used by at least two cards. Within each section,
the largest chapter may contain no more than twice as many cards as the smallest
chapter. Interdogpendence and Takeaways are assessed independently and may have
different chapter counts.

These bounds prevent singleton or grossly lopsided chapters while leaving the
author enough flexibility to choose the strongest semantic organization. They
are editorial/data-contract rules, not a substitute for responsive frontend
layout.

## Compatibility

The v0.4 extension is backward compatible:

- decks created before the registry contract may retain legacy card-level
  `theme_group` values and omit the top-level registry;
- a deck using the new registry must use `theme_group_id` consistently and may
  not retain legacy `theme_group` values on participating cards;
- `subtitle` remains optional in final validation so existing v0.4 decks do not
  require migration merely to remain readable;
- the frontend may retain a deterministic legacy fallback, but a section never
  mixes registry, legacy, and fallback sources.

Backward-compatible validation does not require every historical deck to be
rewritten. New SBE/semantic-closure output always uses the current registry.

## Editing authority

Ordinary polish treats the registry and card assignments as locked structural
metadata. Theme-regrouping edits are exposed only when validation explicitly
identifies a registry or balance defect. Existing subtitles become editable
only inside that same bounded theme-group repair authority.

## Explicit exclusions

This contract does not decide:

- Quick versus Complete WoofMap products;
- whether multiple products share or independently author chapter plans;
- qualitative critic defaults;
- frontend grid-selection policy; or
- automatic prose backfills for historical decks.
