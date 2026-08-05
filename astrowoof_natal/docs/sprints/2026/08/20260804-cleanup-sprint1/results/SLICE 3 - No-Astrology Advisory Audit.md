# Slice 3 — No-Astrology Advisory Audit

## Purpose

Measure the no-astrology validator advisory against preserved decks, separate
ordinary English from genuine astrology leakage, and narrow only triggers whose
false positives are demonstrated by the corpus.

## Baseline inventory

The original detector produced 106 field warnings across 16 preserved decks.
Only six tokens caused every warning:

| Token | Fields |
| --- | ---: |
| `chart` | 44 |
| `house` | 40 |
| `doghouse` | 10 |
| `square` | 9 |
| `Jupiter` | 3 |
| `Saturn` | 3 |

Counts overlap when one field contains multiple tokens.

`doghouse`, planet names, and explicit aspect vocabulary were genuine leakage.
The other three tokens mixed distinct meanings.

## Classification

### Demonstrated false positives

- `house` meaning the physical home: “The house becomes quiet again.”
- `square` meaning an area or map position: “the same soft square of room” and
  “the first square on a little map.”
- `chart` inside an ordinary compound: “The Sofa Has a Seating Chart.”

These phrases satisfy the no-astrology product contract and should not consume
review attention.

### Demonstrated true positives

- numbered or ordinal astrological houses: `House 7`, `seventh house`;
- projected `Doghouse` references;
- possessed or definite chart references: `your chart`, `Ella's chart`, `the
  chart`;
- an aspect treated as an entity: `the square`, `the square's friction`;
- explicit planet and aspect names such as `Jupiter–Saturn`.

### Unchanged ambiguous vocabulary

The audit did not justify broad changes to words such as `Sun`, `Moon`, or
`node`. They remain advisory triggers. Future corpus evidence may support
contextual treatment, but this slice does not predict unobserved false-positive
rates.

## Implemented refinement

Bare `house`, `square`, and `chart` were replaced with contextual patterns:

- houses warn when numbered, ordinal, or expressed as `Doghouse`;
- square warns for `the/this/that square`, possessive square-friction phrasing,
  or `square aspect`;
- chart warns when possessed by the subject/reader or introduced as `the chart`.

All unambiguous existing terms remain unchanged.

## Result

The same corpus now produces 56 advisories across seven decks, removing 50
demonstrated false positives. Manual review of the remaining inventory found
genuine astrology references in every retained field. The final sprint Ella
deck drops from eight advisories to one: `The square's friction finds a track.`

This improves signal without converting advisories into automatic polish
targets. The warning remains nonblocking and conservative.
