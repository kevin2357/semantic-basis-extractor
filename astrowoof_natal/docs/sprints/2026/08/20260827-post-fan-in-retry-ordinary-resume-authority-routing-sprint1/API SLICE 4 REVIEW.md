# API Slice 4 Review — Public Post-Fan-In Qualification Fixture

Date: 2026-08-27  
Disposition: **one correction required before approval**

## What is good

The new component has the right public boundary:

- packaged fixture, schema, Python reader/validator, and CLI;
- closed receipt with fixture digest, package identity, ordered public phase
  evidence, endpoint evidence, safety totals, and privacy declarations;
- no raw native state, provider IDs/payloads, workspace paths, prompts, or retained
  QA data in the public output;
- a scoped endpoint of `detached_provider_pending`, correctly not claiming
  API-owned persistence or reader delivery; and
- actual provider-free use of reconciliation, lifecycle inspection, local-work
  consumption, ordinary-v2 request/grant/intent/dispatch, and exact replay.

The API handoff is also correctly scoped: Sprint 54 consumes the installed surface
and owns persistence, one-slot fairness, stale worker handling, and reader delivery.

The Slice 4 targeted tests passed locally (with one expected optional `jsonschema`
skip).

## Required correction: reproducible receipt evidence

The fixture digest is stable, but the receipt is currently **not** stable across two
identical provider-free invocations. I ran the public runner twice from the same
source runtime and observed:

```text
same_receipt=False
same_phase_digests=False
all seven phase evidence digests differ
endpoint evidence digest differs
```

The likely cause is the random `TemporaryDirectory` root flowing into a native
inspection/snapshot value (the materialized workspace records an absolute logical
root), then being hashed as phase/endpoint evidence. This does not expose that path
in the public receipt, but it means the content-addressed receipt cannot serve as a
reproducible installed qualification identity.

Please correct this by ensuring the evidence values used for public phase and
endpoint digests are canonicalized independently of ephemeral filesystem paths, or
by materializing under a deterministic logical root using the supported test/runtime
mechanism. Do not weaken the privacy boundary or hash private `run.json` directly.

Add a regression test that calls `run_post_fan_in_retry_qualification()` twice in
the same package/version context and requires equal phase evidence, endpoint
evidence, and `receipt_sha256`.

Once that is green, this is approved for Slice 5 installed-wheel qualification.
