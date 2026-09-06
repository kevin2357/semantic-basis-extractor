# Plan

Status: Slices 0–1 and Voof-paws 1 complete; Slice 2 production replay in
progress. No editorial-policy or runtime change is approved before Voof-paws 3.

## Goal

Calibrate AstroWoof's lint, whole-deck acceptance, polish-candidate adoption, and
terminal-review rules against a representative initial cohort. Produce a
near-term implementation recommendation grounded in exact production evidence
and independent editorial judgment rather than the first plausible threshold
change.

## Frozen principles

- A lint finding is an observation, not automatically a rejection.
- Whole-deck acceptance, polish-candidate adoption, and terminal disposition are
  separate decisions and require explicit precedence.
- Finding identity, severity, population, and change matter; aggregate counts
  alone are insufficient evidence of improvement or regression.
- API queue state and native editorial outcome remain separate authorities.
- Provider Responses alone cannot reproduce native assembly or QA where exact
  source workspaces, selected packets, and prior candidate decks are required.
- Unknown or unavailable evidence remains explicit; it is never reconstructed
  from expected behavior.

## Slice 0 — Freeze cohort and prepare one evidence-access campaign

Create one closed four-run audit manifest for Madeleine, Doughmeat, Macaron, and
Frisbee. It must bind:

- subject, API run, native run, and every provider Response ID;
- stage and attempt ordering;
- exact final checkpoint/archive identity where previously recorded;
- expected selected-packet, accepted-pass, candidate-deck, validation, lint,
  polish-target, polish-response, result, and receipt paths;
- local evidence already present and its verified digest;
- evidence still missing; and
- the minimum reason each requested artifact is needed.

Ask API/owner for **one consolidated coordinate packet and one authorization
decision covering the complete campaign**, not one round per dog. The packet
should include all four immutable final checkpoints even where prior coordinates
already exist, while marking previously downloaded and hash-verified archives so
SBE does not retrieve them again unnecessarily.

If R2 access is needed, plan one conditional `HEAD` and one `GET` per genuinely
missing exact object. Do not list storage. Do not perform provider work, recovery,
reconciliation, or mutation. Coordinate preparation and retrieval may occur at
different times, but no newly discovered object expands the closed campaign.

Deliverables:

- `FOUR-RUN AUDIT MANIFEST.json`;
- `FOUR-RUN CHECKPOINT COORDINATE REQUEST.md`; and
- an access ledger separating reused local evidence from new reads.

### Voof-paws 1

Pause for API review of identities, missing evidence, coordinate completeness,
and the proposed bounded R2 operation count before any new retained-object read.

Slice 0 result: Doughmeat, Macaron, and Frisbee already have locally retained,
archive-hash-verified checkpoints and require no new R2 reads. Madeleine alone
requires a consolidated coordinate plus one conditional `HEAD` and one bounded
`GET`. See `FOUR-RUN AUDIT MANIFEST.json`,
`FOUR-RUN CHECKPOINT COORDINATE REQUEST.md`, and `R2 ACCESS LEDGER.md`.

## Slice 1 — Normalize provider and native lineage evidence

For each run, build a private deterministic lineage packet joining:

- initial and polish Responses in exact action order;
- each sparse-polish edit to its target field and prior candidate;
- validation and lint findings before and after every candidate;
- whole-deck acceptance and rejection reasons;
- polish adoption/rejection/error outcome and exact comparison basis; and
- final native result/receipt and terminal inventory.

Use the released production assembly, validation, lint, and sparse-polish
functions as the semantic oracle. Audit-specific scripts may orchestrate and
visualize the comparison but must not define alternate acceptance semantics.

Prove replay equality against retained artifacts wherever possible. Record text,
semantic, and byte equality separately so metadata-only differences do not hide
or fabricate content drift.

## Slice 2 — Complete the four exact production replays

### 2A — Doughmeat

Reproduce the complete two-polish lineage. Extract all six surviving `you do not`
fields, their surrounding card identities, the whole-deck acceptance result, and
the exact terminal-selection rule. Determine whether the final candidate was
acceptable under the same deck-level standard applied to Frisbee.

### 2B — Macaron

Reproduce the accepted first polish and malformed second response. Present the
three exact-duplicate groups, both dominant-opening groups, and the duplicate
sparse-edit path. Confirm that any revised rule still distinguishes substantive
defects and invalid candidate materialization from harmless residual warnings.

### 2C — Madeleine

Recover the exact final structural-validation failure and affected content. Prove
whether the problem was authored content, assembly metadata, a legacy/dormant
feature, or another structural contract. Do not classify editorial merit until
the exact validator evidence is available.

### 2D — Frisbee control replay

Reuse the existing exact replay without new provider or retained-object reads.
Produce the same normalized lineage packet used for the other three runs so
cross-case comparison does not depend on prose summaries with different shapes.

### Voof-paws 2

Pause after all four evidence packets are reproducible. Review any replay gaps or
cases where historical artifacts cannot establish the original decision before
introducing human/model judgments.

## Slice 3 — Independent editorial review packet

Build a bounded, consistently formatted review packet for each meaningful
candidate transition. Reviewers should see:

- affected text fields and enough neighboring context to judge repetition;
- prior and candidate versions;
- exact machine findings before and after;
- finding identities and severity, with aggregate counts secondary;
- the whole-deck acceptance decision;
- the historical adoption and terminal decision; and
- no dog/run label that reveals which decision the reviewer is expected to
  defend, where blinding is practical.

Collect at least:

- one owner/human judgment; and
- one independent editorial-model judgment using a frozen rubric and prompt.

Allowed judgments are closed and separate for deck acceptability and candidate
adoption: `accept`, `accept_with_advisory`, `request_another_polish`,
`retain_prior_candidate`, `terminal_review`, and `insufficient_context`.

Store full private review packets outside the repository. Commit only bounded,
sanitized comparison results unless separately approved.

## Slice 4 — Cross-case calibration matrix

Compare machine and reviewer decisions across the cohort. At minimum, test these
candidate policy families without implementing them:

1. current raw finding-count monotonicity;
2. whole-deck acceptance dominance after structural/integrity checks;
3. severity-weighted finding comparison;
4. finding-identity-aware partial-order comparison;
5. accept-with-advisory for bounded residual style warnings; and
6. explicit hard classes for structural invalidity, exact duplication, suspicious
   artifacts, and malformed sparse edits.

For every family, show the predicted disposition for all four runs and identify
false acceptance, false rejection, no-progress, and regression risks. Do not
optimize solely to make Frisbee or Doughmeat pass.

## Slice 5 — Recommendation and implementation boundary

Produce a decision document that states:

- which findings remain hard rejection conditions;
- which become advisories;
- how candidate improvement is compared;
- when whole-deck acceptance can dominate a residual warning;
- when a candidate passing deck QA must still be rejected for forbidden changes,
  evidence/binding failure, or material regression;
- how malformed polish output differs from an editorial rejection;
- how attempts are exhausted and when terminal review is justified;
- whether polish prompts/target construction need corresponding changes; and
- the exact fixtures required for an implementation sprint.

Prefer explicit decision precedence over another magic aggregate threshold.

### Voof-paws 3 — implementation decision

Pause for owner and API review. No production code, prompt, schema, or release
change begins until the recommendation and cross-repo consumer impact are
approved.

## Possible follow-on slices

After Voof-paws 3, amend this plan or open a focused implementation sprint for:

- production rule and prompt changes;
- migration/compatibility treatment for retained historical workspaces;
- regression fixtures covering all four cases;
- packaged and installed-wheel qualification; and
- an appropriately scoped SBE/API release gate.

The exact implementation slices are intentionally not precommitted before the
calibration result.
