# Slice 3 — Feasibility conclusion

## Classification

`assembled_deck_required`

Exact read-only OpenAI retrieval is practical for recent Responses and provides
the complete structured model outputs. It is not, by itself, an editorial audit:
initial outputs are authored-field maps, and polish outputs are sparse edits.
The retained source workspaces, selected authoring packet, baseline deck, and
lineage reports supply the meaning needed to evaluate those outputs.

Once those native inputs are available, the existing production functions can
replay the pipeline locally without provider access or runtime mutation. An
audit-specific script is useful for staging, provenance, comparisons, and human
reporting; it need not and should not define a separate assembler or QA policy.

## Frisbee result

The complete replay is exact:

1. Six downloaded initial outputs reproduce the retained authored maps.
2. Production assembly produces a structurally valid 50-card baseline with five
   combined lint/acceptance findings.
3. Polish 1 reproduces the retained 20-edit candidate, reduces the score from
   five to one, and is accepted.
4. Polish 2 reproduces the retained two-edit candidate. It lowers the remaining
   repeated-opening occurrence count from seven to six, but the finding count
   stays at one, so the candidate is rejected by the frozen improvement rule.
5. The replay-selected final deck equals the retained final deck.

This proves that Frisbee's editorial outcome was reproducible and that no
assembly or result-lineage corruption occurred. It also exposes a legitimate
future calibration question: should a measurable reduction inside one retained
finding count as improvement? This sprint does not change that policy.

## Recommended repeatable workflow

For a recent sampled run:

1. Build a closed response-ID manifest from authoritative traces/native action
   evidence.
2. Retrieve only those exact Responses and preserve their raw hashes privately.
3. Obtain the exact final checkpoint or a separately persisted neutral evaluated
   deck package.
4. Verify archive and member inventory identities before extraction.
5. Replay production extraction, assembly, validation, lint, and optional-stage
   edits in lineage order.
6. Publish a sanitized comparison receipt plus a human-readable warning/edit
   report; keep prompts and full generated content private.

Separately persisting the final evaluated deck—both accepted delivery and the
last terminal-review candidate—would remove the need to retrieve a full
checkpoint for most future editorial audits. Retaining the checkpoint remains
valuable when the question concerns assembly inputs or lineage integrity.
