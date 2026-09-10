# Sprint — Operator-disposition assessment native diagnostics

## Goal

Make failures of SBE's in-process, read-only operator-disposition assessment diagnosable by phase and bounded reason while preserving native authority, host-process independence, and fail-closed behavior.

## Slice 0 — Reproduce and inventory

**Status: complete, pending API review.** The provider-free reproduction and logging ruling are recorded in `SLICE 0 - IN-PROCESS LOGGING AND RESTORE-PATH REPRODUCTION.md`.

Before changing the contract:

- identify the exact exception persisted for Baskerville if it is available through already-authorized evidence;
- build a provider-free fixture or restored-shape reproduction for that failure without requiring additional live workspace access;
- map every exception boundary in `read_operator_disposition_assessment()` and its directly called helpers;
- distinguish expected unsupported/inconsistent native states from malformed or inaccessible workspaces; and
- inventory how API invokes the installed reader and translates errors;
- run the reader in an operator-runner-equivalent in-process host with the current logging configuration;
- test the existing SBE `configure_logging()`/structured formatter as the primary capture path; and
- determine whether a host bootstrap is sufficient to place valid `astrowoof.sbe_worker_log.v1` records on captured stderr without duplication.

No retained-workspace access is authorized by this plan.

**Gate:** one precise reproduced failure or a documented evidence limitation, an agreed phase/reason matrix, and a concrete ruling on reuse of normal SBE sparkle logging. Do not design a callback before this ruling.

## Slice 1 — Extend the existing sparkle-log vocabulary

**Status: implemented, pending review.** Three bounded events were added to the existing worker-log catalog.

Define minimal assessment events in the existing SBE worker-log catalog. Candidate fields:

- schema version;
- phase;
- outcome;
- reason code;
- native run ID when proven;
- state revision when proven;
- lifecycle schema when proven;
- snapshot/checkpoint digests when already safely established;
- custody class and quarantine posture only after classification; and
- fallback-used boolean where relevant.

Preserve the existing one-argument reader call. Decide which process owns logging bootstrap and prove that configuring the existing formatter does not disturb API execution-event stdout or duplicate host records. A callback or typed public diagnostic error is a fallback requiring a separately recorded justification.

**Gate:** SBE and API review approve event names, field closure, logging bootstrap ownership, and observation-failure behavior.

## Slice 2 — Implement bounded native observations

**Status: implemented, pending review.** Entry, safe preflight fingerprint, completion, and phase/reason failure records are covered provider-free.

Instrument only the meaningful assessment boundaries:

- workspace state loaded;
- initial snapshot validation completed/refused;
- native read fence established/not established;
- retry-lineage inspection completed or v0.5 fallback selected;
- lifecycle normalization completed/refused;
- terminal evidence resolved/refused;
- custody classification completed; and
- final snapshot revalidation and assessment validation completed/refused.

Observation uses ordinary SBE log calls and must be demonstrably non-mutating and provider-free.

**Gate:** focused tests prove phase order, safe field closure, correct final failure classification, and valid structured formatting in CLI and in-process host shapes.

## Slice 3 — API companion intake

**Status: awaiting API review/implementation.** No SBE callback or alternate transport is needed by current evidence.

Coordinate the smallest API-side patch needed to configure/carry SBE's existing structured logs in the operator-runner process. API may separately emit its own orchestration-level claim, restore, refusal, and completion execution events.

SBE records explain native assessment progress; API records explain durable request disposition. Neither layer impersonates the other.

**Gate:** installed-wheel API consumer tests prove native sparkle records survive the in-process path without subprocess capture, while API execution-event output remains valid.

## Slice 4 — Package and provider-free qualification

Run focused contract tests, public fixture checks, manifest checks, broad tests proportional to the additive public surface, and installed-wheel/API consumer qualification. Follow the normal SBE release playbook if a package release is required.

**Gate:** exact wheel identity is retained and independently consumable; provider operations remain zero.

## Slice 5 — Bounded live proof

After separately approved deployment and access boundaries, exercise one provider-free assessment request and confirm Better Stack exposes both API orchestration and bounded native assessment phases.

A refusal is an acceptable proof if its native phase and reason are visible and durable diagnostics agree. Quarantine mutation is not required and needs separate explicit authorization.

## Out of scope

- Changing quarantine eligibility or custody classification.
- Reading arbitrary workspace files for diagnostics.
- Adding provider access to the operator runner.
- Repairing Baskerville's provider-reconciliation JSONL consumer mismatch.
- Treating logs as native authorization or persistence.
