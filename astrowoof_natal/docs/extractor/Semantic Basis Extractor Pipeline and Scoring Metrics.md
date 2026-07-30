# Semantic Basis Extractor Pipeline and Scoring Metrics

**Status:** Implemented v0.3 design for selecting a closed, story-complete AstroWoof natal card basis while preserving the complete unselected candidate space.

**Primary implementation:** `src/build_projected_semantic_basis.py`

**Primary output:** `<subject>.selected-authoring-packet.json`

## 1. Purpose

The Semantic Basis Extractor (SBE) converts a complete projected natal graph into a compact set of fifty evidence-grounded claims suitable for AstroWoof card authoring.

The extractor is not the projection engine and does not replace it. Projection has already occurred before this pipeline begins. The input contains canine-domain operators, modes, Doghouses, relationships, evidence references, structural scores, and voice-context materializations. SBE decides which of those semantics—and which properly supported syntheses of them—should survive into a fixed card budget.

The governing product question is:

> If a complete AstroWoof reading had to be written using only fifty claims, which dependency-closed portfolio would preserve the richest, most distinctive, coherent, useful, and entertaining account of this dog?

This is a portfolio-selection problem rather than a simple ranking problem. The fifty individually highest-scoring records may repeat one theme, omit a necessary premise, or fail to preserve the tensions that make the chart distinctive. SBE therefore scores candidates individually but selects them according to their marginal contribution to the evolving packet.

## 2. Architectural boundary

The complete workflow is:

```text
Canonical natal graph
    ↓
Semantic Projection Core
    ↓
Full projected natal graphs
    ↓
Semantic Basis Extractor
    ↓
Closed 50-claim AstroWoof authoring packet
    ↓
Constrained LLM editorial pass
    ↓
Deterministic editorial and schema validation
    ↓
Final natal.<dog>.cards.json
```

SBE owns:

- projected-graph normalization;
- whole-graph structural analysis;
- candidate generation;
- synthesis generation;
- dependency assignment;
- utility scoring;
- closed portfolio optimization;
- evidence preservation;
- authoring-packet construction;
- selection QA and audit output.

The LLM owns:

- warm, readable prose;
- genuinely differentiated voices;
- astrology-density variants;
- dog-specific humor;
- useful `dos` and `donts`;
- editorial polish that does not change selected semantics.

The final validator owns:

- schema conformance;
- locked-field integrity;
- dependency closure;
- evidence integrity;
- pronoun and grammatical-person checks;
- density and voice checks;
- placeholder detection;
- duplicate-copy detection;
- guardrail checks.

## 3. Inputs

The v0.3 implementation expects exactly four structurally equivalent projected natal graphs per subject:

- `general`;
- `handler`;
- `direct_to_dog`;
- `hybrid`.

Each graph contains projected objects and relationships. Records retain canonical source references, which allow equivalent records from different voice contexts to be joined into a single semantic identity.

Selection occurs once at the shared semantic level. The four voice materializations are preserved as evidence/context records. This prevents the handler and direct-to-dog decks from selecting different astrological information merely because their projected wording differs.

An input package may contain one subject's four files directly or one immediate
subdirectory per subject:

```text
input-package/
  bre/
    natal.bre.woof.general.json
    natal.bre.woof.d2d.json
    natal.bre.woof.handler.json
    natal.bre.woof.hybrid.json
  luna/
    natal.luna.woof.general.json
    natal.luna.woof.d2d.json
    natal.luna.woof.handler.json
    natal.luna.woof.hybrid.json
```

Subject identity, source graph identity, target ontology, canonical object
references, canonical relationship references, and context metadata are
validated before analysis. The four projected-term registries are merged
deterministically; identical definitions are deduplicated and conflicts fail
the subject run.

## 4. Normalization

### 4.1 Object identity

Projected objects are joined using their first canonical `source_refs` value. A normalized object therefore contains up to four context records associated with one canonical source object.

### 4.2 Relationship identity

Projected relationships are joined using their first canonical `source_relationship_refs` value. A normalized relationship contains the general, handler, direct-to-dog, and hybrid forms of the same preserved source relationship.

### 4.3 Context completeness

All four contexts are required. A missing, duplicated, mislabeled, or
structurally incompatible context invalidates that subject package. Complete
context coverage continues to contribute to evidence and voice-yield scoring.

### 4.4 Source immutability

The projected graphs are read-only inputs. SBE does not rewrite projected records. Exact input records are embedded in evidence blocks so selection and later prose can be audited without reconstructing graph joins.

## 5. Whole-graph analysis

Selection must not begin from an already truncated list. Before choosing candidates, SBE examines the entire projected graph and records:

- projected mode frequencies;
- projected domain frequencies;
- interaction-mode frequencies;
- object degree and hubs;
- repeated theme tags;
- repeated relationship structures;
- concentrated Doghouses;
- structural bridges;
- reinforcing and tension-heavy regions.

The analysis has two uses.

First, it supplies measurable features such as centrality, rarity, coverage, and motif participation.

Second, it provides a structural seed for the LLM’s later Character Bible or voice brief. The structural seed is not itself evidence and may not leak discarded graph facts into final card prose. It exists to help the editor understand the selected packet as a coherent dog rather than fifty disconnected entries.

## 6. Candidate contract

Every internal candidate conforms to a shared contract:

| Field | Purpose |
|---|---|
| `candidate_id` | Deterministic internal identity |
| `candidate_type` | Mandatory basis, projected object, projected relationship, or synthesized motif |
| `claim_type` | AstroWoof-facing type such as placement, angle, system interaction, or synthesized theme |
| `categories` | One or more controlled AstroWoof structural categories |
| `canonical_claim` | Deterministic semantic draft |
| `mandatory` | Whether the claim is included before optimization |
| `semantic_role` | Anchor, primitive, bridge, compressor, reinforcement, or abstraction |
| `dependencies` | Candidate IDs required for user-visible interpretive closure |
| `source_refs` | Canonical source identities |
| `evidence` | Exact projected records and/or deterministic derivation record |
| `behavioral_domains` | Canine-domain coverage |
| `tags` | Search, motif, and editorial labels |
| `score_components` | Preserved multidimensional utility vector |
| `total_score` | Configured weighted utility |
| `provenance` | Deterministic generation rule and relevant source facts |
| `rejection_reason` | Audit explanation when not selected |

The candidate contract is internal to SBE. The compiled AstroWoof packet transforms it into the target card schema.

## 7. Candidate families

### 7.1 Mandatory basis

Sixteen projected anchors are always selected:

- Sun;
- Moon;
- Mercury;
- Venus;
- Mars;
- Jupiter;
- Saturn;
- Uranus;
- Neptune;
- Pluto;
- ASC;
- DSC;
- MC;
- IC;
- North Node;
- Part of Fortune.

These claims preserve the standard natal-read basis expected by users. They consume sixteen of the fifty slots before competitive selection.

South Node and Vertex may compete when present but are not mandatory under the current profile.

### 7.2 Projected object candidates

Every projected object produces an atomic candidate. Its draft claim combines:

- the projected operator;
- the projected mode;
- the projected Doghouse or domain.

Mandatory objects are selected automatically. Other objects compete normally.

### 7.3 Projected relationship candidates

Every projected relationship produces a structural candidate. The candidate preserves:

- both endpoint objects;
- the projected relationship operator;
- the interaction mode;
- the canonical aspect;
- orb when available;
- theme tags;
- exact context records.

A relationship depends on its two endpoint object claims. This means an edge cannot become a user-visible card while one of the objects required to understand it is absent from the packet.

### 7.4 Object-mode reinforcement syntheses

When two or more projected objects use the same projected mode, SBE generates a deterministic reinforcement candidate. The synthesis states that the shared behavioral style recurs across multiple systems.

The synthesis depends on every participating object candidate.

### 7.5 Object-domain concentration syntheses

When multiple objects act within the same projected domain, SBE generates a domain-concentration candidate. This preserves the fact that several needs or operators converge in the same area of canine life.

### 7.6 Relationship-interaction syntheses

When several relationships share an interaction mode, SBE generates a whole-chart interaction candidate. To keep dependencies and prose manageable, v0.1 uses the four strongest supporting relationships.

### 7.7 Relationship-theme syntheses

Repeated relationship theme tags generate reinforcement candidates. These capture distinctive recurring motifs without requiring an LLM to invent candidate semantics.

### 7.8 Future candidate generators

The candidate contract allows later generators for:

- graph communities;
- bridge motifs;
- polarity chains;
- strongly connected tension clusters;
- configuration-like structures;
- dispositional or operator chains;
- cross-domain regulatory sequences;
- handler-actionable patterns;
- humor-bearing contrasts.

Every new generator must remain deterministic, declare dependencies, preserve provenance, and pass duplicate detection.

## 8. Semantic closure

A packet is semantically closed when every material premise needed to understand a selected derived claim is another selected user-visible claim.

Evidence alone does not satisfy this rule. Evidence proves where a claim came from, but the end user cannot follow a derivation if the premises never appear in the deck.

For example:

```text
Synthesized claim:
Movement can be part of regulation.

Required visible premises:
- Moon regulation claim
- Ascendant response claim
- Mars action claim
```

If one of those premises is not selected, the synthesis is illegal.

Relationships likewise depend on their endpoint objects. Syntheses may depend on relationships, whose endpoints create transitive dependencies. SBE computes the complete closure bundle before considering a candidate.

## 9. Budget accounting

The packet budget is fifty user-visible cards.

```text
Mandatory basis: 16
Competitive capacity: 34
Total: 50
```

A candidate does not always cost one slot. Its marginal cost is:

```text
candidate
+ every required dependency not already selected
+ transitive dependencies of those dependencies
```

This resolves the principal tension between synthesis and closure. A synthesis supported by already-selected anchors may cost one additional slot and offer excellent semantic return. A synthesis requiring four otherwise weak premises costs five slots and must provide enough portfolio value to justify the bundle.

## 10. Utility vector

SBE preserves every score component. The weighted total supports deterministic comparison, but it does not replace the explanatory vector.

All positive components are normalized to `[0, 1]`. Penalty components are also represented as `[0, 1]` and receive negative weights.

### 10.1 Core salience

Measures expected natal and product-level centrality.

Mandatory objects receive maximum core salience. Relationships receive more when both endpoints are mandatory anchors. Syntheses receive more when several load-bearing premises converge.

Core salience is not the same as structural strength. A subtle Moon claim can be core to a natal read even when no especially tight aspect supports it.

### 10.2 Structural score

Measures strength in the supplied projected graph.

For objects and relationships, v0.1 normalizes the graph’s structural-strength score against the profile’s practical maximum. For syntheses, structural score grows with the number of independent supporting candidates.

### 10.3 Projected relevance

Uses the projection engine’s relevance score. This preserves the projection profile’s judgment about how well a source structure maps into the canine target domain.

Projected relevance is one component, not the final rank. Otherwise the selector would merely reproduce source ordering and ignore story coverage, closure, and redundancy.

### 10.4 Evidence score

Combines:

- context completeness;
- exactness where available;
- number of supporting paths;
- deterministic derivation;
- provenance completeness.

This is internal confidence within the symbolic projection system, not empirical confidence about dog behavior.

### 10.5 Centrality

Measures how connected a projected object or relationship is within the graph.

V0.1 uses normalized endpoint degree. Future versions may add:

- betweenness centrality;
- PageRank;
- bridge centrality;
- community participation;
- weighted degree.

Centrality rewards load-bearing structure but must not dominate selection, because highly connected objects can otherwise consume the entire deck.

### 10.6 Coverage

Estimates how much canine semantic territory the candidate preserves. Rare modes and domains receive more credit than another repetition of an already common theme.

During optimization, a separate marginal novelty bonus rewards bundles that introduce behavioral domains not yet represented in the selected set.

### 10.7 Distinctiveness

Measures whether the candidate preserves something unusual rather than restating a frequent interaction mode. Exact relationships and rare modes receive more credit.

Distinctiveness is chart-relative. It does not claim statistical rarity across a population unless a future corpus supplies those statistics.

### 10.8 Compression

Measures how many premises a synthesis organizes into one reusable interpretive unit:

```text
(dependency count - 1) / dependency count
```

Compression does not erase dependency cost. The optimizer rewards the reusable synthesis while still charging for every premise that is not already present.

### 10.9 Narrative yield

Estimates how much coherent card writing a candidate can support. It grows with meaningful operators, theme tags, and converging evidence.

A high-yield claim can support:

- a concise canonical claim;
- multiple astrology densities;
- distinct audience voices;
- practical guidance;
- humor that remains relevant to the claim.

### 10.10 Voice yield

Measures support across the four supplied voice contexts. A candidate represented in all contexts receives the maximum v0.1 value.

Later versions may measure whether the contexts contain substantively distinct voice affordances rather than merely existing.

### 10.11 Humor affordance

Estimates the amount of specific canine imagery and semantic contrast available for humor. It is intentionally low-weighted.

This metric must never reward a generic joke over a semantically important claim. Its purpose is to break close ties in favor of claims likely to produce distinctive AstroWoof writing.

### 10.12 Redundancy penalty

Penalizes candidates drawn from heavily repeated modes or interaction patterns. Portfolio-level redundancy is also handled through marginal coverage.

Future versions should compare semantic signatures and dependency overlap directly.

### 10.13 Dependency cost

Estimates how expensive a candidate is to support. Relationship candidates are penalized when their endpoints are nonmandatory. Syntheses are penalized in proportion to dependency count.

The optimizer then applies exact bundle cost, so this metric serves as an early utility signal rather than the sole budget mechanism.

## 11. Default weights

V0.1 uses:

| Component | Weight |
|---|---:|
| Core salience | `0.14` |
| Structural | `0.12` |
| Projected relevance | `0.12` |
| Evidence | `0.09` |
| Centrality | `0.10` |
| Coverage | `0.10` |
| Distinctiveness | `0.08` |
| Compression | `0.07` |
| Narrative yield | `0.09` |
| Voice yield | `0.05` |
| Humor affordance | `0.04` |
| Redundancy penalty | `-0.08` |
| Dependency cost | `-0.07` |

These weights are configuration, not universal truth. They describe the current AstroWoof natal-card objective. Research or graph-preservation profiles would use different weights.

## 12. Portfolio optimizer

V0.1 uses deterministic greedy bundle selection.

At each decision:

1. Compute every unselected candidate’s transitive closure.
2. Remove dependencies already selected.
3. Reject bundles that exceed the remaining budget.
4. Sum the utility of every newly added candidate.
5. Divide by bundle cost.
6. Add a behavioral-domain novelty bonus.
7. Add a small preference for lower-cost bundles.
8. Choose the highest deterministic tuple.
9. Add the entire closure bundle.
10. Repeat until fifty claims are selected.

The scoring expression is:

```text
marginal bundle utility
    = mean utility of newly retained claims
    + domain novelty bonus
    + small bundle-efficiency tie breaker
```

Candidate ID provides deterministic final tie-breaking.

Future versions may use beam search or mixed-integer optimization. The candidate contract, closure rules, and audit format do not need to change when the optimizer changes.

## 13. Authoring-packet compilation

The selected portfolio is compiled into an AstroWoof-shaped JSON artifact.

The compiler fills and locks:

- schema and generator metadata;
- subject and source metadata;
- coverage and statistics;
- categories and behavioral domains;
- claim IDs and types;
- category arrays, including Big Three membership;
- semantic draft claim;
- importance, confidence, and strength;
- priority order;
- score vector;
- evidence;
- dependencies and claim relations.

The compiler creates explicit `__LLM_FILL__` placeholders for:

- no-astrology headlines and bodies;
- light-astrology headlines and bodies;
- full-astrology headlines and bodies;
- handler voice;
- direct-to-dog voice;
- hybrid voice;
- funny quotes;
- imperative quotes;
- applicable canine jokes;
- chapter-oriented `theme_group` values for selected aspects and syntheses;
- four summary cards;
- per-claim context-filter assignments;
- `dos`;
- `donts`.

This makes the LLM’s allowed work visible and makes incomplete output mechanically detectable.

Humor placeholders occur once at `card` level rather than being repeated under
every astrology-density branch. Sun and Moon use `big3_core_traits`; the
Ascendant uses both `angles` and `big3_core_traits`.

## 14. LLM editing boundary

The LLM may:

- improve `canonical_claim` wording without changing meaning;
- fill every marked prose field;
- create a Character Bible from selected claims and the structural voice seed;
- make voices genuinely distinct;
- make density levels genuinely distinct;
- write claim-specific humor;
- write practical, non-diagnostic guidance.
- assign registered navigation filters to each selected claim;
- assign flexible chapter `theme_group` labels to selected aspects and
  synthesized claims;
- author the four summary cards.

The LLM may not:

- add or remove claims;
- change claim IDs;
- alter scores or priority;
- change evidence;
- change dependencies;
- import discarded graph facts;
- turn symbolic interpretation into diagnosis;
- invent biography, breed, birth data, gender, or pronouns.

The LLM receives `unselected_claims` as locked full-chart preservation
material. Those records may not be imported into ordinary selected-card prose.
The four summary cards are the sole exception: they intentionally synthesize
the complete selected and unselected basis through the Who She Is, How She
Lives, What She Needs, and How She Grows lenses, using the subject's actual
pronouns.

Initial authoring validation permits the LLM to populate context filters,
theme groups, and summaries. Later polish validation uses the completed deck
as its baseline and locks those organizational fields unless a scoped override
was explicitly authorized.

## 15. Output artifacts

Each extraction produces:

### Whole-graph analysis

`<subject>.whole-graph-analysis.json`

Contains graph-level counts, dominant modes/domains, hubs, and the structural voice seed.

### Candidate pool

`<subject>.candidate-pool.json`

Contains every generated candidate, score vector, provenance, dependency list, and final rejection status.

### Selection audit

`<subject>.selection-audit.json`

Contains each optimizer decision, closure bundle, bundle cost, marginal utility, selected IDs, and rejection explanations.

### Selected authoring packet

`<subject>.selected-authoring-packet.json`

The single per-request dataset delivered to the LLM.

It contains the closed selected `cards`, parallel `unselected_claims`, summary
templates, context-filter vocabulary, and the complete merged
`projected_term_registry`.

### Selection QA

`<subject>.selection-qa.json`

Confirms cardinality, mandatory basis, closure, evidence, unique IDs, score ranges, and placeholder presence.

## 16. Handoff bundle

The LLM bundle separates reusable static material from per-request data:

```text
llm-handoff-bundle/
    README.md
    manifest.json
    validate_astrowoof_editorial.py
    bre/
        manifest.json
        static/
            Semantic Basis Extractor Pipeline and Scoring Metrics.md
            AstroWoof Projected Natal Card Authoring Manual.md
            LLM Card-by-Card Authoring Execution Protocol.md
            LLM Editing Permissions and QA Checklist.md
            Proposed LLM Handoff Prompt.md
        request/
            bre.selected-authoring-packet.json
            bre.selection-qa.json
```

Each immediate subject directory is a self-contained single-subject handoff.
The root README and manifest govern batch orchestration, and the root validator
is run independently for each subject. Only files under each `request/`
directory change per dog; static instructions are copied from versioned
repository sources.

The execution protocol is mandatory. It requires persistent working files,
one-complete-card-at-a-time authoring, semantic briefs, unique editorial jobs,
registry decoding, separate voice functions, claim-specific humor, repetition
checkpoints, and a whole-deck audit. This prevents structurally complete output
from satisfying the handoff through sentence-frame substitution.

## 17. QA requirements

A selected packet fails semantic QA if:

- total claims are not exactly fifty;
- mandatory claims are not exactly sixteen;
- a dependency is absent;
- a selected claim lacks evidence;
- claim IDs repeat;
- a source reference cannot be found;
- a synthesis lacks a deterministic derivation record.

A final edited packet fails editorial QA if:

- `__LLM_FILL__` remains;
- direct-to-dog copy uses third-person grammar;
- handler copy addresses the dog as `you` without an intentional quotation;
- unknown pronouns are guessed;
- density variants are identical or violate terminology rules;
- evidence or locked metadata changed;
- jokes repeat excessively;
- `dos` and `donts` contradict one another;
- unsupported certainty or diagnosis appears.

## 18. Known v0.3 limitations

The current implementation is intentionally conservative:

- synthesis templates are structural and require editorial rewriting;
- centrality uses degree rather than community-aware metrics;
- semantic redundancy uses coarse signatures and coverage rather than embeddings;
- evidence independence is approximated;
- selected relationship syntheses use up to four strongest records, while
  fuller maximal-support variants are preserved separately in
  `unselected_claims`;
- humor affordance is lexical and low-weighted;
- final editorial validation is specified but not yet a full linguistic parser;
- the deterministic validator establishes structural integrity but cannot by
  itself prove subject-specific prose, successful semantic decoding, or
  non-templated voice differentiation;
- whole-dog voice inference is deferred to the constrained LLM pass.

These limitations are visible in the artifacts and can be improved independently.

## 19. Reproducibility

Run:

```powershell
python src/build_projected_semantic_basis.py `
  --input-package "C:\path\to\projected-subject-package" `
  --output-dir semantic-basis-output `
  --bundle-dir llm-handoff-bundle
```

Use `--subject bre` to select one subject from a batch package. Each subject
receives the same independent output it would receive in a single-subject run,
and the output root receives an aggregate `run-manifest.json`.

For fixed inputs, weights, generator rules, and implementation version, candidate IDs, scores, selection decisions, and emitted artifacts are deterministic.

## 20. Governing principle

The extractor should not choose claims merely because they are individually strong, easy to explain, or funny.

It should preserve the smallest fixed portfolio that allows the downstream author to reconstruct the dog’s most complete and distinctive projected natal story—while retaining every premise needed to understand that story and every source record needed to audit it.
