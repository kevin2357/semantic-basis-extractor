# API Agent Questions

Status: open; answers required in the final sprint handoff.

This document preserves the integration questions that triggered the sprint.
They must not be treated as answered merely because an implementation slice
passes. The final sprint artifacts must include a separate response document
that answers every numbered question and subquestion using the completed test,
repair, and release evidence.

## Questions

### 1. Defect classification

Is the observed SBE 0.2.1 failure an SBE snapshot-ordering defect at a polish
retry spend-authorization boundary?

The final answer must distinguish, where applicable:

- subject-state publication ordering;
- workspace mutation versus snapshot publication ordering;
- concurrent or overlapping checkpoint publication;
- provider/spend ledger persistence; and
- defects proven generally from circumstances specific to the retained run.

### 2. Authoritative snapshot contents

Should the updated final deck, validation report, and lint report have been
included in the authoritative snapshot before SBE prepared and exited for
polish attempt 2?

The final answer must state the complete expected checkpoint boundary at that
pause, including operator state, public state, spend ledger, authorization
request, provider evidence, subject/polish attempt state, final artifacts, QA
reports, and snapshot revision linkage.

### 3. Existing-run recovery

Is there a supported, provenance-preserving recovery procedure for this
existing run that does not manually bless arbitrary changed workspace bytes?

The final answer must identify:

- what SBE 0.2.1 supported before this sprint;
- what new inspection or repair procedure the sprint provides;
- its exact prerequisites and refusal conditions;
- which bytes and state are reconstructed, retained, or changed;
- how monotonic evidence and spend history are preserved;
- whether the canonical retained run was changed; and
- what authorization or provider-connected action, if any, remains for the API
  owner after repair.

### 4. Required corrective deliverables

If code changes are required, can SBE provide all of the following?

1. a regression test reproducing the exact sequence;
2. corrected snapshot ordering;
3. safe handling of an interrupted provider request followed by
   reconciliation;
4. a supported repair/recovery tool or procedure for the 0.2.1 run; and
5. updated consumer documentation and release guidance.

The final answer must address each item separately rather than answering the
group with one aggregate status.

### 5. Production restart guarantee

Can the API checkpoint an SBE workspace at every provider/spend boundary,
destroy worker scratch, restore the complete checkpoint at the supported
logical location, and resume without duplicate paid work or manual integrity
overrides?

The final answer must define the guarantee precisely, including any remaining
provider atomicity gap, single-writer requirement, stable-path requirement,
API-owned lease/snapshot responsibilities, and machine-distinguishable state
that requires reconciliation rather than automatic resume.

## Required final response format

The final response document must, for every question and enumerated corrective
deliverable, include:

- **Answer:** direct yes/no/qualified conclusion;
- **Confidence:** `high`, `medium`, or `low`;
- **Evidence:** tests, result records, contract or source references, and live
  repaired-copy evidence where applicable;
- **Residual uncertainty:** explicit remaining unknowns or `none`; and
- **Consumer consequence:** what the API worker/operator must do.

Confidence labels mean:

- `high`: directly demonstrated by deterministic tests and applicable retained
  or installed-runtime evidence;
- `medium`: strongly supported but dependent on an external/provider behavior
  or a production environment not fully replayed; and
- `low`: provisional inference requiring further evidence.

The response document is a required delivery artifact, not a substitute for
the underlying detailed sprint evidence.

## AstroWoof API Slice 5 critic-artifact questions

These questions were added while the API prepared durable critic-response
artifact storage and normalized report/finding indexes. They are independent
consumer-contract questions and must each receive their own final answer and
confidence assessment even if their resolution requires a plan revision or is
deferred from the checkpoint patch release.

### 6. Stable critic artifact

Is `critic-findings.json` intended to be a stable, versioned consumer artifact
in the next pinnable SBE release?

### 7. Explicit schema version

Can `critic-findings.json` receive an explicit top-level `schema_version` so the
API can reject unsupported formats deterministically rather than infer
compatibility solely from the SBE release number?

### 8. Closed vocabularies

Which vocabularies should the API treat as contractually closed and stable?
Current SBE code emits:

- `scope`: `summary`, `card`, `deck`;
- `priority`: `high`, `medium`, `low`;
- `repairability`: `local_repair`, `upstream_reconception`, `advisory_only`;
  and
- `quality_dimension` values from `QUALITATIVE_DIMENSIONS`.

Are those exact values the intended persisted contract?

### 9. Guaranteed finding fields

Which normalized fields are guaranteed for every finding, and which are
candidate-generation conveniences that may change independently? In
particular:

- `target_paths`;
- `comparison_paths`;
- `required_context`;
- `selected_for_candidate`;
- `selection_reason`;
- `diagnosis`; and
- `rewrite_objective`.

### 10. Authoritative critic provenance

What is the authoritative provenance chain from `critic-findings.json` to:

- the exact criticized final-deck bytes;
- the raw provider response;
- the provider Response ID;
- critic model and reasoning configuration; and
- SBE release, resource, and generation-profile identities?

Does the normalized artifact contain or reference these identities, or should
the API derive them from `run.json` and the surrounding delivery/run manifest?

### 11. Private artifact versus PostgreSQL index

Is it correct for the API to keep complete diagnosis, rewrite objective,
strengths, risks, target paths, and comparison paths only in the immutable
private JSON artifact, while indexing only bounded operational dimensions such
as category, scope, priority, confidence, repairability, target count, and
candidate-selection status in PostgreSQL?

### 12. Canonical critic fixtures

Are the existing Kevin and Ella `critic-findings.json` files valid canonical
fixtures for the upcoming release contract, or should SBE publish refreshed
fixtures with the release?

## Critic-question answer requirements

For questions 6-12, the final response must additionally identify:

- whether the conclusion is normative contract, current implementation only,
  or a proposed future contract;
- the exact schema/catalog/document authority supporting the conclusion;
- backward-compatibility and unsupported-version behavior;
- whether an SBE source, schema, packaged-resource, fixture, or release change
  was made during this sprint; and
- whether the API may implement its Slice 5 persistence/index design against
  the answer immediately or must wait for a later artifact.
