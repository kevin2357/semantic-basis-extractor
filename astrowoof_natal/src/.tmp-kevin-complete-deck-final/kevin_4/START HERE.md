# Start Here — Pass 4 of 6

## Assignment

This pass contains exactly Stories 031 through 040. Complete those 10 story directories in numeric order. The assignment is complete when their writing files and the whole-dog profile contain no unfinished fields.

## Read first

Read `GUIDING LIGHTS.md` as the creative doctrine for this pass. Its independent-card standard is part of the assignment, not optional inspiration.

## Working sequence

Begin by reading `AUTHORING BRIEF.md` and `DOG DETAILS.md`. Read `FULL CHART BASIS.md` in full and complete `WRITE WHOLE DOG PROFILE.md`. Then author each supplied story as a fresh miniature essay while retaining a coherent understanding of Kevin.

## Mechanical acceptance requirements

Your completed pass will be checked automatically before it is accepted.

- Do not use a recurring sentence, sentence fragment, transition, conclusion, headline pattern, or explanatory frame across cards.
- Every headline must be written specifically for its card. Density and audience labels are not headline templates.
- Do not give every handler story the same progression, every direct-to-dog story the same reassurance, or every hybrid story the same dog-and-human exchange.
- Do not append stock interpretive sentences such as “this pattern can express itself in more than one way,” “the practical task is,” or “repetition turns the next step into trust.”
- No reader-facing field may be copied exactly between cards.
- A sequence of twelve words appearing in three different cards automatically rejects the entire pass.

Consistency belongs in the characterization of the dog, not in the architecture of the prose.

## Required pre-delivery check

After completing every field, run:

```text
python lint_authoring_pass.py . --output authoring-pass-acceptance.json
```

A report status of `reject` means the pass is not complete. Rewrite the identified cross-card reuse and run the checker again until its status is `accept`. Include `authoring-pass-acceptance.json` in the returned ZIP.

Preserve every field marker and replace every unfinished field. Return this complete pass directory as a ZIP archive.
