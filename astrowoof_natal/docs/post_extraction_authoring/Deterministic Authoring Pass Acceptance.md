# Deterministic Authoring Pass Acceptance

The six-pass AstroWoof authoring workflow may submit each returned pass to a
deterministic acceptance check before combining it with the other passes. This
check identifies obvious schema-completion and prose-template failures without
asking another language model to judge the writing.

Run the check against an extracted authored pass directory:

```text
python src/lint_authoring_pass.py path/to/kevin_1
```

Use `--output report.json` to save the complete machine-readable report. Exit
code `0` means `accept`; exit code `2` means `reject`.

The checker rejects a pass when reader-facing text is copied exactly between
distinct cards or summaries. It also rejects a pass when the same twelve-word
passage appears in three or more distinct cards or summaries. Headlines,
bodies, dos, don'ts, and humor are included in exact-duplicate checks.

All density and audience renderings belonging to one card are treated as one
location. Their expected semantic overlap therefore cannot reject the pass.
Only reuse across different claims or summaries counts.

The verdict is deterministic: the same files and checker version always
produce the same result. An accepted pass has cleared a minimum independence
threshold; it has not received a full literary or semantic endorsement.
Naturalness, insight, evidence fidelity, and genuinely distinct narrative
angles still benefit from final editorial review.

Recommended orchestration:

1. Submit one ten-card pass or the four-summary pass.
2. Extract the returned workspace.
3. Run `lint_authoring_pass.py`.
4. Keep an accepted pass.
5. Resubmit a rejected pass in a fresh authoring session.
6. Assemble the six accepted passes.
7. Run the normal full-deck linter, validator, and global editorial review.

The standard JSON deck linter also includes the same verdict under
`authoring_pass_acceptance`, allowing the final assembled deck to be checked
with identical rules.
