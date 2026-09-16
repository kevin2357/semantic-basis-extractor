# Slice 4A Correction — Supervision Capability Then Force Fence

## Discovery

The first packaged candidate encoded an impossible causal order. Its immutable
pre-launch envelope required an already-admitted operator `force_fence`, but
API can admit that fence only after an operator acts against an already-running
lease. Backdating or synthesizing that authority would invalidate the very
boundary this protocol is intended to preserve.

## Corrected chronology

1. Before `Popen`, API creates one immutable, request-isolated supervision
   capability and binds its ID and digest into the launch envelope.
2. The capability grants no stop, revocation, release, provider, workspace, or
   settlement authority. It only anchors the channel through which a later
   exact request may be published and read.
3. After launch, an operator may admit an immutable force fence for the exact
   running lease and supervision invocation.
4. API publishes one suspension request that joins both the pre-launch
   capability and the later force fence.
5. SBE validates that complete request at a supported native safe point and
   publishes immutable result, receipt, and command-result documents that bind
   both identities independently.

## Closed-document consequences

- `native_supervision_invocation.v1` carries
  `supervision_capability_id` and `supervision_capability_sha256`; force-fence
  fields are forbidden by the closed envelope schema.
- `native_suspension_request.v1` repeats the capability join and adds
  `force_fence_id` and `force_fence_sha256`.
- The result, receipt, and command result carry both pairs. A mutation of
  either pair cannot be repaired by recomputing only downstream digests.
- Request conflict remains invocation-wide. The split does not authorize a
  second request, weaken ordinary-result precedence, or grant SBE API resource
  release authority.

## Qualification boundary

The prospective `0.4.65` candidate and its wheel hash are superseded and were
never released. The correction will use a fresh prospective `0.4.66` version
to prevent ambiguous same-version wheel substitution. API Slice 3B must bind
only the corrected wheel and must independently validate the real force-fence
fact before accepting the request/result chain.
