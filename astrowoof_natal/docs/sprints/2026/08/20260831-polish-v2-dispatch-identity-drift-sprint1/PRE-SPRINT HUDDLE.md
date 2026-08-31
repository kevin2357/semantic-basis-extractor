# Pre-sprint huddle — polish v2 dispatch identity drift

## Initial reading

The retained incident presents two related-looking facts that must not be
collapsed prematurely:

1. several external-authority request digests appear in the trace around one
   polish handoff; and
2. the provider-capable v2 command refuses before provider I/O with native
   `action_state_or_custody_mismatch`, surfaced as `authorization_mismatch`.

An external-authority request is immutable once materialized, but repeated
inspection can legitimately produce distinct request objects if the underlying
checkpoint basis or ordered action inventory changed. The investigation must
therefore determine whether the trace contains one object whose bytes changed,
several objects derived from different observations, or misleading log labels.

The current executor also performs several distinct checks. Before applying the
grant it reads native state under the lifecycle writer, validates the workspace
snapshot, requires every selected action to be providerless `PREPARED` work,
rebuilds the current temporal inspection at the supplied observation time, joins
the request to that inspection, requires exact inspection equality, and then
validates the grant and authorization documents. A refusal at this boundary may
be caused by native action/custody state even when API's durable action and grant
records are mutually coherent.

## Working hypotheses, not conclusions

- **Multiple-observation hypothesis:** `07300…`, `c5ac68…`, and `a838af…`
  are separate request projections from distinct basis/inventory observations;
  the request did not mutate.
- **Native-action-posture hypothesis:** the polish action is not providerless
  `PREPARED` at writer revalidation because an earlier continuation or legacy
  authorization path changed it without publishing the expected v2 intent.
- **Stale-input join hypothesis:** the command receives an internally valid
  request/grant pair but an inspection or authorization document from another
  observation, causing strict current-state revalidation to refuse.
- **Creative-retry contamination hypothesis:** the post-reconciliation
  `authoring_attempt_ambiguous` transition changes native lineage or custody in
  a way that affects polish preparation. This may be causal, adjacent, or an
  independent defect.
- **Diagnostic-label hypothesis:** one or more trace messages label a payload
  digest as an external-authority request digest, making distinct identities
  appear comparable when they are not.

No hypothesis is accepted until joined to protected native bytes, public
contract bytes, and the API's frozen admission/grant evidence.

## Safety posture

- Delerium remains suspended and is not a recovery target.
- No provider call, reconciliation, resume, denial, repair, or new authority is
  authorized.
- Protected storage access is exact-object `HEAD`/`GET` only, beginning with
  generation 11. Generation 10 is conditional on a documented differential
  need.
- Logs are diagnostic evidence, never authority.
- API-owned reservation, lease, and global admission facts are not inferred by
  SBE.

## Desired result

Produce one provenance-backed causal statement and one provider-free regression
through the supported production boundary. If retained evidence cannot select a
cause, record the evidence ceiling and preserve the competing explanations. Any
runtime correction must repair the general identity/state seam rather than
special-case this retained run.

## Offline-inspector tooling decision

A separate planned sprint already exists for promoting the repeated retained-
workspace readers into `astrowoof-checkpoint-inspect`. Its proper scope is much
larger than copying the current one-off parser: bounded archive validation,
contained extraction, declared-member verification, native snapshot/journal/
result/receipt joins, closed sanitized output, version compatibility, privacy
tests, and installed packaging.

This investigation will therefore not absorb that entire tooling sprint. It
will:

- reuse or narrowly adapt the existing incident-local read-only parser;
- keep remote download authorization separate from native inspection;
- record every missing/reusable validator encountered here;
- add Delerium's request/inspection/grant/action-identity projections to the
  dedicated inspector requirements; and
- reconsider a small shared helper only if Slice 0 proves it can be extracted
  without creating a partial, misleading public inspector.

The goal is to avoid both extremes: another disposable parser with no lessons
carried forward, and a forensic incident blocked behind a new tooling release.
