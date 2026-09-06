# Evidence

## Immutable publication

- Annotated tag `astrowoof-natal-authoring-v0.4.51` peels remotely to the exact
  approved release-lock commit
  `3b19a08fa4fa9d166272d1bf562b7a11877664c6`.
- GitHub Release ID: `383654277`; published `2026-09-06T16:54:29Z`.
- Wheel asset ID `547435197`: 1,228,560 bytes; GitHub digest and fresh-download
  SHA-256 both equal
  `ba39020b6d7f37ab422c99766839067603127d104ea15cde44b7e53e10491b6d`.
- Checksum asset ID `547435198`: 116 bytes; SHA-256
  `2360fe58763baca90506822976d8615175a4a40e783a6f0269bc7a40b843e16e`.
- The freshly downloaded manifest names and matches the downloaded wheel.
- QA deployment was not performed and remains a separate reviewed API action.

## Release-lock verification

- Release-lock commit:
  `3b19a08fa4fa9d166272d1bf562b7a11877664c6`.
- Two clean exports of that commit, using the recorded epoch `1788712494`,
  reproduced the candidate exactly: 1,228,560 bytes, 269 members, SHA-256
  `ba39020b6d7f37ab422c99766839067603127d104ea15cde44b7e53e10491b6d`.
- Reinstallation from the release-lock wheel passed `pip check`, reported SBE
  `0.4.51` with SPC `0.11.1` from isolated `site-packages`, and retained both
  packaged structured-log resources.
- Generic smoke and all four public qualification artifacts were byte-identical
  to the first installed qualification.
- `git diff --check` is clean. One unrelated API-authored fairness review file
  remains modified in the shared working tree and is excluded from the release
  commit and candidate artifact.
- Tag, publication, and deployment have not occurred.

## Slice 6 — regression and release preparation

- Candidate identity was frozen at `0.4.51` before release-bound testing.
- The release-derived providerless-denial fixture was aligned to `0.4.51` and
  its canonical receipt hash recomputed before the broad suite.
- Focused logging, contract, execution-event, trace, reporter, and
  release-derived-fixture matrix: 60 passed, 3 expected optional-schema skips
  in 16.109 seconds.
- Broad/full repository suite: 1,076 passed, 56 expected skips in 1,095.939
  seconds under Windows Python 3.12.14.
- Source-mode traces reported the installed distribution metadata (`0.4.50`),
  as expected from `importlib.metadata`; the clean installed-wheel gate must
  prove runtime version `0.4.51` from `site-packages`.
- Artifact-source commit `527a74c1289e8ace6909e780d662e69b346691a9`
  produced two byte-identical clean-export wheels using epoch `1788712494`:
  1,228,560 bytes, 269 members, SHA-256
  `ba39020b6d7f37ab422c99766839067603127d104ea15cde44b7e53e10491b6d`.
- One intervening build accidentally targeted the dirty repository root rather
  than its clean export. It differed and was explicitly disqualified; it is not
  part of the reproducibility pair or release candidate.
- Clean installed qualification proved SBE `0.4.51`, SPC `0.11.1`, `pip check`,
  packaged log schema/catalog, generic release smoke, trace observability,
  mixed-log reporting, decision-evidence observability, and providerless-denial
  qualification.
- No full-suite rerun is pending and no post-suite runtime/schema/validator/test
  correction has occurred.

## Slice 5 — production-boundary and API relay qualification

- API reconciliation relays a closed `astrowoof.sbe_worker_log.v1` stderr
  record verbatim while keeping authoritative reconciliation stdout private to
  its parser.
- Ordinary resume and constrained-v2 dispatch inherit diagnostic stderr only
  when event streaming is enabled; their disabled routes intentionally suppress
  it. Their authoritative JSONL/output-file transports remain separate.
- A structured application record cannot satisfy the terminal command-result
  discriminator.
- The privacy fixture proves an already-sanitized SBE record remains free of
  its pre-sanitization sentinel after raw relay and bounded-tail capture. It
  does not claim API-side generic redaction.
- API focused result: 37 passed. The test/docs-only qualification is committed
  as API revision `fa6a359`; its environment had SBE 0.4.50 installed and its
  fixture explicitly models the new v1 log contract.
- No provider, R2, QA database, retained workspace, deployment, or
  configuration access occurred.

## Slice 4 — dual-format reporter migration

- Recognized, validated SBE v1 JSON takes precedence over pipe parsing.
- Native JSON event/correlation/payload fields are used directly; message prose
  cannot override them.
- Mixed pipe/JSON, Render prefix, chronological normalization, exact duplicate
  accounting, malformed/truncated JSON, foreign JSON, historical pipe, and
  privacy-boundary fixtures pass.
- Exact duplicates remain visible but their later line numbers are reported.
- Focused combined matrix: 56 passed, 2 expected optional-schema skips.

## Slice 3 — high-value decision-point adoption

- Existing bounded workspace, state, lifecycle decision, optional-stage,
  validation, publication, finalization, and CLI-exit adapters now emit explicit
  event names and closed payloads.
- Lifecycle decision records distinguish `positive_permission` from branch,
  outcome, and capacity labels.
- Missing identities remain null; record-level correlation can augment bound
  context but is never recovered from message prose.
- The reporter has a minimal validated v1 bridge so default JSON output does not
  break the existing end-to-end trace regression; full migration hardening
  remains Slice 4.
- Focused trace/qualification/formatter/contract/event/reporter matrix:
  52 passed, 2 expected optional-schema skips.
- No API-relay visibility claim is made before Slice 5's route matrix.

## Slice 2 — formatter and context implementation

- The configured SBE application handler now emits one closed JSON object per
  stderr line; stdout and execution-event transports remain separate.
- Context now distinguishes caller-supplied API run, native run, subject,
  invocation, paid action, provider operation, and checkpoint object IDs.
- Existing `run_id=` bindings remain a compatibility alias for native run ID;
  no API identity is inferred.
- Sanitized messages retain `✨🐶`; exceptions exclude raw traceback and use
  the bounded sanitized representation.
- Invalid event extras produce one valid nonrecursive fallback record and do
  not raise through the logging call.
- Focused formatter/contract/event/reporter tests: 33 passed.
- High-value helpers intentionally remain `application_message` until Slice 3
  supplies their cataloged payloads explicitly.

## Slice 1 — structured record/privacy contract

- Added packaged closed envelope schema
  `sbe-worker-log.v1.schema.json`.
- Added packaged closed payload vocabulary
  `sbe-worker-log-event-catalog.v1.json`.
- Added a reader/validator enforcing exact keys, event-specific payload fields,
  bounded JSON values, nullable correlation, sanitized exception shape, and
  privacy sentinels.
- Recorded the invocation-specific API stderr relay matrix; reconciliation is
  verbatim, while ordinary resume/v2 visibility depends on event-stream
  configuration.
- Focused contract + existing logging/event/reporter tests: 29 passed.
- Runtime formatter, stdout, execution-event JSONL, provider I/O, and native
  state remain unchanged.

## Current gate

Slices 0–6 and immutable `0.4.51` publication are complete. Only separate
consumer intake/deployment work remains.

## Source findings

- One shared application formatter emits the pipe-delimited stderr records.
- Nine public CLI/configuration paths use the shared logging arguments.
- Approximately 169 ordinary logging calls exist in the authoring package.
- Four context variables currently bind host, native run, invocation, and native
  state.
- Typed execution events already use JSON envelopes and isolated sinks.
- Seven bounded observability helpers compute structured values before
  flattening them into messages.
- The run reporter currently reparses pipe messages with a boundary-event set
  and safe-field allowlist.

## Safety characterization

- Ordinary application logs use stderr and do not contaminate command stdout.
- Ordinary application records are distinct from execution-event envelopes.
- No provider, R2, QA, API database, deployment, or retained workspace was
  accessed or mutated.
