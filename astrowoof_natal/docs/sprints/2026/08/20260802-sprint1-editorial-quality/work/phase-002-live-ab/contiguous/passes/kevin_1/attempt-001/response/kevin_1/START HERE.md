# Start Here — Pass 1 of 6

## Assignment

This pass contains exactly Stories 001 through 010. Complete those 10 story directories in numeric order. The assignment is complete when their writing files and the whole-dog profile contain no unfinished fields.

## Read first

Read `GUIDING LIGHTS.md` as the creative doctrine for this pass. Its independent-card standard is part of the assignment, not optional inspiration.

## Working sequence

Begin by reading `AUTHORING BRIEF.md` and `DOG DETAILS.md`. Read `FULL CHART BASIS.md` in full and complete `WRITE WHOLE DOG PROFILE.md`. Then author each supplied story as a fresh miniature essay while retaining a coherent understanding of Kevin.

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

## If the gate rejects the pass

Treat a rejection as an editorial signal, not as a puzzle about the checker. The most reliable response is to return to the affected cards' plans, recover what makes each insight memorable, and rewrite the prose in a natural voice with genuinely distinct movement and character. Surface-level interventions—filler, recurring catchphrases, bracketed insertions, or cosmetic paraphrase—do not create editorial independence. Writing that sincerely follows `GUIDING LIGHTS.md` is the best route to a successful pass.

Preserve every field marker and replace every unfinished field. Return this complete pass directory as a ZIP archive.
