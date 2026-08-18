# Bounded Authoring Topology and Transport Parity Sprint 2 Plan

Date: 2026-08-18
Status: in progress; Slices 0-7 complete, Slice 7 awaiting API consumer review
Starting release: SBE 0.4.5

## Purpose

Make bounded-Natal authoring use the same quality-preserving six-context editorial
topology as exact Natal, then support bounded Batch as a transport over those same
logical authoring requests.

The central invariant is:

> The semantic route determines the evidence representation; the authoring topology
> determines the model's editorial workload; the transport determines only how an
> identical logical request is submitted and retrieved.

For either exact or bounded Natal, initial authoring consists of five isolated
ten-card story passes plus one summary/global-theme pass. This fan-out is an
editorial-quality control, not a throughput optimization. It prevents one model
context from treating hundreds of short prose fields as a bulk templating task.

The current exact route already follows this topology in both interactive and Batch
mode. The current bounded interactive adapter asks one Response to author the whole
bounded deck and bounded Batch is rejected. This sprint corrects the bounded
topology first and adds Batch without allowing transport choice to change the
editorial assignment.

## Starting behavior

### Exact Natal

- A selected 50-claim packet is transformed into five balanced ten-card story
  workspaces and one summary/theme workspace.
- The default `stratified-v1` assignment is deterministic and deliberately mixes
  claim types, categories, domains, and priority bands while avoiding semantically
  homogeneous adjacency.
- Interactive mode submits each pass as an isolated Responses request.
- Batch mode wraps the same logical pass requests as JSONL members in one or more
  durable Batch rounds.
- Per-pass output is reapplied to locally retained authority, validated, accepted or
  retried, and assembled into canonical final order.

### Bounded Natal

- Selection and delivery already have separate bounded schemas and admit invariant
  evidence only.
- Interactive authoring currently sends the complete bounded editorial workload in
  one structured Responses request.
- Bounded provider output is minimized and SBE deterministically reattaches claim
  identity, invariant authority, projected terms, and evidence provenance.
- Interactive detach/resume and provider reconciliation are supported.
- `service_level=batch` currently fails closed before submission.

## Frozen design direction

### Two independent dimensions

| Dimension | Values | May change |
|---|---|---|
| Semantic route | exact Natal / bounded Natal | admitted evidence, epistemic rules, packet schema, authority reattachment, route-specific prompt version |
| Provider transport | interactive Responses / Batch | submission, provider identity, detach/poll/retrieval, cost settlement |

Transport must not change pass purpose, pass membership for a frozen assignment,
prompt content, writable-field schema, retry feedback, or deterministic assembly.

### Authoring topology

Both routes use:

1. card passes 1-5, each containing exactly ten selected claims in a deliberately
   heterogeneous authoring order; and
2. pass 6, containing summaries and global thematic work without the burden of
   authoring all card prose.

Each pass remains a self-contained story folder/request with sufficient whole-dog
context for coherent characterization. Isolation of model context is required even
when operations execute sequentially because of external authorization or capacity.

### Deterministic assignment

The exact default remains `stratified-v1`. For one frozen selected packet, subject,
assignment-policy version, and explicit seed identity, interactive and Batch must
consume the same ordered assignment plan. Across independent runs the selected
basis or a future versioned assignment policy may differ; the contract does not
permanently bind a claim to one pass.

Bounded assignment will adopt the same goals and replay guarantees through a
bounded feature adapter. The resulting plan must be durable and include policy,
algorithm version, seed, pass cardinality, and ordered claim IDs. No uncontrolled
runtime randomness is introduced. A future variable per-run seed would require an
explicit immutable profile/request identity and is outside this sprint.

### Route-specific prompt resources

Bounded authoring receives its own versioned copy of the exact editorial packet,
workspace, and prompt resources. At sprint entry the intended shared editorial
content is identical. Separate identity permits later bounded-specific explanation
without silently changing exact Natal—for example, guidance about invariant
families, absent scores, and prohibitions on inferred exact placement.

Any future divergence must be explicit, reviewed, versioned, and qualified. Tests
will identify which resource bytes are intentionally identical and prevent
accidental drift.

### Transport parity

For one frozen route/pass request:

- interactive mode submits the request through Responses;
- Batch mode places the same provider-visible system instructions, ordered user
  segments, model/reasoning configuration, structured-output schema, and maximum
  output into a JSONL member; and
- normalization may remove only documented transport-envelope fields before parity
  comparison.

The release-blocking comparison is bounded interactive versus bounded Batch for the
same frozen bounded pass request. Exact and bounded may share intentionally byte-
identical editorial resources, but their route-specific packets, authority notices,
and structured-output schemas are not expected to match each other.

Exact Batch behavior is the compatibility baseline. Bounded Batch will initially
cover initial authoring and creative-retry rounds. Polish, critic, and qualitative
candidate retain their currently supported interactive mechanism unless contract
review finds a concrete reason to broaden them.

## Ownership and safety boundary

SBE remains authoritative for:

- selected claims and deterministic pass assignment;
- minimized provider-visible packet construction;
- exact paid-action binding and immutable per-run spend enforcement;
- native pass, retry, provider-operation, snapshot, journal, and result state;
- reattachment of locked exact or bounded semantic authority;
- pass acceptance, assembly, final QA, and delivery interpretation; and
- packaged schemas, fixtures, readers, CLI behavior, and release evidence.

The AstroWoof API remains authoritative for cross-run reservations, quotas, global
circuit breakers, entitlements, worker capacity, account billing reconciliation,
PostgreSQL/R2 transactions, and public product state.

Provider-visible payloads must retain the established minimized subject boundary.
No protected birth datetime, coordinates, location evidence, internal provenance,
authorization document, secret, or arbitrary workspace path may enter prompts,
Batch JSONL, fixtures, events, or logs.

## Scope

- Record provider-free baseline evidence for current exact interactive/Batch pass
  parity and current bounded single-response behavior.
- Define and validate the bounded six-pass assignment and packet contracts.
- Add separately versioned bounded prompt/workspace resources, initially matching
  the exact editorial resources where intended.
- Build transport-neutral bounded pass request specifications.
- Run bounded interactive authoring as six isolated Responses operations.
- Add bounded initial/retry Batch rounds with durable File/Batch/member evidence.
- Preserve pass-local creative retries and deterministic final assembly.
- Extend lifecycle inspection, reconciliation cycles, native transition journal,
  receipts, events, CLI, schemas, and consumer fixtures where bounded Batch creates
  new validated route/mechanism evidence.
- Qualify exact route non-regression and bounded live/Batch semantic parity from the
  installed wheel on Python 3.11/Linux.

## Non-goals

- Changing exact claim selection, scoring, the fifty-claim semantic budget, or the
  released `stratified-v1` behavior.
- Randomizing assignments between otherwise identical runs.
- Altering unknown-time claim suppression, bounded invariant-admission policy,
  Quick/Complete product policy, hierarchy design, or critic product policy.
- Sending full protected packets or native authority to OpenAI.
- Batching bounded polish, critic, or qualitative candidate merely because initial
  authoring used Batch.
- Changing API reservation, capacity, quota, billing, or publication policy.
- Running paid provider qualification without separate explicit authorization and
  approved dollar limits.
- Publishing a release before final consumer review and explicit authorization.

## Slice 0 — Baseline and editorial-invariant evidence

### Work

- Trace the exact selected-packet to assignment-plan to six-workspace flow.
- Prove exact interactive and Batch builders derive the same logical requests for a
  frozen pass after documented transport-envelope normalization.
- Record exact deterministic assignment replay and heterogeneity evidence.
- Reproduce provider-free that bounded interactive currently presents the whole
  card/summary workload to one Response and bounded Batch fails before submission.
- Inventory bounded lifecycle/action assumptions that currently encode one initial
  operation rather than six passes or one Batch round.
- Identify exact Batch code that is transport-generic versus exact-workspace-specific.

### Tests

- Existing exact split-assignment determinism, balance, and canonical reassembly.
- Existing exact interactive and Batch request-builder tests.
- Existing bounded provider minimization, lifecycle, and Batch-refusal tests.
- A compact provider-free baseline report with zero provider operations and spend.

### Gate

Pause for review of the reproduction, shared-engine seam, proposed pass/action
cardinality, and any lifecycle/schema migration before changing contracts.

## Slice 1 — Contract, identity, and resource freeze

### Work

- Define a versioned bounded split-assignment artifact with five ordered ten-claim
  passes and one separately identified summary/theme pass.
- Freeze bounded pass IDs, operation routes, attempt numbering, replay tuple, and
  action/Batch-round binding.
- Freeze bounded interactive at one paid action per pass/attempt, uniquely bound to
  route, pass, and attempt, and document how its six external-authority boundaries
  are prepared, authorized, executed, and resumed.
- Freeze bounded Batch at one SBE paid action and one API global reservation per
  Batch round, with member-level usage and outcomes settling beneath that round
  rather than multiplying API reservations. Both modes remain bounded by the same
  immutable per-run SBE spend authority.
- Freeze the expectation that bounded six-pass interactive and bounded Batch reuse
  the existing public lifecycle, terminal, custody, consumer-authority, and cost-
  disposition vocabularies. They add supported route-specific trajectories, not new
  state names. If implementation reconnaissance finds a genuinely unrepresentable
  fact, pause for contract review rather than adding an unvalidated state or payload.
- Define a versioned successor to the packaged route-parity transition oracle. The
  current v1 `bounded_batch_rejected` scenario remains historical evidence and must
  not be silently reinterpreted as supported behavior.
- Define normalized bounded-interactive/bounded-Batch logical-request parity and its
  permitted transport-only fields. Do not compare route-specific exact packet/schema
  bytes to bounded packet/schema bytes.
- Copy exact editorial resources into a separately identified bounded resource set;
  record intentional byte parity and future divergence rules.
- Define legacy handling: incomplete pre-sprint bounded runs fail closed unless a
  narrow proven migration is explicitly accepted; do not reinterpret one-operation
  state as six-pass state.

### Tests

- Strict JSON Schema and unknown-field rejection for assignment/pass identities.
- Resource inventory/hash tests and intentional-parity assertions.
- Request-parity fixture validation.
- Contradictory route, transport, pass, attempt, or action binding rejection.
- Table-driven proof that planned bounded interactive/Batch trajectories compose
  only existing lifecycle events and dispositions; any proposed vocabulary addition
  is an explicit review failure at this gate.

### Gate

Pause for SBE and API consumer review before runtime or public lifecycle schemas are
implemented. Review includes the route-parity-oracle successor and the exact API
oracle traces expected later. No paid provider operation is authorized at this gate.

## Slice 2 — Bounded deterministic six-pass packet generation

### Work

- Implement bounded assignment features that distribute claim families/editorial
  characteristics and avoid homogeneous adjacency while preserving every selected
  claim exactly once.
- Generate five self-contained bounded ten-card story packets and one summary/theme
  packet from the single authoritative bounded basis.
- Supply each pass with minimized subject data, relevant decoded terms, bounded
  authority notices, and sufficient whole-dog context.
- Keep locked invariant authority and evidence provenance local where the provider
  needs only editorial interpretation.
- Persist the exact ordered assignment plan and packet/resource identities.
- Implement deterministic reassembly into canonical selected-claim order.

### Tests

- Exactly 50 unique claims, five groups of ten, no omission/duplication.
- Deterministic replay for frozen input and policy identity.
- Claim-family/category/tier balance and adjacency regression checks.
- Pass-local term closure and complete whole-dog summary basis.
- Provider disclosure allow-list and protected-value canaries for every pass.
- Canonical reassembly independent of authoring order.
- Variable input ordering and stable identity/path behavior.

### Gate

The six provider-visible packets are self-contained, heterogeneous, minimized,
replayable, and reassemble without loss of bounded authority. Pause for editorial
packet inspection before submitting any provider work.

## Slice 3 — Shared pass engine and exact-route compatibility

### Work

- Introduce the smallest shared transport-neutral pass-request/result seam needed by
  exact and bounded routes without collapsing their semantic adapters.
- Keep exact workspace construction, prompt bytes, assignment plans, output schemas,
  retry feedback, and assembly behavior unchanged.
- Represent bounded pass input/output through the shared orchestration seam while
  retaining bounded-specific validation and authority hydration.
- Bind route, pass, attempt, prompt/resource hashes, output schema, and maximum
  output into request/action identity.

### Tests

- Golden/request-digest comparison proving exact behavior did not drift.
- Exact interactive and Batch fake-provider regressions.
- Shared pass protocol replay and conflicting-binding refusal.
- Route-crossing negative tests: exact evidence cannot hydrate bounded output and
  bounded evidence cannot enter exact assembly.

### Gate

All exact installed behavior remains compatible, and bounded requests can traverse
the shared seam without weakening route authority.

## Slice 4 — Bounded interactive six-context authoring

### Work

- Replace the bounded whole-deck Response with five card-pass Responses and one
  summary/theme Response using the frozen bounded packets.
- Preserve external spend authorization before every new paid submission.
- Persist each Response ID before further mutation; resume/poll known operations
  without duplicate commitment or submission.
- Validate and hydrate each result independently, run pass QA, and retry only the
  rejected/error pass under frozen creative-retry policy.
- Exhaust safely runnable local work, detach at authorization/provider boundaries,
  and publish coherent snapshot/journal/result evidence before exit.

### Tests

- Six initial isolated fake-provider calls with exact pass membership.
- Authorization wait/resume at every pass boundary.
- Concurrent or reordered completion with deterministic assembly.
- One rejected pass causes only that pass to retry.
- Provider identity persistence, interrupted submission ambiguity, reconciliation,
  and no-resubmit behavior.
- Optional-stage continuation after accepted assembly.
- Blocking scheduler re-drive regression: after the initial six-pass wave completes,
  the run reaches its next applicable authorization/provider boundary—optional
  continuation or pass-local retry—and the supported worker lifecycle reclaims and
  re-drives it to the next durable checkpoint. It must not retain a lease
  indefinitely, silently stop after native `awaiting_external_authority`, or require
  operator repair.
- Exact/bounded protected-data and event-redaction tests.

### Gate

Bounded interactive produces a complete delivery through six isolated authoring
contexts with pass-local retry and no whole-deck bulk-generation request. The
multi-pass scheduler re-drive regression is release-blocking at this gate.

## Slice 5 — Bounded Batch transport

### Work

- Serialize the same six bounded logical requests as ordered `/v1/responses` JSONL
  members with stable `custom_id` bindings.
- Reuse/generalize exact Batch upload, create, detach, poll, output/error download,
  and ingestion machinery rather than create a competing Batch subsystem.
- Persist input JSONL hash, File ID, Batch ID/status, request counts, ordered member
  inventory, output/error File identities, and immutable downloaded artifacts.
- Bind one paid action/API authority to one Batch round; retain per-member Response,
  usage, pass, attempt, prompt, and outcome evidence.
- Treat partial member failure as pass-local failure and prepare only eligible
  failed/rejected passes in a later creative-retry Batch round.
- Preserve missing usage as billing reconciliation pending rather than zero cost.

### Tests

- One initial six-member bounded Batch round.
- Exact normalized request-body parity with bounded interactive for all six passes.
- Detach/resume before upload, after upload, after Batch creation, while pending,
  after terminal files, and during member ingestion.
- Reordered output JSONL, duplicate/unknown/missing `custom_id`, output/error split,
  mixed success, and terminal failed/expired/cancelled Batch.
- One-member creative-retry round for one failed pass.
- Aggregate commitment/usage settlement without member-level reservation inflation.
- Durable provider identity and no duplicate Batch creation after known identity.

### Gate

Bounded Batch is semantically identical to bounded interactive at the pass boundary
and differs only in provider transport/custody mechanics. Pause for API fixture and
lifecycle review.

## Slice 6 — Assembly, whole-deck QA, and optional-stage continuity

### Work

- Assemble accepted bounded passes in canonical claim order and restore complete
  invariant authority, projected registry, claim-local evidence, and broader
  summary/whole-dog evidence scopes.
- Prove whole-deck linter/validation catches repetition across independently authored
  passes without collapsing their prose into one regeneration request.
- Preserve polish, critic, and qualitative-candidate behavior as explicitly
  classified interactive optional stages for both initial transports.
- Preserve generation-profile-driven optional skipping and required-stage terminal
  denial semantics.
- Ensure final bounded delivery schemas remain compatible unless a reviewed schema
  version is demonstrably necessary.

### Tests

- Cross-pass duplicate/template normalization failures.
- Missing/duplicate claim, summary, registry term, and evidence-scope failures.
- Interactive-initial and Batch-initial decks enter identical optional-stage state.
- Polish retry snapshot/resume and critic/candidate reconciliation regressions.
- Monotonic accepted evidence through waiting, warning, review, budget, ambiguity,
  policy-stop, and delivery outcomes.

### Gate

Both transports converge on the same bounded assembly, QA, optional-stage, and
delivery contracts without misrepresenting authoring order as canonical claim order.

## Slice 7 — Public lifecycle, consumer fixtures, and handoff

### Work

- Extend strict lifecycle inspection, reconciliation-cycle results, transition
  journal, execution result/receipt, event catalog, and CLI only where required to
  admit bounded Batch identities safely.
- Expose native route, mechanism, round/action/member binding, provider custody,
  consumer authority, `resume_not_before`, and cost disposition without requiring
  API interpretation of private state.
- Package sanitized route-neutral fixtures for bounded interactive and Batch:
  pending, completed, partial failure, retry, review, ambiguity, unavailable usage,
  terminal provider failure, and delivery.
- Package and validate the versioned SBE route-parity-oracle successor, replacing the
  old bounded-Batch refusal only in the new contract version with supported prepared,
  pending, `not_due`, reclaimed, completed, mixed-member continuation, retry,
  unavailable-usage, ambiguity/review, provider-failure, and delivery trajectories.
- Deliver route-specific provider-free traces for the API's otherwise route-neutral
  effective transition oracle. Prove bounded Batch follows its existing claim,
  provider-pending, release-until-due, reclaim, completion, local-continuation, and
  terminal/publication transitions without adding enum values or events.
- Include explicit bounded Batch traces for partial member failure, pass-local retry,
  pending/`not_due`/reclaim, unavailable usage with retained consumer authority, and
  final delivery.
- Deliver bounded live multi-pass traces proving sequential pass actions cannot cause
  premature delivery or authority/capacity release, cross-pass provider-operation
  confusion, or replacement of one pass's authority by another pass's retry.
- Document bounded transport request parity, paid-action cardinality,
  migration/refusal behavior,
  provider atomicity gaps, and API ownership.

### Tests

- Strict public-reader and CLI schema validation.
- Fixture hashes and installed-resource discovery.
- Strict validation and deterministic replay of the new route-parity oracle plus the
  API-consumable bounded route traces against existing transition vocabulary.
- Early `not_due` is nonmutating; bounded reconciliation respects per-call/per-cycle
  limits and never submits new work.
- Transition publication and orphan repair across snapshot/journal/receipt crash
  boundaries.
- Events are redacted, non-authoritative, failure-isolated, and route accurate.

### Gate

Pause for API consumer review of packaged fixtures, versioned SBE oracle, API
transition-oracle traces, and handoff before final release qualification. “No new
states” is not accepted as a reason to omit route-specific oracle adoption evidence.

## Slice 8 — Installed qualification and release recommendation

### Work

- Build a candidate wheel and verify packaged schemas, prompt resources, fixtures,
  CLI entry points, and `py.typed`.
- Run installed Python 3.11 Linux smoke/qualification for exact interactive, exact
  Batch, bounded interactive, and bounded Batch with fake transports.
- Run Windows source/installed compatibility checks proportional to changed code.
- Validate exact supported AGF/SPC inputs and both evolved identity paths through
  basis, authoring state, delivery provenance, and installed-wheel smoke.
- Record artifact hashes, source commit, tests, platform/runtime identities, zero-
  provider proof, known limitations, and consumer response.
- Prepare release notes and recommendation only; tagging/publication require explicit
  authorization.

### Tests

- Focused route/pass/transport/lifecycle suites.
- Complete repository suite.
- Hash-locked offline Linux wheel installation and `pip check`.
- Installed exact/bounded four-route fake-provider smoke.
- Snapshot restore at the stable logical absolute path and fresh-worker resume.
- No credentials, protected payloads, temporary qualification trees, or provider
  operations in release evidence.

### Gate

Both semantic routes preserve their six-pass editorial topology across live and
Batch transport, exact behavior remains compatible, consumer review is accepted,
and the repository is clean. Pause for version/tag/publication authorization.

## Cross-slice testing strategy

### Contract and determinism

- Strict schemas, closed vocabularies, exact hashes, unknown-field rejection.
- Assignment completeness, deterministic replay, anti-homogeneity, and canonical
  reassembly.
- Separate exact/bounded resource identities with asserted intentional parity.
- Normalized live/Batch logical-request parity for every pass and retry.

### Provider and spend safety

- Authorization checked before every new paid submission.
- Single-writer consumption and exact request/action binding.
- No new commitment for polling known Response/Batch work.
- Failure injection around prepare, authorization, upload, Batch/Response creation,
  provider-ID persistence, output retrieval, ingestion, settlement, snapshot, and
  terminal publication.
- Explicit ambiguity when provider creation cannot be proved absent or identified.

### Editorial quality

- Five heterogeneous ten-card contexts plus a separate summary/theme context.
- No whole-deck initial or retry generation call.
- Pass-local rejection and creative retry.
- Cross-pass repetition/template lint and whole-deck coherence checks.
- Provider-free structural tests plus optional separately authorized bounded live QA
  only if deterministic/fake evidence cannot establish editorial utility.

### Privacy and provenance

- Field-level disclosure allow-list and protected-value canaries in every Response
  and Batch member.
- Immutable local reattachment of exact/bounded authority.
- Separate selected-card and summary/whole-dog evidence scopes.
- Complete registry closure, resource/profile/release identity, and durable native
  transition evidence.

### Compatibility and release

- Exact interactive and Batch are release-blocking regressions.
- Existing bounded delivery consumers remain compatible or receive an explicitly
  reviewed versioned migration.
- Source tests do not substitute for installed Windows/Linux wheel tests.
- No paid qualification is implied by fake-provider success.

## Standard slice gate procedure

At every slice gate:

1. run the focused tests and any specified broader suite;
2. run `git diff --check`;
3. inspect the complete diff and generated artifact inventory;
4. update `LOG.md`, `EVIDENCE.md`, and a compact result document;
5. record provider-operation count and spend, expected to remain zero unless a paid
   gate was separately authorized;
6. pause for review before commit; and
7. after approval, commit and push only the reviewed slice before continuing.

## Exit criteria

The sprint is complete only when:

1. bounded initial authoring and creative retry use five ten-card isolated contexts
   plus one summary/theme context in both interactive and Batch modes;
2. the deterministic bounded assignment is complete, heterogeneous, replayable, and
   durably identified;
3. live and Batch consume the same normalized logical requests for each frozen pass;
4. bounded Batch supports durable authorization, upload/create, detach/resume,
   member ingestion, retry, settlement, and ambiguity/refusal semantics;
5. exact live/Batch request, topology, assembly, lifecycle, and installed behavior
   remain compatible;
6. provider-visible fields remain minimized and locked authority is reattached only
   inside SBE;
7. final bounded assembly preserves canonical order, registry closure, and distinct
   claim-local versus whole-dog provenance;
8. strict public lifecycle/transition fixtures are packaged and accepted by the API
   consumer;
9. complete tests and installed Python 3.11 Linux qualification pass with no
   unapproved provider operations;
10. documentation records the editorial reason for fan-out and forbids transport-
    driven collapse; and
11. release recommendation, known limitations, and exact evidence are reviewed
    before any tag or publication.
