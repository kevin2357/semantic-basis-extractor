# Multi-Subject LLM Handoff v0.4.3

This root contains one or more independent AstroWoof subject handoffs.

## Required workflow

1. Enumerate the immediate subject directories and read each `manifest.json`.
2. Process one complete subject before opening the next.
3. Within a subject, follow
   `static/LLM Card-by-Card Authoring Execution Protocol.md` exactly.
4. Read and apply
   `static/AstroWoof Independent Card Writing Brief.md`: author 50 independent
   miniature essays about the same dog, with consistent understanding and
   diverse expression.
5. Use only that subject's request files as its factual and semantic basis.
6. Never transfer chart facts, personality descriptions, prose, humor,
   imagery, filter assignments, theme labels, or summaries between subjects.
7. Produce the exact output filename declared by each subject manifest.
8. Run the root `validate_astrowoof_editorial.py` independently against each
   subject's original authoring packet with `--phase authoring`.
9. Correct every validation error before marking that subject complete.
10. Keep a separate working deck, checkpoint, and editorial ledger per subject.
11. If interrupted, resume the current subject at its first unfinished
    priority ID. Do not restart completed subjects or shorten later subjects.
12. Complete the subject's whole-chart authoring portrait before card 1.
13. Run and save the required editorial-linter audit after each five-card
    checkpoint without waiting for user approval.
14. Never use scripts or deterministic templates to generate reader-facing
    prose.

Continue automatically until every subject is complete.

## Required delivery

For each subject, deliver:

- `natal.<subject>.cards.json`;
- `<subject>.whole-chart-authoring-portrait.json`;
- `<subject>.authoring-ledger.json`;
- `<subject>.final-editorial-lint.json`;
- `<subject>.validation-report.json`.

Package all completed subject artifacts together only after every deck passes
its separate validation run.

The Bre gold reference is an editorial standard, not a source of reusable
facts or phrases. Every subject must receive an independently authored deck.
