# SBE Run Config — Slice 0 Findings

## Scope and conclusion

This is discovery only. No runtime configuration mechanism, command line,
worker image, provider invocation, or deployment setting was changed.

The proposed configuration work is feasible, but it is not a simple shared
``config.json`` bolted onto four commands. The safe unit is an immutable,
admission-bound **processing profile**: a reviewed named profile, represented
by canonical bytes and a digest, that is compatible with one route and the
four worker roles. Each worker may consume only its own fragment, but all
fragments must derive from the same overall profile identity.

That distinction matters because three things are otherwise easy to conflate:

1. Deployment configuration is static service/environment wiring (image,
   secret references, endpoint names). It must not become per-job freeform
   input.
2. A processing profile is a selected, non-secret set of approved execution
   choices for one job. It belongs in API admission, job state, and every
   durable worker handoff.
3. Prompt release selection is a provider-facing subcomponent of the profile.
   Its separate findings are in `SBE LLM Prompt Versioning Slice 0 Thoughts.md`.

## What SBE actually exposes today

The exact-Natal closure entry point already has many independently supplied
options. Its parser includes provider, model, reasoning effort, service level,
token cap, retry/polish model settings, polling/timeouts, cache policy,
full-chart basis format, split-assignment policy, and an exact-Natal policy.
The current defaults are therefore command behavior, not a versioned profile.

The closure parser currently exposes two selection-policy identifiers:

- `legacy_atomic.v1` — the current/default policy.
- `axis_aware.v1` — explicitly experimental.

`axis_aware.v1` is not merely a cosmetic flag. The present source implementation
is named `AxisAwareExactNatalPolicy`, and its current parser wiring therefore
only proves the exact-route implementation we inspected. That is an
implementation inventory fact, not a product taxonomy. The intended profile
model must treat selection policy as orthogonal to both birth-time route
(`exact`/`bounded`) and service level (`live`/`batch`). Gate A must determine
which combinations are actually supported by each qualified release and fail
closed for a combination that is not. It must not make a category such as
“exact-Natal/axis-aware” appear to be a third route.

Bounded-Natal is also not simply the exact command with a boolean switched.
SBE has a distinct `bounded_run` CLI and a distinct durable route contract,
`astrowoof.bounded_natal.authoring_run.v2`. It accepts a bounded family,
input package, subject and generation-profile paths, and constructs an
`OpenAIBoundedLifecycleProvider`. Its model, reasoning, service level, and
maximum token defaults happen to resemble the exact route, and its authority
and reconciliation concepts are familiar, but basis construction, portfolio
selection, artifact compilation, resume behavior, and the durable contract
are route-specific. The provider lifecycle can be reused conceptually; the
route materialization cannot be treated as a copy-paste command line.

## Four-role launch inventory

The requested inventory is now complete enough to distinguish real launch
boundaries from the logical AGF/SPC/SBE/closure stages. It also corrects the
initial shorthand that all four are independently launched scripts.

| Logical role | Current process boundary and configuration evidence | Profile-relevant inputs / present gap |
| --- | --- | --- |
| AGF canonical calculation | The API deterministic worker invokes `astrowoof-deterministic-runtime calculate-canonical --invocation … --result …`; AGF is not launched as a separate API subprocess. | The active generation manifest pins AGF version/wheel, Python 3.11, PySwissEph 2.10.3.2, and `moshier` ephemeris mode. The invocation supplies job/birth evidence. House system and bounded calculation choices need an explicit profile fragment rather than an inferred worker default. |
| SPC projection | The same deterministic-runtime executable receives `project-all-contexts --canonical-result … --workspace … --result …`; SPC is likewise not a separately launched service command. | The active manifest pins SPC version/wheel, `woofmapped_astrology.v0@0.1.0`, and the four contexts `general`, `handler`, `direct-to-dog`, and `hybrid`. Bounded SPC has its own CLI contract requiring context ID/version and profile ID/version. These become route-specific fragment fields. |
| SBE workspace initialization and lifecycle | API launches `astrowoof-semantic-closure` directly with input package, subject, run dir, generated spend-policy file, and frozen live arguments. | Current frozen live arguments are `provider=openai`, `service-level=interactive`, `routing-policy=cost_optimized`, `split-assignment-policy=stratified-v1`, `full-chart-basis-format=compact-v2`, `max-workers=6`, `max-attempts=3`, polish enabled/capped at 2, qualitative critic enabled, critic model Luna, critic reasoning medium. The absence of an explicit `--exact-natal-policy` means the parser’s legacy selection default is used today; a compatibility profile must state it explicitly. |
| Closure/authoring behavior | This is the semantic-closure CLI invoked in the SBE worker, rather than a fourth independently deployed worker. Its parser additionally owns model routing, retry/polish/critic choices, prompt cache, timeouts, transport retry, output cap, qualitative caps, and the authority/event handoff files. | Separate profile-bound behavior from authority inputs (spend grants, reconciliation, external authority request/grant), job evidence (input package/subject/run dir), and secrets (`OPENAI_API_KEY` / endpoint wiring). The prompt-release reference belongs here but its registry is a separate immutable layer. |

The API’s current production generation manifest already persists useful
compatibility evidence: profile ID, deterministic/SBE compatibility identities,
AGF and SPC wheel identities, SBE wheel identity, service execution mode,
projection contexts, and a spend-policy fragment. It does **not** yet provide
one validated profile digest whose role fragments cover the actual command
arguments above. In particular, several SBE behavior choices are hard-coded in
`live_frozen_arguments()` and are not represented as explicit manifest fields.

### Classification of the current surface

| Class | Current members | Profile rule |
| --- | --- | --- |
| job evidence | birth-data handoff, input package, subject, workspace/run paths, exact authority documents, checkpoint identity | Derived per job; never selectable profile values. |
| secret / deployment wiring | OpenAI key environment name/value, base URL, database/R2 credentials, executable locations, worker roots | Remain platform configuration; profile may name a capability but never contain the secret or private endpoint. |
| operational worker behavior | SBE service level, routing/model policy, concurrency, retries, token cap, cache mode, poll/HTTP limits, polish/critic behavior | Candidate SBE profile fragment, subject to capability and spend-policy validation. |
| deterministic semantic behavior | AGF ephemeris/house/bounded basis choices, SPC context/profile/version, route contract, SBE split policy/basis format/selection policy | Candidate shared profile fragments; must be pinned before AGF/SPC/SBE consume work. |
| authority/custody | spend policy, grants, reconciliation, lifecycle/terminal commands, event transports | Not general runtime flags. They retain existing exact handoff contracts and must not become mutable profile choices. |

Thus a profile launcher must not copy every CLI argument into JSON. It selects
only approved semantic/operational behavior; paths, sealed authority documents,
and secrets retain their separate boundaries.

Bounded authoring is a distinct `bounded_run` command with its own input
package/subject/generation-profile inputs, model/reasoning/service-level/token
settings, and bounded route contract. Its lifecycle concepts can be shared,
but neither its input semantics nor SPC bounded profile/context requirements
are evidence that it can consume an exact-run profile fragment unchanged.

## Recommended profile boundary

Define one canonical, non-secret `processing_profile.v1` with at least:

- `profile_id`, schema version, and canonical SHA-256;
- route family and exact route contract expected by each worker;
- an allowlisted AGF calculation/basis fragment;
- an allowlisted SPC projection/generation fragment;
- an allowlisted SBE fragment (including exact-Natal policy where applicable,
  authoring/provider behavior, and the prompt-release reference);
- a closure/finalization fragment;
- output/artifact namespace rules, rather than ad-hoc filename strings; and
- release compatibility constraints for the participating packages.

The API should select one profile at admission and persist both `profile_id`
and `profile_sha256` before AGF begins. Each stage should receive that same
identity and reject an absent, unknown, incompatible, or digest-mismatched
profile before doing work. Checkpoints and safe structured events should carry
only the ID/digest and route — never secret values or arbitrary config text.

For an in-flight run, a CLI override must not replace a persisted profile.
Resume, reconciliation, and detached continuation must re-open the exact
admitted profile or fail closed. A new selection belongs only before the first
durable processing action of a new job.

## Delivery options and recommendation

A process environment variable per option is the weakest design: it is hard to
review as one object, can drift role-to-role, and does not naturally provide a
durable digest. A single API database row is better for admission but does not
by itself make the selected bytes available or independently verifiable to
every worker.

The smallest credible initial design is a versioned, canonical profile bundle
shipped with (or otherwise immutably installed alongside) each qualified worker
image. API passes only an allowlisted ID plus the expected digest. The worker
loads the local bundle, resolves the ID, recomputes the digest, validates its
role/route compatibility, and records that identity in durable state. This
avoids runtime fetch races and makes image/profile compatibility auditable.

If independent profile rollout becomes necessary later, use an immutable
release asset/object with a pinned digest and retain the same local validation
rules. Do not let workers fetch a mutable ``latest`` profile at launch.

## Initial profile set and proof obligations

The first profile should explicitly encode today’s exact-Natal/live behavior;
it must be a compatibility profile, not a behavioral redesign. Future profiles
select independent values for route, service level, and selection policy. A
selection-policy experiment must therefore name its compatible exact/bounded
and live/batch matrix instead of being labeled as a route-like profile. Profiles
remain separate named immutable objects even where several settings coincide.

Before implementation approval, the next gate should inventory the actual AGF,
SPC, SBE, and closure command inputs and classify every field as:

| Class | Rule |
| --- | --- |
| secret | Environment/secret reference only; never profile bytes or logs. |
| deployment-only | Static service wiring; cannot vary per job. |
| profile-bound | Canonical, reviewed, allowed to vary only by selected profile. |
| job evidence | Derived from the user/job and never configurable as a profile. |

Required provider-free tests for a later implementation include: exact legacy
compatibility; bounded profile admission; every explicitly supported
route/service-level/selection-policy combination; each unsupported combination;
unknown or altered digest; role-specific fragment mismatch; and
resume/reconciliation refusal when the persisted profile is not available
byte-for-byte. Filename differences should be asserted as derived artifact
identity, not accepted as an alternative source of route truth.

## Slice 0 decision

Proceed to Gate A only after the four-role input inventory is frozen and API
confirms where profile ID/digest will become admission evidence. There is no
reason to change SBE defaults, add a generic config reader, or expose bounded
selection in this slice.
