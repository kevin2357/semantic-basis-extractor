# Plan

Status: Slices 0–2, Voof-paws 2, and Slice 3A tooling are complete. No review
answers have been collected. Slice 3B must freeze the real judgment rubric and
regenerate the review page before owner or independent-model review begins.
No editorial-policy or runtime change is approved before Voof-paws 3.

API Slice 0-alpha now also has deterministic private real-corpus inputs for all
three candidate query shapes. This supports the companion schema experiment but
does not satisfy or replace the two pending editorial judgments.

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

## Relationship to the joint retention companion

The API companion sprint at
`astrowoof-api/docs/sprints/2026/09/20260907-editorial-review-evidence-retention-companion-sprint87/`
now owns the prospective **routine** `editorial_review_packet.v1`, its API
transport envelope, Better Stack capture boundary, byte ceiling, omission
semantics, and post-terminal delivery hook.

This calibration sprint retains a different responsibility:

- reproduce and normalize the four historical lineages;
- determine which evidence a human or independent editorial model actually
  needs to judge them;
- perform the blinded calibration exercise; and
- recommend editorial-policy changes from that evidence.

The private lineage/review packets created here are research artifacts and
schema inputs. They are not automatically the public/package contract for
routine capture, and their existence does not authorize API transport or
Better Stack publication. Conversely, the companion sprint must not narrow the
private calibration evidence merely to make a small routine log packet fit.

Slice 3 should feed measured evidence back into the companion contract pause:

- canonical UTF-8 size of finding-local review packets;
- incremental size of complete selected-deck text;
- minimum useful content for accepted controls with no rejected finding;
- fields reviewers actually use versus fields needed only for provenance; and
- any evidence that cannot be represented faithfully within the proposed
  routine packet ceiling.

If the routine packet excludes complete deck text, this sprint may continue to
use complete private decks for calibration. Their separately governed durable
retention is a companion/API storage decision, not a reason to weaken the
calibration exercise.

## Implementation split after Slice 3A

The five-run reconstruction appropriately served both tracks during discovery:
it exposed the evidence humans/models need for calibration and supplied real
content, cardinality, query, and size inputs for API Sprint 87. Continuing both
purposes here would now blur this sprint's original research goal.

All production/package work for routine evidence collection now belongs to the
separate SBE companion sprint:

`20260907-editorial-review-packet-collection-contract-sprint1`

This calibration sprint retains only owner/human and independent-model
judgments, cross-case policy comparison, and recommendations for lint,
candidate adoption, polish exhaustion, terminal review, prompts, and future
calibration cohorts. It does not own a public packet schema/reader, runtime
builder, terminal hook, Better Stack transport, installed-wheel qualification,
or coordinated release.

The collection companion may cite this sprint's measurements and conclusions,
but routine capture cannot become editorial decision authority or a prerequisite
for completing the calibration honestly.

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

Build a bounded, consistently formatted **private calibration packet** for each
meaningful candidate transition. This is a research presentation format, not a
silent freeze of `editorial_review_packet.v1`. Reuse the joint packet's field
names and ordering where that improves comparability, but do not omit evidence
needed for judgment merely because the eventual Better Stack packet may have a
smaller ceiling. Reviewers should see:

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

The approved successful-delivery control is API run
`665cd3d2-332a-4ba7-9c0b-bb3fb4e1a177`, native run
`468479aa4a8d818392b2705919817c2ebca44cab78e3868657f8746b5e50f50e`,
checkpoint generation 10. Its one authorized HEAD and conditional GET are
complete. The archive, inventory, workspace snapshot, delivery result, and
publication receipt all validate exactly. It contributes two ordinary accepted
polish transitions and must remain in the blinded review set.

For each packet, also record canonical UTF-8 size with and without complete
selected-deck text. Summarize those measurements, plus which fields reviewers
actually needed, for the companion sprint's joint contract review.

## Slice 3A — Local blinded-review interface

Build a local-only, static review page over the eight frozen finding-local
packets. It must:

- present exact before/after field text, prior/candidate findings, structural
  validation, and whole-deck acceptance without revealing source run, subject,
  historical adoption, or terminal outcome;
- use the closed judgment vocabulary separately for deck acceptability and
  candidate adoption;
- support optional reviewer rationale and `insufficient_context` without
  forcing a substantive decision;
- show progress and prevent accidental silent omission at export time;
- export deterministic JSON containing the frozen packet ID/digest, rubric
  version, reviewer role supplied locally, judgments, and rationale;
- perform no network, provider, API, R2, Better Stack, or retained-workspace
  operation; and
- keep both packets and exported judgments outside the repository.

Generate the page deterministically from the frozen private packets and add a
provider-free verification that checks packet order, identity binding, closed
choices, blinding, HTML escaping, and export round-trip semantics. The separate
answer key must never be embedded in the page.

Slice 3A is review tooling only. It does not complete Slice 3 until an owner
judgment and an independent-model judgment have actually been collected.

Slice 3A result: the deterministic eight-sample local review page and its
receipt are generated under
`.tmp-editorial-calibration-r2/private-review-ui/`. The page contains no answer
key, source/run/subject identity, network dependency, or external resource.

The generated page is a pre-review prototype only. Its shared mixed choice
vocabulary is not an approved judgment rubric and must not be used to collect
or compare answers.

## Slice 3B — Freeze the judgment rubric and regenerate the review tool

Before any owner or independent-model judgment, write and approve one short,
closed rubric that both reviewers receive verbatim. It must:

- define **deck acceptability** separately from **candidate adoption**;
- state that finding counts and deterministic labels are evidence, not automatic
  verdicts;
- require reviewers to assess whether the targeted issue disappeared, improved,
  remained, or worsened, and whether new material regressions appeared;
- preserve structural validity, authorized edit scope, evidence/binding
  integrity, and available context as explicit considerations;
- prohibit guessing source identity, historical production outcome, or the
  decision the exercise is expected to vindicate;
- define when insufficient evidence requires `insufficient_context`; and
- request a concise evidence-based rationale for each decision.

Use question-specific closed vocabularies rather than the Slice 3A prototype's
mixed list:

Deck acceptability:

- `accept`;
- `accept_with_advisory`;
- `request_another_polish`;
- `terminal_review`; and
- `insufficient_context`.

Candidate adoption:

- `adopt_candidate`;
- `retain_prior_candidate`; and
- `insufficient_context`.

The rubric must define these terms precisely, including that a locally improved
candidate need not be a globally acceptable deck and that an acceptable deck
need not imply every optional warning is resolved.

After approval:

1. bind a stable rubric version and SHA-256 to every review packet;
2. regenerate the local page with separate question-specific controls;
3. embed the complete rubric visibly in the page;
4. update the export contract and tests to reject cross-question choices;
5. prove the packet order, identities, blinding, escaping, completeness gate,
   and deterministic export remain intact; and
6. discard any answers produced with the placeholder Slice 3A vocabulary.

### Rubric paws point

Pause for owner review of the written rubric and exact vocabularies before
regenerating the page or soliciting either reviewer. The independent model must
receive the identical frozen rubric and packet evidence, without the answer key
or the owner's judgments.

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

Routine evidence collection is no longer one of these possible follow-on
slices; it belongs to the named implementation companion above. Editorial-policy
or prompt changes informed by the judgments remain a separate later decision.
