# Slice 2 — Existing replay surface

## Answer

The production assembly and editorial checks can be replayed without changing
SBE runtime code. They cannot be replayed exactly from OpenAI response objects
alone. Audit-specific scripts are welcome for extracting, staging, orchestrating,
diffing, and reporting the replay; they should use the production functions as
the authoritative semantics rather than inventing an alternate assembler or QA
decision rule.

## Initial assembly

Each initial Response contains a structured authored-field map. The released
provider path normally:

1. extracts that map with `response_output_text()`;
2. applies it to the pass's source workspace with `apply_authored_fields()`;
3. verifies the authored workspace is complete; and
4. persists that reconstructed response workspace.

After all six passes are accepted, `assemble_subject()` copies their accepted
workspaces, loads the subject-specific selected authoring packet, and invokes
`assembly.assemble(..., allow_partial=False)`. The resulting deck is passed to
the existing validation and editorial-lint commands.

The provider Responses supply the authored maps, but not the source workspaces or
selected packet. Those exact native inputs are necessary because the maps modify
template fields; they are not standalone complete decks.

## Polish replay

The released polish path is deterministic after provider output exists. It:

1. loads the current best assembled deck and its validation/lint reports;
2. computes the exact editable target paths;
3. applies the returned sparse edit list with `apply_sparse_polish()`;
4. runs polish-phase structural validation and editorial lint; and
5. accepts a candidate only if it improves the frozen comparison metrics.

The raw polish Responses reveal the proposed edits, but exact replay also needs
the baseline deck, reports, and derived target inventory. Polish attempt 2 must
be evaluated against the accepted output of attempt 1—not against the original
six-pass baseline.

## Practical next step

A single bounded read of Frisbee's final retained checkpoint should contain the
selected packet, source/accepted pass workspaces, assembled baseline, polish
candidates, and reports. With those files, the audit can:

- independently reassemble the initial six responses;
- prove what polish attempt 1 changed and why it was accepted;
- prove what polish attempt 2 changed and why it was rejected; and
- compare reconstructed artifacts with the retained native versions.

This would be workspace access for evidence only. It requires no provider call,
resume, reconciliation, mutation, recovery, or new SBE implementation.

An audit script may turn the result into more useful human-facing artifacts such
as a six-pass contribution map, baseline-to-polish diffs, warning changes, and a
compact editorial review packet. Those are derived analysis products; the
production assembly, validation, and lint outputs remain the decision evidence.
