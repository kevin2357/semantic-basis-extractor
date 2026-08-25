# Sprint Log

## 2026-08-25 — Full saunter plan prepared

Created as the SBE companion to API Sprint 45 after fresh QA external-authority
v2 invocations returned `ambiguous_submission`. No implementation, provider
activity, retained-run mutation, or release occurred.

Expanded the initial skeleton into a complete five-waypoint saunter plan after
tracing the current production CLI and dispatcher boundary. The current
hypothesis is now explicit: `CALL_ENTERED` is persisted before the callback
performs local payload resolution and provider setup, so deterministic local
failures can be conservatively but incorrectly collapsed into provider ambiguity.

The plan requires evidence-based execution phases rather than exception-type
classification, strict public outcomes and joins, provider-free failure
injection, installed-wheel qualification, and four joint review checkpoints.
Implementation remains paused before Scenic Waypoint 0 pending owner/API review.

## 2026-08-25 — Plan approved; Scenic Waypoint 0 opened

Owner and API approved the saunter direction. API decisions incorporated:

- use a fresh closed command-result schema version;
- make `pre_provider_refusal` an explicit outcome;
- use a closed provider-I/O/custody assertion rather than a boolean;
- preserve API ownership of reservation/admission identity and policy;
- retain all review checkpoints; and
- publish the complete requested sanitized consumer-fixture matrix.

Scenic Waypoint 0 is authorized to begin provider-free boundary tracing and
failure injection. No retained QA or real provider work is authorized.

## 2026-08-25 — Scenic Waypoint 0 initial reproduction

Added a production-shaped provider-free regression that separates entry into the
dispatch callback from entry into the scripted provider transport. Removing the
exact prepared payload causes local request materialization to fail after the
current durable `CALL_ENTERED` checkpoint. The transport call count remains zero,
but 0.4.22 returns `ambiguous_submission`, persists
`AMBIGUOUS_PROVIDER_SUBMISSION`, and reports provider I/O as performed.

The companion before-entry test proves the immediately preceding failure point
remains replayable and makes zero callback/provider calls. The full boundary
inventory remains in progress before Waffle Checkpoint 0.

## 2026-08-25 — Scenic Waypoint 0 complete

Completed the boundary inventory and froze the public CLI reproduction. The
recommended correction is a prepared-create value built before the fence plus a
transport-only operation after it. Classification is thereby determined by the
durable execution phase, never by exception class.

Recommended versioning is provider dispatch result v3 embedded by command result
v2. Historical v2 ambiguity remains review-only.

Focused provider-free gate: 25 tests passed. No source/runtime behavior changed.
Paused at Waffle Checkpoint 0 for API review before schemas or implementation.
