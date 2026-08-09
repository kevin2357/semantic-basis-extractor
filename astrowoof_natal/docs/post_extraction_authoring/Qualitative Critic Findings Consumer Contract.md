# Qualitative Critic Findings Consumer Contract

`critic-findings.json` is a private, stable consumer artifact beginning with
`astrowoof.qualitative_critic_findings.v0.1`. Consumers must dispatch on its
top-level `schema_version` and reject unsupported versions. The packaged
authority is `resources/contracts/qualitative-critic-findings.schema.json`,
registered by `resources/contracts/contract-catalog.json`.

## Closed vocabularies

For v0.1 the following sets are closed:

- `scope`: `summary`, `card`, `deck`;
- `priority`: `high`, `medium`, `low`;
- `repairability`: `local_repair`, `upstream_reconception`, `advisory_only`;
- `quality_dimension`: `summary_thesis_overlap`, `conceptual_card_overlap`,
  `repeated_comic_mechanism`, `repeated_rhetorical_posture`,
  `exchangeable_headline`, `over_explained_body`,
  `incomplete_compound_semantics`, `insufficient_audience_distinction`,
  `insufficient_astrology_density_progression`, `other_editorial_quality`;
- `required_context`: `nearby_prose`, `claim_evidence`, `whole_chart`, `none`;
- `selection_reason`: `eligible`, `not_locally_repairable`, `low_priority`,
  `confidence_below_0.70`, `field_cap`, `card_cap`, or `null` before selection.

Adding or changing values requires a new schema version. Consumers must not map
unknown values into an existing value silently.

## Finding fields

Every item in `critic.findings` guarantees:

- `finding_id`, `quality_dimension`, `scope`, `priority`, `confidence`, and
  `repairability`;
- `target_paths`, `comparison_paths`, and `required_context` arrays;
- complete private `diagnosis` and `rewrite_objective` strings; and
- normalized `selected_for_candidate` and `selection_reason` fields.

`deck_assessment.strengths` and `deck_assessment.primary_risks` are also private
artifact fields. `eligible_findings`, `selected_target_paths`,
`selected_location_count`, and `limits` are versioned denormalized orchestration
projections. The authoritative per-finding record remains
`critic.findings`; consumers should not treat projection ordering as a durable
database identity.

## Provenance chain

`provenance.criticized_deck` identifies the exact criticized final-deck bytes
by run-relative path, filename, byte count, SHA-256, and role.
`provenance.raw_provider_response` does the same for the private raw provider
response. `provenance.provider` records the Response ID, model, reasoning
effort, and service level. `provenance.run` records the run and operator schema,
state revision, authoring-profile identity and digest, installed runtime
identity, and packaged resource-set identity.

The artifact therefore contains its authoritative joins. `run.json` remains
the operator authority for overall run state and spend history, but the API
does not need to infer critic compatibility or byte identity from release
number or filesystem adjacency.

## API storage guidance

Keep the complete artifact—including diagnosis, rewrite objective, strengths,
risks, and paths—in immutable private object storage. A PostgreSQL operational
index may contain only bounded dimensions such as schema version, finding ID,
quality dimension, scope, priority, confidence, repairability, target and
comparison counts, and candidate-selection status. Preserve the artifact hash
and object reference as the authoritative join. Do not place prose or subject
material in broadly queryable operational columns.

The packaged sanitized fixture at
`resources/fixtures/critic/critic-findings.v0.1.json` is canonical for contract
tests. Pre-v0.1 Kevin and Ella live-run files are valuable historical evidence
but are unversioned and are not canonical fixtures for API persistence.
