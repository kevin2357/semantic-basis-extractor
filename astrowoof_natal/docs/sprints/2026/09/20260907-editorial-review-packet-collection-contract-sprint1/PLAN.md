# Plan — editorial-review packet collection contract

Status: Kevin, API, and SBE jointly adopted the textual contracts in API Sprint
87: [Slice 1α shapes](<C:/dev/github/astrowoof-api/docs/sprints/2026/09/20260907-editorial-review-evidence-retention-companion-sprint87/SBE Agent Slice 1α Contract Proposals.md>), [Slice 1β relationships](<C:/dev/github/astrowoof-api/docs/sprints/2026/09/20260907-editorial-review-evidence-retention-companion-sprint87/SBE Agent Slice 1β Semantic Relationship Contract Proposal.md>), and [Slice 1γ fixtures](<C:/dev/github/astrowoof-api/docs/sprints/2026/09/20260907-editorial-review-evidence-retention-companion-sprint87/SBE Agent Slice 1γ Provider-Free Contract Fixture Proposal.md>). Slices 1δ.0–1δ.1, 1ε.0–1ε.2, and 2–3 are complete and jointly approved. Slice 3 now covers honest initial-pass/creative-retry materialization, immutable pre-optional deck retention, polish/critic/candidate semantics, exact native joins, deterministic construction, and typed no-packet outcomes. Slice 4 is in release qualification under frozen candidate version `0.4.54`; its focused and final broad source gates are green. Better Stack transport, provider work, retained-run access, API intake, deployment, tag creation, and publication remain outside the completed gate.

## Goal

Publish a narrow SBE-owned, closed, deterministic editorial-review evidence
packet for eligible ordinary live-exact terminal outcomes. Give API canonical
opaque bytes it can observe best-effort after authoritative settlement without
letting observation become lifecycle, cleanup, retry, recovery, or editorial
decision authority.

## Contract principles

- Status names never grant eligibility.
- Eligibility is reader-bound to exact result, receipt, checkpoint/snapshot,
  custody, action/binding/Response, release, compatibility, and evidence facts.
- The invocation-returned result wins; latest-result discovery is excluded.
- Decision order is preserved. Candidate adoption, whole-deck acceptance,
  structural validation, and terminal disposition remain distinct.
- Absence, empty evidence, non-materialization, exclusion, inconsistency,
  unknown version, and oversize are distinguishable typed outcomes.
- Canonical bytes are atomic. Query projections are rebuildable,
  non-authoritative indexes bound to packet ID/digest.
- Complete decks and provider responses live in separate self-describing
  artifact records; their absence never makes editorial evidence ambiguous.
- Native correlations are digest-owned by SBE; API observation correlations are
  added separately and never alter native packet/object identity.
- Construction and reading perform no provider, network, or storage work.
- Observation failure cannot affect the completed run.

## Slice 0 — Native eligibility and evidence inventory

**Maps to API Plan Slice 0 — Joint contract and boundary inventory.**

Inventory released native surfaces for ordinary exact `delivery_complete` and
normal editorial terminal closeout with final custody. Trace exact result and
canonical receipt compatibility plus selected deck, six pass decisions,
creative retries, optional stages, validation/lint/acceptance reports,
action/binding/Response joins, snapshot/checkpoint, runtime release,
profile/resources, builder/prompt identity, and native timestamps.

Enumerate every near-neighbor route that must be excluded. Prove which complete
facts can be built from an already restored terminal workspace with zero I/O.
Do not infer unavailable facts from filenames, terminal status, result-index
order, or API state.

Deliver:

- `NATIVE ELIGIBILITY AND EVIDENCE INVENTORY.md`;
- a closed eligibility/exclusion matrix; and
- a proposed typed construction-outcome vocabulary.

## Slice 1 — Candidate packet and projection contract

**Maps to API Plan Slice 0 and Slice 0-alpha.**

Using the approved post-0-alpha split, draft:

- canonical packet schema and packet-ID/digest derivation;
- ordered decisions, findings, field context, selected deck, result/receipt,
  and provenance;
- minimal promoted query projections if hybrid is chosen;
- exact inclusion/exclusion predicates;
- canonical byte ceiling and all-or-none accounting;
- typed capture status for ineligible/incomplete/oversize outcomes; and
- separate artifact-envelope schema for digest-identified initial,
  materialized-candidate, and terminal-selected deck roles plus exact joined
  provider responses;
- privacy/content treatment for artifacts, prompts, and protected evidence;
- one-request record/byte ceilings for the atomic editorial set; and
- bounded deterministic artifact batching whose partial absence is explicitly
  permitted.

The editorial packet retains deck/response identities, digests,
materialization/selection relationships, and relevant finding-local context—not
the complete artifact payloads. Use real accepted/rejected examples for
deterministic size checks while keeping private authored bytes outside Git.

### Joint paws point 1 — API Slice 0 contract freeze

Pause for Kevin/API review of shape, content, eligibility, projections, ceiling,
and status semantics. No public schema or production implementation begins
before approval.

## Slice 1δ.0 — Alloy tooling, scope, and translation feasibility

**Maps to API Plan Slice 1δ — Bounded Alloy relational-model spike.**

- Inventory supported local Java/Alloy command-line execution without adding a
  production or package dependency.
- Freeze a minimal content-free vocabulary covering two packets, multiple
  post-initial decisions, terminal-owned validation, repeated deck-payload
  equality, and absent artifact evidence.
- Map approved 1β rule IDs one-to-one to candidate Alloy facts/assertions and
  future validator/mutation targets.
- Establish satisfiable accepted and editorial-closeout worlds before treating
  any assertion result as meaningful.
- Record exact tool/version, finite scopes, model digest, commands, and any
  environment limitation.

### Voof-paws 1δ-A — feasibility review

Pause for Kevin/API review of tooling viability and faithful translation. If
Alloy is unavailable or becomes a second hidden specification, record that
bounded result and proceed to required Slice 1ε without delaying it.

## Slice 1δ.1 — Alloy counterexample campaign and adoption decision

**Maps to API Plan Slice 1δ — Bounded Alloy relational-model spike.**

- Encode chronology, deck-transition, selection, Response, ownership,
  projection, artifact-scope, and observation-non-authority rules.
- Run bounded satisfiability checks first, then deliberately weaken rules and
  record the smallest counterexamples.
- State every finite scope in a text/JSON receipt; bounded exhaustiveness is not
  described as universal proof.
- Reflect any discovered contract gap in prose before later manifest/validator/
  test changes.
- Recommend `adopt`, `retain as optional`, or `do not adopt`. Alloy may not
  become a production dependency or required release gate here.

### Voof-paws 1δ — formal-model decision

Pause for Kevin/API review of model, counterexamples, scope limits, and adoption
recommendation before Slice 1ε implementation.

## Slice 1ε.0 — Closed schemas, semantic manifest, and validator skeleton

**Maps to API Plan Slice 1ε — Executable semantic-validator stack.**

- Package the approved closed 1α schemas, typed validation-result schema, and a
  bounded semantic manifest carrying stable rule IDs/owners, digest domains, ID
  tuples, enums, cardinalities, ordering, gzip parameters, and API transport
  preflight ownership.
- Implement strict parsing and staged validation for SBE-owned native packet,
  projection, artifact, and deterministic native event-set content.
- Exclude live API correlations/timestamps/final request bytes from SBE
  validation; fixed synthetic envelopes are fixture evidence only.
- Add bidirectional rule-registry coverage: every native manifest rule has a
  validator/test target and no native validator rule is undocumented.

## Slice 1ε.1 — Positive fixtures and deterministic qualification

**Maps to API Plan Slice 1ε and the approved API Plan Slice 1γ contract.**

- Build separate privacy-safe production-shaped accepted-delivery and ordinary
  editorial-closeout bundles through the public source contract surface.
- Cover initial-wave ordering, faithfully supported retry/optional-stage deck
  transitions, terminal-owned validation, claim-less context, action/binding/
  Response joins, projections, and packet-scoped artifacts.
- Qualify deterministic native bytes and fixed synthetic-envelope JSON/gzip in
  fresh temporary workspaces without claiming live API envelope byte identity.
- Add capture-status fixtures proving absence of packet and projection native
  bytes, IDs, and digests.

## Slice 1ε.2 — Rehashed mutations and no-side-effect campaign

**Maps to API Plan Slice 1ε and the approved API Plan Slice 1γ contract.**

- Implement the full approved rehashed mutation matrix across provenance,
  chronology, decks, actions/Responses, ownership, projections, artifacts,
  summaries, source/event combinations, record count, and compressed size.
- Require exact typed classification, rule ID, and safe detail code.
- Fence provider/network/R2/API/database/subprocess access, observable secret
  environment reads, workspace mutation, and payload leakage into receipts,
  diagnostics, stdout, or public handoffs.
- Produce a compact qualification receipt and API consumer handoff.

### Voof-paws 1ε — executable contract review

Pause for Kevin/API review of schemas, manifest, validator, rule coverage,
fixtures, and mutations before the existing Slice 2 runtime builder. Passing
source fixtures does not authorize installed-wheel work, runtime integration,
or release.

Explicitly revisit the manifest's proposed 9 MiB safe compressed threshold at
this paws point. It is intentionally below Better Stack's verified 10 MiB
ceiling, but remains a joint API-transport parameter rather than native truth.

## Slice 2 — Closed schemas, readers, and provider-free fixtures

**Maps to API Plan Slice 1 — Provider-free contract fixtures.**

**Status: complete and approved via Slices 1ε.0–1ε.2.** The expanded
executable-contract work supersedes this older, less detailed statement without
weakening any requirement below.

Implement packaged schemas and strict readers for the canonical editorial
packet, capture status, projections, and artifact envelope. Build one accepted
and one editorial-rejection fixture through production native readers/building
primitives. Prove canonical bytes, stable IDs/digests, complete decision order,
selected-deck binding, exact result/receipt/checkpoint and
action/binding/Response joins, deck-role consistency, and release identity.

Add rehashed mutation coverage for reordered/omitted/duplicated decisions;
wrong selected deck/candidate; stale or mismatched identities; projection
disagreement; malformed/non-materialized ambiguity; unknown versions; incomplete
or oversize evidence; and excluded routes masquerading as ordinary eligibility.
Ineligible construction returns typed status only—never partial packet bytes/ID.

### SBE review point 2

Pause for API consumer review of packaged fixtures before runtime integration.

**Decision: approved.** API's Slice 1ε review accepts the schemas, readers,
positive fixtures, 24 rehashed mutations, no-side-effect boundary, 99-event
maximum, and 9 MiB compressed safe threshold. Runtime construction remains a
separate Slice 3 boundary.

## Slice 3 — Narrow native packet builder

**Maps to API Plan Slice 2 — Narrow runtime implementation.**

Integrate one read-only builder at the approved ordinary terminal publication
boundary. It consumes the exact invocation/result identity and durable workspace
evidence; it cannot discover latest results, mutate the workspace, access
providers/storage/network, or participate in terminalization.

Return one complete canonical editorial packet plus approved projections (or one
typed status with no partial editorial set), and an independently complete set
of artifact records eligible for bounded best-effort batching. Prove
deterministic, idempotent, privacy-bounded behavior and unchanged
lifecycle/custody if either construction path fails.

**Current gate:** Slices 3C–3F are incorporated and approved. Coordinated v5
resources now use only durable native checkpoint-basis, snapshot, state,
runtime, profile, resource-set, action, binding, and request facts. Optional
action-level prompt provenance is all-or-none and absent from historical
evidence. The exact-reader collector recomputes and cross-joins these facts, and
the focused contract/runtime suite passes.

Complete translation of the collected native evidence into one canonical
packet/projection set plus independently complete artifact records, or one
typed capture status with no partial output.

The first runtime-construction increment now proves the simplest complete
branch: six accepted initial passes, an assembly-owned terminal deck, no
optional-stage history, and an eligible terminal publication. It emits one
schema-valid packet, six decision projections, the deck artifact, and six exact
provider-response artifacts without changing the workspace. Rejected initial
attempts, accepted creative retries, exact polish input/candidate/output
transitions, read-only critic findings, and explicitly non-adopting qualitative
candidates are translated as well. Unsupported or incomplete histories fail
closed with one typed no-packet status rather than a partial lineage.

**Approved Slice 3G correction:** an adopted optional-stage candidate can
overwrite the ordinary subject deck path, while the assembly report does not
bind those displaced bytes. SBE now preserves a separate immutable initial
assembled deck and canonical digest before any optional stage. Historical
workspaces without it remain typed no-packet cases; unmodeled reconstruction
stays excluded.

**Current gate:** Slice 3 runtime construction is approved. Slice 4 source,
reproducible-wheel, and installed-package qualification is complete for the
approved ordinary-live-exact surface; the exact candidate now awaits the joint
installed-consumer handoff before any immutable tag or publication.

## Slice 4 — Package and installed-wheel qualification

**Maps to API Plan Slices 2–3.**

From a clean wheel, exercise accepted, editorial-rejection, incomplete,
oversize/over-count editorial sets, artifact partial availability, excluded, and
unknown-version cases. Verify packaged resources and entry point,
source/installed byte equality, exact release/resource bindings, zero
provider/R2/Better Stack/API/network operations, zero workspace mutation, and no
private authored bytes in public handoffs.

Produce a bounded API consumer handoff with exact wheel and fixture digests.

### Joint paws point 3 — installed consumer handoff

Pause for API confirmation that its post-commit hook consumes the installed SBE
artifact without inference or lifecycle coupling.

**Current gate:** paused here with candidate `0.4.54`, wheel SHA-256
`6ade10180b56913fc1a90d88b76f2cd7b84685c026b8acee99a3300d920f9723`,
and deterministic installed qualification receipt SHA-256
`3c0d46fac5a13ddc5b4ea51722ac1626a83c9f0b5898f38a93cc5e9564dec50a`.

**Completed:** API technical approval and explicit owner authorization were
received. Immutable tag `astrowoof-natal-authoring-v0.4.54` was created at
exact commit `c5af5c34b1afdf2c6a7e828e0f424fbec44fd3d6`; the GitHub release and
verified wheel are published.

## Slice 5 — Joint provider-free end-to-end qualification

**Post-release API Slice 2A finding:** API confirmed that fresh ordinary
delivery lacks the exact sealed result identity in its structured cycle handoff.
SBE has implemented a narrow closed delivery-success command result carrying
the already-sealed exact result/receipt identity, without latest-result
discovery or lifecycle change. Source qualification is in progress; a fresh
release and installed consumer review remain gated.

**Maps to API Plan Slice 3 — Joint provider-free end-to-end qualification.**

Support API's fake-receiver campaign for accepted/rejected outcomes plus
timeout, connection failure, non-2xx, replay, incomplete, oversize, excluded,
and unknown-version cases. Prove exact native bytes/envelope correlation and
that every observation failure leaves native/API terminal state unchanged.

Record packet examples, source separation, content/size choice, compatibility,
and zero provider/spend evidence.

### Joint paws point 4 — release decision

Decide whether SBE needs a fresh immutable release and API a coordinated
deployment. Follow the release playbook with regression scope proportional to
the actual surface; technical qualification does not imply release approval.

## Explicitly deferred

- Human/model judgments and policy calibration (original calibration sprint).
- Threshold, prompt, polish-comparison, or attempt-ceiling changes.
- Batch, bounded, mixed-custody, recovery, interrupted, repair, compatibility,
  unsupported, or ambiguous capture.
- Historical backfill, authoritative storage, delivery retry queues, corpus
  completeness guarantees, and population reporting.
- User-facing review workflow and judgment persistence.
