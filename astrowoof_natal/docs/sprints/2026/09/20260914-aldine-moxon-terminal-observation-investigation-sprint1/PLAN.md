# Plan — Aldine / Moxon Terminal Observation Investigation

## Working classification

**Final SBE disposition:** investigation complete. Exact-workspace
reproduction clears the SBE reader, root validation, capture builder, API
envelope builder, and deterministic request preflight. Remaining work is owned
by API's live observer/runtime boundary; no SBE implementation or release is
required.

There were two opening questions. Corrected logs now substantially answer the
first and isolate the second:

1. Aldine legitimately reached terminal review after six accepted initial
   provider results and two rejected polish attempts. No eligible continuation
   is visible at closure.
2. Why did both terminal routes reach API's observer but return local
   `capture_or_preflight` unavailability after the Sprint 97 root correction?

The original supplied export cannot answer either question. Its 1,000 records
stop more than an hour before the reported terminal events and contain none of
the six frozen Aldine/Moxon identities. Eight replacement unfiltered segments
now provide complete uncapped coverage through both closeouts.

## Slice 0 — Repair the evidence boundary

**Status: complete.** Correct unfiltered segmented exports were supplied and
validated.

- Retain the supplied export only as hash-verified truncation evidence.
- Export later worker logs using server-side filters for the exact API run,
  native run, or SBE job identities where supported.
- Otherwise divide `19:08Z–20:45Z` into short non-overlapping windows whose
  individual record counts remain below Render's 1,000-record cap.
- Record each file's requested and observed time bounds, byte size, SHA-256,
  outer-record count, parseable-event count, and per-target identity counts.
- Require coverage through both terminal observer completions and closeout.
- Cross-check only lifecycle/custody facts against API's authoritative database;
  worker logs remain progress evidence.

**Exit:** complete, non-truncated per-run event sets exist for Aldine and Moxon,
or an exact missing interval is documented before deeper interpretation.

## Slice 1 — Aldine fast terminal-review classification

**Status: complete from corrected log evidence.** Aldine exhausted two bounded
polish attempts after failed final QA; no eligible continuation remained.

- Reconstruct every Aldine SBE attempt by attempt ID, execution branch,
  checkpoint generation, invocation, result, receipt, and provider dependency
  count.
- Separate six initial submissions from later worker attempts; neither count
  may be used as a proxy for the other.
- Trace all six exact provider identities through retrieval, acceptance, pass
  QA, fan-in/final QA, and optional-stage eligibility.
- Identify the exact terminal result schema, route, custody finality, action
  dispositions, terminal command, cause/reason, and review evidence.
- Prove whether any prepared or eligible polish/critic/candidate authority
  remained live when `retain_for_review` was selected.
- Classify the outcome as legitimate zero-action/final-review closure, valid
  failed-QA closure after exhausted authority, or premature native closure.

**Exit:** Aldine's terminal review is explained by exact native evidence, with
no provider retry, latest-result discovery, or workspace mutation.

## Slice 2 — Post-rollout observer identity and phase joins

**Status: complete to the retained-evidence boundary.** Exact IDs and stable
native roots are proven; current API telemetry collapses the first failing
subphase and omits three live root identities, so further localization is
gated on Slice 3.

Run independently for Aldine's review result and Moxon's delivery result.

- Bind the exact terminal invocation/result/receipt to the API attempt that
  emitted `editorial.observation.completed`.
- Verify deployed API/SBE release identities and establish that Sprint 97's
  root correction was present for both fresh workspaces.
- Join four root identities without reconstruction:
  1. SBE `run.json` durable logical root;
  2. checkpoint `logical_restore_path`;
  3. registered worker allocation/current restore target;
  4. the workspace actually passed to `observe_terminal()`.
- Treat initial terminal handling and terminal-publication retry as distinct
  paths. Prove exact result-ID and root carry-forward across each.
- Localize `capture_or_preflight` among exact native read, runtime evidence,
  typed capture-status fallback, packet construction, envelope construction,
  and API request preflight. Record only bounded phase and exception class/
  fingerprint—never authored prose, provider bodies, secrets, or raw packets.
- For Aldine, verify the v0.2/v0.3 terminal-review capture contract separately
  from Moxon's v0.1 accepted-delivery contract.

**Exit:** each observer failure has a first proven local boundary and owner.

## Slice 3 — Conditional exact-workspace reproduction

**Status: complete.** Both exact archives were retrieved within the authorized
budget and reproduced at their contract-bound roots. Deterministic SBE capture,
API envelope construction, and request preflight do not reproduce the shared
live failure. Stop for joint review before API runtime diagnostics or changes.

**Review and owner-authorization gate.** Run only if complete logs and source
joins cannot classify a failure.

- Obtain hash-verified immutable checkpoint coordinates from API persistence;
  do not discover latest results or workspaces.
- With separate owner authorization, perform at most one conditional HEAD and
  one bounded GET per named checkpoint.
- Keep archives/restores outside Git and verify size, archive SHA-256, inventory
  identity, native durable root, and exact terminal result ID.
- Reuse the hardened reproduction pattern proven in the Garamond/Quill sprint:
  network disabled, read-only filesystem and mounts, all capabilities dropped,
  and `no-new-privileges`.
- Exercise each archive at the API-observed root and its contract-bound native
  root, reporting only safe identities, counts, digests, phases, and bounded
  exception fingerprints.

**Exit:** retained bytes reproduce or exclude the suspected root/capture path
without provider activity or native mutation.

## Slice 4 — Provider-free correction fence

**Status: transferred to API.** API accepted ownership of the remaining live
runtime diagnostic/refactoring work. This sprint authorizes no SBE correction,
version bump, release, further retained-workspace access, or live action.

- Assign each issue only at its first proven boundary; Aldine's terminal reason
  and shared observer behavior may have different owners.
- Build the smallest provider-free regression for each confirmed defect.
- Preserve exact result and workspace identity; never add run-wide/latest
  discovery or weaken SBE's stable-root validation.
- Observation remains post-authoritative and best effort: failure cannot alter
  terminal state, custody, spend, cleanup, retry, or capacity release.
- Check test-manifest and Alloy impact explicitly. Root carry-forward or
  observability changes should not alter the native lifecycle model; any native
  selection/eligibility change requires separate Alloy review.
- Stop for joint API/SBE review before runtime code, versioning, release,
  deployment, retained-workspace access, or live-state action.

## Investigation boundaries

- No provider call, retry, resume, reconciliation, recovery execution, QA
  mutation, Better Stack write, or run reinterpretation is authorized.
- No R2 access is authorized by this opening plan.
- Raw exports and any future restored workspace remain outside Git.
- Do not retain or publish authored decks, prompts, reports, provider payloads,
  packet bodies, secrets, or absolute private workspace paths.
