# Ingesting Bounded Birth-Time Natal Projection Artifacts

```yaml
status: design-input-for-sprint-planning
date: 2026-08-14
repository: semantic-basis-extractor
upstream_agf_release: astrology-graph-foundry 0.8.1
upstream_spc_release: semantic-projection-core 0.11.0
bounded_output_contract: projected_bounded_semantic_graph.v1
confirmed_initial_product_boundary:
  pipeline: separate_bounded_pipeline
  authored_authority: invariant_only
```

## Purpose

This document records SBE's pre-planning assessment of the new bounded birth-time
Natal artifacts produced by Astrology Graph Foundry (AGF) and projected by Semantic
Projection Core (SPC). It summarizes the recent upstream sprint history, the
released contracts and consumer guidance, direct validation of a real four-context
fixture, the exact assumptions in SBE that do not carry across the new boundary,
and the initial architectural direction accepted by the product owner.

This is an input to later sprint planning. It is not the sprint plan and does not
authorize implementation.

## Upstream semantic model

The bounded artifact is not a collection of possible exact charts, a midpoint
chart, a most-likely chart, or an exact chart with nullable fields. AGF evaluates
the admitted birth-time interval and promotes only categorical semantic facts that
are supported across the complete interval under its declared proof policy.

The result has two related but distinct surfaces:

1. a bounded canonical invariant subgraph containing supported invariant objects
   and relationships; and
2. structured uncertainty evidence retaining ranges, possibilities, prerequisites,
   transitions, counterexamples, unavailable features, and provider or calculation
   failures.

Absence from the invariant subgraph does not mean that a fact is false. It may be
variable, conditional, unavailable, inconclusive, unsupported, or simply outside
the retained invariant subgraph.

### AGF ownership and recent sprint sequence

The four most recent relevant AGF sprints establish a deliberate source boundary:

- **AGF/SPC runtime and ownership decoupling:** AGF owns calculation, canonical
  source graphs, structural and uncertainty evidence, registries, and serialized
  projection-neutral artifacts. SPC owns projection. AGF is independently
  installable and does not execute SPC internally.
- **Coordinate-derived bounded Natal expansion:** AGF evaluates bodies, signs,
  motion, dignity, antiscia, contra-antiscia, harmonics, derived aspects, and
  declination relationships across the interval. Numeric coordinates remain
  evidence; only invariant categorical material is promoted.
- **Time/frame-derived bounded Natal expansion:** AGF adds qualified house and angle
  ranges, invariant house membership, cusp semantics, rulers, sect, triplicity,
  lots, Vertex, and angle relationships without manufacturing representative
  degrees or flattening formula branches.
- **Bounded evidence schema reconciliation:** AGF 0.8.1 reconciles producer and
  schema vocabularies and strengthens whole-artifact validation without changing
  astrology, epistemic meanings, bounded graph 1.7.0, evidence contract 1.0.0, or
  calculation profile 1.12.0.

AGF distinguishes three evidence fields that downstream systems must not collapse:

- `classification` is the epistemic result, such as `invariant`, `conditional`,
  `variable`, `unavailable`, or `inconclusive`;
- `availability` describes the state of the configured calculation path, provider
  input, or prerequisite; and
- `status_reason` is open explanatory text rather than a closed semantic code.

AGF deliberately withholds bounded structural-strength scores and canonical claims.
Raw graph counts are topology, not confidence, importance, or independent support.

### SPC bounded projection boundary

SPC 0.11.0 implements bounded Natal as a sibling route rather than weakening its
existing exact/static contract:

- request: `bounded_natal_projection_request.v1`;
- profile: `woofmapped_bounded_astrology.v0@0.1.0`;
- output: `projected_bounded_semantic_graph.v1` with numeric
  `contract_version: 1.0.0`;
- installed command: `semantic-bounded-project`; and
- parallel-family validator: `validate_parallel_bounded_contexts()`.

The existing `projected_semantic_graph.v1` remains unchanged. Bounded output uses
`source_artifact_ref`, not `source_graph_ref`, because the authoritative source is
the complete bounded package with capabilities and evidence beyond its canonical
subgraph.

SPC preserves:

- opaque source identity and immutable source-artifact identity;
- source capabilities, feature dispositions, and limitations;
- direct evidence plus resolvable prerequisite closure;
- epistemic classification and proof scope;
- root-owner and evidence-family identity;
- source and mapping references;
- context-independent `correspondence_id` values;
- complete artifact-scoped projected-term definitions; and
- installed runtime, resource, schema, profile, context, route, and output-contract
  provenance.

SPC forbids bounded output from acquiring exact longitudes, representative
positions, orbs, structural strength, confidence, or a most-likely state. Context
may vary declared target relevance or framing but cannot vary source certainty,
evidence, capabilities, limitations, family identity, semantic primitives,
mappings, operators, or projected-term definitions. No projection context has
canonical epistemic priority.

## Direct fixture assessment

The reviewed archive is:

`astrowoof-bounded-1981-10-10-denver-1300-1700-agf-0.8.1-spc-0.11.0.zip`

It contains one projected artifact for each supported Woofmapping context. All four
artifacts passed SPC's official bounded JSON Schema validation and specialized
parallel-context validation.

### Shared verified identity

- profile: `woofmapped_bounded_astrology.v0@0.1.0`;
- source artifact SHA-256:
  `715366da9887ccac6104bca6d826238dca1ef84b29c52ffaa2a5a481643d7105`;
- object correspondences: 106;
- relationship correspondences: 1,520;
- epistemic SHA-256:
  `bcaa357f9c4418b070505344c6d9d49daf63ae3a8f9e24278fe6c4f189ee8166`;
- structural-semantic SHA-256:
  `a466bd43a83435a055d09b127a9c0e4f6a4f2bb377a09975df7b6604777d1008`;
- context priority: none; and
- validation status: passed.

### Per-context scale

| Surface | Count |
| --- | ---: |
| Source objects | 108 |
| Projected objects | 106 |
| Ordinary mapped operators | 10 |
| Orientation objects | 2 |
| Derived operators | 94 |
| Source/projected relationships | 1,520 |
| Object evidence families | 24 |
| Relationship evidence families | 476 |
| Materialized evidence records | 1,544 |
| Full source evidence-registry records | 2,856 |
| Used projected terms | 43 |

SPC deliberately classifies the calculated point `Spirit` and the bounded `sect`
object outside its current bounded mapping scope. All 1,520 source relationships
are mapped. The artifacts report no validation errors, warnings, or informational
diagnostics.

Every projected object has `projection_relevance_score: null`. This is intentional:
SPC has not established a bounded object-relevance measure. Ninety-four topology-
only coordinate-transform relationships likewise have null relevance. Semantic
interaction relationships may carry target relevance, but SPC allocates it within
the shared evidence family so sibling multiplicity cannot inflate the family total.

The materialized evidence contains 139 unresolved prerequisite identifiers. These
are preserved opaque upstream feature identifiers, not dangling direct evidence
references. SBE should retain them without inventing local registry records or
silently treating them as broken closure.

The artifacts explicitly declare these limitations:

- bounded invariant subgraph, not an exact chart;
- no representative or midpoint positions;
- no exact longitudes or orbs;
- no structural strength or canonical claims; and
- no temporal activation.

## Why the current exact SBE path cannot be widened safely

SPC has already demonstrated that SBE 0.3.0's shallow four-file loader and
projected-term registry merge can accept a small bounded fixture. Candidate
construction then fails because the exact path performs arithmetic on a null object
relevance score. That failure is only the first visible incompatibility.

The exact SBE pipeline assumes:

1. `source_graph_ref` rather than the bounded `source_artifact_ref`;
2. numeric object relevance;
3. structural strength or a safe numeric fallback;
4. exactly sixteen mandatory Natal candidates;
5. missing mandatory placements indicate malformed or incomplete input;
6. exact-style object attributes and aspect geometry are available;
7. projected records can participate independently in ranking;
8. the existing exact claim-deck and mandatory-card rules apply; and
9. one context can conveniently act as a baseline even though the bounded family
   declares no epistemically canonical context.

These are internally consistent exact-chart product assumptions. Adding null guards
or aliases would make the code execute without establishing truthful bounded
selection semantics.

## Confirmed initial SBE direction

The product owner has confirmed two high-level decisions before sprint planning:

1. **Bounded ingestion and extraction will use a separate pipeline.** It may share
   lifecycle and authoring infrastructure with exact runs, but it will not disguise
   bounded input as an exact projected graph or reuse exact selection invariants by
   default.
2. **The initial bounded authoring contract will author invariant material only.**
   Conditional, variable, unavailable, and inconclusive material remains preserved
   as evidence and explicit disposition, but it will not become definite authored
   claims in the first product boundary.

The initial conceptual flow is therefore:

```text
four projected bounded artifacts
    -> strict bounded packet admission
    -> invariant candidates plus evidence-family topology
    -> bounded-specific eligibility and selection
    -> versioned bounded claim deck
    -> shared spend/lifecycle/provider machinery
    -> bounded-aware authoring and delivery provenance
```

Exact and bounded execution can share mature SBE infrastructure after the semantic
basis boundary, including spend authorization, prepare/authorize/execute, durable
snapshots, detach/resume, structured events, retries, polish, critic, and delivery
packaging. Input admission, candidate semantics, selection invariants, claim-deck
schema, and authoring instructions remain route-specific.

## Recommended admission contract

The future bounded packet admission boundary should require at least:

- `projected_bounded_semantic_graph.v1` and numeric contract version 1.0.0;
- exact bounded profile ID/version;
- the exact four supported context ID/version pairs;
- one common source artifact and opaque source identity;
- matching capabilities, feature dispositions, limitations, evidence identity,
  family identity, and registry identity;
- complete projected-term definitions;
- valid source, mapping, evidence, endpoint, and correspondence references;
- successful parallel-context validation; and
- no mixture of exact and bounded artifacts.

SBE should retain `source_artifact_ref` as a native bounded field. Renaming it to
`source_graph_ref` would hide the broader source authority. Admission should produce
a compact machine-readable summary suitable for orchestration and structured
events without logging protected birth facts or full graphs.

## Recommended candidate and selection semantics

The first bounded release should make only invariant projected rows eligible for
authored claims. Other epistemic classes should remain available to private
provenance, diagnostics, and explicit exclusion/disposition reporting.

Ranking should separate:

- **epistemic authority**, supplied by the bounded proof contract; from
- **target/editorial utility**, supplied by a versioned SBE bounded-selection
  policy.

All initially eligible claims have invariant authority. SBE may still rank them by
semantic breadth, novelty, role diversity, relationship support, and incremental
coverage, but must not call those measures confidence or source strength.

SPC relationship relevance may be used as target-domain relevance only under its
family-allocation contract. Null object relevance must not become zero, one, 0.55,
or another convenience default. Object prioritization needs an explicit SBE-owned
bounded policy.

`evidence_family_group` should be a first-class selection and audit unit. The
fixture's 1,520 relationships collapse to 476 relationship families, while 94 of
106 objects are derived. Without family-aware accounting, derived topology will
overwhelm a compact basis through representational multiplicity.

Selection should therefore:

- measure independent semantic coverage at the family level;
- prevent siblings from earning repeated independent coverage credit;
- permit multiple family members only for demonstrably distinct selected meaning;
- retain excluded rows and their evidence in provenance; and
- record stable exclusion reasons such as `duplicate_evidence_family`,
  `lower_incremental_coverage`, and `selection_budget_displaced`.

The existing exact requirement for sixteen mandatory candidates must not cross the
bounded boundary. A bounded basis needs its own foundational-coverage policy and
must allow variable deck size. It must not add filler or manufacture absent
placements merely to satisfy an exact quota.

## Claim-deck and authoring boundary

The bounded claim deck should have its own schema and version. It should make the
authority class, proof scope, evidence references, root-owner family, projected
context correspondence, limitations, and source-artifact identity explicit.

The initial deck should describe a stable portrait composed only of material that
is invariant across the admitted interval. A future contract may add restrained
alternative or uncertainty narratives, but that work should not be smuggled into
the first release through prose-friendly synthesis.

The provider-visible view must remain minimized. SBE should privately preserve the
full bounded evidence and provenance while exposing to OpenAI only the selected
semantic material and the minimum editorial qualification needed to write it. Raw
birth datetimes, interval endpoints, coordinates, location evidence, complete
graphs, and full uncertainty registries should not enter authoring, retry, polish,
or critic prompts without a separately documented editorial requirement.

## Release-identity qualification point

The reviewed archive is labeled AGF 0.8.1 plus SPC 0.11.0 and passes the official
SPC validators. AGF 0.8.1 preserves the bounded contract identities qualified by
SPC while repairing schema enforcement. SPC 0.11.0's published compatibility text,
however, names AGF 0.8.0 as its exact qualified source release.

This is not presently a semantic blocker, but the SBE release must make the
artifact boundary explicit:

- qualify and document the exact AGF 0.8.1 and SPC 0.11.0 wheels used by the
  production chain;
- retain their external wheel hashes and runtime receipts in orchestration and
  release evidence;
- recognize that the projected JSON embeds upstream contract identities and the
  source artifact hash, but does not by itself prove the originating AGF wheel; and
- request or record an SPC compatibility clarification naming AGF 0.8.1 as the
  preferred repaired patch when the consumer handoff is finalized.

## Expected planning areas

Subject to the remaining product-design discussion, the bounded sprint will likely
need to cover:

1. final contract and product-policy decisions;
2. strict four-context bounded admission and installed validation;
3. a bounded candidate and evidence-family model;
4. bounded selection, foundational coverage, and a variable-size claim deck;
5. invariant-only synthesis and minimized provider-visible representation;
6. integration with the existing provider, spend, checkpoint, and lifecycle
   machinery;
7. negative, scale, determinism, privacy, and snapshot/resume qualification; and
8. installed AGF 0.8.1 to SPC 0.11.0 to SBE acceptance and consumer handoff.

The API-agent requests already stored in this sprint directory must be reconciled
against the lifecycle and structured-event capabilities delivered in SBE 0.3.0.
They should not be blindly reimplemented as bounded-only features when the shared
execution contract already satisfies them.

## Current assessment

The upstream handoff is technically ready for SBE planning. Packaged schemas,
specialized validators, four real context artifacts, evidence and family semantics,
runtime identity, and consumer guidance all exist and agree on the essential
boundary.

The remaining work is not about discovering what the upstream files mean. It is
about defining a truthful bounded semantic basis and authored product. The accepted
starting point is a separate bounded pipeline producing an invariant-only stable
portrait, with uncertainty evidence preserved for provenance and future evolution
rather than converted into definite prose.
