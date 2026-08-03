# Start Here — Pass 6 of 6

## Assignment

This is the summary pass. Complete the four supplied Summary directories through their distinct lenses: who the dog is, how the dog lives, what the dog needs, and how the dog grows. Give each summary its own central argument, examples, advice, and language. Also complete `ASSIGN THEME GROUPS.md`, which creates one coherent chapter plan for every aspect and synthesis story.

## Read first

Read `GUIDING LIGHTS.md` as the creative doctrine for this pass. Its independent-card standard is part of the assignment, not optional inspiration.

## Working sequence

Begin by reading `AUTHORING BRIEF.md` and `DOG DETAILS.md`. Read `FULL CHART BASIS.md` in full and complete `WRITE WHOLE DOG PROFILE.md`. Then write all four summaries from the complete chart understanding of Brandi.

## Mechanical acceptance requirements

Your completed pass will be checked automatically before it is accepted.

- No reader-facing field may be copied exactly between cards.
- Reused language, recurring prose frames, metric-gaming artifacts, and cosmetic word insertion do not satisfy editorial independence.

These are rejection boundaries, not the creative quality standard. An `accept` verdict proves that detectable copying was avoided; it does not prove that the prose is insightful, natural, memorable, or sufficiently varied. Use `GUIDING LIGHTS.md` as the higher standard.

## Required pre-delivery check

After completing every field, run:

```text
python lint_authoring_pass.py . --output authoring-pass-acceptance.json
```

A report status of `reject` means the pass is not complete. Rewrite the identified cross-card reuse and run the checker again until its status is `accept`. Include `authoring-pass-acceptance.json` in the returned ZIP.

Preserve every field marker and replace every unfinished field. Return this complete pass directory as a ZIP archive.
