# Evidence

## Slice 6 — regression and release preparation

- Candidate identity was frozen at `0.4.51` before release-bound testing.
- The release-derived providerless-denial fixture was aligned to `0.4.51` and
  its canonical receipt hash recomputed before the broad suite.
- Focused logging, contract, execution-event, trace, reporter, and
  release-derived-fixture matrix: 60 passed, 3 expected optional-schema skips
  in 16.109 seconds.
- Broad/full repository suite: 1,076 passed, 56 expected skips in 1,095.939
  seconds under Windows Python 3.11.
- Source-mode traces reported the installed distribution metadata (`0.4.50`),
  as expected from `importlib.metadata`; the clean installed-wheel gate must
  prove runtime version `0.4.51` from `site-packages`.
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
- API focused result: 37 passed. The evidence was produced from the current
  API `main`-based working tree with test/docs-only uncommitted changes and SBE
  0.4.50 installed; it is not represented as an immutable API revision.
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

Slices 0–6 regression and documentation are complete. Reproducible builds and
clean installed-wheel qualification remain before the final release-review
boundary.

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
