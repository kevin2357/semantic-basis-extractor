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

The two relevant exact-Natal policy identifiers are:

- `legacy_atomic.v1` — the current/default policy.
- `axis_aware.v1` — explicitly experimental and exact-Natal-only.

`axis_aware.v1` is not merely a cosmetic flag. It selects the
`AxisAwareExactNatalPolicy`, whose route is `exact_natal` and whose candidate
generation and axis strategy differ from the legacy policy. A future profile
must reject `axis_aware.v1` paired with a bounded route unless and until a
bounded policy is separately defined and qualified. Silently ignoring that
mismatch would recreate the sort of cross-layer ambiguity the profiles are
intended to remove.

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
it must be a compatibility profile, not a behavioral redesign. The next two
profiles can be bounded-Natal/live and exact-Natal/axis-aware. They should be
separate named profiles even where several settings coincide.

Before implementation approval, the next gate should inventory the actual AGF,
SPC, SBE, and closure command inputs and classify every field as:

| Class | Rule |
| --- | --- |
| secret | Environment/secret reference only; never profile bytes or logs. |
| deployment-only | Static service wiring; cannot vary per job. |
| profile-bound | Canonical, reviewed, allowed to vary only by selected profile. |
| job evidence | Derived from the user/job and never configurable as a profile. |

Required provider-free tests for a later implementation include: exact legacy
compatibility; bounded profile admission; axis-aware exact admission; each
invalid route/policy pairing; unknown or altered digest; role-specific fragment
mismatch; and resume/reconciliation refusal when the persisted profile is not
available byte-for-byte. Filename differences should be asserted as derived
artifact identity, not accepted as an alternative source of route truth.

## Slice 0 decision

Proceed to Gate A only after the four-role input inventory is frozen and API
confirms where profile ID/digest will become admission evidence. There is no
reason to change SBE defaults, add a generic config reader, or expose bounded
selection in this slice.
