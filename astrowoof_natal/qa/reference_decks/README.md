# AstroWoof Full-Deck Reference Corpus

This directory is the repository-owned corpus of AstroWoof natal deck artifacts
used for editorial comparison, regression analysis, QA research, and pipeline
evaluation. It includes completed modern decks plus explicitly labeled legacy
or intermediate artifacts whose missing modern fields are historically useful.

## Layout

```text
reference_decks/
  <subject>/
    params.json
    selected-authoring-packet.json
    README.md
    <dated-version>/
      natal.<subject>.cards.json
      README.md
```

The corpus preserves distinct historical outputs, including unsuccessful or
superseded editorial attempts when they provide useful evidence about a
pipeline stage. A file's presence here does not mean it is approved production
content. Read its version README before treating it as a positive reference.

## Subjects and versions

| Subject | Versions | Preferred current reference |
| --- | ---: | --- |
| Ashley | 4 | `20260730-six-pass-manual-assembly` |
| Brandi | 4 | `20260730-six-pass-manual-assembly` |
| Bre | 14 | `20260727-gold-standard` |
| Kevin | 10 | Research-dependent: manual final or automated live candidates |
| Ella | 4 | `20260801-batch-optimized-final` |

## Corpus policy

- Preserve distinct deck hashes; do not store duplicate copies merely because
  they appeared in several downloads or deployment bundles.
- Do not include selected authoring packets, unfinished checkpoint decks, or
  fake-provider fixtures as completed reference decks.
- Keep source files immutable once admitted. Create a new dated version for a
  revision.
- Store subject identity and birth metadata once in the subject `params.json`.
- Store one current selected authoring packet per subject for convenient
  validator and evidence-grounding work. It is a QA companion and is not
  necessarily the exact source packet for every historical version.
- Record generation conditions and known caveats in each version README.
- Large run logs and provider responses remain in external run directories;
  reference them from sprint results when needed.

## Provenance note

Descriptions were reconstructed from the development conversation, filenames,
artifact locations, timestamps, and known pipeline milestones. Where an exact
prompt revision was not recoverable, the README labels the context as inferred
rather than asserting unsupported precision.

Ten early Bre artifacts predate summary cards; the oldest legacy website sample
contains 26 cards. They remain deliberately because they document the evolution
of the deck format and editorial process. Modern-shape regression fixtures
should select versions with 50 cards and four summaries.
