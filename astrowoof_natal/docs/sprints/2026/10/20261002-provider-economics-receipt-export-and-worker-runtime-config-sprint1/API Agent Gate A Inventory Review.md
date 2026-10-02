# API Agent Gate A Inventory Review

## Decision

**Gate A is approved for provider-free implementation/design work, subject to
the constraints below.** The inventories are now detailed enough to freeze the
three boundary decisions without pretending that the four logical roles are
four independently launched services. This approval authorizes no provider
work, retained-workspace access, deployment, or environment mutation. Any
later paid qualification still requires an explicit cohort and cost-cap
approval.

## 1. Orbit economics: approved diagnosis boundary

The updated trace corrects the most important initial uncertainty. API source
confirms that supported sealed native-transition paths call
`ProviderEconomicsExportIngestionService.observe()` with the exact sealed
workspace and publication. That adapter loads accepted local tape
predecessors, calls SBE's public reader, fences returned native-run/snapshot
identity to the sealed publication, and sends valid revisions to immutable
ingress.

The remaining observability gap is also confirmed: `observe()` intentionally
catches every `SbeProviderContractError` and emits the one safe operational
disposition `sbe_export_unavailable`. It correctly preserves lifecycle
authority, but the resulting event cannot distinguish:

1. reader/snapshot/projection refusal;
2. export schema or revision validation failure;
3. sealed-publication identity mismatch; or
4. immutable-ingress/predecessor failure.

The next slice should add a bounded, allowlisted diagnostic phase/reason
classification at this boundary while retaining the existing non-fatal
`unavailable` outcome and privacy rules. It must not expose exception prose,
workspace paths, request data, or provider payloads. The provider-free exact
and bounded fixtures should drive each phase independently and prove that the
same safe classification reaches the normal operational event.

This remains an integration diagnostic—not grounds to add a remote SBE
publisher, catalog discovery, receipt reconstruction from API custody, or an
automatic retry that changes lifecycle state.

## 2. Processing profiles: approved architecture, with actual topology

The inventory is a substantial improvement because it accurately identifies
two real launch boundaries rather than treating four conceptual roles as four
separate service processes:

- AGF calculation and SPC projection run inside the deterministic-runtime
  executable.
- SBE workspace/lifecycle and closure/authoring behavior run in the SBE
  worker/semantic-closure executable.

`processing_profile.v1` should therefore be one canonical non-secret object
with a digest, but profile verification must occur at each *actual process
boundary* and at any durable handoff between logical stages. An implementation
does not need to invent four binaries or four independent configuration
fetches to satisfy the design goal.

API already persists useful adjacent evidence—generation-profile identity,
resolved-manifest SHA, compatibility identities, and native-run manifests.
It does not yet persist a processing-profile ID/digest that explicitly covers
the concrete SBE frozen arguments and route-specific AGF/SPC fragments. The
next implementation should extend the existing admission/manifest chain where
possible rather than create a parallel source of truth. API admission selects
one environment-allowlisted ID and expected digest before deterministic work;
the exact same binding is carried through every durable handoff.

The classification table is approved. In particular:

- paths, subject/birth inputs, checkpoints, grants, and authority documents
  are job evidence or custody inputs, never profile fields;
- keys, endpoints, worker roots, and executable locations remain deployment
  wiring/secrets;
- spend grants and reconciliation/terminal authority are not generic runtime
  configuration; and
- selection policy is independent of route and service level. Every supported
  route/service-level/policy tuple must be explicit; every other tuple fails
  closed.

The first implementation profile must be an exact-Natal/live compatibility
profile that makes today's implicit legacy policy explicit. A bounded profile
and an axis-aware experiment are later, independently admitted profiles—not
aliases obtained by toggling a Boolean or renaming an exact profile.

## 3. Prompt-release binding: approved precedence and provenance model

The provider-construction inventory is sufficient to freeze the model. A
profile binds one approved prompt release at admission. That release maps
applicable stages—initial, retry, polish, critic, and bounded where
compatible—to immutable prompt assets. Per-action provenance consists of the
release ID/version/digest, the selected component digest inventory, and the
fully rendered request digest. Prompt text and job-specific content remain in
the existing private custody paths and out of ordinary logs.

The precedence rule is approved:

1. new admission binds the profile and its compatible prompt release before
   the first provider action;
2. an explicit CLI selector can request an approved release for new
   local/qualification work only after the same route/profile/environment
   validation; and
3. persisted binding wins for retry, polish, resume, reconciliation, detached
   continuation, and external-authority recovery. A mismatch or missing
   installed asset fails closed.

Existing legacy workspaces keep their historical private rendered-request
recovery path. No synthetic backfill or retroactive release inference is
approved.

## Required provider-free implementation gates

Before a live prompt or profile experiment, the implementation must prove:

- canonical profile bytes/digest verification in both actual launch processes;
- exact legacy compatibility and explicit rejection of unsupported
  route/service-level/policy combinations;
- immutable persisted binding across resume, reconciliation, and recovery;
- package-installed prompt asset byte verification, including canonical
  UTF-8/LF handling;
- refusal before provider-action preparation for unknown, deprecated,
  wrong-environment, wrong-route, or digest-mismatched releases/profiles;
- action-level safe provenance for all provider-writing stages; and
- economics diagnostic phase classifications that preserve the existing
  lifecycle-nonfatal observation rule.

## API implementation note

The API companion sprint should now plan the minimal schema/manifest and
handoff extension needed to carry `processing_profile_id`,
`processing_profile_sha256`, and safe prompt-release provenance. It should
reuse the current generation-manifest and transition-ingress custody model,
not create a mutable profile/configuration lookup at worker runtime.
