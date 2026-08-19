# Response Retrieval Observability Patch Sprint 1 Plan

Date: 2026-08-19  
Status: implementation committed; 0.4.10 release qualification active  
Starting release: SBE 0.4.9  
Proposed release: SBE 0.4.10 after separate release authorization

## Purpose

Make interactive Response reconciliation failures diagnosable without weakening
provider custody, lifecycle, snapshot, or spend-authority guarantees. Add a
read-only installed-wheel probe that exercises the same configured Response GET
transport against one existing provider Response ID without opening or mutating an
SBE run.

This is intentionally a fast, narrow patch sprint. It does not redesign provider
reconciliation, add retries, alter backoff, change public lifecycle states, or run
paid authoring qualification.

## Problem statement

The concurrent Response retrieval boundary currently catches every exception and
retains only the generic lifecycle outcome `transport_warning`. Apart from the
separately recognized provider-identity mismatch, HTTP failures, timeouts,
malformed responses, TLS/configuration errors, and other transport exceptions lose
the sanitized facts needed to diagnose a QA run.

## Frozen safety boundary

- Existing lifecycle outcomes and custody semantics remain authoritative and
  unchanged: `completed`, `pending`, `transport_warning`, and
  `identity_conflict` retain their current meanings.
- Diagnostics are durable operational evidence, not provider truth, spend
  settlement, authorization, retry permission, delivery authority, or proof that
  an operation does or does not exist.
- Provider response IDs and native action/run IDs may be recorded. Credentials,
  authorization headers, cookies, prompt/output bodies, raw HTTP bodies, and
  arbitrary exception representations must never be recorded or printed.
- Endpoint identity is the fixed method and sanitized route shape
  `GET /responses/{response_id}` plus a safe configured-host identity if the
  transport exposes one. It must contain no query secrets, userinfo, or headers.
- Error text passes through one closed sanitizer with bounded length. Known secret
  shapes and the configured credential are redacted; an error fingerprint is
  derived from the sanitized classification/text, never raw secret-bearing bytes.
- HTTP status and provider request ID are best-effort optional facts extracted
  from supported exception/response metadata. Their absence remains explicit.
- Reconciliation-attempt recording must be included in the normal serialized
  state/snapshot publication protocol. Diagnostic-write failure must fail closed
  rather than silently claim complete durable observability.
- The probe performs one retrieval only. It accepts no run directory, cannot
  submit/cancel/delete provider work, does not consume spend authority, and does
  not mutate native state.

## Proposed public surface

- A closed, versioned reconciliation-attempt diagnostic schema and validator.
- A durable per-action attempt artifact under the existing lifecycle provider-
  reconciliation evidence boundary, with deterministic attempt identity and
  linkage from the reconciliation cycle evidence.
- A public Python function for a single read-only Response inspection.
- Installed-wheel CLI, provisionally:

  ```console
  astrowoof-inspect-response --response-id resp_...
  ```

  It uses the same supported OpenAI Response retrieval/configuration construction
  as reconciliation and emits one sanitized JSON result to stdout or an explicit
  output path outside any native run workspace.

The exact contract identity, artifact filename, optional-field representation,
and CLI spelling will be frozen in Slice 0 before implementation.

## Slices

### Slice 0 — Contract and redaction freeze

Define the closed diagnostic fields and outcome vocabulary:

- native run ID, action ID, provider Response ID;
- endpoint/method identity;
- attempt start, finish, and measured duration;
- HTTP status and provider request ID when safely available;
- normalized provider status for returned Responses;
- exception class, sanitized bounded message, and stable error fingerprint;
- outcome: `completed`, `pending`, `transport_warning`, or
  `identity_conflict`; and
- explicit null/absence behavior for unavailable facts.

Define deterministic attempt identity, ordering under parallel retrieval, cycle
linkage, sanitizer rules, supported HTTP metadata extraction, and the probe's
read-only/configuration boundary. Confirm whether malformed returned objects are
classified as transport warnings while returned ID mismatch remains identity
conflict.

Gate: contract examples and threat/redaction table reviewed; no production code
changed. Pause for Kevin/API review only if the proposed public shape departs
materially from this plan.

### Slice 1 — Durable reconciliation diagnostics

Instrument the existing concurrent Response retrieval path. Capture wall-clock
timing around each GET, normalize successful/pending/provider-error results, retain
sanitized exception metadata, write per-action attempt artifacts in deterministic
action order, and bind them into the cycle evidence before normal state/snapshot
publication.

Do not serialize native mutation from worker threads: external retrieval remains
parallel; diagnostic reduction and all workspace writes remain single-writer.

Targeted tests:

- completed Response retains diagnostics and permits existing fan-in;
- `in_progress` remains provider-pending;
- 401, 404, 429, timeout, malformed return, and Response-ID mismatch retain the
  exact expected structured diagnostic;
- secrets/raw response bodies are absent from artifacts;
- parallel completion order does not destabilize durable action ordering; and
- diagnostics survive a fresh-reader/snapshot validation boundary.

Gate: focused reconciliation/lifecycle tests, schema validation, snapshot test,
`git diff --check`, compact slice evidence, commit/push approval.

### Slice 2 — Read-only provider probe

Implement the Python API and `astrowoof-inspect-response` command using the same
provider transport/configuration factory and timeout policy as reconciliation.
Return the same sanitized diagnostic contract without creating or changing an SBE
workspace.

Targeted tests:

- completed and pending scripted Responses;
- 401/404/429/timeout/malformed/identity-conflict diagnostics;
- stdout and output-file behavior;
- rejection of unsupported arguments and output locations that resolve inside a
  recognized native run workspace;
- secret and raw-body redaction; and
- proof that only one GET occurs and no create/cancel/delete method is reachable.

Gate: focused API/CLI tests, entry-point/package inspection, `git diff --check`,
compact slice evidence, commit/push approval.

### Slice 3 — Installed-wheel qualification and handoff

Build a non-published candidate and prove the installed CLI with a provider-free
scripted transport or supported injection seam. Confirm packaged schema/API/entry
point presence and unchanged lifecycle outcome semantics. Publish a concise API/QA
handoff with command examples, field interpretation, redaction guarantees, and the
warning that diagnostics do not authorize retry or reservation release.

Run only proportionate gates:

- all new focused tests;
- directly affected reconciliation, lifecycle-contract, snapshot, CLI, and
  packaging tests;
- installed-wheel provider-free smoke on Windows and Linux if readily available;
- no live provider call and no paid spend; and
- full-suite expansion only if focused work reveals shared-contract breakage.

Gate: clean diff, compact manifest/evidence, consumer review if requested, then
pause for explicit version/tag/publication authorization.

## Exit criteria

- A failed Response GET leaves enough durable, sanitized evidence to distinguish
  common HTTP/configuration/timeout/malformed/identity cases.
- Successful and pending retrieval behavior, concurrency, custody, backoff, and
  fan-in semantics are unchanged.
- The installed-wheel probe performs exactly one read-only GET through the same
  supported transport/configuration path and never mutates a run.
- Schemas and examples are closed-world validated and packaged.
- Targeted source and installed-wheel evidence passes with zero provider
  submissions and zero spend.
- Release work occurs only after separate explicit authorization.

## Explicitly out of scope

- New lifecycle states or automatic retry decisions.
- Changes to retrieval concurrency/backoff/time limits.
- Batch retrieval diagnostics beyond shared sanitizer/helper reuse required to
  avoid inconsistent handling.
- Provider submission, cancellation, deletion, or response repair tooling.
- API database/logging changes or global spend/reservation policy.
- Broad full-route authoring qualification or paid tests.
