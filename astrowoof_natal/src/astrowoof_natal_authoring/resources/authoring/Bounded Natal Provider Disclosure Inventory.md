# Bounded Natal Provider Disclosure Inventory

Contract: `astrowoof.bounded_natal.provider_disclosure.v1`

This inventory governs every provider-visible bounded-Natal authoring request,
including initial generation, retries, polish, and critic use once the route is
connected to shared lifecycle orchestration.

## Subject fields

Allowed when supplied:

- `subject_id`
- `display_name`
- `subject_type`
- `gender`
- `pronouns`
- `breed`

Protected and prohibited:

- birth date or datetime;
- interval start/end or birth-time basis;
- latitude, longitude, or coordinates;
- birth location and location evidence; and
- birth-date precision.

## Selected semantic fields

Provider-visible object rows are limited to projected object type/name/operators
and these attributes:

- canonical object name;
- bounded source object type;
- invariant sign;
- projected mode;
- coordinate-transform label;
- projection composition; and
- selected term/mode references.

Invariant sign and transform labels are included because the bounded editorial
task cannot explain the selected projected meaning without them. They are
categorical facts proven over the full interval, not reconstructed exact positions.

Provider-visible relationship rows are limited to projected relationship type,
operators, theme tags, invariant source aspect, interaction mode, topology flag,
and selected relation/mode references.

## Evidence and registry

The provider receives invariant classification, proof-scope labels, dependency
claim IDs, and a digest of the private selected evidence. It does not receive raw
evidence records, ranges, transition witnesses, counterexamples, orbs, structural
strength, relevance-accounting values, or source-owner/source-record identifiers.

Only definitions for projected terms used by selected claims or their selected
dependencies are disclosed. The complete projected registry is not disclosed.

## Never provider-visible

- complete projected or canonical graphs;
- `source_identity` or `source_artifact_ref` objects;
- the complete bounded disposition report;
- unselected, variable, unavailable, inconclusive, or outside-scope material;
- private source/evidence/correspondence/root-owner references;
- selection-audit component details; and
- raw protected provenance.

The Python boundary `assert_provider_minimized()` enforces forbidden keys and can
also scan for seeded protected values. Route integration must call the same
allow-listed packet builder for initial requests, retries, polish, and critic; it
must not rebuild prompts from private artifacts.
