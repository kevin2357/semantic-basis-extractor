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
