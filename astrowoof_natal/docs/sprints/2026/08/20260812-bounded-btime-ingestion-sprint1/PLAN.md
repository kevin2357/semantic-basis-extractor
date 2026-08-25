# Bounded Birth-Time Natal Ingestion Sprint 1 Plan

```yaml
status: complete; 0.4.0 tagged, published, and verified
created: 2026-08-12
reconciled: 2026-08-14
owner: semantic-basis-extractor
consumers:
  - astrowoof-api
  - astrowoof-frontend
qualified_upstream_candidates:
  agf: astrology-graph-foundry 0.8.1
  spc: semantic-projection-core 0.11.0
target_input_contract: projected_bounded_semantic_graph.v1
implementation_authorized: true
```

## 1. Outcome

Add a distinct bounded birth-time Natal extraction and authoring pipeline that
consumes SPC's exact four-context bounded projection family and produces an
invariant-only, dependency-closed, exactly fifty-claim AstroWoof basis under a
separate bounded claim and final-card contract.

The pipeline must preserve the source artifact's proof scope, capabilities,
limitations, evidence closure, root-owner/evidence-family identity, projected-term
registry, and runtime provenance. It must never select a representative birth time,
manufacture an exact placement, reinterpret absence as falsity, or label SBE's
editorial utility as confidence or astrological strength.

The sprint will also factor the current exact-Natal semantic policy away from the
shared extraction mechanics. Existing exact output remains the default and must be
regression-equivalent. A separately selectable experimental exact angle-axis policy
will permit controlled deck comparison without becoming a bounded-release gate.

## 2. Product context

Bounded birth time is AstroWoof's standard support for dogs whose birth time is
unknown or approximate. A user may know the whole day, a part of the day, or a
narrow interval. AstroWoof records what is actually known rather than substituting
noon or another arbitrary instant.

AGF evaluates the admitted interval and promotes categorical facts supported across
the complete domain. SPC maps the invariant subgraph into canine semantics while
preserving uncertainty evidence and anti-inflation family identity. SBE turns that
material into a coherent stable portrait.

The reader-facing product should feel like a legitimate reading of what remains
stable, not a degraded exact reading covered in repeated warnings. Public UI design
and a possible one-time uncertainty notice remain frontend/product work.

## 3. Approved design decisions

### Separate semantic route, shared execution engine

- Bounded input has its own admission, normalization, candidate, scoring,
  selection, claim-deck, final-card, prompt, and QA policies.
- Exact and bounded routes share genuinely generic mechanics: stable identities,
  candidate-contract validation, canonicalization, dependency closure, overlap and
  conflict grouping, deterministic optimization, provenance, audits, lifecycle,
  spend control, provider execution, snapshots, events, and delivery packaging.
- The refactor must not claim to solve future Synastry or Transit policy. It should
  expose stable seams that those concrete routes may later use.

### Invariant-only authored authority

- Only rows whose projected `epistemic_basis.classification` is `invariant` may
  enter the initial bounded candidate pool.
- Conditional, variable, unavailable, inconclusive, and outside-scope material is
  preserved and classified in private disposition/provenance artifacts but cannot
  become definite card prose.
- Epistemic classification is an admission rule, not a score component.

### Exactly fifty selected claims

- A successful bounded basis contains exactly fifty invariant, dependency-closed
  claims.
- SBE never pads the deck with non-invariant, fabricated, or semantically duplicate
  claims.
- If a valid input cannot produce fifty defensible closed claims, SBE fails closed
  with a machine-readable `insufficient_invariant_basis` outcome.
- Selection records editorial tiers such as `foundational`, `primary`,
  `supporting`, and `supplemental`. Every tier remains equally invariant; tiers
  describe editorial contribution and allow a future UI to vary prominence without
  regenerating or reclassifying truth.

### Configurable foundational policy

The bounded generation profile records one exact policy:

- `strong_preference` is the default;
- `mandatory_when_available` preselects eligible invariant foundations; and
- `portfolio_neutral` supplies no special foundation preference for research.

The exact sixteen-mandatory-claim rule does not apply to bounded input.

### Derived-family policy

- Antiscia, contra-antiscia, harmonic, and other supported derived material remains
  eligible.
- Root-owner/evidence-family membership is the independence and coverage unit.
- Raw sibling count cannot multiply salience, coverage, relevance, or apparent
  support.
- Diminishing returns apply within one family; ordinary foundational and
  individualized material wins close comparisons.
- Derived material remains selectable when it adds distinct semantic territory or
  completes a useful invariant configuration.

### Bounded editorial utility

- Null object relevance and absent structural strength receive no numeric default.
- Relationship target relevance may be consumed only under SPC's declared family
  allocation policy and is never called certainty or source strength.
- SBE defines and versions a route-owned `bounded_editorial_utility` using
  defensible dimensions such as foundational salience, family-collapsed centrality,
  incremental coverage, distinctiveness, topology/configuration value, narrative
  yield, context completeness, compression, redundancy, dependency cost, and
  derived-family saturation.
- All score components, weights, policy identities, and selection decisions remain
  auditable and replayable.

### Configuration synthesis

- Deterministic syntheses may combine premises only when every material premise is
  invariant over the same validated source artifact and proof domain.
- Syntheses retain visible semantic dependencies, source/evidence-family lineage,
  and deterministic derivation records.
- No synthesis may reconstruct missing exact geometry or import variable evidence.

### Separate bounded artifacts

- Bounded claim decks and final cards use separate schemas and contract versions.
- A private `<subject>.bounded-disposition-report.json` records admitted, selected,
  represented, redundant, displaced, variable, unavailable, inconclusive,
  unsupported, and outside-scope material.
- Compact disposition statistics may be embedded in the bounded packet and
  delivery provenance; the complete report is not provider input.
- The provider-visible bounded view is allow-listed and minimized. It excludes raw
  birth facts, interval endpoints, coordinates, location evidence, complete graphs,
  and full uncertainty registries.

### Upstream validation

- Pin the latest qualified released SPC boundary, initially SPC 0.11.0, and use its
  public bounded schema and `validate_parallel_bounded_contexts()` interface.
- Qualify the exact AGF 0.8.1 to SPC 0.11.0 to SBE chain represented by the supplied
  four-context archive.
- Preserve external wheel hashes/runtime receipts because projected JSON alone does
  not prove the originating AGF wheel.

### Experimental exact angle policy

- Current exact behavior remains `legacy_atomic.v1` and the default.
- Add an optional `axis_aware.v1` exact-Natal angle-selection strategy.
- Axis-aware mode retains component edges as evidence, suppresses or groups
  structurally inevitable angle-frame edges, and generates deterministic
  planet/point-to-axis candidates where supported.
- Policy identity enters the generation profile, run identity, audit, candidate
  identity rules, and artifact digest.
- Axis-aware output is experimental and does not gate bounded release acceptance.

## 4. Included scope

- common extraction-engine seams and an explicit exact-Natal policy preserving
  legacy behavior;
- optional exact `axis_aware.v1` selection policy and comparative evidence;
- exact SPC bounded input dependency and installed resource validation;
- strict four-context bounded packet admission;
- bounded normalization using correspondence, source, evidence, and family
  identities;
- invariant-only candidate construction;
- family-aware object, relationship, and deterministic configuration candidates;
- bounded editorial utility and deterministic exactly-fifty optimization;
- bounded claim-deck, disposition-report, authoring-packet, and final-card schemas;
- minimized provider-visible bounded authoring resources;
- bounded-specific semantic and editorial validation;
- reuse of SBE 0.3.0 lifecycle, spend, event, checkpoint, retry, polish, critic,
  and delivery contracts;
- bounded structured-event catalog additions;
- privacy, determinism, scale, negative, restore, and installed-runtime tests; and
- consumer handoff, compatibility, release recommendation, and compact evidence.

## 5. Excluded and deferred scope

- authored conditional, variable, alternative, probabilistic, frequency-weighted,
  rectified, midpoint, or most-likely interpretations;
- bounded Synastry, Transit, returns, or temporal combinations;
- broad exact-Natal scoring redesign beyond the isolated angle strategy;
- Quick/Complete product redesign;
- arbitrary variable-size bounded decks in the initial contract;
- frontend page implementation or public UI copy;
- API queues, leases, database persistence, R2 custody, cleanup authority,
  publication authority, quotas, billing reconciliation, or product entitlements;
- OpenAI live spending unless separately approved for a later qualification gate;
  and
- release tagging or publication without a distinct approval boundary.

## 6. Architectural target

The intended logical boundary is:

```text
exact projected packet -> ExactNatalPolicy ---------+
                                                    |
bounded projected packet -> BoundedNatalPolicy -----+-> shared basis engine
                                                    |       |
future concrete routes -----------------------------+       +-> route compiler/QA
                                                            +-> shared lifecycle
```

Policy-owned hooks should include:

- source admission and normalized graph construction;
- candidate-family resolution and generation;
- foundational policy and family-independence semantics;
- utility components and portfolio constraints;
- claim-deck/materialization contract; and
- route-specific semantic QA and authoring resources.

The shared engine remains policy-agnostic wherever evidence from both exact and
bounded routes proves that behavior is genuinely common. No speculative abstraction
is required solely for hypothetical future routes.

## 7. Slice sequence

### Slice 0: Baseline, contract freeze, and fixture strategy

#### Outcome

Freeze the current exact behavior and bounded upstream boundary before refactoring.

#### Work

- Record current source/release/worktree state and preserve the previously accepted
  unreleased `py.typed` packaging follow-up.
- Freeze representative exact candidate, selection, packet, and installed smoke
  identities under `legacy_atomic.v1`.
- Retain hashes and compact metrics for the supplied large bounded archive without
  checking its expanded 27 MB contents into Git.
- Create or adopt a sanitized small four-context bounded fixture suitable for
  repository tests, plus a controlled full-scale qualification procedure.
- Define versioned names for bounded input admission, candidate policy,
  editorial-utility profile, claim deck, disposition report, authoring packet, and
  final cards.
- Confirm the exact AGF 0.8.1/SPC 0.11.0 compatibility statement or record the
  remaining documentation qualification.

#### Tests

- Current full suite and `git diff --check`.
- Existing exact extraction replay and release smoke.
- Official SPC validation and parallel-context validation over both sanitized and
  supplied full-scale fixtures.
- Hash, schema, registry, and context inventory checks.

#### Gate 0

Inputs, identities, fixture custody, expected exact output, and new contract names
are frozen. No production refactor begins until review approves this boundary.

### Slice 1: Shared engine seam and exact legacy policy

#### Outcome

Move exact-Natal-specific behavior behind an explicit policy while preserving the
default exact pipeline's semantic output.

#### Work

- Separate generic candidate, dependency, optimization, provenance, and audit
  mechanics from exact-Natal admission, mandatory basis, scoring, and compilation.
- Introduce an explicit `ExactNatalPolicy` using `legacy_atomic.v1` angle behavior.
- Preserve existing CLI/API defaults and artifact paths.
- Add policy/profile identity without destabilizing candidate IDs whose semantics
  are unchanged.

#### Tests

- Golden exact candidate inventory, selected IDs/order, dependencies, packet, and
  QA equivalence.
- Exact batch, installed smoke, lifecycle, delivery, and provenance regressions.
- Policy-resolution rejection for unknown names/versions.
- Full suite, focused static analysis, diff review, and `git diff --check`.

#### Gate 1

Legacy exact output and public behavior remain regression-equivalent; shared seams
are narrow, documented, and independently testable.

### Slice 2: Experimental exact axis-aware policy

#### Outcome

Provide a selectable exact-Natal angle strategy without changing the default.

#### Work

- Add `axis_aware.v1` angle-frame classification and axis candidate generation.
- Preserve all component edges as evidence.
- Mark structural angle-frame exclusions with closed reasons such as
  `structurally_inevitable` and `represented_by_axis_configuration`.
- Produce deterministic baseline-versus-axis comparison reports covering displaced
  claims, topology, coverage, closure cost, and portfolio drift.
- Expose a named CLI/generation-profile option suitable for later API configuration.

#### Tests

- ASC/DSC and MC/IC structural-frame fixtures.
- Planet/point-to-axis synthesis and incomplete-axis negative cases.
- Stable IDs, dependency closure, evidence preservation, and deterministic replay.
- Proof that omitted policy option remains byte/semantic equivalent to legacy mode.

#### Gate 2

The experimental policy is inspectable and reversible, the legacy default is
unchanged, and axis-aware quality can be evaluated without enabling it in the API.
This gate may succeed experimentally without becoming a bounded-release dependency.

### Slice 3: Strict bounded packet admission

#### Outcome

Admit only one complete, compatible, certainty-invariant bounded four-context
family through SPC's supported public contract.

#### Work

- Pin and package/declare the SPC 0.11.0 consumer boundary.
- Validate each official bounded schema and the exact context set.
- Invoke specialized parallel-context validation.
- Require common source artifact, opaque source identity, capabilities,
  dispositions, limitations, evidence identity, profile, ontology, registry,
  runtime, and correspondence structure.
- Reject mixed exact/bounded, source, interval, context, profile, contract,
  registry, or resource identities.
- Emit a compact safe admission summary and bounded input events.

#### Tests

- Official positive fixtures and the supplied full-scale archive.
- Schema mutations and every identity/context mismatch class.
- Missing/conflicting terms, references, correspondence IDs, capabilities, proof
  identities, and runtime resources.
- Source-order independence and exact-route nonacceptance of bounded input.
- Protected-field event/redaction tests.

#### Gate 3

SBE can distinguish valid, invalid, unsupported, and mixed bounded packets without
guessing, rewriting upstream artifacts, or invoking a provider.

### Slice 4: Bounded normalization, candidates, and family topology

#### Outcome

Construct a deterministic invariant-only bounded candidate pool with correct
independence, evidence, and topology.

#### Work

- Normalize rows by `correspondence_id` and preserve all four context records.
- Admit invariant material only.
- Model root-owner, evidence-family, record-independence, source refs, proof scope,
  prerequisites, and projected terms explicitly.
- Generate foundational object, individualized relationship, derived-family, and
  initial configuration candidates.
- Apply the configured foundational policy.
- Produce the complete bounded disposition report, including non-admitted and
  policy-excluded source material.

#### Tests

- Every supported bounded object/relationship family and outside-scope behavior.
- Conditional/variable/unavailable/inconclusive rejection from the candidate pool.
- Opaque prerequisite preservation and direct evidence closure.
- Family duplication/adversarial multiplicity and stable reorder tests.
- No exact scalar, structural score, confidence, or representative state in any
  candidate.

#### Gate 4

Every candidate is invariant, traceable, family-accounted, deterministic, and
classified; raw multiplicity cannot create false independent support.

### Slice 5: Bounded editorial utility and exactly-fifty portfolio

#### Outcome

Select an invariant, dependency-closed, family-aware portfolio of exactly fifty
claims using an explicitly editorial objective.

#### Work

- Implement and version `bounded_editorial_utility` components and weights.
- Use family-collapsed centrality/coverage and diminishing returns.
- Preserve SPC relationship relevance only as declared target relevance.
- Implement invariant configuration completion and dependency closure.
- Assign editorial tiers without implying epistemic differences.
- Fail closed with `insufficient_invariant_basis` rather than pad.
- Emit complete selection audit, rejection reasons, and disposition updates.

#### Tests

- Exactly fifty, unique IDs, dependency closure, evidence, and invariant authority.
- Foundational-policy comparison for all three modes.
- Derived-family saturation and relevance-conservation adversarial cases.
- Configuration completion, overlap, redundancy, and capacity displacement.
- Insufficient-basis negative fixture.
- Deterministic replay, source-order independence, score bounds, and audit truth.
- Full-scale performance/memory measurements using the supplied archive.

#### Gate 5

The selected basis contains fifty defensible invariant claims, preserves meaningful
family/topology breadth, exposes supplemental material honestly, and never invents
upstream strength or certainty.

### Slice 6: Bounded claim deck, authoring, and final-card contracts

#### Outcome

Compile the selected basis into separate bounded schemas and provider-minimized
authoring resources capable of producing a stable portrait.

#### Work

- Define/package bounded claim-deck, authoring-packet, disposition-report, and
  final-card schemas.
- Lock invariant authority, source-artifact identity, proof/evidence/family lineage,
  dependencies, editorial tiers, registry terms, and policy identities.
- Create bounded-specific authoring instructions and workspace representation.
- Keep all ordinary prose invariant-only and prevent unselected uncertainty from
  leaking into summaries.
- Build a field-level provider-disclosure inventory for bounded prompts, retries,
  polish, and critic.
- Reuse common final-card assembly/validation only where the separate schema proves
  compatibility.

#### Tests

- Schema and locked-field mutation tests.
- Provider-visible disclosure allow-list and seeded protected-value absence.
- No variable/unavailable evidence or full registry in authoring bundles.
- Summary and whole-dog evidence remain separately identified.
- Registry merge/closure and selected/unselected provenance remain complete.
- Deterministic fake-provider bounded deck through final validation.

#### Gate 6

A provider can author the bounded stable portrait without seeing protected source
facts or receiving authority to change epistemic meaning, selection, or evidence.

### Slice 7: Shared lifecycle, events, snapshots, and failure recovery

#### Outcome

Run bounded authoring through SBE 0.3.0's released operational contracts without a
second lifecycle implementation.

#### Work

- Wire bounded runs into common prepare/authorize/execute, spend, detach/resume,
  retry, polish, critic, closeout, and delivery paths.
- Add bounded admission, family, selection, disposition, and artifact event payloads
  to the existing catalog.
- Include every new authoritative bounded artifact in snapshot and restore rules.
- Preserve distinct bounded terminal reasons and contract identities in common
  lifecycle inspection/closeout output.

#### Tests

- Provider-free bounded denial, closeout, replay, and restored terminal checkpoint.
- Provider identity and ambiguous-submission fail-closed cases.
- Failure injection across every new snapshot/state-persistence boundary.
- No duplicate provider action, no lost accepted evidence, and monotonic spend/run
  state.
- Event loss/duplication/sink failure does not affect execution.
- Complete workspace relocation/restore under the supported path contract.

#### Gate 7

Bounded input kind does not weaken spend authority, idempotency, quiescence,
snapshot integrity, or API-consumable lifecycle truth.

### Slice 8: Deterministic, scale, privacy, and product QA

#### Outcome

Qualify the bounded semantic product across representative intervals, topology,
capability reductions, and adversarial inputs.

#### Work

- Exercise narrow, four-hour, whole-day, and maximum supported intervals where
  upstream fixtures are available.
- Compare invariant retention, family collapse, editorial tiers, and selected
  topology without treating counts as quality or confidence.
- Exercise terrestrial-frame unavailable/inconclusive cases and large derived
  families.
- Capture compact machine-readable results and remove expanded temporary artifacts.

#### Tests

- Positive exact-fifty invariant decks across the interval matrix.
- Mixed subject/source/interval/context/contract rejection.
- Missing terms/evidence, unknown families, corrupted hashes, and unsupported
  versions.
- Repeat and serialization-order determinism.
- Full privacy/redaction corpus across events and every provider-visible stage.
- Full exact-route regression suite and both angle policy modes.
- Performance and memory guardrails based on observed evidence, not unsupported SLA
  claims.

#### Gate 8

Representative real and adversarial cases pass with truthful compact evidence; any
input that cannot support fifty invariant claims fails explicitly rather than
degrading semantic authority.

### Slice 9: Installed cross-repository acceptance and handoff

#### Outcome

Prove the exact installed AGF 0.8.1 to SPC 0.11.0 to SBE candidate chain and prepare
the next pinnable SBE artifact without publishing it.

#### Work

- Build reproducible SBE candidate wheels and install outside all source trees.
- Verify `py.typed` packaging as the already accepted post-0.3.0 follow-up.
- Install exact qualified AGF/SPC artifacts and verify versions, hashes, runtime
  manifests, schemas, profiles, contexts, and resource fingerprints.
- Run bounded admission, extraction, fake authoring, lifecycle, snapshot/restore,
  validation, and delivery smoke using installed interfaces only.
- Produce API/frontend consumer handoff, schema inventory, sample sanitized
  artifacts, release notes, compatibility matrix, known limitations, and exact
  pin/hash instructions.
- Reconcile API-request status and obtain API-agent review before release
  recommendation.

#### Tests

- Clean Windows and Linux installed-runtime smoke where supported by the release
  process.
- `pip check`, resource discovery, public Python/CLI boundary, and wheel-content
  inspection.
- Full installed test suite and cross-repository fixture replay.
- Two controlled reproducible builds and artifact hash comparison.
- No network or paid provider call required for the acceptance gate.

#### Gate 9

A downstream worker can pin exact artifacts, validate and author a bounded reading,
persist native lifecycle state, restore safely, and consume bounded delivery without
source-checkout imports or undocumented SBE internals. Tagging and publication
remain separately authorized.

## 8. Sprint-wide testing strategy

### Contract and semantic tests

- Official SPC schema plus specialized parallel-context validation.
- SBE bounded schemas with positive and mutation fixtures.
- Every selected claim is invariant and traceable to complete direct evidence.
- Every synthesis has same-domain invariant premises and visible dependency closure.
- No exact-only or prohibited numeric fields enter bounded artifacts.

### Regression tests

- Legacy exact default candidate inventory and selection remain stable through the
  refactor.
- Existing exact authoring, lifecycle, spend, snapshot, critic, polish, delivery,
  release smoke, and public interfaces remain passing.
- Axis-aware exact behavior is opt-in and independently replayable.

### Determinism and property tests

- Input row, evidence-registry, and context-file ordering cannot change semantic
  output.
- Family duplication cannot increase independent coverage or total family
  relevance.
- Candidate, claim, correspondence, dependency, and artifact identities remain
  deterministic.
- Exactly-fifty and invariant-only properties hold for every successful fixture.

### Negative and failure-injection tests

- Contract/version/profile/context/source/proof/resource mismatch.
- Missing/conflicting registry, evidence, endpoint, or correspondence references.
- Non-invariant candidate contamination.
- Insufficient invariant basis.
- Interrupted state persistence, snapshot publication, provider identity recording,
  authorization, closeout, and restore.
- Unknown policy names and unsupported combinations fail before execution.

### Privacy tests

- Seed dog/handler names, dates, local/UTC datetimes, timezone, coordinates,
  locations, evidence excerpts, prompts, responses, keys, headers, and filesystem
  paths.
- Prove none enter events or provider-visible bounded authoring, retry, polish, or
  critic requests unless explicitly allow-listed by the disclosure inventory.
- Private provenance and disposition retention remains complete.

### Installed and cross-platform tests

- Exact wheels installed non-editably outside source trees.
- Windows and Linux qualification with exact release dependencies.
- Runtime/resource/schema/profile/context identity checks.
- Hash-locked offline worker-image compatibility where the API harness supports it.

### Gate discipline

At every slice gate:

1. inspect worktree and preserve unrelated user changes;
2. run focused tests and proportionate full regression tests;
3. validate changed JSON/Markdown and relative links;
4. run focused static checks and `git diff --check`;
5. review the actual diff and compact result artifacts;
6. update append-only `LOG.md` and add a durable slice result under `results/`;
7. link the current plan, log, and evidence/result documents in the handoff; and
8. pause for product-owner approval before committing.

## 9. Exit criteria

The sprint is complete only when:

1. exact legacy behavior remains the default and passes regression equivalence;
2. the experimental exact axis policy is selectable, versioned, deterministic,
   auditable, and not enabled implicitly;
3. one exact four-context bounded packet is validated through SPC's official public
   interfaces and every mixed/incompatible variant fails closed;
4. only invariant bounded material can enter authored candidates;
5. root-owner/evidence-family identity prevents multiplicity inflation;
6. successful bounded decks contain exactly fifty dependency-closed invariant
   claims, while scarcity fails explicitly;
7. bounded editorial utility is versioned and never presented as confidence,
   probability, or structural strength;
8. bounded claim, disposition, authoring, and final-card schemas are distinct and
   fully validated;
9. provider-visible bounded input is minimized and passes protected-field tests;
10. common spend/lifecycle/event/snapshot contracts operate unchanged for bounded
    runs and survive interruption/replay;
11. narrow, broad, unavailable/inconclusive, family-rich, malformed, and
    insufficient fixtures have durable QA outcomes;
12. exact AGF 0.8.1, SPC 0.11.0, and candidate SBE wheels pass installed
    cross-repository acceptance outside source checkouts;
13. API/frontend handoff documents identities, schemas, pins, outputs, limitations,
    and ownership boundaries; and
14. no release is tagged or published without separate explicit approval.

## 10. Evidence and artifact policy

- `LOG.md` is append-only once implementation begins.
- Each slice receives a durable result document under `results/`.
- Compact JSON summaries record hashes, counts, classifications, test results, and
  installed identities.
- Large projected graphs, expanded decks, wheels, environments, caches, and
  provider artifacts stay outside Git. Retain their hashes and reproduction basis.
- Sanitized minimal fixtures may be packaged when required for installed contract
  smoke.
- The supplied full-scale archive remains external test evidence unless a later
  gate approves a minimized repository fixture derived without protected data.

## 11. Review boundary

This plan is proposed for product-owner review. No implementation slice has begun.
Approval authorizes Slice 0 only; every later slice retains its own review and
commit gate.
