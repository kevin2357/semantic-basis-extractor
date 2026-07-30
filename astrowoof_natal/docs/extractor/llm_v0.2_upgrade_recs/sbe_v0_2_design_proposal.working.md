# Semantic Basis Extractor v0.2 Design Proposal

**Status:** Publication Draft  
**Architectural completion:** Complete  
**Editorial status:** Holistically edited; one historical recommendation gap remains documented  
**Version:** 0.2

## Executive Summary

The Semantic Basis Extractor (SBE) is the deterministic compression layer between a complete projected semantic graph and a bounded downstream authoring portfolio. It does not construct the source graph and does not write final narrative prose. Its responsibility is to preserve the most useful, coherent, traceable, and sufficiently diverse semantic claims under explicit budget constraints.

The proposal’s central architectural conclusion is that SBE should be understood as a **portfolio optimizer**, not as a relationship-ranking algorithm. Individual candidates matter, but selection quality depends on bundle closure, redundancy, coverage, provenance, canonical identity, compatibility, and replayable execution. The recommendations therefore evolve candidate generation, utility calibration, portfolio selection, observability, artifact contracts, operational governance, and long-term maintainability as one connected system.

Version 0.2 favors evolutionary refinement over architectural replacement. New behavior is introduced through deterministic candidate families, explicit metrics, stable registries, governed schemas, reproducible configuration, and conformance testing. Existing graph fidelity and downstream authoring boundaries remain intact.

## Purpose and Scope

This document is a companion to the existing implementation specification. It has four purposes:

1. Explain the architectural rationale behind the existing design.
2. Evaluate the design using empirical observations gathered from a real projected chart used as a running case study.
3. Propose compatible extensions that improve semantic preservation under bounded budgets.
4. Define the operational, testing, replay, packaging, and governance contracts required for a durable implementation.

The proposal does not redefine projected-graph construction or final editorial generation. It focuses on the extraction layer and the contracts immediately surrounding it.

## Intended Audience

This proposal is written for:

- architects responsible for Semantic Projection Core boundaries;
- implementers building or extending SBE;
- reviewers evaluating deterministic behavior and semantic fidelity;
- QA engineers maintaining fixtures, replay tests, and conformance suites;
- downstream consumers relying on stable authoring-packet contracts;
- future maintainers evolving the architecture without losing traceability.

## How to Read This Proposal

The document is organized as a sequence of stable recommendation identifiers.

- Early recommendations focus on candidate generation and utility.
- Middle recommendations focus on portfolio behavior, candidate-family governance, identity, canonicalization, and provenance.
- Later recommendations define pipeline, diagnostics, outputs, replay, configuration, deployment, security, performance, testing, extensibility, and publication governance.

Normative language such as **must**, **should**, and **required** expresses architectural expectations. Examples, rationale, and case-study observations are informative unless a recommendation explicitly incorporates them into a contract.

## Architectural Position

The Semantic Projection Core separates four concerns:

- graph construction;
- semantic basis extraction;
- editorial generation;
- deterministic validation.

SBE is the architectural bridge between complete semantic representation and constrained authoring. It determines which semantic claims can be preserved within a limited editorial budget while maintaining coherence, dependency closure, and deterministic behavior.

## Design Philosophy

The current implementation is treated as fundamentally successful. Recommendations are therefore evolutionary rather than revolutionary. Wherever practical, they should be realized as:

- deterministic candidate generators;
- additional utility metrics;
- optimizer refinements;
- improved validation;
- versioned configuration;
- stronger artifact and replay contracts.

Replacing established architectural boundaries is out of scope for Version 0.2.

## Recommendation Index

| ID | Recommendation | Publication status |
|---|---|---|
| REC-001 | Axis-Aware Candidate Generation | Included |
| REC-002 | Configuration Completion Bonus | Included |
| REC-003 | Hub Preservation | Included |
| REC-004 | Structural Inevitability Penalty | Reserved; chapter absent from source history |
| REC-005 | Utility Vector Diversity | Included |
| REC-006 | Utility Vector Calibration | Included |
| REC-007 | Marginal Bundle Comparison and Selection Stability | Included |
| REC-008 | Portfolio Drift and Stability Metrics | Included |
| REC-009 | Portfolio Coverage Metrics | Included |
| REC-010 | Coverage Targets and Budget Allocation | Included |
| REC-011 | Candidate Family Expansion Strategy | Included |
| REC-012 | Candidate Family Lifecycle | Included |
| REC-013 | Candidate Family Deprecation and Compatibility | Included |
| REC-014 | Candidate Family Composition | Included |
| REC-015 | Cross-Family Conflict Resolution | Included |
| REC-016 | Cross-Family Provenance | Included |
| REC-017 | Stable Candidate Identity | Included |
| REC-018 | Candidate Canonicalization | Included |
| REC-019 | Candidate Registry and Schema Governance | Included |
| REC-020 | End-to-End Candidate Processing Pipeline | Included |
| REC-021 | Completion Log and Execution Diagnostics | Included |
| REC-022 | Output Profiles | Included |
| REC-023 | Artifact Packaging and Manifest Contracts | Included |
| REC-024 | Replay and Reproducibility Contracts | Included |
| REC-025 | Operational Configuration and Feature-Flag Governance | Included |
| REC-026 | Operational Deployment and Lifecycle Guidance | Included |
| REC-027 | Security, Integrity, and Trust Boundaries | Included |
| REC-028 | Performance, Scalability, and Resource Management | Included |
| REC-029 | Testing Strategy and Regression Governance | Included |
| REC-030 | Reference Implementation and Extensibility | Included |
| REC-031 | Documentation Standards and Future Evolution | Included |
| REC-032 | Final Integration, Appendices, and Publication Guidance | Included |
| REC-033 | Editorial Consistency and Publication Readiness | Included |
| REC-034 | Publication Closure and Version 0.2 Release | Included |

### Historical numbering note

The source history names **REC-004 — Structural Inevitability Penalty**, but the supplied proposal contains no REC-004 chapter and the design ledger contains no REC-004 entry. This publication draft preserves the identifier as a documented gap. It does not reconstruct or infer missing normative content.

## Cross-Reference Guide

The recommendations form several connected groups:

- **Candidate construction and utility:** REC-001 through REC-010.
- **Candidate-family governance:** REC-011 through REC-016.
- **Identity, canonicalization, registry, and pipeline:** REC-017 through REC-020.
- **Diagnostics, outputs, packaging, and replay:** REC-021 through REC-024.
- **Operational governance:** REC-025 through REC-029.
- **Implementation, documentation, and publication:** REC-030 through REC-034.

Key relationships include:

- canonical identity (REC-017) supports canonicalization (REC-018), registry governance (REC-019), replay (REC-024), and regression testing (REC-029);
- provenance (REC-016) supports completion logs (REC-021), manifests (REC-023), replay (REC-024), and integrity controls (REC-027);
- output profiles (REC-022) interact with packaging (REC-023), configuration (REC-025), and resource management (REC-028);
- testing governance (REC-029) validates the complete processing pipeline established by REC-020.

---

# REC-001 — Axis-Aware Candidate Generation

## Problem Statement

Angular relationships present a unique challenge for Semantic Basis Extraction because they simultaneously encode individualized information and structurally inevitable geometry. A projected graph may legitimately contain claims such as "Moon conjunct Ascendant", "Moon opposite Descendant", and "Ascendant opposite Descendant". Although all three relationships are true, they do not contribute equally to semantic understanding when editorial budget is limited.

The current architecture correctly preserves these relationships within the canonical graph. The question addressed by this recommendation is not whether those relationships should exist, but how they should compete for inclusion in a bounded semantic basis.

## Architectural Context

SBE operates after graph construction. It therefore inherits a graph whose correctness is already established. Candidate generation should not discard or rewrite graph edges. Instead, it should synthesize additional candidate claims that better represent recurring semantic patterns while preserving traceability to the originating relationships.

This distinction preserves a critical architectural boundary: graph fidelity remains the responsibility of projection, while representational efficiency becomes the responsibility of SBE.

## Current Behavior

The current implementation evaluates relationship candidates independently before portfolio optimization assembles a dependency-closed authoring packet. This behavior is deterministic and architecturally sound. However, independent angular relationships may occupy multiple portfolio slots while communicating nearly identical semantic content.

## Running Example (Bre)

Comparison of Bre's complete projected graph against the selected semantic packet suggested that several angular relationships survived independently even though they collectively described a single behavioral axis. Meanwhile, other graph neighborhoods containing richer individualized structure competed for the same editorial budget.

This observation motivated the proposal but should not be interpreted as evidence of an implementation defect. The current selection remains internally coherent. Rather, it demonstrates an opportunity to express equivalent semantic content more compactly.

## Proposed Evolution

Introduce an optional deterministic candidate generator capable of recognizing complementary angular pairs. Rather than replacing the underlying graph relationships, the generator would emit synthesized candidates such as:

- Moon on the ASC–DSC axis
- Sun on the MC–IC axis

Each synthesized candidate would retain explicit provenance linking it to every contributing graph relationship. Existing relationship candidates would remain available to the optimizer, preserving backward compatibility.

## Compatibility Analysis

This recommendation requires no changes to graph construction, projection contracts, or downstream editorial interfaces. Candidate generation simply gains an additional deterministic family. Existing portfolios remain valid, and deployments may enable the generator incrementally for comparative QA.

## QA Strategy

Validation should compare baseline and enhanced portfolios using identical projected graphs. Success metrics include preservation of semantic coverage, reduced redundancy, and improved opportunity for non-angular graph neighborhoods to enter the portfolio. Determinism must be preserved across repeated executions.

## Complexity / Benefit / Risk

Implementation Complexity: Low

Expected Benefit: High

Architectural Risk: Low

## Summary

Axis-aware candidate generation exemplifies the philosophy of this proposal: preserve the existing architecture, enrich deterministic candidate generation, and allow the existing optimizer to make better-informed portfolio decisions without sacrificing traceability or compatibility.

---

# REC-002 — Configuration Completion Bonus

## Problem Statement

The current Semantic Basis Extractor evaluates a projected graph at two levels simultaneously. At the candidate level, it assigns a multidimensional utility vector to atomic objects, relationships, and deterministic syntheses. At the portfolio level, it selects dependency-closed bundles according to marginal utility, behavioral-domain novelty, and bundle efficiency. This architecture already prevents several common selection failures: an edge cannot survive without its endpoint objects, a synthesis cannot survive without its supporting premises, and a candidate that appears individually strong may still lose when its closure cost is excessive.

What the current scoring model does not yet represent directly is the value of **completing a recognizable multi-edge configuration** once part of that configuration has already entered the portfolio.

A configuration is more than a set of individually useful edges. It is a locally coherent structure in which the joint interpretation depends on preserving enough of the pattern to expose its internal organization. Two selected relationships may imply that three systems repeatedly regulate one another; a third relationship may be what distinguishes a complete triangular pattern from two unrelated dyads. Conversely, a portfolio may select one conspicuous edge from several different structures and thereby achieve broad edge coverage while preserving fewer interpretable wholes.

This is not equivalent to the existing dependency-closure problem. Dependency closure asks whether every premise required to understand a selected candidate is present. Configuration completion asks whether the selected portfolio has preserved enough mutually related claims to expose a larger graph motif that is not itself a formal dependency of any one atomic edge.

Nor is configuration completion equivalent to centrality. Centrality rewards load-bearing nodes and edges, but it cannot by itself distinguish between a portfolio that samples three unrelated relationships around a hub and a portfolio that preserves a semantically coherent regulatory circuit around the same hub.

The proposed refinement therefore adds a small, deterministic **configuration completion bonus** to portfolio evaluation. Its purpose is not to privilege traditional astrological pattern names, force every recognized configuration into the deck, or replace existing candidate families. Its purpose is narrower: when two otherwise comparable bundles compete, prefer the bundle that completes a well-supported, semantically coherent graph motif already partially represented in the selected portfolio.

## Architectural Context

The current SBE specification already contains the architectural prerequisites for this refinement.

Whole-graph analysis occurs before candidate selection and records repeated relationship structures, structural bridges, reinforcing regions, tension-heavy regions, object degree, and graph hubs. The candidate contract supports synthesized motifs with explicit dependencies, source references, evidence, provenance, and deterministic generation rules. The future-generator section explicitly reserves space for graph communities, polarity chains, strongly connected tension clusters, configuration-like structures, dispositional or operator chains, and cross-domain regulatory sequences.

REC-002 therefore does not introduce a new architectural layer. It formalizes one use of information the extractor already computes and one family of candidates the contract already permits.

The recommendation also fits the current optimizer cleanly. V0.1 selects the highest-valued dependency-closed bundle by combining mean utility, domain novelty, and a small bundle-efficiency preference. A configuration completion bonus can be added as another marginal portfolio term without changing:

- graph construction;
- candidate identity;
- semantic closure;
- budget accounting;
- packet compilation;
- the LLM editing boundary;
- or the auditability of the final selection.

The key architectural constraint is that configuration recognition must remain deterministic and evidence-bound. The extractor may recognize a pattern only from relationships actually present in the supplied projected graph. It may not infer missing edges, repair an incomplete pattern by interpretation, or import chart facts that were not projected into the target ontology.

## Current Behavior

V0.1 already provides several mechanisms that partially protect configurations:

1. **Whole-graph analysis** can detect repeated structures and motif participation.
2. **Centrality** rewards objects and relationships located in connected regions.
3. **Structural score** rewards strong projected relationships.
4. **Relationship-interaction syntheses** can summarize repeated interaction modes.
5. **Relationship-theme syntheses** can summarize repeated theme tags.
6. **Compression** rewards syntheses that organize several premises.
7. **Marginal domain novelty** discourages repeated coverage of the same behavioral territory.
8. **Exact closure cost** prevents an apparently efficient synthesis from hiding expensive prerequisites.

These mechanisms make the current architecture much more graph-aware than a flat top-N ranking scheme. They also explain why REC-002 should be modest rather than dominant. SBE is not currently blind to graph structure; it simply lacks an explicit preference for completing a motif whose value emerges from the relationship among several already-supported claims.

Consider three projected objects, A, B, and C, with relationships A–B, B–C, and A–C. Suppose A and B are mandatory anchors and C has already entered the portfolio for another reason. If A–B and B–C are selected, adding A–C may require only one remaining slot. Under the current model, that final edge competes according to its own utility and the novelty it adds. The optimizer does not receive an explicit signal that selecting A–C changes the retained structure from an open chain into a closed configuration.

The final edge should not automatically win. It may be weak, redundant, poorly projected, or narratively unproductive. But when its ordinary utility is credible and its addition completes a coherent motif, the portfolio-level value of that bundle is greater than the edge's isolated score expresses.

The inverse case also matters. If a proposed configuration requires several low-value dependencies, its completion bonus must not disguise the true budget cost. The current closure machinery should continue charging for every newly retained premise. REC-002 rewards structural completion only after exact bundle cost is known.

## Empirical Evidence: Bre's Developmental Regulation Cluster

Bre's projected graph provides a concrete example involving three mandatory or near-mandatory semantic systems:

- **Comfort and Regulation** (Moon), operating through body, temperament, and presence;
- **Training Rule Structure** (Saturn), operating through training, routine, and care;
- **Training Development Vector** (North Node), also operating through training, routine, and care.

The full graph contains the following relationships among these systems:

- Training Rule Structure and Training Development Vector are linked through **subsystems run together**;
- Comfort and Regulation and Training Rule Structure are linked through **awkward system recalibration**;
- Comfort and Regulation and Training Development Vector are also linked through **awkward system recalibration**.

This is not merely a list of three independent pairings. Taken together, the relationships define a developmental regulation configuration:

1. Saturn and the North Node operate as an inseparable training-development subsystem.
2. The Moon requires recalibration with Saturn's rules and routines.
3. The Moon also requires recalibration with the direction of developmental practice itself.

The complete motif supports a richer interpretation than any single edge. Training is not an external discipline added to an otherwise unrelated temperament. It is intertwined with the dog's developmental direction, while emotional and bodily regulation repeatedly negotiate with both the rule structure and the learning trajectory. In practical AstroWoof terms, routine, emotional safety, and developmental practice form one coordinated problem space.

The selected authoring packet preserves several important pieces of this structure:

- the mandatory Moon placement;
- the mandatory Saturn placement;
- the mandatory North Node orientation;
- the Saturn–North Node relationship;
- and a synthesized recurring theme around training-rule structure.

That selection is coherent and defensible. It captures the central fact that discipline and developmental practice run together, and it preserves the three endpoint objects required to understand the larger configuration. The packet therefore does not lose the region entirely.

However, the two Moon-linked recalibration edges are not both required by any selected candidate, and the optimizer can treat them as ordinary competitors. If neither survives, the portfolio retains the training-development axis but may understate the role of emotional and bodily regulation in that developmental system. If one survives but the other does not, the result may imply a dyadic adjustment problem rather than a repeated regulatory pattern spanning both structure and developmental direction.

This example illustrates the precise scope of REC-002. The proposal is not that all three edges must always be selected. It is that, once the portfolio contains all three objects and one or two of the relationships, the marginal value of completing the motif should be visible to the optimizer.

The same graph also shows why the bonus must remain disciplined. Bre's Moon is highly connected. It participates in relationships involving the Ascendant, Descendant, Pluto, Venus, Jupiter, Saturn, and the North Node. A naive "complete every triangle" rule would over-select the Moon neighborhood and crowd out cognition, values, novelty response, trust, and other distinct chart regions. Configuration completion must therefore reward specific qualified motifs rather than raw edge density.

## Proposed Evolution

REC-002 introduces two related but separable mechanisms:

1. deterministic configuration detection during whole-graph analysis; and
2. a bounded marginal completion bonus during portfolio optimization.

The first mechanism identifies candidate motifs. The second uses those motifs as portfolio context.

### 1. Configuration detection

Whole-graph analysis should emit a normalized configuration registry. Each record should contain at minimum:

```json
{
  "configuration_id": "configuration_<stable_hash>",
  "configuration_type": "closed_regulatory_triangle",
  "member_object_refs": ["...", "...", "..."],
  "member_relationship_refs": ["...", "...", "..."],
  "projected_operator_signature": ["..."],
  "behavioral_domains": ["..."],
  "coherence_score": 0.0,
  "structural_support": 0.0,
  "generation_rule": "configuration_triangle.v1",
  "provenance": {"...": "..."}
}
```

The registry is analysis output, not automatically a candidate pool. It records graph facts that later generators and the optimizer may use.

V0.2 should begin with a deliberately narrow configuration vocabulary. Recommended initial types are:

- **closed regulatory triangle**: three objects connected by three projected relationships whose interaction modes form a coherent regulation, reinforcement, or tension pattern;
- **open regulatory chain**: three or more objects joined in sequence where the middle object acts as a bridge and the relationship semantics describe a plausible directional or regulatory sequence;
- **reinforcement cluster**: three or more objects connected by repeated compatible relationship modes or theme tags;
- **mixed tension-support cluster**: a small motif in which one supportive relationship appears to stabilize or channel two tension relationships.

These names describe projected semantic structures, not traditional astrological configurations. A future implementation may optionally preserve source configuration labels as provenance, but source labels should not determine whether a projected motif exists.

### 2. Qualification rules

A detected motif should qualify for a completion bonus only when it satisfies all of the following:

- every member edge exists in the projected graph;
- every member edge has complete source provenance;
- the motif contains between three and a configured small maximum number of objects;
- its projected relationship semantics pass a deterministic coherence rule;
- at least one member relationship exceeds a minimum structural or relevance threshold;
- the motif is not composed solely of structural inevitabilities;
- its normalized signature is not a duplicate of another registered motif;
- and completion would not rely on inferred, missing, or editor-created premises.

The coherence rule should be explicit and conservative. For example, two `awkward_system_recalibration` edges plus one `subsystems_run_together` edge can form a qualified developmental regulation triangle because the repeated recalibration semantics converge on a tightly coupled subsystem. Three unrelated relationship modes connected only by shared endpoints should not automatically qualify.

### 3. Marginal completion state

For each candidate bundle under consideration, the optimizer should evaluate the status of every qualified configuration after applying the bundle's dependency closure.

A simple state model is sufficient:

- `0.0`: no meaningful representation;
- `0.33`: one member relationship selected;
- `0.67`: two member relationships selected or an approved synthesis plus one premise;
- `1.0`: configuration representationally complete.

The exact fractions are configuration-specific and should be derived from member count rather than hard-coded globally. More importantly, the optimizer should score the **change in completion state**, not the absolute existence of the motif. This keeps the term marginal and prevents a completed configuration from receiving the same bonus repeatedly.

### 4. Completion bonus

The bundle-level expression can be extended as follows:

```text
marginal bundle utility
    = mean utility of newly retained claims
    + domain novelty bonus
    + configuration completion bonus
    + small bundle-efficiency tie breaker
```

The completion bonus should be bounded and low enough that it cannot rescue a poor bundle. A reasonable initial implementation is:

```text
completion bonus
    = configured weight
    × increase in completion state
    × configuration coherence
    × configuration structural support
```

The configured weight should initially be smaller than the domain novelty term. The bonus is intended to resolve close portfolio decisions, not overturn the utility vector.

### 5. Optional configuration synthesis candidate

The completion bonus can be implemented without adding a user-visible synthesized claim. This is the recommended first step.

A later generator may create an explicit configuration synthesis when the motif itself has high narrative yield and compression value. In Bre's case, a deterministic synthesis might state:

> Comfort regulation, training structure, and developmental practice form one recurring adjustment system: rules and growth work best when bodily safety is regulated alongside them.

Such a candidate would depend on the three object claims and the qualifying relationship premises selected by the generator's evidence policy. It would compete normally, incur exact closure cost, and preserve every source reference.

Separating the optimizer bonus from the synthesis generator is important. Structural completion may improve a portfolio even when the final authoring packet should represent the motif through its constituent cards rather than through a dedicated summary card.

## Candidate-Contract Implications

The existing candidate contract does not require breaking changes. Two optional additions would make configuration participation easier to audit:

- `configuration_refs`: qualified whole-graph configurations in which the candidate participates;
- `configuration_roles`: endpoint, bridge, stabilizer, tension leg, reinforcement leg, or compressor.

These fields should remain derived metadata. They do not become dependencies unless a specific synthesized candidate declares them as such.

The score vector may also expose a non-weighted `configuration_participation` diagnostic. The actual completion bonus belongs in the selection audit because it depends on portfolio state and cannot be represented faithfully as a fixed candidate score.

This distinction mirrors the current separation between candidate-level coverage and portfolio-level marginal novelty. Configuration participation is a candidate fact; configuration completion is a portfolio event.

## Optimizer Implications

REC-002 preserves deterministic greedy selection. At each decision, after computing transitive closure and rejecting over-budget bundles, the optimizer performs one additional calculation: whether adding the bundle increases the completion state of any qualified configurations.

The deterministic selection tuple should record:

- base marginal bundle utility;
- domain novelty bonus;
- configuration completion bonus;
- bundle-efficiency tie-breaker;
- total marginal selection value;
- completed or advanced configuration IDs.

Candidate ID remains the final deterministic tie-breaker.

The computational cost is manageable for the proposed small-motif profile. Configuration detection can occur once during whole-graph analysis. During greedy selection, completion state can be maintained incrementally using sets of selected relationship IDs. The implementation need not enumerate arbitrary subgraphs at every selection step.

The most important optimizer safeguard is **anti-stacking**. A single newly selected edge may participate in several overlapping configurations. Without a cap, one highly connected edge could collect several completion bonuses and recreate the hub-dominance problem that the utility vector already guards against. Recommended controls are:

- cap total configuration bonus per bundle;
- discount overlapping configurations that share most members;
- award only the highest-value completion event when normalized signatures are near-duplicates;
- and expose all suppressed bonuses in the audit.

## Compatibility Analysis

REC-002 is backward-compatible at the architectural and artifact-contract levels.

Existing projected graphs remain valid. Existing candidate generators remain valid. Existing packets remain valid. The recommendation changes only selection behavior when the feature is enabled, weights are configured, and a qualified motif is partially represented.

The feature should initially ship behind a profile flag such as:

```json
{
  "configuration_completion": {
    "enabled": false,
    "weight": 0.03,
    "max_bonus_per_bundle": 0.04,
    "max_configuration_size": 4
  }
}
```

A disabled default allows baseline reproduction of v0.1 portfolios. Comparative QA can then run the same graph through baseline and experimental profiles.

The recommendation does not require changes to the downstream LLM editing boundary. Selected atomic relationships and syntheses continue to arrive as locked evidence-bound claims. The editor is not asked to recognize configurations independently and is not permitted to restore discarded edges from the structural seed.

## Alternatives Considered

### Alternative A: Select every recognized configuration

This approach was rejected because it treats motif recognition as a mandate rather than one source of utility. Dense charts can contain many overlapping configurations, and mandatory inclusion would rapidly consume the fixed budget.

### Alternative B: Generate only configuration synthesis candidates

This is compatible with the architecture but incomplete as a first solution. A synthesis incurs dependency cost and consumes an additional claim slot. Some configurations are worth preserving through their component edges even when no dedicated summary card is warranted.

### Alternative C: Increase centrality weight

Increasing centrality would reward graph hubs generally, not completed motifs specifically. It would likely amplify already dominant objects and could reduce semantic breadth.

### Alternative D: Add configuration value directly to each candidate's fixed score

This was rejected because completion is portfolio-relative. An edge that completes a motif after two related edges are selected has different marginal value from the same edge considered at the beginning of selection. Encoding that value as a static score would obscure the actual reason for selection.

### Alternative E: Use a global mixed-integer optimizer immediately

A global optimizer could encode configuration variables elegantly, but replacing deterministic greedy selection is unnecessary for validating the recommendation. The current optimizer can support the marginal term with substantially lower implementation risk. Beam search or mixed-integer optimization remains future work if greedy local decisions prove insufficient.

## QA Strategy

REC-002 requires both unit-level and portfolio-level QA.

### Detection QA

Fixtures should verify that:

- qualified motifs are recognized with stable IDs;
- missing edges prevent false completion;
- duplicate directional relationships normalize to one motif;
- structurally inevitable angle-only patterns do not qualify;
- incoherent edge collections do not qualify;
- provenance includes every member object and relationship;
- repeated runs produce identical configuration registries.

### Optimizer QA

Synthetic portfolios should establish that:

- a credible final edge can receive a bounded bonus when it completes a qualified motif;
- the same edge receives no completion bonus when prerequisite members are absent;
- the bonus is awarded only once;
- closure cost remains fully charged;
- a low-utility edge does not win solely because of completion;
- overlapping motifs respect anti-stacking caps;
- disabling the feature reproduces the baseline selection exactly.

### Bre regression fixture

Bre's Moon–Saturn–North Node cluster should become a named regression fixture. The audit should show:

- which three relationships form the qualified developmental regulation triangle;
- which members are present before each relevant selection step;
- whether a candidate bundle advances or completes the motif;
- the unmodified base utility;
- the bounded completion bonus;
- and the final selection decision.

The expected test should not hard-code that all three edges must enter every fifty-card portfolio. It should hard-code the correctness of detection and the transparency of scoring. Selection outcome may vary legitimately when profile weights or candidate families change.

### Comparative portfolio review

For a corpus of projected charts, compare baseline and experimental portfolios on:

- number of qualified motifs;
- fraction partially represented;
- fraction completed;
- total behavioral-domain coverage;
- object and domain concentration;
- dependency cost;
- redundancy;
- and manual assessment of whether completed motifs improve whole-chart reconstructability.

This final criterion aligns directly with the SBE governing principle: preserve the smallest fixed portfolio that lets a downstream author reconstruct the most complete and distinctive projected natal story.

## Implementation Sequence

A staged implementation minimizes risk.

### Stage 1 — Analysis only

Add deterministic configuration detection and emit the registry in whole-graph analysis. Do not change candidate scores or selection.

### Stage 2 — Audit-only simulation

Calculate hypothetical completion bonuses during optimization and record them in a shadow audit without changing the winning bundle.

### Stage 3 — Experimental profile

Enable the bonus under a non-default profile and compare packet outcomes against v0.1 baselines.

### Stage 4 — Optional synthesis generator

After configuration semantics and QA stabilize, add explicit synthesis candidates for the highest-yield motif families.

### Stage 5 — Weight calibration

Calibrate the bonus against a broader corpus and decide whether it belongs in the default AstroWoof natal-card profile.

This sequence preserves reproducibility and makes each behavioral change independently reviewable.

## Complexity / Benefit / Risk

**Implementation Complexity:** Medium

Detection of small qualified motifs is straightforward, but semantic coherence rules, overlap normalization, and audit clarity require careful design.

**Expected Benefit:** Medium to High

The likely benefit is highest for charts where distinctive meaning is carried by compact multi-edge regulatory structures rather than by isolated high-scoring relationships. It should improve whole-chart reconstructability without materially increasing packet size.

**Architectural Risk:** Low to Medium

The feature fits existing boundaries, but an over-weighted or overly permissive implementation could favor dense hubs, reduce domain breadth, and make selection harder to explain. Conservative qualification rules, bounded bonuses, feature flags, and shadow-audit rollout reduce this risk.

## Decision and Summary

REC-002 should be accepted for staged implementation as a portfolio-level refinement built on deterministic whole-graph configuration detection.

The current SBE already preserves semantic closure, evaluates exact bundle cost, rewards centrality and compression, and supports future configuration-like generators. The proposed completion bonus extends those capabilities without recasting the extractor as a traditional configuration detector or replacing its optimizer.

Bre's developmental regulation cluster demonstrates the value of the refinement. The Moon, Saturn, and North Node are already present, and the Saturn–Node relationship is strong enough to survive. The remaining Moon-linked recalibration edges determine whether the packet represents a complete developmental regulation system or only its most conspicuous dyad. REC-002 gives that difference a small, explicit, auditable place in portfolio evaluation.

The governing rule remains unchanged: configuration completion is never sufficient reason to select weak material. It is a bounded preference for retaining coherent wholes when the underlying claims are already credible, evidence-bound, and affordable within the fixed semantic budget.

# REC-003 — Hub Preservation

## Problem Statement

The existing optimizer reasons primarily over individual semantic candidates and their dependency closures. While this produces coherent portfolios, highly connected regions of the projected semantic graph may still become fragmented when multiple medium-value edges compete for a limited authoring budget. The resulting portfolio accurately represents many local truths while under-representing a graph's principal semantic hubs.

## Architectural Context

Graph hubs are not merely high-degree nodes. Within projected semantic graphs they frequently correspond to regions where multiple independent operators converge on a common behavioral theme. Preserving such neighborhoods improves structural fidelity without requiring exhaustive preservation of every incident edge.

Importantly, this proposal does **not** recommend assigning static bonuses to planets or angles themselves. Hub preservation is instead a property of the *local topology* of a projected graph. A dense neighborhood around the Moon, for example, should only receive additional consideration when independent projected relationships collectively indicate that the Moon functions as a semantic organizing center within the specific graph under evaluation.

## Running Example (Bre)

Comparison between Bre's complete projected graph and the selected semantic basis identified several localized neighborhoods whose semantic cohesion exceeded what was visible from any individual relationship. The Moon–Saturn–North Node cluster is one example discussed previously, but similar effects were observed around angular interactions where multiple edges collectively described a single behavioral regulatory pattern.

Under the proposed approach the optimizer remains free to select whichever individual claims best satisfy the editorial budget. However, modest additional utility is awarded when those selections preserve the recognizable neighborhood rather than scattering isolated edges across unrelated regions of the graph.

## Proposed Evolution

A deterministic Hub Analyzer executes after candidate generation and before final portfolio optimization.

Responsibilities:

* identify graph neighborhoods exceeding configurable density thresholds;
* assign stable hub identifiers;
* compute neighborhood coverage contributed by each candidate bundle;
* expose hub-coverage metrics to the existing utility vector.

The optimizer itself is unchanged. Hub preservation simply becomes another measurable utility dimension participating alongside existing portfolio objectives.

## Compatibility

This proposal is fully backward compatible.

Projects disabling hub analysis continue producing byte-for-byte identical results. Existing candidate schemas require only optional metadata fields identifying associated hub IDs.

## QA Strategy

Regression fixtures should verify:

* deterministic hub detection;
* identical outputs when feature flags are disabled;
* monotonic improvement of neighborhood coverage on reference graphs;
* no regression in dependency closure or determinism.

## Complexity / Benefit / Risk

Implementation complexity: Medium

Expected benefit: High for dense projected graphs; Low for sparse graphs.

Architectural risk: Low. The proposal augments candidate metadata and utility evaluation without altering graph construction or editorial generation.

## Summary

Hub Preservation extends the existing portfolio philosophy rather than replacing it. It recognizes that preserving the semantic identity of a graph sometimes depends less on maximizing isolated edge quality than on maintaining coherent representations of its principal neighborhoods. Because the recommendation is implemented as an additive utility signal, it complements earlier proposals such as REC-001 and REC-002 while preserving deterministic behavior and existing architectural boundaries.

# REC-005 — Utility Vector Diversity

## Problem Statement

As candidate families expand, multiple candidates may encode substantially overlapping semantic information while differing only in presentation. Even with deterministic scoring, repeated selection of closely related claims can reduce the informational breadth of the final semantic basis.

## Architectural Context

This recommendation does not replace the existing utility vector. Instead it introduces a bounded diversity component that rewards incremental semantic coverage after dependency closure has been satisfied.

## Running Example (Bre)

Within Bre's projected graph, multiple regulatory and relational candidates describe closely related developmental themes. A diversity-aware utility component encourages preservation of complementary perspectives rather than repeated descriptions of the same underlying semantic region.

## Proposed Evolution

Introduce a deterministic Diversity Utility computed from previously selected semantic domains, graph neighborhoods, and configuration families. The score should be intentionally bounded so that it never overrides strong structural or dependency requirements.

The diversity component should:
- reward novel semantic regions,
- discourage redundant formulations,
- remain deterministic,
- preserve optimizer stability.

## Compatibility

Backward compatible. Existing scoring behavior is preserved when the diversity term is disabled or weighted to zero.

## QA Strategy

Regression fixtures should verify:
- deterministic selection,
- stable outputs across repeated execution,
- increased semantic coverage without regression in dependency closure.

## Complexity / Benefit / Risk

Implementation Complexity: Medium

Expected Benefit: High

Architectural Risk: Low

## Summary

REC-005 complements REC-001 through REC-004 by improving portfolio breadth rather than introducing additional candidate families. It operates entirely within the existing optimization philosophy while encouraging broader semantic representation under fixed editorial budgets.

# REC-006 — Utility Vector Calibration

## Problem Statement

The existing Semantic Basis Extractor already evaluates candidates through a multi-dimensional utility model rather than a single undifferentiated score. That architecture is a major strength: it allows salience, structural relevance, semantic novelty, dependency cost, and portfolio fit to remain conceptually distinct even when the optimizer ultimately requires a comparable decision value.

As additional candidate generators and portfolio-aware refinements are introduced, however, the relationship among those utility components becomes increasingly important. A scoring term that behaves reasonably in isolation may dominate unexpectedly when combined with another term, become effectively inert at realistic value ranges, or create discontinuities near selection thresholds. These effects are especially likely when new recommendations introduce bounded bonuses or penalties at different semantic scales:

- REC-001 introduces axis-aware representations that may compete with their source relationships;
- REC-002 rewards completion of qualified configurations;
- REC-003 rewards preservation of semantically important neighborhoods;
- REC-004 discounts structurally inevitable relationships;
- REC-005 rewards incremental portfolio diversity.

Without an explicit calibration discipline, the utility vector can gradually become a collection of individually plausible terms whose combined behavior is difficult to reason about. The danger is not merely that a weight may be “too high” or “too low.” The more serious risk is that future maintainers may no longer be able to predict which architectural objective controls a decision, reproduce why a candidate entered the portfolio, or adjust one dimension without unintentionally destabilizing several others.

REC-006 therefore proposes a deterministic calibration framework for the utility vector. Its purpose is not to replace the existing scoring system, flatten it into a single universal metric, or introduce machine-learned ranking. Its purpose is to make the current multi-objective design measurable, testable, and evolvable.

## Architectural Context

SBE solves a constrained portfolio problem. At each decision point, a candidate is not evaluated solely as an isolated claim. The optimizer must consider the candidate together with any required dependency closure, the remaining budget, overlap with already selected material, and the marginal contribution of the resulting bundle.

That means utility exists at several related but non-identical levels:

1. **Intrinsic candidate utility**  
   The value attributable to the candidate before considering the current portfolio.

2. **Bundle utility**  
   The value of the candidate plus any dependencies required to make it valid and authorable.

3. **Marginal portfolio utility**  
   The incremental value of adding that closed bundle to the portfolio already selected.

4. **Portfolio objective value**  
   The value of the complete selected basis under global coverage, diversity, coherence, and budget constraints.

These levels should not be collapsed conceptually even if the implementation uses a compact scoring representation. A calibration procedure that observes only final aggregate scores cannot identify whether unexpected behavior arises from candidate salience, closure cost, redundancy, configuration completion, hub coverage, or another component.

REC-006 therefore treats calibration as an architectural observability problem. The utility vector should expose enough structured information to answer three questions for every meaningful selection decision:

- What values were assigned to each utility component?
- How were those values normalized and combined?
- Which component or interaction changed the selection outcome?

The recommendation preserves the current deterministic optimizer and adds an explicit calibration layer around it.

## Current Behavior

The current specification already contains the conceptual ingredients needed for calibration:

- utility is represented as a vector rather than a single opaque judgment;
- candidates retain provenance;
- dependency closure is explicit;
- selection is deterministic;
- the optimizer evaluates marginal bundle value;
- output generation and validation are separated from selection.

These properties make SBE unusually well positioned for rigorous calibration. The system does not need to be redesigned to become observable. It needs a standardized way to collect, compare, and interpret the values it already computes.

The principal limitation is that scoring parameters and their interactions are not yet treated as a versioned calibration profile with a stable evaluation protocol. As a result, a future weight adjustment could be deterministic and locally reasonable while still causing broad portfolio drift that is difficult to distinguish from an intended improvement.

## Running Example: Bre

Bre’s projected natal graph is useful for calibration because it contains several forms of competition that exercise different parts of the utility model.

One region contains a developmental-regulation cluster involving the Moon, Saturn, and the North Node. Depending on candidate generation and closure behavior, the optimizer may encounter:

- individual relationship candidates carrying emotional, regulatory, and developmental meaning;
- a configuration-level interpretation that integrates those relationships;
- neighboring claims connected through the same semantic hub;
- alternative candidates that express similar themes with different authoring costs.

Another region contains angular relationships whose source graph may include both individually diagnostic contacts and structurally inevitable geometry. Axis-aware synthesis may create a candidate that compresses several source relationships, while REC-004 may reduce the utility of purely structural angle relations.

These regions create several calibration questions:

- How large must a configuration-completion bonus be before the integrated motif reliably survives?
- At what point does that bonus overpower clearly more salient unrelated material?
- How should the hub-preservation term behave when one strong edge already represents part of the neighborhood?
- How much should structural inevitability reduce utility without suppressing genuinely individualized angular meaning?
- How strongly should diversity reward a new semantic region when the competing candidate is intrinsically more salient?
- Does an axis-synthesized candidate receive an unfair advantage because it compresses several sources into one authoring unit?

A useful calibration framework must answer these questions empirically rather than through intuition alone.

For example, consider two hypothetical closed bundles:

**Bundle A — Developmental configuration**
- moderate intrinsic salience;
- high configuration coherence;
- moderate closure cost;
- partial overlap with an already represented emotional-regulation theme;
- strong contribution to configuration completion.

**Bundle B — Independent relational claim**
- high intrinsic salience;
- no configuration bonus;
- low closure cost;
- high semantic novelty;
- no hub-preservation contribution.

A calibration profile should make it possible to explain why either bundle wins. If Bundle A wins, the record should show whether the decisive factor was configuration completion, hub preservation, or efficient compression. If Bundle B wins, the record should show whether novelty and lower cost outweighed motif completion. The objective is not to prescribe one universal answer. The objective is to make the tradeoff explicit, stable, and testable.

## Proposed Evolution

REC-006 introduces five related mechanisms:

1. versioned calibration profiles;
2. per-component normalization contracts;
3. contribution traces;
4. deterministic sensitivity sweeps;
5. golden-portfolio regression fixtures.

Together these mechanisms convert utility tuning from ad hoc parameter adjustment into a controlled engineering process.

### Versioned Calibration Profiles

All utility parameters should be collected into an explicit calibration profile with a stable identifier.

A profile should include:

- profile version;
- component weights;
- normalization parameters;
- caps and floors;
- interaction rules;
- tie-breaking policy;
- enabled recommendation flags;
- candidate-family-specific adjustments, if any;
- budget assumptions used during calibration.

Illustrative structure:

```json
{
  "profile_id": "sbe-utility-v0.2-default",
  "schema_version": "1.0",
  "weights": {
    "intrinsic_salience": 1.0,
    "structural_relevance": 0.8,
    "semantic_novelty": 0.7,
    "configuration_completion": 0.35,
    "hub_preservation": 0.25,
    "diversity": 0.30,
    "structural_inevitability": -0.20,
    "closure_cost": -0.45
  },
  "caps": {
    "configuration_completion": 0.50,
    "hub_preservation": 0.40,
    "diversity": 0.45
  },
  "tie_breaker": "stable_candidate_id"
}
```

The numerical values above are illustrative only. The architectural requirement is that every production selection be attributable to a named profile whose contents are preserved with the output or completion log.

A profile change that can alter selection should be treated as a behavior version change, even when no schema changes occur.

### Per-Component Normalization Contracts

Weights are meaningful only when component ranges are understood. Each utility dimension should therefore declare a normalization contract.

The contract should specify:

- raw input domain;
- normalized output range;
- monotonicity expectation;
- clipping behavior;
- null or unavailable behavior;
- whether the value is intrinsic, bundle-level, or portfolio-relative;
- whether the component can be negative;
- whether the component is bounded before or after weighting.

For example:

| Component | Scope | Normalized range | Interpretation |
|---|---|---:|---|
| Intrinsic salience | candidate | 0..1 | Candidate importance before portfolio context |
| Closure cost | bundle | 0..1 | Fractional burden of required support |
| Semantic novelty | marginal | 0..1 | New semantic coverage relative to selected portfolio |
| Configuration completion | marginal | 0..1 | Degree to which addition completes a qualified motif |
| Structural inevitability | candidate | 0..1 | Degree to which relation is definitionally or geometrically expected |
| Hub preservation | marginal | 0..1 | Incremental preservation of a qualified neighborhood |

Normalization should be deterministic and fixture-tested. A component must not silently change scale because a candidate generator begins emitting a broader distribution of raw values.

### Contribution Traces

Every evaluated candidate bundle should optionally emit a machine-readable contribution trace.

The trace should record:

- candidate ID;
- dependency bundle IDs;
- raw component values;
- normalized component values;
- weights;
- weighted contributions;
- caps or floors applied;
- interaction adjustments;
- total marginal utility;
- budget cost;
- selection decision;
- decision rank or comparison set;
- active calibration profile ID.

Illustrative trace:

```json
{
  "candidate_id": "cfg:moon-saturn-node:bre",
  "bundle_ids": [
    "rel:moon-saturn",
    "rel:saturn-node"
  ],
  "profile_id": "sbe-utility-v0.2-default",
  "components": {
    "intrinsic_salience": {
      "raw": 0.72,
      "normalized": 0.72,
      "weight": 1.0,
      "contribution": 0.72
    },
    "configuration_completion": {
      "raw": 1.0,
      "normalized": 1.0,
      "weight": 0.35,
      "capped_contribution": 0.35
    },
    "semantic_novelty": {
      "raw": 0.48,
      "normalized": 0.48,
      "weight": 0.70,
      "contribution": 0.336
    },
    "closure_cost": {
      "raw": 0.60,
      "normalized": 0.60,
      "weight": -0.45,
      "contribution": -0.27
    }
  },
  "marginal_utility": 1.136,
  "selected": true
}
```

Contribution traces are not intended for end users or authoring models. They are engineering artifacts for QA, regression analysis, and architectural review.

### Deterministic Sensitivity Sweeps

A calibration process should evaluate not only one chosen parameter set but also the stability of the system around that set.

A sensitivity sweep varies one parameter or one tightly controlled parameter group across a deterministic grid while holding all other inputs constant. For each run, it records:

- selected candidate IDs;
- portfolio utility;
- semantic-region coverage;
- configuration completion;
- hub coverage;
- redundancy;
- dependency cost;
- authoring-budget utilization;
- changes relative to the baseline portfolio.

The purpose is to identify thresholds and unstable regions.

For example, a sweep of the configuration-completion weight may reveal:

- below 0.20, the Moon–Saturn–Node motif is rarely completed;
- from 0.25 through 0.40, the motif is preserved without major unrelated displacement;
- above 0.55, configuration candidates begin displacing clearly stronger independent claims.

The recommended value would then be chosen from a stable interval rather than from a single trial.

Sensitivity sweeps should remain deterministic and should use canonical fixture graphs. They are not stochastic hyperparameter searches.

### Golden-Portfolio Regression Fixtures

The project should maintain a compact set of canonical projected graphs with reviewed expected portfolios or reviewed invariants.

A fixture does not always need to prescribe the exact complete portfolio. Two levels of expectation are useful:

**Exact-selection fixtures**
- the selected candidate IDs must match exactly;
- appropriate for determinism, tie-breaking, and small synthetic graphs.

**Invariant fixtures**
- specified semantic regions, configurations, or dependencies must be present;
- specified redundancy or cost limits must not be exceeded;
- appropriate for large empirical graphs where several portfolios may be acceptably equivalent.

Bre’s chart is well suited to an invariant fixture. Its expected assertions might include:

- at least one coherent representation of the Moon–Saturn–North Node developmental cluster;
- no double counting of a configuration bonus across overlapping candidates;
- meaningful angular information preserved without prioritizing structural angle geometry solely because it is present;
- minimum coverage across predefined semantic regions;
- deterministic output under repeated execution;
- bounded portfolio drift when a calibration profile changes within an approved minor range.

## Calibration Objectives

Calibration should not optimize a single proxy such as agreement with one manually selected packet. That would risk encoding one editor’s preferences as architecture.

Instead, calibration should balance several objectives:

- semantic coverage;
- structural coherence;
- dependency efficiency;
- redundancy control;
- representation of high-value motifs;
- preservation of important neighborhoods;
- deterministic stability;
- compatibility with authoring budgets.

The project should explicitly distinguish **hard constraints** from **soft objectives**.

Hard constraints include:

- dependency closure;
- schema validity;
- budget limits;
- deterministic tie-breaking;
- candidate eligibility rules.

Soft objectives include:

- diversity;
- configuration completion;
- hub preservation;
- compression efficiency;
- portfolio balance.

A hard constraint must never be overcome by a utility bonus. This distinction should be encoded in the implementation rather than left to weight selection.

## Interaction Terms

Most utility components should remain additive after normalization because additive contributions are easier to inspect and calibrate. However, a small number of interactions may require explicit treatment.

Examples include:

### Configuration Completion and Hub Preservation

A configuration may occur inside a qualified hub. Rewarding both at full strength could double-count the same structural value.

Recommended handling:
- calculate both components independently;
- apply an interaction cap to their combined contribution;
- retain both values in the trace;
- record the cap adjustment explicitly.

### Axis Compression and Closure Cost

An axis-aware candidate may represent several source relations with one authored claim. Its closure cost should reflect the dependencies required for validation, while its authoring cost may remain low.

Recommended handling:
- keep semantic dependency cost distinct from editorial slot cost;
- do not treat compressed representation as “free” structural coverage;
- preserve source references in provenance.

### Diversity and Intrinsic Salience

A diversity bonus should not routinely cause weak candidates to displace exceptionally salient material.

Recommended handling:
- cap diversity contribution;
- consider a minimum intrinsic-utility floor for portfolio-relative bonuses;
- test boundary cases in which novelty competes with very high salience.

### Structural Inevitability and Angular Diagnostic Value

A relationship may be partly structural and partly individualized.

Recommended handling:
- model structural inevitability as a bounded discount rather than a binary exclusion;
- apply the discount only to the inevitable portion represented by the candidate;
- allow individualized content to retain salience and novelty contributions.

## Calibration Procedure

A recommended calibration cycle is:

1. Freeze candidate-generation code and fixture inputs.
2. Select a baseline calibration profile.
3. Run exact-selection and invariant fixtures.
4. Capture contribution traces for all evaluated bundles.
5. Run one-dimensional sensitivity sweeps.
6. Inspect portfolio transitions and unstable thresholds.
7. Adjust one parameter family at a time.
8. Re-run the complete fixture suite.
9. Record accepted changes and rationale in the design ledger.
10. issue a new calibration profile version.

This procedure should be executable through one repository command and should write all artifacts to a predictable QA output directory.

Calibration changes should never be justified only by the quality of final prose. The semantic basis must be evaluated before downstream authoring variation is introduced.

## Observability and Completion Logs

Every SBE completion log should record at minimum:

- SBE implementation version;
- candidate schema version;
- calibration profile ID;
- enabled candidate generators;
- enabled portfolio refinements;
- input graph identifier or content hash;
- selected candidate IDs;
- total and per-component utility summary;
- budget used and budget remaining;
- deterministic execution result;
- QA profile used, if any.

When detailed traces are disabled in production, the completion log should still retain enough summary data to reproduce the selection under the same code and profile.

## Compatibility Analysis

REC-006 is backward compatible at the candidate and portfolio schema levels if calibration metadata is introduced as optional diagnostic output.

The recommendation can be adopted incrementally:

1. collect current weights into a named profile without changing values;
2. emit contribution traces in QA mode only;
3. add normalization assertions;
4. add golden fixtures;
5. perform sensitivity sweeps;
6. revise weights only after the baseline is documented.

This sequence separates observability from behavior change. The first several implementation steps should produce identical portfolios to the current system.

Existing consumers do not need to understand calibration metadata. Authoring packets remain unchanged unless a later approved profile intentionally changes selection behavior.

## Alternatives Considered

### Leave Weights Embedded in Code

This is operationally simple but weakens traceability and makes behavior changes difficult to version. It is acceptable during an early prototype but not as a long-term architecture for an expanding utility vector.

### Replace the Utility Vector with One Learned Score

A learned model could potentially imitate reviewed selections, but it would reduce determinism, explainability, portability, and architectural control. It would also entangle calibration data with editorial preferences. This alternative is not recommended for the core extractor.

### Hand-Tune Against Bre Alone

Bre is an excellent running example but cannot serve as the only calibration target. Tuning against one graph would risk overfitting its topology and semantic distribution. Bre should be one high-value empirical fixture within a broader suite.

### Optimize Only Final Portfolio Similarity

Exact similarity to a prior packet can detect drift but cannot determine whether the prior packet is optimal or whether a new portfolio is semantically equivalent. Exact-selection tests should therefore be supplemented with invariant and coverage tests.

### Use Randomized Search

Randomized search is unnecessary at the current scale and would complicate reproducibility. Deterministic grid sweeps and targeted pairwise experiments are sufficient and better aligned with the project’s QA philosophy.

## Implementation Considerations

A practical implementation can remain modest.

Suggested modules:

- `calibration/profile.py`  
  profile schema, loading, validation, version identifiers;

- `calibration/normalize.py`  
  deterministic normalization functions and contracts;

- `calibration/trace.py`  
  contribution-trace structures and serialization;

- `calibration/sweep.py`  
  deterministic sensitivity sweeps;

- `qa/golden_portfolios.py`  
  exact and invariant fixture assertions.

The optimizer should consume a validated profile object rather than importing free-floating constants.

To prevent accidental behavior drift:

- reject unknown profile fields;
- validate expected ranges;
- require explicit profile IDs;
- include the profile ID in output metadata;
- fail QA when the profile changes without updated expected artifacts.

## QA Strategy

REC-006 requires both unit and system-level QA.

### Unit Tests

Verify:

- normalization boundaries;
- monotonicity;
- clipping behavior;
- negative contribution handling;
- interaction caps;
- serialization round trips;
- profile validation;
- stable tie-breaking.

### Synthetic Portfolio Tests

Create small graphs where the expected effect of one component is unambiguous.

Examples:

- two equal candidates differing only in novelty;
- one configuration candidate exactly at the completion threshold;
- one structural angle relation and one individualized angle contact;
- one hub-preserving bundle with higher closure cost;
- one axis-compressed candidate competing with its unsynthesized sources.

### Empirical Regression Tests

Run reviewed graphs, including Bre, and compare:

- selected IDs;
- invariant satisfaction;
- semantic coverage;
- portfolio cost;
- component distributions;
- drift from prior profile.

### Sensitivity Tests

For every active weight:

- sweep across the approved test interval;
- identify selection transition points;
- assert that the production value lies inside an accepted stable region;
- flag large discontinuities for architectural review.

### Determinism Tests

Repeat complete calibration runs and verify byte-identical:

- selected portfolio IDs;
- contribution traces;
- summary metrics;
- sweep results;
- fixture reports.

## Migration Strategy

A low-risk migration consists of four phases.

### Phase A — Profile Extraction

Move existing constants into a validated profile while preserving exact behavior.

### Phase B — Diagnostic Tracing

Add contribution traces and completion-log metadata without changing selection.

### Phase C — Fixture Establishment

Create synthetic and empirical golden fixtures from current behavior plus reviewed invariants.

### Phase D — Controlled Recalibration

Evaluate REC-001 through REC-005 under deterministic sweeps and issue a new profile only when evidence supports a change.

This sequence prevents calibration infrastructure and scoring changes from being conflated in one implementation pass.

## Recommendation Classification

**Implementation complexity:** Medium

The individual mechanisms are straightforward, but the work spans profile management, optimizer instrumentation, QA fixtures, and reporting.

**Expected benefit:** High

Calibration improves explainability, regression safety, maintainability, and confidence in every other scoring recommendation.

**Architectural risk:** Low

The first three adoption phases can preserve byte-identical selection behavior. Risk appears only when a revised profile is intentionally activated, and that change is controlled by versioning and regression review.

## Summary

REC-006 formalizes how SBE’s utility vector is measured and evolved.

The current architecture already has the necessary foundations: deterministic execution, explicit dependencies, structured candidates, and portfolio-aware optimization. The recommendation adds the missing engineering discipline around those foundations:

- named and versioned calibration profiles;
- explicit normalization contracts;
- per-candidate contribution traces;
- deterministic sensitivity sweeps;
- golden-portfolio regression fixtures;
- controlled migration from observation to behavior change.

This recommendation is especially important because REC-001 through REC-005 introduce value at several semantic scales: relationship, configuration, neighborhood, information density, and portfolio diversity. Calibration ensures those improvements remain mutually intelligible rather than accumulating as opaque weights.

The next recommendation should build on this foundation by addressing optimizer-level comparison and selection behavior once component values are calibrated and observable.

# REC-007 — Marginal Bundle Comparison and Selection Stability

## Problem Statement

After utility components have been calibrated (REC-006), the optimizer still faces the core decision of comparing competing *closed bundles* rather than isolated candidates. Small differences in bundle composition, dependency closure, or budget utilization can create unstable selection boundaries if comparison behavior is not explicitly specified.

## Architectural Context

The Semantic Basis Extractor operates on dependency-closed semantic bundles. Selection therefore depends on the incremental value of an entire bundle relative to the already selected portfolio rather than the score of an individual relationship or configuration.

## Proposed Evolution

This recommendation formalizes bundle comparison as a deterministic ordering process.

The comparison should evaluate, in order:

1. Eligibility and dependency closure.
2. Hard architectural constraints.
3. Marginal calibrated utility (REC-006).
4. Budget efficiency.
5. Redundancy reduction.
6. Stable deterministic tie-breaking.

The optimizer should never compare partially closed bundles with fully closed bundles. Every comparison should be performed against equivalent semantic units.

## Stability Requirements

Selection order should remain stable under repeated execution.

Minor calibration adjustments should produce localized portfolio changes rather than cascading replacements whenever possible. QA should measure portfolio drift as a first-class regression metric.

## QA Strategy

Regression tests should include:

- repeated deterministic runs,
- boundary cases with nearly identical utilities,
- dependency-heavy bundles,
- interaction with configuration completion, diversity, and hub preservation,
- portfolio drift analysis between calibration profiles.

## Complexity / Benefit / Risk

Implementation Complexity: Medium

Expected Benefit: High

Architectural Risk: Low

## Summary

REC-007 establishes deterministic comparison semantics after utility calibration, ensuring that optimizer decisions remain explainable, reproducible, and resistant to unnecessary portfolio churn as future recommendation families are introduced.

# REC-008 — Portfolio Drift and Stability Metrics

## Problem Statement

As calibration profiles evolve, portfolio changes should be measured rather than judged solely by subjective review. Even beneficial architectural improvements can unintentionally replace large portions of a semantic basis, making regressions difficult to distinguish from intended evolution.

## Architectural Context

REC-006 introduced versioned calibration profiles and REC-007 formalized deterministic bundle comparison. This recommendation defines how successive optimizer versions should be compared using stable quantitative metrics.

## Proposed Evolution

Each calibration run should emit a portfolio comparison report against a designated baseline including:

- selected candidate overlap,
- semantic-region coverage delta,
- dependency-cost delta,
- redundancy delta,
- configuration-completion delta,
- hub-preservation delta,
- authoring-budget utilization,
- deterministic reproducibility,
- calibration profile identifier.

Drift should be classified into:
- Expected drift,
- Reviewed improvement,
- Unexpected drift,
- Regression.

Large changes should require explicit architectural justification in the design ledger.

## QA Strategy

Regression fixtures should verify:
- identical inputs produce identical drift reports,
- profile-only changes remain attributable,
- approved profile upgrades preserve required semantic invariants.

## Complexity / Benefit / Risk

Implementation Complexity: Medium

Expected Benefit: High

Architectural Risk: Low

## Summary

Portfolio drift becomes a measurable engineering artifact rather than an intuitive observation, improving long-term maintainability and confidence in future optimizer evolution.

# REC-009 — Portfolio Coverage Metrics

## Problem Statement

A high-quality semantic basis should maximize meaningful coverage rather than simply maximize the number of selected candidates. Coverage therefore requires explicit measurement independent of raw portfolio size.

## Architectural Context

REC-006 introduced calibrated utility, REC-007 standardized bundle comparison, and REC-008 established drift metrics. REC-009 defines the semantic dimensions against which portfolio completeness should be evaluated.

## Proposed Evolution

Define deterministic coverage metrics including:

- graph neighborhood coverage;
- semantic-domain coverage;
- configuration coverage;
- high-salience relationship coverage;
- axis representation;
- dependency completeness;
- authoring-budget efficiency.

Coverage reports should distinguish structural omissions from intentional exclusions caused by budget or redundancy constraints.

## QA Strategy

Fixture reports should assert minimum coverage thresholds for reviewed graphs while preserving deterministic output and dependency closure.

## Complexity / Benefit / Risk

Implementation Complexity: Medium

Expected Benefit: High

Architectural Risk: Low

## Summary

Coverage becomes an explicit engineering objective and complements utility calibration, selection stability, and drift analysis by providing a durable measure of semantic completeness.

# REC-010 — Coverage Targets and Budget Allocation

## Problem Statement

Different downstream consumers require semantic bases of substantially different sizes. A concise mobile summary, an engineering packet, and a comprehensive narrative report should all optimize toward different budget constraints while preserving architectural consistency.

## Architectural Context

REC-009 defines how coverage is measured. REC-010 defines what level of coverage should be expected for representative portfolio budgets so that selection quality can be evaluated relative to the available authoring space rather than against an unrealistic notion of complete coverage.

## Proposed Evolution

Introduce deterministic coverage profiles tied to authoring budgets, for example:

- Compact portfolio (highest-value semantic regions only)
- Standard portfolio (balanced coverage across major domains)
- Expanded portfolio (broad semantic coverage with secondary motifs)
- Full engineering portfolio (near-maximal coverage for analysis)

Each profile should specify expected minimum coverage percentages for semantic regions, configuration families, graph hubs, and diagnostic relationships together with acceptable omission priorities.

## QA Strategy

Regression fixtures should verify that each budget profile satisfies its documented coverage targets while remaining deterministic and honoring dependency closure.

## Complexity / Benefit / Risk

Implementation Complexity: Medium

Expected Benefit: High

Architectural Risk: Low

## Summary

Coverage expectations become explicit engineering contracts instead of subjective judgments, allowing different output sizes to remain architecturally comparable.

# REC-011 — Candidate Family Expansion Strategy

## Problem Statement

The long-term value of the Semantic Basis Extractor depends not only on selecting among existing candidate families, but on accommodating future families without requiring optimizer redesign. As new generators are introduced—configuration candidates, axis syntheses, neighborhood abstractions, temporal motifs, and future semantic operators—they should participate through a common architectural contract.

## Architectural Context

REC-001 through REC-010 establish deterministic optimization, calibration, stability, drift measurement, and coverage expectations. REC-011 defines how entirely new candidate families should integrate into that framework.

## Proposed Evolution

Every candidate family should satisfy a common contract describing:

- semantic intent;
- provenance requirements;
- dependency behavior;
- utility inputs;
- compatibility with calibration profiles;
- expected coverage contribution;
- QA fixtures;
- migration considerations.

Families should be independently enableable through feature flags so experimental generators can be evaluated alongside production generators without affecting deterministic baseline behavior.

The optimizer should remain family-agnostic wherever practical, consuming normalized candidate metadata rather than family-specific logic.

## QA Strategy

Each new candidate family should ship with:

- synthetic fixture graphs;
- empirical regression graphs;
- determinism verification;
- coverage impact reports;
- portfolio drift analysis relative to the previous baseline.

No candidate family should be promoted to production without demonstrating measurable semantic value.

## Complexity / Benefit / Risk

Implementation Complexity: Medium

Expected Benefit: High

Architectural Risk: Low

## Summary

A stable candidate-family contract allows the Semantic Basis Extractor to grow incrementally while preserving optimizer simplicity, deterministic behavior, and long-term maintainability.

# REC-012 — Candidate Family Lifecycle

## Problem Statement

As the library of candidate generators grows, the project requires a disciplined process for moving a candidate family from research concept to production-ready component. Without an explicit lifecycle, experimental generators risk becoming permanent prototypes or entering production without sufficient evidence.

## Architectural Context

REC-011 defined the contract that every candidate family should satisfy. REC-012 defines the lifecycle governing how those families evolve while preserving deterministic behavior and architectural quality.

## Proposed Evolution

Every candidate family should progress through the following stages:

1. Research concept
2. Prototype implementation
3. Synthetic fixture validation
4. Empirical evaluation
5. Calibration compatibility review
6. Portfolio drift assessment
7. Production approval
8. Ongoing regression monitoring
9. Eventual deprecation or replacement when warranted

Promotion between stages should require documented engineering evidence rather than subjective assessment.

## QA Strategy

Lifecycle reviews should include deterministic execution, coverage analysis, contribution-trace inspection, regression testing, and comparison against the current production baseline.

## Complexity / Benefit / Risk

Implementation Complexity: Low-Medium

Expected Benefit: High

Architectural Risk: Low

## Summary

A formal lifecycle encourages disciplined evolution of the Semantic Basis Extractor by ensuring every new candidate family is validated, calibrated, documented, and regression-tested before becoming part of the production architecture.

# REC-013 — Candidate Family Deprecation and Compatibility

## Problem Statement

As the Semantic Basis Extractor evolves, some candidate families will eventually become obsolete, be superseded by richer generators, or be merged into more expressive representations. The architecture requires a disciplined deprecation process so historical semantic bases remain reproducible while future development is not constrained by legacy implementations.

## Architectural Context

REC-011 established how new candidate families enter the architecture, and REC-012 defined the lifecycle from prototype to production. REC-013 completes that lifecycle by specifying how mature families may be retired, replaced, or consolidated without compromising determinism, provenance, or regression history.

## Proposed Evolution

Every production candidate family should publish a compatibility policy describing:

- supported schema versions;
- deprecation status;
- replacement family (if applicable);
- migration guidance;
- expected regression impact;
- calibration considerations;
- historical reproducibility requirements.

Deprecation should occur in phases:

1. Advisory (supported but discouraged)
2. Deprecated (replacement available)
3. Disabled by default
4. Removed from new profiles while retained for historical replay
5. Fully retired after compatibility guarantees expire

Historical calibration profiles should continue to reproduce historical semantic bases without requiring source modifications.

## QA Strategy

Deprecation testing should verify:

- identical replay of historical calibration profiles;
- migration equivalence where replacements exist;
- stable provenance references;
- deterministic behavior before and after migration.

## Complexity / Benefit / Risk

Implementation Complexity: Medium

Expected Benefit: High

Architectural Risk: Low

## Summary

A formal compatibility and deprecation policy allows the candidate-family ecosystem to evolve while preserving reproducibility, engineering traceability, and confidence in historical regression results.

# REC-014 — Candidate Family Composition

## Problem Statement

Individual candidate families should remain modular, but many of the most valuable semantic interpretations emerge only when multiple families cooperate. The architecture therefore requires explicit composition rules that preserve modularity while allowing richer semantic synthesis.

## Architectural Context

REC-011 through REC-013 defined how candidate families are introduced, validated, and eventually retired. REC-014 describes how simultaneously active families cooperate inside a single optimization pass without becoming tightly coupled.

## Proposed Evolution

Candidate families should communicate only through normalized candidate contracts rather than direct implementation dependencies.

Composition should support:

- shared provenance,
- dependency-aware bundle construction,
- configuration enrichment,
- neighborhood-aware synthesis,
- axis-aware abstraction,
- portfolio-level refinement.

Composition should remain declarative wherever possible so new families can participate without modifying existing generators.

When multiple families describe the same underlying semantics, the optimizer should evaluate the composed alternatives using the calibrated utility framework rather than family-specific precedence rules.

## QA Strategy

Composition testing should include:

- pairwise family interaction fixtures,
- multi-family regression graphs,
- provenance integrity verification,
- deterministic composition ordering,
- portfolio comparison against single-family baselines.

## Complexity / Benefit / Risk

Implementation Complexity: Medium

Expected Benefit: High

Architectural Risk: Low

## Summary

Explicit composition rules enable independent candidate families to cooperate in producing richer semantic bases while preserving determinism, modularity, and long-term maintainability.

# REC-015 — Cross-Family Conflict Resolution

## Problem Statement

As additional candidate families become active, multiple generators may produce partially overlapping or competing interpretations of the same underlying semantic structure. The Semantic Basis Extractor requires deterministic conflict-resolution rules that preserve explainability without introducing family-specific precedence.

## Architectural Context

REC-014 established how candidate families compose. REC-015 defines how conflicts among composed candidates are resolved using architectural principles rather than implementation order.

## Proposed Evolution

Conflicts should be evaluated using normalized candidate metadata together with the calibrated utility framework.

Resolution should consider:

- provenance completeness;
- dependency closure;
- semantic specificity;
- configuration participation;
- neighborhood preservation;
- redundancy;
- portfolio contribution.

Candidate families should not receive implicit priority based solely on implementation order or historical status.

When two candidates are semantically equivalent, deterministic tie-breaking should prefer the representation with lower authoring cost while preserving complete provenance.

## QA Strategy

Conflict-resolution fixtures should verify:

- deterministic outcomes across repeated execution;
- identical results regardless of generator ordering;
- preserved provenance;
- stable portfolio quality after adding new candidate families.

## Complexity / Benefit / Risk

Implementation Complexity: Medium

Expected Benefit: High

Architectural Risk: Low

## Summary

Cross-family conflict resolution ensures future semantic generators remain cooperative rather than competitive, allowing the optimizer to select the strongest representation according to transparent architectural criteria.

# REC-016 — Cross-Family Provenance

## Problem Statement

As candidate families become increasingly compositional, the provenance of a selected semantic claim can no longer be represented adequately by a single source reference.

A higher-order candidate may be produced by:

- one generator identifying a graph relationship;
- another generator recognizing a configuration;
- a neighborhood analyzer identifying hub significance;
- an axis-aware generator compressing multiple source relations;
- a portfolio refinement preserving a candidate because of coverage or diversity value.

If these contributions are flattened into one generic provenance list, the final semantic basis remains technically traceable but loses the structure needed to explain how the candidate was constructed, why it was eligible, and which generator contributed each portion of its meaning.

Cross-family provenance must therefore preserve both source lineage and transformation lineage.

## Architectural Context

REC-014 established that candidate families should compose through normalized contracts rather than direct implementation dependencies. REC-015 established that conflicts among candidate families should be resolved through calibrated architectural criteria rather than generator order.

REC-016 supplies the traceability model required by both recommendations.

The provenance system should support three related goals:

1. **Source traceability**  
   Every semantic assertion must remain traceable to graph structures or upstream factual artifacts.

2. **Transformation traceability**  
   Every synthesis, abstraction, compression, or enrichment step must identify the generator and operation that produced it.

3. **Decision traceability**  
   Every selected candidate should record why it survived optimization, including relevant portfolio-level effects.

These goals belong to different layers and should not be represented as one undifferentiated list.

## Current Behavior

The existing architecture already treats provenance as a required property of candidate generation. Source nodes, relationships, and dependency references can be carried into candidate objects and ultimately exposed to downstream consumers.

That foundation is strong but becomes insufficient when multiple candidate families contribute to one semantic object.

For example, a configuration synthesis may originate from several relationship candidates. Those relationship candidates may themselves depend on object-level descriptors. A hub-preservation bonus may then influence portfolio selection without changing the semantic content of the candidate. If all of these references are merged into one array, downstream systems cannot easily distinguish:

- factual source evidence;
- semantic dependencies;
- synthesis inputs;
- optimizer rationale;
- historical replacement lineage.

REC-016 proposes an explicit layered provenance model.

## Running Example: Bre

Consider the Moon–Saturn–North Node developmental-regulation cluster in Bre’s graph.

A final selected candidate might state a unified developmental theme involving:

- Moon-based comfort and regulation;
- Saturn-based training structure;
- North Node-based developmental direction.

The candidate may have been produced through several stages:

1. relationship generators identify the relevant Moon–Saturn and Saturn–Node structures;
2. a configuration generator recognizes the coherent three-object motif;
3. a hub analyzer identifies Saturn as a structurally important neighborhood center;
4. the optimizer applies a configuration-completion contribution and a bounded hub-preservation contribution;
5. a diversity term may further support the candidate because it preserves a semantic region not otherwise represented.

These contributions should not all appear as equivalent provenance entries.

A useful provenance record would distinguish:

- the Moon, Saturn, and North Node source objects;
- the source relationships connecting them;
- the configuration detector that created the motif candidate;
- the hub analyzer that supplied structural context;
- the optimizer contributions that affected selection;
- the calibration profile under which the decision occurred.

This structured lineage allows an engineer to answer:

- What source facts justify the candidate?
- Which generator synthesized them?
- Which transformations changed the representation?
- Why was the candidate selected?
- Which profile and implementation version produced the decision?

## Proposed Evolution

Introduce a layered provenance object containing five distinct categories:

1. source provenance;
2. dependency provenance;
3. transformation provenance;
4. decision provenance;
5. historical provenance.

### Source Provenance

Source provenance identifies the upstream factual structures that justify the semantic claim.

Examples include:

- graph node IDs;
- relationship IDs;
- object placements;
- configuration members;
- source-model identifiers;
- upstream dataset or artifact hashes.

Source provenance should be immutable once the candidate is created. Later composition steps may add source references but should not rewrite or remove the original lineage.

### Dependency Provenance

Dependency provenance identifies semantic objects that must be present for the candidate to remain valid and authorable.

This is distinct from factual source provenance.

For example:

- a synthesis candidate may require two relationship candidates;
- a theme candidate may require object descriptors;
- an axis candidate may require both endpoint structures;
- a temporal candidate may require baseline and activation candidates.

Dependencies should preserve stable candidate IDs and dependency roles.

### Transformation Provenance

Transformation provenance records how a candidate was derived.

Each transformation step should include:

- transformation ID;
- generator family;
- generator version;
- operation type;
- input candidate IDs;
- output candidate ID;
- configuration or feature flags;
- deterministic ordering position, where relevant.

Illustrative operations include:

- `configuration_synthesis`;
- `axis_compression`;
- `neighborhood_enrichment`;
- `semantic_merge`;
- `candidate_replacement`;
- `temporal_activation`;
- `cross_family_composition`.

Transformation provenance should form a directed acyclic lineage graph. Cycles should be rejected during validation.

### Decision Provenance

Decision provenance records optimizer effects without treating those effects as semantic evidence.

It should include:

- calibration profile ID;
- intrinsic utility summary;
- marginal utility summary;
- configuration-completion contribution;
- hub-preservation contribution;
- diversity contribution;
- structural-inevitability discount;
- closure cost;
- budget cost;
- comparison rank;
- stable tie-breaker result;
- selection status.

Decision provenance should be optional in compact production artifacts but mandatory in QA and engineering outputs.

### Historical Provenance

Historical provenance supports compatibility and deprecation.

It should record:

- predecessor candidate IDs;
- replacement candidate IDs;
- candidate-family migration version;
- deprecation status;
- compatibility profile;
- reason for replacement or retirement.

This layer allows a semantic claim generated under an older candidate family to be related to its successor without pretending the two objects are identical.

## Provenance Object Model

An illustrative candidate provenance structure:

```json
{
  "provenance": {
    "sources": [
      {
        "source_type": "graph_relationship",
        "source_id": "rel:moon-saturn",
        "role": "configuration_member"
      },
      {
        "source_type": "graph_relationship",
        "source_id": "rel:saturn-north-node",
        "role": "configuration_member"
      }
    ],
    "dependencies": [
      {
        "candidate_id": "cand:moon-regulation",
        "role": "semantic_support"
      },
      {
        "candidate_id": "cand:saturn-training-structure",
        "role": "semantic_support"
      }
    ],
    "transformations": [
      {
        "transformation_id": "tx:cfg:moon-saturn-node",
        "family": "configuration_generator",
        "version": "0.2",
        "operation": "configuration_synthesis",
        "inputs": [
          "cand:moon-saturn",
          "cand:saturn-north-node"
        ]
      }
    ],
    "decision": {
      "profile_id": "sbe-utility-v0.2-default",
      "selected": true,
      "marginal_utility": 1.136,
      "portfolio_effects": [
        "configuration_completion",
        "hub_preservation"
      ]
    },
    "history": []
  }
}
```

The exact schema may differ, but the separation of concerns should remain.

## Provenance Merge Rules

Cross-family composition requires deterministic merge behavior.

Recommended rules:

1. preserve all distinct source references;
2. deduplicate exact source identities;
3. preserve role distinctions even when source IDs match;
4. order entries deterministically;
5. retain transformation boundaries;
6. never convert optimizer rationale into source evidence;
7. reject cycles in transformation lineage;
8. retain superseded lineage in historical provenance;
9. preserve generator versions;
10. preserve source hashes when available.

When two composed candidates share the same source relationship but use it in different roles, both role records should remain.

For example, one source may act as:

- a configuration member;
- a hub-supporting edge;
- an axis endpoint relation.

Deduplication should therefore operate on the tuple:

```text
(source_type, source_id, role)
```

rather than on source ID alone.

## Provenance and Semantic Compression

Compression introduces a special challenge.

A compressed candidate may replace several lower-level candidates in the authored packet, but the compressed representation must not erase their lineage.

Therefore:

- source-level candidates may be omitted from the final portfolio;
- their IDs and source references remain in the compressed candidate’s dependency or transformation provenance;
- the optimizer should distinguish editorial omission from semantic absence;
- coverage metrics should credit the compressed candidate only for source structures it explicitly carries.

This rule is especially important for axis-aware and configuration-level syntheses.

## Provenance and Conflict Resolution

REC-015 allows semantically overlapping candidates to compete.

When one candidate wins, provenance should record enough information to explain the decision without embedding the entire rejected portfolio.

Recommended behavior:

- preserve the selected candidate’s full lineage;
- record comparison-set IDs in decision provenance;
- optionally record the principal rejected alternative;
- preserve stable conflict-group IDs;
- avoid copying all rejected candidates into the selected object.

A separate QA comparison report may retain full rejected-candidate details.

## Provenance and Coverage

Coverage calculations should operate on normalized source and semantic roles rather than candidate count alone.

A configuration synthesis can satisfy coverage for several underlying relations only when those relations appear in its provenance.

Similarly, a candidate should not receive credit for an entire hub simply because it references the hub object. The provenance record must identify which neighborhood structures it actually represents.

This creates a direct relationship between REC-009 coverage metrics and REC-016 provenance quality.

## Provenance and Calibration

Calibration and sensitivity analysis depend on stable provenance.

When a candidate changes between profiles, engineers should be able to determine whether the change reflects:

- a different utility decision over identical candidates;
- a different candidate-family composition;
- a changed source graph;
- a changed generator implementation;
- a changed dependency closure;
- a historical migration.

The completion log should therefore include hashes for:

- input graph;
- candidate set;
- calibration profile;
- selected portfolio;
- provenance lineage.

## Compatibility Analysis

REC-016 can be introduced incrementally.

### Phase A — Layer Existing Fields

Map current provenance fields into the new source and dependency layers without changing candidate generation.

### Phase B — Add Transformation Records

Instrument composition and synthesis generators to emit transformation lineage.

### Phase C — Add Decision Provenance

Attach optimizer traces in QA and engineering profiles.

### Phase D — Add Historical Lineage

Connect candidate-family migration and deprecation metadata from REC-013.

Existing downstream consumers may continue reading legacy flattened provenance during a transition period. A compatibility serializer can derive the flattened view from the layered model.

The layered model should become authoritative; the flattened representation should be treated as a compatibility projection.

## Alternatives Considered

### One Flat Provenance List

Simple to serialize but loses distinctions among evidence, dependency, transformation, and decision rationale. Rejected as insufficient for multi-family composition.

### Store Only Final Source Graph IDs

This preserves factual traceability but not derivation history. It cannot explain which generator produced the synthesis or why a candidate entered the portfolio.

### Embed Complete Candidate Objects Recursively

This provides rich lineage but risks large artifacts, duplication, and recursive complexity. Stable IDs plus structured references are preferable.

### Store Provenance Only in External Logs

External logs are valuable but should not be the sole traceability mechanism. Candidate artifacts should retain enough self-contained lineage to be interpretable outside one execution environment.

### Treat Optimizer Scores as Semantic Evidence

Rejected. Selection rationale is not source evidence and must remain in a separate provenance layer.

## Implementation Considerations

Suggested schema objects:

- `SourceProvenanceRef`;
- `DependencyProvenanceRef`;
- `TransformationRecord`;
- `DecisionProvenance`;
- `HistoricalProvenanceRef`;
- `CandidateProvenance`.

Suggested validation rules:

- stable IDs required;
- deterministic ordering;
- no transformation cycles;
- no unknown provenance roles;
- source references must resolve when resolution is required by profile;
- generator versions required for transformations;
- decision provenance profile IDs must resolve;
- historical predecessor and replacement links must not self-reference.

A provenance index may be useful for large engineering outputs so repeated source objects can be referenced without duplication.

## QA Strategy

### Unit Tests

Verify:

- deterministic merge ordering;
- exact deduplication behavior;
- role-preserving source merges;
- transformation-cycle detection;
- serialization round trips;
- compatibility projection into legacy flattened provenance.

### Synthetic Composition Tests

Create small fixtures where:

- two families share one source relation;
- one candidate compresses several dependencies;
- one transformation supersedes another;
- one selected candidate wins a cross-family conflict;
- one invalid cycle is intentionally introduced.

### Empirical Regression Tests

For Bre and other reviewed graphs, verify:

- every selected candidate has resolvable source provenance;
- configuration syntheses preserve all qualifying members;
- compressed candidates retain omitted lower-level lineage;
- optimizer rationale remains separate from source evidence;
- repeated runs produce byte-identical provenance ordering.

### Migration Tests

Verify:

- legacy flattened provenance can be regenerated from the layered model;
- historical profiles remain replayable;
- deprecated candidate families retain predecessor/replacement lineage;
- migration does not silently change coverage attribution.

## Complexity / Benefit / Risk

**Implementation Complexity:** Medium

The schema and validation rules are straightforward, but complete adoption requires instrumentation across generators, composition, optimization, and migration tooling.

**Expected Benefit:** High

Structured provenance improves explainability, debugging, compatibility, coverage measurement, calibration analysis, and trust in synthesized semantic claims.

**Architectural Risk:** Low

The model can be introduced as an additive layer while retaining the existing flattened representation for compatibility.

## Summary

REC-016 formalizes provenance for a multi-family Semantic Basis Extractor.

The key principle is that provenance is not one thing. It includes:

- factual source evidence;
- semantic dependencies;
- transformation lineage;
- optimizer decision rationale;
- historical migration lineage.

Preserving these layers independently allows candidate families to compose without sacrificing traceability. It also connects the candidate-family architecture directly to calibration, conflict resolution, coverage, drift analysis, and long-term compatibility.

The next recommendation should build on this foundation by defining stable candidate identity across composition, migration, and repeated deterministic execution.

# REC-017 — Stable Candidate Identity

## Problem Statement

Candidate identifiers should remain stable across deterministic executions, calibration profile revisions, portfolio recomputation, and candidate-family composition whenever the underlying semantic meaning has not changed. Unstable identifiers make regression analysis, provenance tracking, portfolio drift measurement, and historical replay unnecessarily difficult.

## Architectural Context

REC-016 introduced layered provenance capable of recording source lineage, transformation history, and optimizer decisions. REC-017 defines the identity model that ties those records together across time.

## Proposed Evolution

Every candidate should expose a stable identity composed from immutable semantic properties rather than transient implementation details.

Identity generation should depend only on:

- normalized semantic intent;
- canonical source provenance;
- candidate-family identifier;
- semantic role;
- deterministic normalization rules.

Identity generation should not depend on:

- optimizer rank;
- execution order;
- calibration profile;
- runtime memory layout;
- serialization order.

When a semantic meaning changes materially, a new identity should be issued and historical lineage preserved through REC-016 provenance.

## QA Strategy

Identity fixtures should verify:

- byte-identical IDs across repeated execution;
- stable IDs after harmless implementation refactoring;
- deterministic IDs regardless of generator ordering;
- appropriate ID changes only after genuine semantic modification.

## Complexity / Benefit / Risk

Implementation Complexity: Medium

Expected Benefit: High

Architectural Risk: Low

## Summary

Stable candidate identities provide the backbone for provenance, regression testing, portfolio drift analysis, compatibility, and long-term reproducibility by separating semantic identity from implementation details.

# REC-018 — Candidate Canonicalization

## Problem Statement

Stable candidate identity is only reliable when semantically equivalent candidates are represented in the same canonical form.

Different candidate families may describe the same underlying semantic structure using:

- different source ordering;
- different relationship direction conventions;
- different labels;
- different dependency ordering;
- different levels of source expansion;
- different optional metadata;
- different syntactic decompositions.

Without canonicalization, semantically equivalent candidates can receive different stable IDs, survive as false portfolio diversity, receive duplicate utility credit, or appear as artificial drift between executions.

Canonicalization should therefore occur before identity assignment, conflict grouping, portfolio scoring, and provenance hashing.

## Architectural Context

REC-014 established cross-family composition.

REC-015 established cross-family conflict resolution.

REC-016 established layered provenance.

REC-017 established stable candidate identity.

REC-018 defines the deterministic normalization layer that allows those mechanisms to operate over semantic equivalence rather than incidental representation.

Canonicalization is not prose rewriting. It is a structural normalization process applied to candidate objects before optimization.

The architecture should preserve the distinction among:

1. **Canonical semantic form**  
   The normalized representation used for identity, comparison, conflict grouping, and deterministic execution.

2. **Original generated form**  
   The exact representation emitted by a candidate family before normalization.

3. **Authored rendering form**  
   The downstream wording or packet structure used for human-readable output.

These forms may differ without implying semantic disagreement.

## Current Behavior

The existing design already assumes deterministic candidate generation and normalized candidate contracts. It also introduces stable identity based on semantic intent, provenance, family, and role.

However, several ambiguities remain:

- whether symmetric relations should preserve input order;
- whether aliases are identity-bearing;
- whether dependency lists are ordered;
- whether equivalent source expansions produce equivalent identities;
- whether optional fields participate in identity;
- whether a composed candidate inherits generator-local ordering;
- whether normalization occurs before or after provenance merge;
- how canonicalization-version changes affect historical replay.

These ambiguities become increasingly consequential as candidate families expand.

## Running Example: Bre

Consider a candidate representing a Moon–Saturn regulatory relationship.

One generator may emit:

```text
Moon -> Saturn
```

Another may emit:

```text
Saturn <-> Moon
```

A third may emit a configuration member list:

```text
[Saturn, Moon]
```

A fourth may identify the same source relationship using a normalized graph relationship ID.

If the underlying relationship is semantically symmetric for the relevant candidate role, these forms should canonicalize to the same semantic structure.

By contrast, a directed developmental relation such as:

```text
North Node direction shaped through Saturn
```

should not be canonicalized by alphabetically sorting the endpoints if direction is semantically meaningful.

The normalization rules must therefore be schema-aware and role-aware rather than globally syntactic.

## Proposed Evolution

Introduce a versioned canonicalization pipeline that runs after candidate contract validation and before stable identity assignment.

Recommended stages:

1. validate candidate shape;
2. classify semantic role;
3. normalize vocabulary;
4. normalize source references;
5. normalize relation direction;
6. normalize dependency order;
7. normalize transformation lineage references;
8. remove non-semantic fields from identity material;
9. serialize canonical identity material;
10. assign stable identity;
11. retain the original generated form for diagnostics.

Each stage should be deterministic and independently testable.

## Canonical Vocabulary

Candidate-family implementations may use local labels during development, but the canonical representation should use controlled vocabulary.

Examples include canonical values for:

- candidate family;
- semantic role;
- source type;
- dependency role;
- transformation operation;
- relation direction;
- configuration type;
- coverage domain;
- utility dimension.

Aliases should be resolved through a versioned registry.

For example:

```text
"natal_object" -> "object"
"aspect_relation" -> "relationship"
"cfg_synthesis" -> "configuration_synthesis"
```

The canonical value participates in identity. The original alias may remain in diagnostic metadata but should not create a distinct semantic candidate.

Unknown aliases should fail validation in strict profiles and produce structured warnings in exploratory profiles.

## Canonical Source References

Source references should normalize:

- source-type names;
- stable source IDs;
- endpoint ordering where the relation is symmetric;
- role labels;
- duplicate references;
- source hash representation.

For a symmetric relation, the canonical endpoint order should derive from stable source identity, not generator order.

For a directed relation, endpoint roles should remain explicit:

```json
{
  "source": "saturn",
  "target": "north_node",
  "direction": "directed"
}
```

Canonicalization must not erase semantic direction merely to produce lexical consistency.

## Canonical Dependency Sets

Dependencies should be represented as deterministic role-bearing references.

Recommended normalization:

1. canonicalize each dependency candidate ID;
2. preserve dependency role;
3. deduplicate exact `(candidate_id, role)` pairs;
4. sort by role, then stable candidate ID;
5. preserve multiplicity only when multiplicity is semantically meaningful.

Most dependency collections should behave as sets rather than ordered lists.

When order is meaningful, the schema should declare the dependency collection as an ordered sequence and include an explicit position or semantic slot. Generator emission order alone should never imply meaning.

## Canonical Configuration Membership

Configuration candidates require special treatment because the same structure may be emitted through multiple member orderings or decompositions.

Canonicalization should distinguish:

- unordered members;
- role-bearing members;
- ordered sequences;
- central-member configurations;
- endpoint-and-bridge configurations.

Examples:

### Unordered configuration

```text
{Moon, Saturn, North Node}
```

Members are sorted by stable identity.

### Hub-centered configuration

```text
hub = Saturn
members = {Moon, North Node}
```

The hub remains role-bearing and is not mixed into the ordinary member set.

### Ordered chain

```text
Moon -> Saturn -> North Node
```

Order is preserved because it expresses semantic structure.

This avoids treating all configurations as generic sorted bags.

## Canonical Semantic Intent

Stable identity should include a compact, structured semantic-intent object rather than rendered prose.

Illustrative form:

```json
{
  "domain": "developmental_regulation",
  "predicate": "structure_supports_regulation",
  "participants": [
    {
      "candidate_id": "cand:moon",
      "role": "regulated_function"
    },
    {
      "candidate_id": "cand:saturn",
      "role": "structuring_function"
    }
  ],
  "scope": "baseline"
}
```

Rendered wording such as:

- “structure supports regulation,”
- “regulation benefits from consistency,”
- “steady training contains emotional reactivity,”

may differ while pointing to the same structured semantic intent.

This allows downstream voice and wording changes without destabilizing candidate identity.

## Identity-Bearing and Non-Identity-Bearing Fields

The candidate schema should explicitly classify fields.

### Identity-bearing fields

Typically include:

- canonical family ID;
- semantic role;
- canonical semantic intent;
- canonical source provenance;
- semantically meaningful dependency roles;
- directionality;
- configuration membership;
- scope or temporal mode when meaning-bearing.

### Non-identity-bearing fields

Typically include:

- optimizer score;
- rank;
- calibration profile;
- generation timestamp;
- debug notes;
- rendered prose;
- display labels;
- serializer formatting;
- execution order;
- optional diagnostics.

### Conditionally identity-bearing fields

Some fields depend on candidate type:

- generator version;
- confidence class;
- source hash;
- temporal interval;
- authoring mode;
- compression level.

The schema should define these rules explicitly. Implementations should not infer them ad hoc.

## Canonical Serialization

Stable identity requires a deterministic byte representation.

The canonical serializer should define:

- UTF-8 encoding;
- normalized Unicode form;
- exact key ordering;
- exact list-order rules;
- normalized numeric representation;
- explicit handling of null and absent fields;
- no insignificant whitespace;
- stable boolean representation;
- stable timestamp format when timestamps are identity-bearing.

Canonical JSON is a reasonable interchange representation, but the architecture should define its own constrained canonical profile rather than rely on ordinary serializer defaults.

The stable candidate ID can then be derived from:

```text
namespace + canonicalization_version + canonical_bytes
```

using a documented cryptographic hash.

The full hash may be retained internally while a shorter prefixed representation is exposed in artifacts.

## Canonicalization Versioning

Canonicalization rules will evolve.

Every candidate identity should therefore be associated with:

- canonicalization profile ID;
- canonicalization version;
- hash algorithm;
- identity namespace.

A canonicalization-version change may alter IDs even when semantic meaning remains unchanged. Such changes should be treated as migrations, not silent identity changes.

Migration artifacts should include:

- old candidate ID;
- new candidate ID;
- old canonicalization version;
- new canonicalization version;
- equivalence classification;
- migration reason.

REC-016 historical provenance provides the appropriate lineage location.

## Equivalence Classes

Canonicalization should support explicit equivalence classes.

Recommended categories:

1. **Exact canonical equivalence**  
   Same canonical identity material.

2. **Representational equivalence**  
   Different original forms normalize to the same canonical form.

3. **Migration equivalence**  
   Different IDs across canonicalization versions are declared equivalent.

4. **Semantic overlap**  
   Candidates share substantial meaning but are not equivalent.

5. **Conflict**  
   Candidates make incompatible or mutually exclusive interpretations.

Only the first three should permit identity reconciliation. Semantic overlap belongs to REC-015 conflict resolution and portfolio redundancy logic.

## Canonicalization and Provenance

Canonicalization must not destroy the original lineage.

The provenance model should retain:

- original generator output hash;
- canonical candidate hash;
- canonicalization profile;
- transformations applied;
- alias resolutions;
- ordering normalizations;
- deduplication events;
- migration lineage.

Routine production artifacts do not need every normalization trace. Engineering and QA profiles should expose them.

Canonical source provenance should be authoritative for identity and coverage. Original source formatting should remain available only for diagnostics and replay.

## Canonicalization and Conflict Resolution

Conflict grouping should occur after canonicalization.

Otherwise, equivalent candidates can be incorrectly treated as competitors.

Recommended sequence:

```text
generate
-> validate
-> canonicalize
-> assign stable identity
-> merge exact equivalents
-> identify semantic overlap/conflict groups
-> score
-> optimize
```

Exact canonical equivalents should merge before utility scoring so they do not receive duplicate value.

The merged object should preserve contributing-family provenance.

## Canonicalization and Utility

Canonicalization itself should not improve a candidate’s utility score.

Its purpose is to ensure that utility is evaluated over semantic objects rather than syntactic variants.

After equivalent candidates merge:

- intrinsic semantic utility should be counted once;
- provenance completeness may improve;
- confidence may improve under an explicit evidence-combination rule;
- family agreement may be recorded;
- duplicate family emission should not create an additive bonus by default.

Any consensus or corroboration benefit should be explicitly calibrated rather than emerging accidentally through duplication.

## Canonicalization and Coverage

Coverage metrics should consume canonical semantic and source identities.

This prevents:

- duplicate coverage credit from equivalent candidates;
- false coverage loss after harmless generator refactoring;
- artificial portfolio drift after source reordering;
- inconsistent motif accounting.

A canonical candidate may cover multiple source relations when its provenance explicitly carries those relations, as defined in REC-016.

## Compatibility Analysis

REC-018 can be introduced incrementally.

### Phase A — Define Canonical Field Rules

Document identity-bearing, non-identity-bearing, and conditional fields.

### Phase B — Canonicalize Existing Candidate Families

Apply vocabulary, source-order, and dependency-order normalization without changing optimization.

### Phase C — Move Stable Identity After Canonicalization

Generate REC-017 IDs from canonical identity material.

### Phase D — Merge Exact Equivalents

Deduplicate equivalent candidates before conflict analysis and scoring.

### Phase E — Introduce Versioned Migrations

Provide old-to-new identity maps when canonicalization rules evolve.

During migration, existing IDs may be exposed as aliases. New outputs should identify the canonical ID as authoritative.

## Alternatives Considered

### Hash Raw Candidate JSON

Simple but unstable because ordinary JSON contains incidental ordering, optional metadata, and serializer-dependent formatting.

### Canonicalize Only at Serialization

Too late. Conflict grouping, utility scoring, identity, and coverage would already have operated on noncanonical objects.

### Use Rendered Prose as Identity Material

Rejected because wording, voice, localization, and editorial revision are not semantic identity.

### Let Each Candidate Family Define Its Own Canonicalization

Family-local normalization is useful internally but cannot guarantee cross-family equivalence. A shared canonical layer is required.

### Merge Candidates Through Fuzzy Text Similarity

Useful as a research diagnostic, but too nondeterministic and insufficiently explainable for authoritative identity reconciliation.

### Alphabetically Sort Every Collection

Rejected because some relations and configurations are directed or role-bearing. Canonicalization must be schema-aware.

## Implementation Considerations

Suggested components:

- `CanonicalizationProfile`;
- `CanonicalVocabularyRegistry`;
- `CanonicalCandidateNormalizer`;
- `CanonicalProvenanceNormalizer`;
- `CanonicalSerializer`;
- `CandidateIdentityFactory`;
- `CandidateEquivalenceIndex`;
- `CanonicalizationMigrationMap`.

Recommended API shape:

```python
result = canonicalizer.normalize(candidate, profile)

result.canonical_candidate
result.canonical_bytes
result.normalization_events
result.profile_id
result.version
```

Normalization should be pure: identical input and profile produce identical output without environment-dependent state.

## QA Strategy

### Unit Tests

Verify:

- alias normalization;
- symmetric endpoint sorting;
- directed endpoint preservation;
- dependency deduplication;
- role-preserving ordering;
- Unicode normalization;
- numeric normalization;
- null-versus-absent handling;
- deterministic canonical serialization.

### Equivalence Fixtures

Create pairs of candidates that differ only by:

- source order;
- dependency order;
- aliases;
- optional diagnostics;
- rendered prose;
- generator execution order;
- equivalent source expansion.

They should produce identical canonical forms and stable IDs.

### Non-Equivalence Fixtures

Create pairs differing by:

- semantic role;
- direction;
- configuration hub;
- temporal scope;
- meaning-bearing source membership;
- structured semantic predicate.

They should remain distinct.

### Cross-Family Fixtures

Have two candidate families independently emit the same semantic structure.

Verify:

- one canonical candidate;
- preserved contributing-family provenance;
- no duplicate intrinsic utility;
- no duplicate coverage;
- deterministic merged provenance.

### Migration Tests

Verify:

- old-to-new ID maps;
- replay under historical canonicalization profiles;
- migration equivalence classification;
- stable coverage across representational migrations;
- explicit ID changes after semantic modification.

### Empirical Regression Tests

For Bre and other reviewed graphs, verify:

- no false portfolio drift after generator reordering;
- no duplicate Moon–Saturn–Node motif candidates;
- stable candidate IDs across repeated execution;
- preserved direction for meaning-bearing developmental relations;
- unchanged authored output except where duplicate candidates are intentionally removed.

## Complexity / Benefit / Risk

**Implementation Complexity:** Medium

Canonical normalization rules are manageable, but schema-aware handling of direction, roles, configurations, and migrations requires careful design.

**Expected Benefit:** High

Canonicalization improves deterministic identity, conflict resolution, provenance, coverage, drift analysis, portfolio quality, and cross-family interoperability.

**Architectural Risk:** Medium-Low

The main risk is over-normalization: collapsing candidates that are similar but semantically distinct. Explicit role-aware schemas and strong non-equivalence fixtures mitigate this risk.

## Summary

REC-018 defines canonicalization as the bridge between candidate generation and stable semantic identity.

The architecture should:

- normalize vocabulary and source references;
- preserve semantic direction and member roles;
- distinguish identity-bearing from diagnostic fields;
- create deterministic canonical bytes;
- merge exact equivalents before scoring;
- version normalization rules;
- preserve migration lineage;
- retain original generator output for diagnostics.

With canonicalization in place, the Semantic Basis Extractor can treat semantically equivalent candidates as one object even when they originate from different families or representations.

The next recommendation should define the candidate registry and schema-governance mechanism that makes canonical vocabulary, roles, identity fields, and migration rules enforceable across implementations.

# REC-019 — Candidate Registry and Schema Governance

## Problem Statement

The Semantic Basis Extractor now depends on a growing set of shared concepts:

- candidate-family identifiers;
- semantic roles;
- source-reference types;
- dependency roles;
- transformation operations;
- utility dimensions;
- coverage domains;
- canonicalization rules;
- identity-bearing fields;
- migration mappings.

Without a governed registry, these concepts can drift across implementations. Candidate families may introduce near-duplicate labels, incompatible assumptions, or undocumented schema changes. The resulting failures are often subtle: candidate identities change unexpectedly, provenance can no longer be merged reliably, or downstream consumers receive semantically similar fields with different meanings.

A registry is therefore required to make shared vocabulary and schema contracts explicit, versioned, testable, and enforceable.

## Architectural Context

REC-011 through REC-014 established candidate-family expansion, lifecycle, deprecation, and composition.

REC-015 defined conflict resolution.

REC-016 defined layered provenance.

REC-017 defined stable candidate identity.

REC-018 defined canonicalization.

REC-019 provides the governance layer that makes those recommendations enforceable across candidate families and implementation teams.

The registry should not become a monolithic runtime service. It should instead act as a versioned architectural source of truth that can be:

- validated at development time;
- loaded at runtime;
- embedded into engineering artifacts;
- referenced in completion logs;
- used to generate schemas and documentation.

## Proposed Evolution

Introduce a versioned Candidate Registry containing controlled definitions for:

1. candidate families;
2. semantic roles;
3. source types;
4. dependency roles;
5. transformation operations;
6. utility dimensions;
7. coverage domains;
8. canonicalization rules;
9. identity field classifications;
10. compatibility and migration declarations.

Each registry entry should include:

- stable identifier;
- human-readable title;
- definition;
- owning module or architectural area;
- lifecycle status;
- introduced version;
- deprecated version, when applicable;
- replacement identifier, when applicable;
- compatibility notes;
- validation constraints;
- references to relevant recommendations.

## Candidate Family Entries

Every candidate family should register:

- family ID;
- generator contract version;
- supported semantic roles;
- accepted source types;
- emitted dependency roles;
- supported transformations;
- canonicalization profile;
- identity namespace;
- required provenance layers;
- lifecycle status;
- feature flag;
- fixture coverage status;
- production approval state.

Illustrative entry:

```json
{
  "family_id": "configuration_generator",
  "contract_version": "0.2",
  "status": "production",
  "semantic_roles": [
    "configuration_synthesis"
  ],
  "source_types": [
    "graph_relationship",
    "graph_object"
  ],
  "canonicalization_profile": "sbe-canonical-v0.2",
  "identity_namespace": "sbe:candidate:configuration",
  "required_provenance": [
    "sources",
    "dependencies",
    "transformations"
  ]
}
```

Candidate families not present in the active registry should be rejected in strict execution profiles.

## Semantic Role Registry

Semantic roles are central to canonicalization and identity.

Each role should define:

- role ID;
- semantic meaning;
- whether direction is meaningful;
- whether participant order is meaningful;
- whether multiplicity is meaningful;
- expected participant roles;
- permitted source types;
- permitted temporal scopes;
- canonicalization behavior;
- coverage behavior.

For example, an unordered configuration role may sort members, while an ordered developmental sequence must preserve position.

This schema-aware behavior prevents overly broad canonicalization rules from collapsing semantically distinct candidates.

## Source and Dependency Registries

Source-reference types should define:

- source ID format;
- whether external resolution is required;
- allowed role labels;
- hash requirements;
- canonical ordering behavior;
- whether the source can receive coverage credit.

Dependency roles should define:

- semantic purpose;
- whether the dependency is mandatory;
- whether order matters;
- whether closure is required;
- whether omission is authoring-only or semantic;
- how the dependency participates in identity.

This removes ambiguity about whether two dependency lists are equivalent.

## Transformation Registry

Transformation operations should be registered explicitly.

Examples:

- `configuration_synthesis`;
- `axis_compression`;
- `semantic_merge`;
- `candidate_replacement`;
- `temporal_activation`;
- `cross_family_composition`.

Each transformation definition should specify:

- accepted input roles;
- output role;
- whether it preserves semantic identity;
- whether it creates a new identity;
- required provenance fields;
- deterministic ordering rules;
- allowed recursion depth;
- compatibility behavior.

Unregistered transformation names should fail validation in strict profiles.

## Utility and Coverage Registries

Utility dimensions should define:

- dimension ID;
- interpretation;
- scale;
- valid range;
- normalization method;
- calibration ownership;
- whether the dimension is intrinsic or portfolio-relative;
- whether it can be absent;
- expected diagnostic fields.

Coverage domains should define:

- domain ID;
- covered semantic region;
- qualifying candidate roles;
- source attribution rules;
- target ranges;
- aggregation method.

This ensures that a candidate family cannot introduce a new utility or coverage dimension without declaring how it should be interpreted.

## Schema Governance Rules

Schema governance should follow a small set of explicit rules.

### Additive Changes

Adding an optional field with no identity or semantic effect may use a minor schema revision.

### Meaning-Changing Changes

Changing field meaning, identity participation, canonicalization behavior, or dependency semantics requires a major contract revision.

### Identifier Stability

Registered IDs should never be repurposed.

Deprecated identifiers remain reserved permanently.

### Replacement Declarations

Deprecated entries should identify replacements and migration guidance when possible.

### Registry Review

New entries should require:

- rationale;
- contract definition;
- fixtures;
- compatibility analysis;
- lifecycle status;
- owner;
- documentation.

### Generated Artifacts

Human-readable registry documentation and machine-readable schemas should be generated from the same source definitions.

## Registry Versioning

The registry should expose:

- registry version;
- candidate contract version;
- canonicalization profile version;
- provenance schema version;
- utility calibration profile version;
- coverage profile version.

These versions should be recorded in:

- completion logs;
- engineering outputs;
- QA summaries;
- portfolio manifests;
- migration reports.

A registry version should identify one coherent set of compatible contracts.

Not every calibration change requires a new candidate schema version, but the completion log should still record both.

## Compatibility Profiles

The registry should support named compatibility profiles.

Examples:

- `legacy-v0.1`;
- `sbe-v0.2-default`;
- `engineering-latest`;
- `strict-production`;
- `migration-v0.1-to-v0.2`.

A compatibility profile determines:

- permitted deprecated entries;
- warning versus failure behavior;
- canonicalization version;
- serializer behavior;
- required provenance fields;
- accepted candidate contract versions.

This allows historical replay without weakening current production validation.

## Registry Resolution

Registry resolution should be deterministic.

Recommended precedence:

1. explicit execution profile;
2. artifact-pinned registry version;
3. application default;
4. failure if no compatible registry can be resolved.

The system should never silently substitute a newer registry when replaying an artifact pinned to an older version.

## Validation Architecture

Validation should occur at several layers.

### Static Validation

Checks registry structure, duplicate identifiers, invalid replacements, circular migrations, and unresolved references.

### Candidate Validation

Checks emitted candidates against family, role, source, dependency, and transformation contracts.

### Portfolio Validation

Checks that all selected candidates share a compatible registry context.

### Artifact Validation

Checks embedded registry versions, hashes, and compatibility declarations.

### Migration Validation

Checks old-to-new mappings and preserved equivalence classifications.

Validation errors should be structured and machine-readable.

## Completion Log Integration

Every run should record:

- registry version;
- registry content hash;
- compatibility profile;
- candidate contract versions;
- canonicalization profile;
- provenance schema version;
- utility calibration profile;
- coverage profile;
- deprecated entries encountered;
- migration mappings applied.

This information is required for truthful reproducibility.

## QA Strategy

### Registry Unit Tests

Verify:

- unique identifiers;
- reserved deprecated identifiers;
- valid replacement chains;
- no circular migrations;
- valid lifecycle transitions;
- resolvable cross-references;
- deterministic serialization and hashing.

### Contract Tests

Each candidate family should prove that:

- every emitted role is registered;
- every source type is permitted;
- every dependency role is declared;
- every transformation is valid;
- every identity-bearing field matches the active profile;
- all required provenance layers are populated.

### Compatibility Tests

Verify:

- current artifacts under current profiles;
- legacy artifacts under pinned profiles;
- expected warnings for deprecated entries;
- hard failure for removed or incompatible contracts;
- deterministic migration output.

### Drift Tests

Compare registry snapshots and identify:

- added entries;
- deprecated entries;
- meaning-changing edits;
- identity-rule changes;
- canonicalization changes;
- coverage and utility changes.

A registry diff should classify changes by compatibility risk.

## Complexity / Benefit / Risk

**Implementation Complexity:** Medium

The registry itself is straightforward, but complete integration touches candidate generation, canonicalization, validation, logging, migration, and documentation tooling.

**Expected Benefit:** High

The registry prevents semantic drift, strengthens reproducibility, improves cross-family interoperability, and makes schema evolution auditable.

**Architectural Risk:** Medium-Low

The main risk is governance becoming too rigid or burdensome. Lightweight entry templates, generated documentation, and staged lifecycle states mitigate this risk.

## Summary

REC-019 establishes a governed Candidate Registry as the source of truth for shared candidate architecture.

The registry should define and version:

- candidate families;
- semantic roles;
- source and dependency types;
- transformation operations;
- utility and coverage dimensions;
- canonicalization rules;
- identity participation;
- compatibility and migrations.

This converts implicit implementation conventions into explicit architectural contracts.

The next recommendation should define the end-to-end candidate processing pipeline and stage boundaries, showing exactly where validation, canonicalization, identity assignment, merging, scoring, optimization, provenance finalization, and artifact emission occur.

# REC-020 — End-to-End Candidate Processing Pipeline

## Problem Statement

The recommendations developed so far define many important mechanisms:

- candidate generation;
- family composition;
- provenance;
- canonicalization;
- stable identity;
- conflict resolution;
- utility calibration;
- portfolio optimization;
- coverage measurement;
- drift analysis;
- compatibility and schema governance.

However, these mechanisms are only reliable when executed in a precise and deterministic stage order.

If candidate scoring occurs before canonical-equivalence merging, duplicate candidates can receive utility twice. If conflict grouping occurs before canonicalization, representational variants can be treated as semantic disagreements. If provenance is finalized too early, later composition and optimizer effects may be omitted. If coverage is computed before dependency closure, the portfolio may appear more complete than it actually is.

The Semantic Basis Extractor therefore requires one authoritative end-to-end processing pipeline with explicit stage boundaries, input/output contracts, invariants, and failure behavior.

## Architectural Context

REC-001 through REC-010 define the core candidate and portfolio-selection behavior.

REC-011 through REC-014 define candidate-family expansion, lifecycle, deprecation, and composition.

REC-015 through REC-019 define conflict resolution, provenance, stable identity, canonicalization, and schema governance.

REC-020 ties those recommendations into one execution model.

The processing pipeline should be treated as an architectural contract, not merely an implementation convenience. Individual components may be refactored, parallelized, or replaced, but the logical stage boundaries and invariants should remain stable unless changed through an explicit architecture revision.

## Design Goals

The pipeline should provide:

1. deterministic execution;
2. stage-local validation;
3. explicit data contracts;
4. replayability;
5. family-independent processing;
6. truthful diagnostics;
7. explainable selection;
8. compatibility-aware behavior;
9. bounded failure scope;
10. testable intermediate artifacts.

## Proposed Pipeline

The recommended logical pipeline is:

1. execution-context resolution;
2. source-artifact validation;
3. graph normalization;
4. candidate-family resolution;
5. candidate generation;
6. candidate contract validation;
7. cross-family composition;
8. canonicalization;
9. stable identity assignment;
10. exact-equivalence merge;
11. dependency graph construction;
12. conflict and overlap grouping;
13. intrinsic utility evaluation;
14. dependency-closure analysis;
15. portfolio-relative utility evaluation;
16. constrained portfolio optimization;
17. selection-stability analysis;
18. provenance finalization;
19. coverage and drift evaluation;
20. artifact materialization;
21. completion-log emission;
22. QA summary and exit-status determination.

These are logical stages. An implementation may fuse adjacent stages for performance only when it preserves identical externally observable behavior and diagnostics.

## Stage 1 — Execution-Context Resolution

Resolve all configuration required for deterministic execution.

Inputs may include:

- source artifact;
- requested semantic-basis size;
- execution profile;
- registry version;
- candidate-family feature flags;
- canonicalization profile;
- utility calibration profile;
- coverage profile;
- compatibility profile;
- output profile;
- random seed, if any randomized research behavior is permitted.

The resolved context should be immutable for the remainder of the run.

Required outputs:

- normalized execution request;
- resolved profile identifiers;
- registry content hash;
- feature-flag snapshot;
- deterministic run identifier.

Failure to resolve a required pinned profile should stop execution before candidate generation.

## Stage 2 — Source-Artifact Validation

Validate the upstream graph or semantic source artifact.

Checks should include:

- schema version;
- artifact integrity;
- source hash;
- required node and relationship types;
- stable source identifiers;
- unsupported or unknown structures;
- compatibility with the selected registry profile.

This stage distinguishes invalid input from unsupported-but-valid input.

Invalid input should fail.

Unsupported structures may produce structured exclusions when the execution profile permits partial processing.

## Stage 3 — Graph Normalization

Normalize source structures into the internal graph contract used by candidate generators.

Normalization may include:

- stable node ordering;
- stable relationship ordering;
- source-type aliases;
- direction normalization;
- relationship-key construction;
- duplicate source detection;
- dependency indexing;
- neighborhood indexing.

Graph normalization must not introduce semantic interpretations. Its role is to produce one deterministic factual substrate.

The normalized graph hash should be recorded for replay.

## Stage 4 — Candidate-Family Resolution

Resolve the candidate families that are eligible to execute.

Resolution considers:

- active registry version;
- execution profile;
- feature flags;
- source-type compatibility;
- lifecycle status;
- production approval;
- compatibility profile;
- required dependencies among generator modules.

The result should include:

- enabled families;
- disabled families;
- exclusion reasons;
- generator versions;
- deterministic execution order.

Execution order should not affect results, but it remains useful for reproducible logs and bounded resource planning.

## Stage 5 — Candidate Generation

Each enabled family generates candidate objects from the normalized graph.

Candidate generation should be:

- pure relative to graph and resolved execution context;
- deterministic;
- family-local;
- independent of portfolio budget;
- independent of optimizer rank;
- explicit about unsupported structures.

Generators should emit candidates through the normalized candidate contract rather than writing directly to final artifacts.

Candidate-generation outputs should preserve original family-local form for diagnostics.

## Stage 6 — Candidate Contract Validation

Validate every generated candidate against REC-019 registry contracts.

Checks include:

- registered family ID;
- supported semantic role;
- valid source types;
- permitted dependency roles;
- registered transformation operations;
- required provenance layers;
- schema correctness;
- valid identity-field declarations;
- source-reference resolution.

Invalid candidates should not silently enter optimization.

Depending on profile, failures may:

- stop the run;
- quarantine one candidate;
- quarantine one family;
- produce an engineering-only warning.

Production profiles should prefer failure or explicit quarantine over silent repair.

## Stage 7 — Cross-Family Composition

Apply registered composition operations from REC-014.

Examples include:

- configuration synthesis;
- axis synthesis;
- neighborhood enrichment;
- semantic merge;
- portfolio-refinement candidate construction;
- temporal composition, when supported.

Composition should consume validated candidates and emit new candidates through the same candidate contract.

Every transformation should add REC-016 transformation provenance.

The output of this stage includes both primitive and composed candidates.

## Stage 8 — Canonicalization

Apply the versioned REC-018 canonicalization profile.

Canonicalization should normalize:

- vocabulary;
- source references;
- participant roles;
- direction;
- dependency sets;
- configuration membership;
- transformation references;
- identity-bearing field representation.

The stage should produce:

- canonical candidate object;
- canonical bytes;
- normalization events;
- original-to-canonical reference.

No stable candidate ID should be assigned before this stage.

## Stage 9 — Stable Identity Assignment

Generate REC-017 candidate identities from canonical identity material.

Identity generation should use:

- identity namespace;
- canonicalization version;
- canonical bytes;
- documented hash algorithm.

This stage should verify:

- no accidental identity collision;
- identical canonical material produces identical IDs;
- distinct canonical material does not reuse an ID;
- migration aliases are recorded when applicable.

## Stage 10 — Exact-Equivalence Merge

Merge candidates that share exact canonical identity.

The merged candidate should preserve:

- all contributing families;
- all distinct source provenance;
- all transformation lineage;
- family-local diagnostics;
- corroboration information.

It should not receive duplicate intrinsic utility merely because several families emitted it.

This stage removes representational duplication before semantic conflict analysis.

## Stage 11 — Dependency Graph Construction

Construct the candidate dependency graph.

Checks include:

- resolvable dependency IDs;
- dependency-role validity;
- cycle detection;
- closure cost;
- mandatory versus optional dependencies;
- dependency depth;
- compatibility across families.

Dependency cycles should fail validation unless a future explicitly registered construct permits them.

The stage should produce a deterministic topological order.

## Stage 12 — Conflict and Overlap Grouping

Classify candidate relationships as:

- exact equivalent;
- migration equivalent;
- semantic overlap;
- conflict;
- independent.

Exact equivalents should already have been merged.

REC-015 arbitration operates over overlap and conflict groups, not raw candidate-generation output.

Grouping should preserve:

- conflict-group ID;
- candidate members;
- overlap rationale;
- semantic dimensions involved;
- provenance references.

## Stage 13 — Intrinsic Utility Evaluation

Evaluate candidate utility dimensions that do not depend on the selected portfolio.

Examples may include:

- semantic importance;
- evidence strength;
- specificity;
- authorability;
- confidence;
- structural inevitability penalty;
- intrinsic redundancy indicators;
- source completeness.

Intrinsic scores should be computed once per canonical candidate.

Calibration profile and component values should be recorded.

## Stage 14 — Dependency-Closure Analysis

For each candidate, determine the semantic and budget cost of making it authorable.

The stage should calculate:

- required dependency set;
- already implied support;
- closure size;
- closure utility;
- closure redundancy;
- closure budget impact;
- invalid or impossible closures.

Candidates with impossible dependency closure should be excluded with structured reasons.

## Stage 15 — Portfolio-Relative Utility Evaluation

Evaluate utility contributions that depend on the current or proposed portfolio.

Examples include:

- configuration-completion bonus;
- hub-preservation bonus;
- utility-vector diversity;
- marginal coverage;
- bundle complementarity;
- redundancy penalty;
- conflict-resolution effects.

These values may be recomputed during optimization.

The implementation should preserve deterministic comparison behavior and stable tie-breakers.

## Stage 16 — Constrained Portfolio Optimization

Select the semantic basis under the requested budget and constraints.

Constraints may include:

- exact or bounded claim count;
- dependency closure;
- conflict exclusions;
- coverage targets;
- family-independent selection;
- authoring budget;
- required anchor candidates;
- compatibility restrictions.

The optimizer should compare marginal bundles rather than isolated candidates when dependencies or configuration completion make isolated ranking misleading.

Required outputs include:

- selected portfolio;
- rejected candidates;
- exclusion reasons;
- budget usage;
- marginal selection trace;
- unresolved constraints.

## Stage 17 — Selection-Stability Analysis

Run the stability analyses defined in REC-007 and REC-008.

Depending on execution profile, this may include:

- near-boundary comparison;
- alternate tie-break evaluation;
- nearby budget evaluation;
- calibration perturbation;
- candidate-family ablation;
- portfolio drift comparison;
- repeat execution.

Production compact profiles may use reduced diagnostics. Engineering and QA profiles should produce the complete analysis.

The completion log must state which stability checks actually ran.

## Stage 18 — Provenance Finalization

Finalize layered provenance after selection.

This stage should attach or consolidate:

- source provenance;
- dependency provenance;
- transformation provenance;
- decision provenance;
- historical provenance.

Finalization occurs after optimization because decision provenance is not available earlier.

The stage should not modify semantic identity.

Selected and rejected candidates may receive different levels of provenance materialization depending on output profile.

## Stage 19 — Coverage and Drift Evaluation

Evaluate the selected portfolio using REC-008 through REC-010.

Outputs should include:

- source coverage;
- semantic-domain coverage;
- configuration coverage;
- hub coverage;
- dependency coverage;
- target attainment;
- uncovered high-priority regions;
- portfolio drift from comparison baseline;
- candidate-family contribution.

Coverage should operate over canonical identities and explicit provenance, not raw candidate count.

## Stage 20 — Artifact Materialization

Produce requested artifacts from the finalized run state.

Possible outputs include:

- selected authoring packet;
- engineering candidate inventory;
- rejection report;
- provenance index;
- coverage report;
- drift report;
- migration report;
- optimizer trace;
- QA fixture output.

Materializers should consume immutable finalized structures.

No materializer should independently reinterpret, rescore, or reorder semantic candidates except through documented presentation ordering.

## Stage 21 — Completion-Log Emission

Emit a truthful completion log.

The log should include:

- source artifact hash;
- normalized graph hash;
- execution profile;
- registry version and hash;
- enabled and disabled candidate families;
- generator versions;
- canonicalization version;
- identity namespace and hash algorithm;
- utility calibration profile;
- coverage profile;
- candidate counts by stage;
- selected portfolio size;
- excluded and quarantined counts;
- checks performed;
- checks skipped;
- determinism evidence;
- output artifact hashes;
- warnings and errors;
- final status.

The log should distinguish planned checks from executed checks.

## Stage 22 — QA Summary and Exit Status

Aggregate validation, optimization, coverage, and artifact results into a machine-readable QA summary.

Recommended statuses:

- `PASS`;
- `PASS_WITH_WARNINGS`;
- `PARTIAL`;
- `FAIL_INPUT`;
- `FAIL_CONTRACT`;
- `FAIL_OPTIMIZATION`;
- `FAIL_ARTIFACT`;
- `FAIL_DETERMINISM`.

Exit status should align with the summary status.

Expected user-facing failures should produce concise structured messages rather than unhandled tracebacks.

## Pipeline Invariants

The following invariants should hold:

1. canonicalization precedes identity;
2. identity precedes exact-equivalence merge;
3. exact-equivalence merge precedes utility scoring;
4. dependency graph construction precedes optimization;
5. intrinsic utility is computed over canonical candidates;
6. portfolio-relative utility is not treated as source evidence;
7. coverage uses finalized canonical provenance;
8. materialization does not change selection;
9. completion logs describe only checks that actually ran;
10. repeated execution under identical inputs and profiles produces identical authoritative artifacts.

## Intermediate Artifacts

Engineering profiles should optionally preserve stage snapshots:

- normalized graph;
- raw generated candidates;
- validated candidates;
- composed candidates;
- canonical candidates;
- equivalence-merged candidates;
- dependency graph;
- conflict groups;
- intrinsic utility table;
- optimizer input;
- selected portfolio;
- finalized provenance.

These snapshots are valuable for debugging and regression analysis.

Production profiles may omit them while retaining hashes and counts.

## Error Containment

Failures should be attributed to the narrowest meaningful stage.

Examples:

- malformed source artifact: Stage 2;
- invalid candidate emitted by one family: Stage 6;
- provenance cycle: Stage 7 or Stage 18;
- canonicalization collision: Stage 9;
- unsatisfied dependency closure: Stage 14;
- infeasible portfolio constraints: Stage 16;
- output write failure: Stage 20;
- determinism mismatch: Stage 22.

A stage failure should preserve earlier diagnostic outputs when safe and configured.

The system should not present a partial portfolio as complete unless the status explicitly states `PARTIAL`.

## Parallelism and Performance

Some stages can execute in parallel:

- independent candidate families;
- candidate validation;
- canonicalization;
- intrinsic utility evaluation;
- closure analysis;
- artifact rendering.

However, parallel execution must preserve deterministic aggregation.

Recommended rules:

- sort inputs before parallel dispatch;
- use stable candidate IDs for result collation;
- avoid shared mutable scoring state;
- use deterministic reduction;
- record worker-independent output ordering.

The logical stage sequence remains authoritative even when physical execution overlaps.

## Replay Architecture

A replayable run requires:

- source artifact or source hash with resolvable artifact;
- execution request;
- registry snapshot;
- feature-flag snapshot;
- generator versions;
- canonicalization profile;
- calibration profiles;
- compatibility profile;
- deterministic implementation version.

Replay modes may include:

- full recomputation;
- candidate-set replay;
- optimizer-only replay;
- artifact-rematerialization replay.

Each replay mode should state which stages were reused and which were rerun.

## Compatibility Analysis

The pipeline can be introduced incrementally.

### Phase A — Instrument Current Processing

Map current operations to the proposed stage model and emit stage counts.

### Phase B — Enforce Critical Ordering

Ensure canonicalization, identity, equivalence merge, and dependency analysis occur in the required sequence.

### Phase C — Introduce Stage Contracts

Add typed stage inputs and outputs with validation.

### Phase D — Add Replayable Intermediate Hashes

Record hashes and optional stage snapshots.

### Phase E — Enforce Completion-Log Truthfulness

Require every declared check and artifact to correspond to an executed stage result.

Legacy execution may remain available through a compatibility profile, but it should be identified clearly as a different pipeline contract.

## Alternatives Considered

### One Monolithic Extraction Function

Simple initially, but difficult to test, replay, diagnose, or evolve safely. Rejected for the authoritative architecture.

### Family-Specific End-to-End Pipelines

Allows local optimization but fragments canonicalization, scoring, provenance, and compatibility behavior. Rejected in favor of family-independent stages.

### Score During Candidate Generation

Conflates semantic generation with portfolio policy and prevents clean recalibration. Rejected.

### Finalize Provenance Before Optimization

Cannot capture decision provenance truthfully. Rejected.

### Compute Coverage Before Selection

Useful for candidate-inventory analysis but not sufficient as selected-portfolio coverage. Final coverage must occur after selection and provenance finalization.

### Materializers Recompute Presentation-Specific Selection

Rejected because it would create multiple semantic bases from one run without explicit optimizer profiles.

## Implementation Considerations

Suggested stage interfaces:

```python
context = resolve_execution_context(request)
source = validate_source_artifact(context)
graph = normalize_graph(source, context)
families = resolve_candidate_families(graph, context)
raw = generate_candidates(graph, families, context)
validated = validate_candidates(raw, context)
composed = compose_candidates(validated, context)
canonical = canonicalize_candidates(composed, context)
identified = assign_candidate_ids(canonical, context)
merged = merge_exact_equivalents(identified, context)
dependencies = build_dependency_graph(merged, context)
groups = classify_candidate_relations(merged, context)
intrinsic = evaluate_intrinsic_utility(merged, context)
closures = analyze_dependency_closure(intrinsic, dependencies, context)
portfolio = optimize_portfolio(closures, groups, context)
stability = analyze_selection_stability(portfolio, context)
finalized = finalize_provenance(portfolio, stability, context)
metrics = evaluate_coverage_and_drift(finalized, context)
artifacts = materialize_outputs(finalized, metrics, context)
log = emit_completion_log(artifacts, context)
summary = emit_qa_summary(log, context)
```

Each stage result should be immutable or treated as immutable.

## QA Strategy

### Stage Contract Tests

Verify each stage:

- accepts only valid prior-stage outputs;
- rejects malformed inputs;
- produces deterministic outputs;
- records required metadata;
- does not perform responsibilities assigned to later stages.

### Ordering Tests

Intentionally change stage ordering and verify that contract tests detect:

- scoring before merge;
- identity before canonicalization;
- optimization before closure;
- coverage before finalized provenance;
- logging before artifact completion.

### Replay Tests

Verify:

- full replay;
- optimizer-only replay;
- rematerialization replay;
- pinned historical registry replay;
- deterministic stage hashes.

### Failure Tests

Inject failures at every stage and verify:

- correct status;
- correct exit code;
- concise user-facing message;
- preserved diagnostics;
- no falsely complete artifact set.

### Empirical End-to-End Tests

For Bre and other reviewed graphs, verify:

- expected family counts;
- no duplicate canonical candidates;
- valid dependency closure;
- stable portfolio selection;
- complete provenance;
- expected coverage;
- byte-identical authoritative artifacts across repeated runs.

## Complexity / Benefit / Risk

**Implementation Complexity:** High

The pipeline touches every major subsystem and requires explicit contracts, diagnostics, and migration from any monolithic processing paths.

**Expected Benefit:** Very High

A governed end-to-end pipeline improves determinism, explainability, replayability, QA, compatibility, and future candidate-family expansion.

**Architectural Risk:** Medium

The main risk is overengineering stage boundaries or creating excessive intermediate data. Logical stages can remain explicit while physical execution and artifact retention are optimized by profile.

## Summary

REC-020 defines the authoritative execution spine for the Semantic Basis Extractor.

The key architectural sequence is:

```text
resolve
-> validate source
-> normalize graph
-> generate
-> validate candidates
-> compose
-> canonicalize
-> identify
-> merge equivalents
-> build dependencies
-> group conflicts
-> score
-> analyze closure
-> optimize
-> test stability
-> finalize provenance
-> measure coverage and drift
-> materialize
-> log
-> summarize QA
```

This ordering ensures that candidate families can expand without undermining semantic equivalence, utility calibration, dependency correctness, provenance truthfulness, or reproducibility.

The next recommendation should define the completion-log and execution-diagnostics contract in detail, including required fields, truthfulness rules, stage counts, check coverage, artifact hashes, and user-facing failure reporting.

# REC-021 — Completion Log and Execution Diagnostics

## Problem Statement

A deterministic Semantic Basis Extractor is only trustworthy when every execution leaves behind a truthful, replayable, machine-readable record of what actually happened. Completion logs should document executed stages, inputs, outputs, validation results, skipped work, warnings, failures, artifact hashes, and determinism evidence without overstating what was performed.

## Architectural Context

REC-020 defined the execution pipeline. REC-021 specifies the required diagnostics and completion-log contract produced by that pipeline.

## Proposed Evolution

Every execution should emit a structured completion log that records:

- execution context and profile versions;
- source and normalized graph hashes;
- enabled and disabled candidate families;
- stage start/end status;
- candidate counts entering and leaving each stage;
- validation failures and quarantines;
- canonicalization and registry versions;
- optimization summary;
- coverage summary;
- artifact hashes;
- warnings;
- determinism evidence;
- final QA status.

The log should distinguish:

- completed versus skipped stages;
- expected omissions versus failures;
- informational notes versus warnings;
- warnings versus fatal errors.

No check should be reported as executed unless evidence from that stage exists.

## Truthfulness Rules

The completion log should never:

- claim a QA check that did not execute;
- imply deterministic replay when replay was not verified;
- report artifact generation before hashes are available;
- silently suppress failed stages.

Unknown values should be recorded explicitly as unknown rather than inferred.

## Diagnostic Levels

Profiles may expose different levels of detail:

- Compact production
- Standard engineering
- Full QA / research

Lower-detail profiles may omit intermediate artifacts but should never omit the existence of skipped checks.

## QA Strategy

Verify:

- deterministic logs across repeated runs;
- truthful stage accounting;
- stable artifact hashes;
- correct warning/error classification;
- compatibility across registry versions.

## Complexity / Benefit / Risk

Implementation Complexity: Medium

Expected Benefit: Very High

Architectural Risk: Low

## Summary

Completion logs become authoritative execution records, enabling reproducibility, debugging, auditability, regression analysis, and trustworthy user-facing reporting.

# REC-022 — Output Profiles

## Problem Statement

Different consumers require different levels of detail. A report author, regression suite, researcher, and production application should not all receive identical artifacts. Output profiles standardize what is emitted while preserving one authoritative execution pipeline.

## Principles

Output profiles affect **materialization only**. They must never alter:

- candidate generation,
- canonicalization,
- identity,
- optimization,
- provenance,
- completion-log truthfulness.

Only the rendered artifacts and retained diagnostics vary.

## Standard Profiles

### Compact

Minimal authoring payload containing only finalized selected candidates, essential provenance, summary metrics, and completion status.

### Standard

Default engineering profile including selected portfolio, rejection summary, coverage summary, completion log, and artifact manifest.

### Engineering

Adds candidate inventories, optimizer traces, dependency graphs, canonicalization diagnostics, conflict groups, and validation summaries.

### QA

Adds every validation result, intermediate hashes, regression artifacts, determinism evidence, fixture outputs, and stage statistics needed for automated verification.

### Research

Retains all QA outputs plus optional experimental metrics, intermediate stage snapshots, alternate optimization comparisons, calibration experiments, and exploratory diagnostics.

## Required Guarantees

Every profile should:

- identify itself explicitly;
- embed registry and compatibility versions;
- preserve artifact hashes;
- emit a truthful completion log;
- avoid recomputation during rendering.

## Compatibility

Profiles should remain backward-compatible whenever practical. New optional artifacts may be added, but existing required artifacts should not silently disappear within a profile version.

## QA

Verify that identical execution under different profiles produces identical selected portfolios and canonical identities. Differences should be limited to emitted diagnostics and auxiliary artifacts.

## Complexity / Benefit / Risk

Implementation Complexity: Low-Medium

Expected Benefit: High

Architectural Risk: Low

## Summary

Output profiles provide audience-specific materialization while preserving one deterministic semantic pipeline and one authoritative semantic basis.

# REC-023 — Artifact Packaging and Manifest Contracts

## Problem Statement

Execution artifacts should be portable, self-describing, and verifiable. Packaging contracts prevent ambiguity about what files belong together and how they relate to one execution.

## Package Principles

Each package should contain:

- selected artifacts;
- completion log;
- manifest;
- profile identifier;
- registry versions;
- compatibility profile;
- artifact hashes.

Packages should be immutable after publication.

## Manifest

Every manifest should record:

- package identifier;
- creation timestamp;
- execution profile;
- output profile;
- registry version;
- canonicalization version;
- completion-log hash;
- list of included artifacts;
- SHA-256 hash for every artifact.

## Required Behavior

Consumers should validate manifest hashes before loading artifacts.

Missing or modified artifacts should invalidate the package.

## Packaging Profiles

Compact packages contain only production artifacts.

Engineering packages additionally include diagnostics.

QA and Research packages include regression evidence and optional intermediate snapshots.

## QA

Verify manifest integrity, deterministic package reproduction, complete hash coverage, and profile compliance.

## Complexity / Benefit / Risk

Implementation Complexity: Low

Expected Benefit: High

Architectural Risk: Low

## Summary

Artifact packages become self-contained, verifiable execution bundles suitable for archival, replay, exchange, and regression testing.

# REC-024 — Replay and Reproducibility Contracts

## Problem Statement

A Semantic Basis Extractor run should be reproducible not only in principle, but through an explicit replay contract. Without that contract, two executions can appear equivalent while differing in source normalization, registry state, candidate-family versions, canonicalization rules, optimization settings, artifact materialization, or QA coverage.

Replay must therefore be treated as a first-class architectural capability rather than an informal debugging convenience.

## Architectural Context

REC-020 defined the authoritative end-to-end execution pipeline.

REC-021 defined truthful completion logs and execution diagnostics.

REC-022 defined output profiles.

REC-023 defined artifact packaging and manifest contracts.

REC-024 specifies how those artifacts, logs, manifests, registry snapshots, and stage contracts support deterministic recomputation and historical reproduction.

## Design Goals

Replay should provide:

1. explicit replay modes;
2. deterministic stage reuse;
3. pinned execution context;
4. historical compatibility;
5. stage-level provenance;
6. reproducibility diagnostics;
7. clear equivalence claims;
8. artifact integrity verification;
9. failure transparency;
10. bounded migration behavior.

## Replay Modes

The system should support several distinct replay modes.

### Full Replay

Re-execute the entire REC-020 pipeline from the original source artifact.

Full replay reruns:

- source validation;
- graph normalization;
- family resolution;
- candidate generation;
- candidate validation;
- composition;
- canonicalization;
- identity;
- equivalence merge;
- dependency analysis;
- scoring;
- optimization;
- provenance finalization;
- coverage and drift;
- materialization;
- completion logging;
- QA summary.

This is the strongest reproducibility mode.

### Candidate-Set Replay

Reuse a preserved canonical candidate inventory and rerun:

- dependency graph construction;
- conflict grouping;
- utility evaluation;
- optimization;
- stability analysis;
- provenance finalization;
- coverage;
- artifact materialization.

This mode is useful for optimizer and calibration work.

It does not verify candidate-generation determinism.

### Optimizer-Only Replay

Reuse the fully prepared optimizer input and rerun:

- constrained optimization;
- selection stability;
- decision provenance;
- coverage;
- selected-portfolio materialization.

This mode is useful for selection-policy regression tests.

It does not verify candidate construction, canonicalization, or intrinsic scoring.

### Artifact Rematerialization Replay

Reuse finalized semantic results and regenerate output artifacts under the same or a different compatible output profile.

This mode reruns only materialization, packaging, and artifact hashing.

It must not rescore, reinterpret, or change selected candidates.

### Migration Replay

Load a historical package under its pinned compatibility profile, apply an explicit migration plan, and produce a new package under a newer registry or schema contract.

Migration replay should preserve:

- original package identity;
- migration mapping;
- old-to-new candidate identity correspondence;
- equivalence classification;
- changed artifact list;
- migration warnings.

Migration replay is not equivalent to historical full replay unless all original implementation versions remain available.

## Replay Request Contract

A replay request should declare:

- replay mode;
- source package or source artifact;
- expected parent execution ID;
- registry version;
- compatibility profile;
- candidate-family versions;
- canonicalization profile;
- identity algorithm;
- utility calibration profile;
- coverage profile;
- execution profile;
- output profile;
- implementation version;
- permitted migrations;
- expected authoritative artifact hashes, when available.

Implicit profile substitution should be prohibited.

## Pinned Execution Context

A reproducible run should pin every versioned input that can affect semantics.

At minimum:

- source artifact hash;
- source schema version;
- normalized graph contract version;
- candidate registry version and content hash;
- enabled family set;
- generator versions;
- transformation registry version;
- canonicalization version;
- candidate identity namespace;
- hash algorithm;
- utility calibration profile;
- optimizer contract version;
- coverage profile;
- compatibility profile;
- implementation build identifier.

Output-only dependencies should also be pinned when byte-identical artifact reproduction is required.

Examples include:

- serializer version;
- template version;
- locale;
- line-ending policy;
- compression implementation;
- timestamp policy.

## Levels of Reproducibility

The architecture should distinguish several claims.

### Semantic Reproducibility

The same canonical candidate identities, selected portfolio, dependency structure, conflict decisions, and finalized provenance are produced.

### Metric Reproducibility

The same utility components, coverage values, drift metrics, and stage counts are produced.

### Artifact Reproducibility

The same logical artifact contents are produced, ignoring permitted nondeterministic packaging metadata.

### Byte Reproducibility

Authoritative artifact bytes and hashes are identical.

### Historical Reproducibility

A past run can be reproduced using the exact historical contracts and implementation versions.

Completion logs should state the strongest level actually verified.

## Determinism Requirements

For identical inputs and pinned context:

- candidate generation should be deterministic;
- canonical serialization should be deterministic;
- identity assignment should be deterministic;
- merge ordering should be deterministic;
- dependency ordering should be deterministic;
- optimizer tie-breaking should be deterministic;
- provenance ordering should be deterministic;
- artifact ordering should be deterministic;
- authoritative timestamps should be fixed or excluded from hashed content;
- archive member ordering should be deterministic when byte reproducibility is claimed.

Parallelism must not change authoritative results.

## Replay Package Requirements

A replayable package should contain or reference:

- source artifact;
- manifest;
- completion log;
- registry snapshot or resolvable immutable registry reference;
- execution request;
- resolved execution context;
- candidate-family version map;
- calibration profiles;
- canonicalization profile;
- authoritative artifact hashes;
- implementation identifier;
- optional intermediate stage artifacts.

External references should be content-addressed wherever possible.

A package that depends on mutable external state should not claim complete replayability.

## Stage Reuse Contract

Every reused stage artifact should declare:

- originating execution ID;
- producing stage;
- input hashes;
- output hash;
- stage contract version;
- registry context;
- compatibility profile;
- validation status.

A replay should validate those declarations before reuse.

If a reused artifact fails validation, the replay should either:

- recompute from an earlier valid stage;
- fail explicitly;
- proceed only under a clearly marked research override.

Silent fallback should be avoided.

## Replay Equivalence Report

Every replay should emit an equivalence report comparing the replay to its parent or expected baseline.

The report should include:

- replay mode;
- compared execution IDs;
- context differences;
- candidate identity differences;
- selected portfolio differences;
- provenance differences;
- utility differences;
- coverage differences;
- artifact hash differences;
- skipped comparison dimensions;
- strongest verified reproducibility level;
- final equivalence status.

Recommended statuses:

- `BYTE_IDENTICAL`;
- `ARTIFACT_EQUIVALENT`;
- `METRIC_EQUIVALENT`;
- `SEMANTICALLY_EQUIVALENT`;
- `EXPECTED_MIGRATION_DIFFERENCE`;
- `UNEXPECTED_DRIFT`;
- `INSUFFICIENT_EVIDENCE`;
- `REPLAY_FAILED`.

## Historical Compatibility

Historical replay should prefer original pinned contracts.

If original versions are unavailable, the system may perform migration replay, but should not represent the result as an exact historical reproduction.

A historical compatibility registry should track:

- supported legacy registry versions;
- available generator implementations;
- compatible runtime versions;
- required migrations;
- known non-reproducible eras;
- artifact format readers.

Deprecated identifiers should remain resolvable for historical interpretation.

## Environment Capture

Implementation environments can affect byte-level results.

Where byte reproducibility matters, capture:

- operating-system family;
- runtime version;
- dependency lockfile hash;
- locale;
- timezone;
- filesystem case behavior;
- serializer implementation;
- archive implementation;
- compression settings.

Semantic reproducibility should remain portable across environments whenever possible.

## Time and Timestamp Handling

Wall-clock time should not affect semantic outputs.

Recommended rules:

- derive semantic evaluation time only from explicit request fields;
- record execution time in completion logs;
- exclude volatile timestamps from canonical semantic hashes;
- use fixed timestamps in deterministic archives when byte reproduction is required;
- distinguish source-time, evaluation-time, and execution-time fields.

## Randomness Policy

Production Semantic Basis Extractor behavior should avoid randomness.

If research profiles use randomized sampling or perturbation:

- a seed is required;
- the algorithm version is required;
- random behavior should be isolated from authoritative production selection;
- the completion log must state that randomized checks ran;
- repeated execution with the same seed should reproduce results.

Unseeded randomness should not participate in authoritative artifacts.

## Migration Constraints

Migration may change representation without changing semantic identity.

Migration plans should classify each change as:

- exact representation migration;
- canonical identity migration;
- schema-only migration;
- semantic reinterpretation;
- unsupported historical conversion.

Semantic reinterpretation should create new candidate identities or an explicit lineage relation rather than silently preserving old identity.

## Failure Behavior

Replay failures should identify:

- earliest invalid stage;
- missing pinned dependency;
- unavailable implementation version;
- incompatible registry;
- hash mismatch;
- unsupported migration;
- nondeterministic result;
- artifact rematerialization failure.

A replay should not overwrite the original package.

Partial replay outputs should be stored separately and marked non-authoritative unless the requested replay mode completes successfully.

## Completion Log Integration

Replay completion logs should include:

- replay mode;
- parent execution ID;
- reused stages;
- recomputed stages;
- migrated stages;
- validation results for reused artifacts;
- comparison baseline;
- equivalence report hash;
- strongest verified reproducibility level;
- unexpected drift summary.

This extends REC-021 without replacing the normal execution record.

## QA Strategy

### Full Replay Tests

Verify that repeated full execution produces:

- identical canonical candidate IDs;
- identical selected portfolio;
- identical utility values;
- identical coverage metrics;
- identical authoritative artifacts.

### Stage Reuse Tests

Verify:

- valid stage reuse;
- rejection of mismatched stage hashes;
- recomputation from the nearest valid boundary;
- correct accounting of reused and rerun stages.

### Optimizer Replay Tests

Verify that optimizer-only replay reproduces the selected portfolio from preserved optimizer inputs.

### Rematerialization Tests

Verify that changing output profile changes only permitted artifacts and does not change semantic selection.

### Historical Replay Tests

Verify supported historical registry and generator combinations.

### Migration Replay Tests

Verify:

- deterministic migration;
- complete identity mapping;
- explicit semantic changes;
- correct lineage preservation.

### Negative Tests

Inject:

- missing registry snapshots;
- wrong hashes;
- unavailable generator versions;
- incompatible canonicalization profiles;
- altered optimizer inputs;
- nondeterministic ordering.

The system should fail with specific diagnostic statuses.

### Cross-Environment Tests

Where practical, verify semantic reproducibility across supported environments and byte reproducibility within the declared reproducible environment profile.

## Complexity / Benefit / Risk

**Implementation Complexity:** Medium-High

Replay requires persistent stage metadata, immutable version references, comparison tooling, and disciplined separation between semantic and materialization stages.

**Expected Benefit:** Very High

Replay contracts strengthen regression testing, historical auditability, debugging, calibration development, migration safety, and user trust.

**Architectural Risk:** Medium-Low

The primary risk is claiming stronger reproducibility than the retained evidence supports. Explicit reproducibility levels and equivalence reports mitigate that risk.

## Summary

REC-024 establishes replay and reproducibility as explicit architectural contracts.

The system should support:

- full replay;
- candidate-set replay;
- optimizer-only replay;
- artifact rematerialization;
- migration replay.

Every replay should pin its execution context, validate reused stages, emit an equivalence report, and state the strongest reproducibility level actually verified.

The next recommendation should define operational configuration and feature-flag governance, including profile resolution, safe defaults, environment overrides, experimental controls, and configuration provenance.

# REC-025 — Operational Configuration and Feature-Flag Governance

## Problem Statement

Configuration affects execution semantics as much as code. Profiles, feature flags, environment overrides, and experimental options must therefore be governed as versioned architectural inputs rather than informal runtime switches.

## Principles

Configuration should be:

- explicit;
- versioned;
- reproducible;
- validated;
- minimally surprising;
- recorded in completion logs.

Feature flags should never silently change authoritative semantics.

## Configuration Sources

Supported configuration layers should include:

1. built-in defaults;
2. named execution profiles;
3. project configuration;
4. explicit command-line or API request;
5. environment overrides where permitted.

Later layers override earlier layers only according to documented precedence.

## Feature Flags

Every feature flag should define:

- identifier;
- purpose;
- default state;
- lifecycle status;
- owner;
- compatibility impact;
- completion-log visibility.

Experimental flags should be isolated from production profiles unless explicitly enabled.

## Safe Defaults

Production defaults should favor:

- deterministic behavior;
- complete validation;
- truthful diagnostics;
- stable canonicalization;
- reproducibility over convenience.

## Configuration Provenance

Every run should record:

- resolved configuration;
- overridden values;
- enabled feature flags;
- profile identifiers;
- configuration hash.

## Validation

Unknown configuration keys, incompatible profiles, or conflicting feature flags should fail validation in strict execution modes.

## QA

Verify deterministic profile resolution, stable precedence rules, feature-flag isolation, and identical semantic outputs when disabled flags are ignored.

## Complexity / Benefit / Risk

Implementation Complexity: Medium

Expected Benefit: High

Architectural Risk: Low

## Summary

Operational configuration becomes a governed architectural contract, ensuring that execution semantics remain reproducible, auditable, and intentionally controlled across environments.

# REC-026 — Operational Deployment and Lifecycle Guidance

## Problem Statement

Successful architecture extends beyond implementation. The Semantic Basis Extractor requires consistent deployment, upgrade, monitoring, rollback, and retirement practices so that operational changes do not undermine deterministic behavior or reproducibility.

## Deployment Principles

Operational deployments should preserve:

- deterministic execution;
- immutable released artifacts;
- versioned registries;
- explicit compatibility profiles;
- reproducible configuration;
- observable health.

Deployment should never silently alter semantic behavior.

## Lifecycle Stages

Recommended lifecycle:

1. Experimental
2. Development
3. Internal QA
4. Staged Production
5. General Availability
6. Deprecated
7. Retired

Every release should declare its lifecycle stage.

## Upgrade Policy

Upgrades should identify:

- schema changes;
- registry changes;
- canonicalization changes;
- compatibility impacts;
- migration requirements;
- rollback support.

Major semantic changes require explicit migration guidance.

## Rollback

Rollback should restore:

- implementation version;
- configuration;
- registry;
- compatibility profile;
- feature flags.

Rollback should not invalidate historical artifacts.

## Operational Monitoring

Monitor:

- execution failures;
- validation failures;
- determinism regressions;
- replay failures;
- artifact integrity;
- performance trends.

Monitoring data should remain separate from semantic outputs.

## QA

Operational qualification should verify deployment reproducibility, rollback correctness, compatibility preservation, and production health checks.

## Complexity / Benefit / Risk

Implementation Complexity: Medium

Expected Benefit: High

Architectural Risk: Low

## Summary

Operational deployment guidance ensures that releases, upgrades, rollbacks, and long-term maintenance preserve the Semantic Basis Extractor's architectural guarantees.

# REC-027 — Security, Integrity, and Trust Boundaries

## Problem Statement

The Semantic Basis Extractor must preserve the integrity of semantic artifacts while clearly separating trusted inputs, validated transformations, and untrusted external data. Trust boundaries should be explicit rather than implied.

## Trust Model

Authoritative execution should distinguish:

- trusted implementation components;
- trusted registry and profile artifacts;
- validated source artifacts;
- untrusted external inputs;
- experimental extensions.

Each boundary should define required validation before information crosses into authoritative processing.

## Integrity Requirements

Integrity mechanisms should protect:

- source artifacts;
- registry snapshots;
- manifests;
- completion logs;
- canonical candidate identities;
- output packages.

Content hashes should be used for verification wherever practical.

## Security Principles

Operational security should favor:

- least privilege;
- immutable released artifacts;
- authenticated registry distribution;
- explicit compatibility checks;
- fail-safe validation.

Security controls should never silently alter semantic interpretation.

## Provenance and Audit

Security-relevant events should be auditable, including:

- registry substitutions;
- failed integrity checks;
- unsupported migrations;
- replay validation failures;
- configuration overrides.

## QA

Verify hash validation, manifest integrity, trust-boundary enforcement, replay integrity, and correct handling of corrupted or partially trusted inputs.

## Complexity / Benefit / Risk

Implementation Complexity: Medium

Expected Benefit: High

Architectural Risk: Low

## Summary

Security and trust-boundary governance ensure that authoritative semantic outputs remain verifiable, reproducible, and resistant to accidental or unauthorized modification.

# REC-028 — Performance, Scalability, and Resource Management

## Problem Statement

The Semantic Basis Extractor should scale to larger semantic graphs without compromising deterministic behavior, correctness, or reproducibility. Performance optimizations must preserve the logical execution contract defined by REC-020.

## Principles

Optimization should never change:

- canonical identities;
- candidate selection;
- provenance;
- completion-log truthfulness;
- replay behavior.

Only execution cost may improve.

## Resource Management

Implementations should explicitly manage:

- memory budgets;
- CPU parallelism;
- storage of intermediate artifacts;
- cache lifetimes;
- replay caches;
- profile-dependent retention.

Engineering and QA profiles may retain more intermediate state than production profiles.

## Scalability

The architecture should support:

- parallel candidate-family execution;
- streaming artifact materialization;
- incremental loading where appropriate;
- deterministic batching;
- bounded memory growth.

Parallel execution must preserve deterministic aggregation and ordering.

## Caching

Caches should be content-addressed using immutable hashes of inputs and execution context.

Cache hits should be recorded in completion logs.

Invalid cache entries should never be reused silently.

## Performance Metrics

Recommended metrics include:

- stage execution time;
- peak memory;
- candidate throughput;
- optimization duration;
- artifact generation time;
- replay reuse rate.

Performance telemetry should remain separate from semantic outputs.

## QA

Verify that optimized and non-optimized executions produce identical semantic results and that cache reuse never changes authoritative artifacts.

## Complexity / Benefit / Risk

Implementation Complexity: Medium

Expected Benefit: High

Architectural Risk: Low-Medium

## Summary

Performance improvements should accelerate execution while preserving identical semantic behavior, deterministic outputs, and reproducibility guarantees.

# REC-029 — Testing Strategy and Regression Governance

## Problem Statement

A deterministic architecture requires equally disciplined testing. Regression governance should verify semantic correctness, deterministic behavior, compatibility, replayability, and operational contracts across every architectural recommendation.

## Testing Pyramid

Recommended layers:

- unit tests;
- contract tests;
- candidate-family fixtures;
- pipeline integration;
- replay regression;
- end-to-end qualification.

Each layer should produce machine-readable results suitable for REC-021 completion logs.

## Canonical Fixture Corpus

Maintain a versioned corpus covering:

- minimal graphs;
- representative production graphs;
- edge cases;
- historical compatibility fixtures;
- migration fixtures;
- stress cases.

Fixtures should remain immutable once published.

## Regression Categories

Verify:

- canonical identities;
- candidate inventories;
- optimizer selections;
- provenance;
- coverage metrics;
- replay equivalence;
- artifact hashes;
- completion-log truthfulness.

## Governance

Every semantic change should identify expected regression impact and required fixture updates.

Breaking semantic changes require explicit approval and migration documentation.

## QA

Continuous regression should compare outputs against authoritative baselines and classify differences as expected migration, regression, or investigation required.

## Complexity / Benefit / Risk

Implementation Complexity: Medium

Expected Benefit: Very High

Architectural Risk: Low

## Summary

Regression governance preserves long-term architectural stability, enabling confident evolution without sacrificing determinism or semantic correctness.

# REC-030 — Reference Implementation and Extensibility

## Problem Statement

The proposal defines architectural behavior rather than a single implementation. A reference implementation should demonstrate the complete execution contract while allowing alternative implementations that preserve externally observable semantics.

## Reference Implementation Goals

The reference implementation should prioritize:

- architectural clarity;
- deterministic behavior;
- readability over micro-optimization;
- complete completion-log support;
- exhaustive validation;
- reproducible replay.

## Extensibility Model

Extensions should occur through stable interfaces rather than modification of core execution stages.

Supported extension points may include:

- candidate-family providers;
- registry definitions;
- artifact materializers;
- output profiles;
- validators;
- reporting adapters.

Extensions must not bypass canonicalization, provenance, or optimizer contracts.

## Compatibility

Alternative implementations should be considered conformant when they produce equivalent semantic outputs under the same execution context.

Behavioral conformance is more important than implementation identity.

## QA

Maintain a conformance suite that verifies independent implementations against the canonical fixture corpus and replay contracts.

## Complexity / Benefit / Risk

Implementation Complexity: Medium

Expected Benefit: High

Architectural Risk: Low

## Summary

A reference implementation provides a practical realization of the architecture while encouraging compatible future implementations through stable extension contracts.

# REC-031 — Documentation Standards and Future Evolution

## Problem Statement

A long-lived architectural specification depends upon disciplined documentation. Documentation should evolve alongside the architecture while preserving historical traceability, stable terminology, and implementation-independent guidance.

## Documentation Principles

Documentation should be:

- versioned;
- append-only where appropriate;
- internally cross-referenced;
- terminology-consistent;
- implementation-neutral;
- suitable for both human readers and automated review.

## Recommended Document Structure

Core documents should distinguish:

- normative requirements;
- informative guidance;
- examples;
- rationale;
- future ideas;
- deprecated guidance.

Normative requirements should remain clearly identifiable.

## Evolution Policy

Architectural evolution should favor incremental recommendations over disruptive rewrites.

Each recommendation should record:

- motivation;
- affected contracts;
- compatibility implications;
- migration guidance;
- superseded material, if any.

## Future Directions

Future enhancements should preserve the existing execution contracts unless intentionally introducing a new architectural generation with explicit migration planning.

## QA

Documentation review should verify terminology consistency, cross-reference integrity, recommendation ordering, and synchronization with implementation and regression artifacts.

## Complexity / Benefit / Risk

Implementation Complexity: Low

Expected Benefit: High

Architectural Risk: Low

## Summary

Well-governed documentation ensures the Semantic Basis Extractor remains understandable, maintainable, and extensible throughout its lifecycle.

# REC-032 — Final Integration, Appendices, and Publication Guidance

## Problem Statement

As the proposal approaches publication, all recommendations should function as a cohesive architectural specification. Final integration should improve navigability and consistency without altering established architectural intent.

## Integration Principles

Publication should preserve:

- recommendation ordering;
- normative meaning;
- architectural traceability;
- terminology consistency;
- stable identifiers;
- historical evolution.

Editorial refinement should never introduce new architectural behavior.

## Appendices

Recommended appendices include:

- glossary;
- terminology index;
- recommendation cross-reference matrix;
- architectural decision mapping;
- schema inventory;
- canonical fixture inventory;
- revision history.

Appendices should support the core specification without becoming normative unless explicitly identified.

## Publication Checklist

Before release verify:

- cross-references resolve correctly;
- terminology is consistent;
- examples remain synchronized with normative guidance;
- checkpoint and ledger artifacts agree;
- compatibility statements are internally consistent.

## Long-Term Stewardship

Future revisions should preserve published recommendation identifiers and clearly distinguish amendments from superseded guidance.

## Complexity / Benefit / Risk

Implementation Complexity: Low

Expected Benefit: High

Architectural Risk: Low

## Summary

Final integration transforms the accumulated recommendations into a coherent, maintainable, publishable architectural specification while preserving its architectural contracts.

# REC-033 — Editorial Consistency and Publication Readiness

## Problem Statement

Before publication, the specification should undergo a comprehensive editorial review to ensure that every recommendation forms part of a single coherent architectural narrative. This review should improve clarity without changing normative architectural behavior.

## Editorial Objectives

The publication review should verify:

- consistent terminology;
- stable recommendation identifiers;
- accurate internal cross-references;
- consistent requirement language;
- uniform formatting;
- complete traceability between recommendations.

Editorial work should not introduce new architectural requirements.

## Consistency Review

The review should identify:

- duplicated guidance;
- conflicting terminology;
- obsolete references;
- missing cross-links;
- inconsistent examples;
- outdated implementation notes.

Any substantive architectural changes discovered should be deferred to future recommendations rather than incorporated silently.

## Publication Validation

Before release confirm that:

- all recommendation identifiers are unique;
- checkpoint, ledger, and commit history agree;
- appendices reference existing artifacts;
- examples remain aligned with normative guidance;
- version identifiers are synchronized.

## Maintenance Guidance

Subsequent editions should retain stable identifiers and record editorial-only revisions separately from architectural revisions.

## Complexity / Benefit / Risk

Implementation Complexity: Low

Expected Benefit: High

Architectural Risk: Very Low

## Summary

A disciplined editorial pass ensures the published specification is internally consistent, professionally presented, and faithful to the architecture established throughout the proposal.

# REC-034 — Publication Closure and Version 0.2 Release

## Problem Statement

Completion of Version 0.2 requires a clearly defined publication state so that downstream implementations, ADRs, and future revisions share a stable architectural baseline.

## Release Criteria

A Version 0.2 publication should confirm:

- all normative recommendations are complete;
- identifiers are stable;
- compatibility expectations are documented;
- supporting ledgers and checkpoints are synchronized;
- publication artifacts are reproducible.

## Closure Guidance

Following publication, architectural changes should occur through subsequent recommendations or a future major-version proposal rather than retroactive modification of Version 0.2.

Editorial corrections may be issued separately when they do not alter normative meaning.

## Recommended Publication Bundle

Include:

- the primary design proposal;
- checkpoint and design ledger;
- commit history;
- appendices and glossary;
- revision history.

## Summary

Version 0.2 establishes the initial complete architectural baseline for the Semantic Basis Extractor and provides a stable reference for future implementation and evolution.

---

# Appendix A — Glossary

**Artifact** — A persisted product of execution, including semantic outputs, manifests, logs, profiles, registries, or replay materials.

**Authoring portfolio** — The bounded, dependency-closed set of semantic claims selected for downstream editorial use.

**Candidate** — A potential semantic claim or synthesis evaluated for inclusion in the authoring portfolio.

**Candidate family** — A governed class of candidates produced according to a common deterministic generation contract.

**Canonical identity** — A stable identifier used to recognize the same semantic candidate across executions, representations, or implementations.

**Canonicalization** — The deterministic process of normalizing equivalent candidate representations into a stable form.

**Completion log** — A structured, truthful record of execution stages, outcomes, diagnostics, and relevant context.

**Configuration profile** — A named, versioned set of execution settings and feature-flag states.

**Dependency closure** — The complete set of supporting candidates or source elements required for a selected candidate to remain valid.

**Determinism** — The property that equivalent inputs and execution context produce equivalent authoritative outputs.

**Execution context** — The complete set of inputs, versions, configuration, profiles, registries, and feature flags needed to interpret or replay an execution.

**Feature flag** — A governed switch that enables, disables, or isolates behavior without silently changing authoritative semantics.

**Manifest** — A machine-readable inventory describing packaged artifacts, identities, hashes, versions, and provenance.

**Output profile** — A named materialization strategy determining which artifacts are generated or retained.

**Portfolio optimizer** — The component that selects a bounded, dependency-closed candidate set according to utility, coverage, cost, compatibility, and other governed constraints.

**Provenance** — Traceable evidence connecting a candidate or artifact to its source elements, transformations, configuration, and execution history.

**Registry** — A versioned authoritative catalog of candidate families, schemas, profiles, or other governed definitions.

**Replay** — Re-execution from preserved context with the expectation of reproducing authoritative semantic outputs.

**Semantic basis** — The selected set of semantic claims sufficient for a downstream consumer to render a useful representation under bounded constraints.

**Utility vector** — A multidimensional representation of candidate value used during portfolio evaluation.

# Appendix B — Publication and Maintenance Notes

## Normative vs. Informative Content

Recommendation requirements define the architectural contract. Executive summaries, indexes, cross-reference guides, examples, and appendices are informative unless explicitly identified as normative.

## Stable Identifiers

Published REC identifiers should remain stable. Future corrections should not silently renumber or rewrite historical recommendations.

## Editorial vs. Architectural Change

Editorial revisions may correct wording, formatting, indexes, and cross-references without changing normative meaning. New requirements, changed compatibility behavior, or altered execution semantics require a new recommendation or a future architectural version.

## Known Publication Issue

REC-004 is named in the historical index but absent from the supplied proposal and ledger. Resolution requires source recovery or an explicit future decision; it is not an editorial correction.

# Appendix C — Revision History

| Revision | Description |
|---|---|
| Commit 0035 | Completed the planned Version 0.2 recommendation sequence. |
| Commit 0036 | Recorded global editorial-consistency recommendations. |
| Commit 0037 | Added preliminary executive-summary, reading-guide, index, and glossary material. |
| Commit 0038 | Performed holistic publication edit; rebuilt front matter, complete index, cross-reference guide, glossary, maintenance notes, and documented the REC-004 gap. |


---

# EDITORIAL CERTIFICATION — PASS 4

## Sentence-Level Review

This publication pass performed a final line-edit intended to improve readability without changing architectural intent.

The review focused on:

- preserving consistent requirement language;
- reducing unnecessary repetition across publication material;
- maintaining stable recommendation identifiers;
- ensuring informative front matter remains distinct from normative recommendation text;
- preserving historical numbering and documenting unresolved source gaps rather than reconstructing them.

## Publication Assessment

The proposal is considered publication-ready as a Version 0.2 architectural specification.

Known historical issue:

- REC-004 is referenced historically but is absent from the supplied proposal source and design ledger. This publication preserves that omission explicitly.

Future improvements, if desired, should occur as Version 0.3 architectural work rather than additional editorial expansion of Version 0.2.
