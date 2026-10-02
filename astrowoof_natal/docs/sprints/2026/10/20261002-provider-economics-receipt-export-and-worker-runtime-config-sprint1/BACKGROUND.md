# Background — provider-economics receipt export and worker runtime configuration

## Status

**Slice 0 discovery complete — 2026-10-02.** This remains a planning-only
companion. Discovery made no package change, release, provider call, Render
mutation, database mutation, retained-workspace access, or paid QA work.

## Why this sprint exists

The API/SBE provider-economics adoption sprint proved that the first half of
the public handoff works, then exposed that its final-settlement half does not.
A fresh, explicitly capped two-reading QA cohort was launched after the API
economics and bounded-retry work landed.

For the completed **Economics Orbit** reading, the authoritative API custody
records show eight paid actions transitioned to `reported` (six initial-wave
and two polish actions) with provider-reported costs and settled reservations.
The reading itself reached successful delivery. However, the public economics
revision export observed by the API stayed at its initial `pending` revisions:
there were no receipt-side revision updates containing reported micro-USD,
tokens, or terminal native/editorial outcome. The normal Better Stack stream
likewise contained initial accepted `provider_economics.ingestion.v1` pending
events, followed by `sbe_export_unavailable` events during later cycles.

This is not an OpenAI-pending explanation for Orbit. The provider-action
custody record already establishes completed/reported work. It is a cross-
repository receipt-export/ingestion gap: SBE has enough normal-runtime data to
settle the action, but the API-facing public export did not make the successor
economics revision available.

The companion **Economics Comet** run remains legitimately in provider
reconciliation with one provider-local dependency. It is useful only as a
live pending witness; it must not be treated as a failure fixture or mutated
while this sprint is planned.

## Second workstream — launch-selected runtime configuration for four worker services

An upcoming SBE release also needs a disciplined way to pass detailed,
reviewable runtime configuration into the four main worker scripts: AGF, SPC,
SBE, and semantic closure. Today, several real processing choices are
hard-coded in commands or deployment environment variables. That was adequate
while the production route was a single exact-natal/live profile, but it does
not give a job launch a safe way to select a reviewed alternate profile.

Near-term examples are a bounded-natal/live route, which requires compatible
but distinct AGF/SPC/SBE inputs, and SBE's axis-aware processing option. The
goal is not free-form per-job settings: a launch chooses one approved,
environment-appropriate configuration identity, then every participating
worker reads and attests the same relevant configuration before work begins.
This should make a bounded-live feasibility run possible without cloning the
pipeline or silently changing the exact-natal/live baseline.

The expected direction is a **versioned run-configuration file**: a
non-secret, schema-validated artifact that names the deployed SBE release,
compatibility identity, generation profile, worker-role behavior, and bounded
operational parameters. Services would receive only the minimal pointer or
digest required to load the same reviewed configuration. Secrets must remain
in the platform secret store and must never be serialized into the artifact.

That is a hypothesis, not a frozen solution. Slice 0 must inventory the actual
four worker roles and all current configuration sources, compare viable
options, and select a design before implementation. Alternatives to assess
include a run-config file plus digest, per-service environment variables with
an attested manifest, and a centrally persisted API-owned configuration
record. The choice must preserve startup failure semantics, rollback behavior,
environment separation, and truthful runtime observation.

## Third workstream — versioned OpenAI prompts

The forthcoming release also needs prompt selection to be explicit, durable,
and reviewable. A worker invocation must not rely on an implicit repository
default when a release, QA cohort, or operator command needs to establish
exactly which OpenAI prompt/query formulation was used.

This sprint must design a prompt-versioning system for OpenAI-facing work and
an explicit command-line parameter that selects the intended query/prompt
version. The existing prompts predate the Render deployment and have served
well, but production review has already identified improvements worth testing,
including direct-to-dog/full-astrology cards that sometimes contain no explicit
astrology. The selection must be validated before any provider request is
made; an absent, unknown, incompatible, or environment-forbidden version must
fail closed rather than silently falling back to a newer default. The selected
version/digest must be included in safe runtime/configuration attestation and
in the bounded evidence needed to join provider economics and editorial
outcomes. Prompt text itself, user inputs, and provider response text remain
out of ordinary logs and configuration artifacts.

The design must assess the relationship between prompt version and the
proposed worker run-configuration identity. A run-config may select a default
approved prompt version, while the CLI parameter may intentionally override it
only under explicit compatibility and environment policy. Slice 0 must decide
precedence, idempotency/replay semantics, rollout/rollback behavior, and
whether stored work checkpoints bind the selected prompt version immutably.

### Prompt-release correction — static workspace guidance is prompt material

The first installed prompt-release record binds only the short system-message
asset. That is useful registry groundwork, but it is not a complete authoring
prompt identity: the authoring agent is also instructed to read `START HERE.md`
and follows static guidance copied into the generated exact/live workspace.
Run-specific cards, chart material, and generated assignment text remain
dynamic input covered by the workspace/generation manifest; the versioned
prompt release must instead inventory every static instruction asset that the
worker places or references in that workspace.

Production editorial samples identified a narrow ambiguity rather than a
contradiction. The exact/live workspace brief says direct-to-dog prose offers
"perspective and dignity," while separately requiring full-astrology prose to
explain relevant planets, angles, signs, Doghouses, aspects, geometry, and orb
strength. Some direct-to-dog/full-astrology cards contain little or no explicit
astrological terminology. The proposed new release will preserve all existing
instruction bytes except for a single clarification attached to each copied
direct-to-dog instruction: audience changes address and tone, never the chosen
astrology density; a direct-to-dog `full_astro` rendering retains the relevant
astrological explanation in warm, readable second-person prose.

The existing compatibility profile and its prompt release remain immutable
fallback evidence. The new axis-aware exact/live profile will bind a new
editorial prompt release and its own copied, fully digested static instruction
set. This permits a clean future comparison without silently changing the
current route.

## Evidence and linked work

- API Sprint 123, [provider-economics adoption and bounded user retry](https://github.com/kevin2357/astrowoof-api/tree/main/docs/sprints/2026/09/20260929-provider-economics-adoption-and-bounded-user-retry-sprint123), created the validated economics-tape ingress, operational event contract, and capped QA cohort procedure.
- SBE Sprint 1, [accounting and performance visibility](../../08/20260821-silly-owner-wants-accounting-and-performance-visibility-sprint1/BACKGROUND.md), and its [public export/API ingestion handoff](../../08/20260821-silly-owner-wants-accounting-and-performance-visibility-sprint1/SLICE%205%20-%20PUBLIC%20EXPORT%20AND%20API%20INGESTION%20HANDOFF.md) define the intended producer-side public export seam.
- API [Provider Economics Reporting](https://github.com/kevin2357/astrowoof-api/blob/main/docs/operations/Provider%20Economics%20Reporting.md) distinguishes append-only accounting evidence from operational logs.
- The QA witness is Orbit API run `bdc1fd8e-9626-43c9-8ad5-cd3b9fd067a1`; it must be inspected read-only through authoritative custody plus matching SBE logs. Comet is `48c98193-5031-4638-a91e-72d69ea66d96`.
- Control Room issue #29 remains the Better Stack maintenance owner; this sprint must link its eventual operational-query outcome rather than create unowned monitoring work.

## Required boundaries

- API/PostgreSQL remains lifecycle, spend, reservation, and publication
  authority. SBE public economics evidence is observational; Better Stack is
  non-authoritative operational evidence.
- A missing receipt is never a zero-cost receipt. The public export must retain
  pending, partial, reported, unavailable, and terminal semantics distinctly.
- Do not reconstruct economics revisions from worker logs, mutable workspace
  files, or raw provider payloads.
- The final public revision must preserve predecessor/replay/idempotency rules.
  A late receipt may enrich accounting evidence but cannot resurrect a failed,
  abandoned, or unpublished reading.
- Runtime configuration artifacts may contain no credentials, prompts,
  response text, subject data, raw provider payloads, or private endpoints.
- Every worker role must either attest the exact config identity it loaded or
  fail closed before consuming work. No silent defaults or cross-environment
  fallback are acceptable.

## Open questions for Slice 0

1. At what exact SBE transition are receipt-side economics revisions produced,
   and why did the public export become unavailable after Orbit's actions were
   reported?
2. Which fields are required in successor revisions: price-book identity,
   detailed bounded record data, tokens, monetary amounts, provider status,
   receipt/retrieval timings, native/editorial outcomes, and publication state?
3. Does the public export API require an explicit finalization flush/readiness
   call, or is the omission a producer bug in normal reconciliation/delivery
   flow?
4. Which exact configuration inputs are consumed by AGF, SPC, SBE, and
   semantic closure, and which are shared versus role-specific? In particular,
   what is required to select bounded-live and axis-aware processing without
   weakening exact-natal/live defaults?
5. Which configuration delivery option gives the strongest reviewability,
   startup validation, rollout atomicity, rollback, and environment isolation?
6. What is the canonical prompt/query-version identifier, where are approved
   prompt assets stored, and how does the CLI selector bind it before provider
   creation without exposing prompt content in routine observability?
7. Which static exact/live workspace instruction resources are copied or
   referenced at authoring time, and how can their release-selected byte set be
   separated from dynamic per-run workspace input without weakening workspace
   manifest custody?
