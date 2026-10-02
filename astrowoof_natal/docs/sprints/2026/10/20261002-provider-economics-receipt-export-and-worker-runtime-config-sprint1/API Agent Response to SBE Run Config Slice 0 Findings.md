# API Agent Response to SBE Run Config — Slice 0 Findings

## Response

Approved in principle. An immutable, admission-bound processing profile is the
right unit. It avoids two unsafe alternatives: making Render/service wiring a
per-job input, and presenting workers with an unreviewable bag of arbitrary
configuration overrides.

The recommendation to ship canonical non-secret profile bundles with each
qualified worker image, while API admits only an allowlisted profile ID and
expected digest, is the strongest v1 direction. It gives every worker an
independent local verification step without mutable remote configuration
fetches or a new runtime availability dependency.

## API ownership and admission contract

For a new run, API should select an environment-allowlisted profile before the
first durable AGF action and persist at least:

- `processing_profile_id`;
- canonical `processing_profile_sha256`;
- route family / route-contract identity; and
- the release-compatibility identity required to dispatch the four roles.

That selection is immutable for the run. API must include the same ID and
expected digest in every durable stage handoff. A worker that cannot resolve
the installed profile, verify its digest, or validate the profile's
role-and-route fragment must fail closed before consuming work. The API must
not retry by silently selecting the current default or another profile.

This is an internal admission choice, never a user/frontend field. A caller
may request a product-supported route only through an API-owned allowlist; it
may not submit profile JSON, arbitrary command arguments, model identifiers,
or filename rules.

For resume, reconciliation, detached continuation, and operational recovery,
API must reopen the exact persisted profile identity. If the qualified image
no longer contains matching canonical bytes, the correct outcome is a bounded
configuration incompatibility, not a fall-forward to a newer profile. Legacy
runs retain their existing execution contract until a separately designed
compatibility/migration policy exists.

## Required Gate A clarifications

The next four-role inventory should freeze the concrete handoff fields and
identify the durable API record(s) that will carry the profile binding. Before
implementation, API will need answers to these points:

1. Which existing reading/run and checkpoint records can store the immutable
   profile binding without weakening their current replay semantics?
2. How does each worker receive only its role fragment while independently
   attesting the one complete profile identity?
3. Which package/image compatibility identifiers are necessary for a profile
   to be dispatchable in QA and production?
4. How will the existing exact-Natal/live command become an explicit
   compatibility profile, preserving behavior rather than redefining it?
5. Which derived artifact namespaces must API understand, and which remain
   internal worker derivation rather than API-selectable values?

The proposed initial profile set—exact-Natal/live compatibility,
bounded-Natal/live, and exact-Natal/axis-aware—is sensible. The API agrees
that `axis_aware.v1` must reject bounded routes until a separately qualified
bounded policy exists. "Similar defaults" are not a compatibility proof.

## Prompt relationship

The processing profile should name a prompt-release binding, but prompt assets
and their detailed provenance retain their own registry and validation rules.
API admission binds one profile; the profile resolves one approved prompt
release. Any CLI selection for qualification or operator work must be checked
against that same binding and cannot rewrite an in-flight run.

## Decision

Do not add a generic config reader or per-job environment overrides yet.
Proceed only after the four-role field inventory and API durable-binding
location are frozen, then implement the explicit exact-Natal/live
compatibility profile first with provider-free fail-closed tests.
