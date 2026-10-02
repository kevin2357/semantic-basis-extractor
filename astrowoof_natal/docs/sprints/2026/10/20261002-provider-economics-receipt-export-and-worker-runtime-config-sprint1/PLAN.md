# Plan — provider-economics receipt export and worker runtime configuration

## Objective

Restore the normal SBE public successor-revision export so completed paid
actions contribute truthful receipt, token, cost, timing, and outcome evidence
to the API economics tape; separately establish a reviewable configuration
delivery design for all four worker-service roles; and design explicit,
versioned OpenAI prompt selection.

## Planning posture

The three workstreams share a release window but not an implementation
assumption. Slice 0 freezes their independent discovery results and interfaces
before any package or deployment work begins. In particular, runtime
configuration is an approved-profile selector, never an unvalidated bag of
per-job overrides.

## Slice 0 — producer/export trace and four-script launch-configuration inventory

### 0A — Economics successor-revision trace

- Trace Orbit's completed normal route from provider custody observation
  through SBE economics-revision production, public validation/export, API
  consumption, and the observed `sbe_export_unavailable` outcome.
- Identify the first transition where a truthful successor revision should be
  available but is absent. Distinguish a producer omission, an explicit
  finalization/readiness requirement, and an API reader/transport mismatch.
- Freeze the minimum successor revision fields and predecessor/replay rules;
  preserve pending, partial, reported, unavailable, and terminal semantics.
- Inspect Orbit read-only. Do not use Comet as a failure fixture and do not
  reconstruct revisions from logs or workspaces.

### 0B — Four-script launch configuration inventory

- Inventory every current processing input for AGF, SPC, SBE, and semantic
  closure: deployment command, environment variable, hard-coded default, and
  persisted/checkpoint-derived value.
- Classify each input as shared, role-specific, secret, environment-specific,
  compatibility-critical, or safely launch-selectable.
- Specifically trace the parameter set required for a bounded-natal/live
  profile and for SBE axis-aware processing. Treat route, service level, and
  selection policy as independent dimensions; inventory the combinations that
  the current installed implementations actually support rather than encoding
  `axis_aware` as a route or service-level variant. Establish whether the
  bounded profile can reuse the exact-natal pipeline lifecycle/provider path
  while preserving a distinct semantic identity and artifact naming.
- Record the real launch topology as well as the logical roles: determine
  whether AGF/SPC are independently launched or are both inputs to the
  qualified deterministic-runtime executable, and place profile verification
  at each actual process boundary.
- Compare a versioned non-secret configuration file plus digest with an
  attested manifest and API-owned record. Require exact-profile startup
  attestation or fail-closed behavior from every participating worker.

### 0C — Prompt-version selection inventory

- Inventory OpenAI-facing prompt/query assets, their current implicit default,
  and each provider-creation call site.
- Define candidate immutable prompt-version identifiers, approved asset
  storage, CLI selector shape, and safe digest/attestation fields.
- Decide precedence among a run-config default, an explicit CLI selection, and
  checkpoint/replay binding. Unknown, incompatible, and environment-forbidden
  versions must refuse before provider creation.
- Keep prompt text, user inputs, and provider responses out of run-config
  artifacts and ordinary logs.

**Gate A:** jointly approve the economics failure boundary, the four-script
configuration inventory/profile-selection model, and prompt-selection
precedence before implementation, package changes, provider work, or deployment
mutation.

## Post–Gate A implementation plan — runtime configuration

Gate A is approved. The following slices implement the runtime-configuration
workstream only. They deliberately do not make a bounded or axis-aware profile
admissible merely by adding a configuration record: each support tuple must be
explicitly implemented, tested, and admitted independently.

### Slice 1 — Freeze the canonical processing-profile and prompt-release contracts

**Implemented provider-free on 2026-10-02; Gate B closed through Slice 1β.**

- Add the versioned, non-secret `processing_profile.v1` contract and its
  canonical serialization rules. A profile has one immutable profile ID and
  SHA-256, and separates the independent dimensions of natal route
  (`exact_natal` or `bounded_natal`), service level (`live` or `batch`), and
  selection policy (`legacy_atomic` or `axis_aware`).
- Define the SBE-owned installed profile bundle as a closed allowlist keyed by
  profile ID. Each entry carries the complete shared profile identity plus its
  SBE semantic-closure fragment and an approved prompt-release reference. It
  contains no paths, workspace roots, credentials, endpoint URLs, executable
  locations, grants, or terminal/reconciliation authority.
- Freeze the complementary cross-package handoff: API admission persists the
  profile ID, full-profile SHA-256, route/contract identity, and compatible
  worker identities; the deterministic-runtime and SBE images each carry the
  matching immutable bundle and validate their own fragment at their actual
  process boundary. The generation manifest is extended as the durable common
  record rather than creating a competing mutable source of truth.
- Publish the initial `exact_natal` / `live` compatibility profile. It makes
  every presently implicit production setting explicit, including the current
  `legacy_atomic` selection policy and prompt release, without changing the
  observable behavior of a newly admitted exact/live run.
- Add a closed prompt-release contract and installed asset inventory: release
  ID, semantic version, release digest, allowlisted component names, and
  canonical LF/UTF-8 asset digests. Keep prompt text and user/provider content
  out of the profile and public records.
- Provider-free coverage: canonical-byte and digest stability; duplicate,
  malformed, unknown, and incompatible profile/release refusal; secret/path
  field rejection; and proof that `axis_aware` remains independent of the
  exact/bounded and live/batch axes.

**Gate B:** API reviews the exact profile/prompt schema, the compatibility
profile identity, and the proposed generation-manifest/handoff extension before
any runtime consumer starts using it.

### Slice 1β — freeze qualified worker compatibility identities

**Completed provider-free on 2026-10-02; replacement profile review pending.**

- Extend the closed canonical profile with one exact compatibility descriptor
  for each actual launch boundary: `deterministic_runtime` and
  `sbe_authoring`. Each descriptor names its exact required package set and a
  SHA-256 derived from that canonical requirement object. It is stable package
  compatibility evidence, not an invented label or a deployment setting.
- Preserve the separate control-plane distinction: API's environment-specific
  deployed-worker `compatibility_identity` continues to fence the selected
  deployment; it is not copied into the cross-environment package profile.
- Freeze the closed worker-role vocabulary as `deterministic_runtime` and
  `sbe_authoring`. API handoff envelopes may carry one of those tokens only;
  later consumers must verify the role against the corresponding profile-owned
  compatibility identity.
- Recompute the profile and catalog identities after the fields are added,
  update prompt/profile cross-reference evidence if needed, and preserve the
  existing exact/live/legacy tuple as the only installed capability.
- Provider-free coverage: each profile contains both identities; an injected,
  missing, or mismatched identity fails closed; and the profile digest changes
  exactly when either compatibility identity changes.

**Gate B closure:** API reviews the republished initial profile digest and its
two field names. Only then may Slice 2 wire the binding into a worker command.

### Slice 2 — Resolve and attest the SBE profile before semantic closure

- Add one narrow SBE resolver that accepts the API-persisted expected profile
  ID and full-profile SHA-256, finds only an installed allowlisted entry, and
  verifies canonical identity and SBE-fragment compatibility before semantic
  closure/provider construction.
- Wire the resolver into the actual SBE semantic-closure command boundary, not
  a wrapper-only code path. Derive the existing closure flags from the resolved
  SBE profile fragment; do not permit arbitrary CLI flag overrides to alter a
  paid run.
- Write safe startup and durable-workspace attestation only after validation:
  profile ID, full-profile SHA-256, local bundle/fragment digest, prompt-release
  ID/digest, route/service/selection tuple, and worker compatibility identity.
  Do not record paths, prompts, raw inputs, responses, secrets, or grants.
- Bind the resolved profile to the native invocation/result lineage so resume,
  retry, reconciliation, and terminal handoffs require the persisted binding
  rather than recomputing a current default. Legacy workspaces without this
  binding remain on their documented legacy reader path and are never silently
  reclassified.
- Provider-free coverage: exact match succeeds; missing/wrong ID or digest,
  unsupported tuple, incompatible SBE fragment, and tampered installed bundle
  fail before any provider action; retry/resume preserves the original binding;
  normal legacy recovery behavior remains unchanged.

### Slice 3 — Make prompt-release selection and request provenance executable

- Replace the implicit prompt-template default with a resolver for the prompt
  release selected by the already validated processing profile. A CLI selector
  is allowed only for new local/qualification invocations after the same
  allowlist and compatibility checks; it cannot override an existing persisted
  run binding.
- Route every OpenAI-facing SBE creation path through that resolver, including
  ordinary initial/retry, polish, critic, bounded-lifecycle, and supported
  authority paths. Preserve each path's existing prompt assembly semantics
  while selecting versioned installed assets.
- Record safe per-action provenance: prompt-release ID/version/digest, selected
  component inventory and digests, and rendered request digest. Preserve the
  existing private/full-payload controls; ordinary logs and public artifacts do
  not gain prompt text or provider responses.
- Provider-free coverage: all supported provider constructors select the
  profile-bound release; unknown or mismatched release refuses before request
  creation; legacy bindings retain their prior selection; request payload bytes
  for the compatibility release remain byte-identical to the pre-registry
  behavior where the existing fixtures cover them.

### Slice 4 — Cross-process profile binding and installed-wheel qualification

**Completed provider-free on 2026-10-02.**

- Coordinate the API/deterministic-runtime half of the contract: admission
  selects an approved profile, writes the immutable binding to the existing
  generation manifest, and passes only the ID/digest and applicable role data
  to the deterministic-runtime and SBE command boundaries.
- Run a provider-free joined replay using the exact installed SBE wheel and the
  matching deterministic-runtime/API artifacts. Prove both actual processes
  independently verify the same profile identity before work; prove the
  manifest and native receipts retain it across retry and terminal routes.
- Exercise the compatibility profile end-to-end, then negative cells for a
  wrong digest, an unsupported tuple, an incompatible worker identity, and a
  profile/prompt mismatch. Every negative cell must refuse before paid provider
  work and without weakening ordinary legacy-workspace recovery.
- Treat bounded/live and every axis-aware tuple as later, separately admitted
  profile candidates. Their addition requires their own capability evidence,
  artifact-naming review, and provider-free qualification; this slice does not
  infer support from the exact/live compatibility proof.

**Gate C runtime-config disposition:** satisfied on 2026-10-02. API and SBE
jointly qualified the exact retained `0.4.66a0` SBE alpha wheel, its real
semantic-closure CLI create/resume boundary, and a separate local-only
deterministic image that carries the same installed SBE profile bundle. Exact
handoffs and returned attestations passed; altered/missing profile references
and deployment identities refused before provider or AGF work. The alpha is
qualification evidence only, not an activated profile, publishable package, or
deployment input. See `GATE C - 0.4.66-alpha CANDIDATE IDENTITY.md` and the
reciprocal API Gate C review.

### Parallel Slice E1 — Economics diagnostic classification (joint, separate release concern)

- Preserve `sbe_export_unavailable` as nonfatal and avoid promoting telemetry
  into a financial source of truth.
- SBE owns the strict local producer proof: a sealed final exact/bounded
  snapshot yields one validated successor export; resubmitting that exact
  accepted successor as the only predecessor yields an explicit zero-revision
  replay. It must never discover remote state, publish remotely, or invent a
  second receipt.
- API owns the bounded safe phase labels and the nonfatal operational event.
  This is the correct location because sealed-publication mismatch and
  immutable predecessor/ingress failure are API-only boundaries, while SBE's
  public reader intentionally exposes no exception prose, paths, workspace
  contents, request data, or provider payloads.
- Joint provider-free exact and bounded fixtures must exercise each classified
  failure phase and prove that the same safe classification reaches API's
  emitted operational event. The final consumer cell must pass the actual
  SBE-produced successor into immutable API ingress, then prove the exact
  replay is idempotent. Neither side may infer a diagnosis from exception
  prose or fall back to generic latest-state discovery.

This slice is intentionally independent of the completed runtime-config Gate C
and may be qualified as its own joint API/SBE evidence track after focused
cross-repository review.

## Required eventual outcomes

- A completed reported action produces an idempotent successor public economics
  revision instead of leaving the initial pending revision as the latest data.
- The revision carries only the approved bounded accounting/performance fields;
  missing usage remains explicit and never becomes zero.
- API and Better Stack can observe the same accepted/replayed/unavailable
  semantics without logs becoming the financial source of truth.
- All four worker roles load one reviewed, environment-specific configuration
  identity and emit/attest that identity at startup or fail closed.
- Secrets stay in platform secret storage; a run-configuration artifact, if
  selected, contains only safe non-secret values and a version/digest.
- Each OpenAI-facing invocation binds an approved prompt/query version through
  an explicit CLI parameter (or an explicitly defined run-config default),
  validates it before provider creation, and records its safe identifier/digest
  in durable evidence without logging prompt or response content.

## Decisions deferred to discovery

- Whether the run-config file plus digest is superior to an attested
  environment-manifest or an API-owned persisted configuration record.
- Exact schema and transport for final public economics revisions.
- Whether Better Stack's `sbe_export_unavailable` is an appropriate bounded
  operational outcome, a missing-export symptom requiring correction, or both.
- Prompt asset registry/storage, the exact CLI flag and its precedence over a
  run-config default, checkpoint/replay binding, and compatibility/rollback
  rules for a selected version.
- Release and QA qualification scope. No provider-backed qualification is
  implied by these planning documents.
