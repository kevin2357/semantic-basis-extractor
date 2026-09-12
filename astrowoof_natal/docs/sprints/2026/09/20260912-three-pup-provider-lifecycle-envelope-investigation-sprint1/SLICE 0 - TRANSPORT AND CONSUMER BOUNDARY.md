# Slice 0 — Transport and Consumer Boundary

## Decision

Slice 0 proves a deterministic API reconciliation-stream consumer defect.
It does not show an SBE provider, lifecycle-selector, command-result, or
checkpoint defect.

The production API reconciliation route requests
`--events-stdout-jsonl`. SBE 0.4.59 consequently emits a closed mixed JSONL
stream containing diagnostic `sbe.execution_event.v1` records followed by the
authoritative `sbe.command_result.v1` record. The API consumer introduced in
`c1b4c3a` requires **every** record to be a command-result envelope and rejects
the first diagnostic record as `SBE reconciliation envelope is unsupported`.

No R2 read is needed to establish this boundary. The authorized generation-2
objects predate reconciliation and cannot reveal the subprocess stdout that
the API rejected.

## Frozen cohort timeline

Times below are America/Denver (MDT, UTC-06:00). The UTC source timestamps
remain in the bounded log export.

| Run | Initial claim | Initial checkpoint accepted | Reconciliation claim | Native reconciliation exit | API failure |
| --- | --- | --- | --- | --- | --- |
| Aldine Eclair | 02:04:55.905 | 02:05:50.063 | 02:06:05.209 | 02:06:10.408 | 02:06:46.714 |
| Ada Baklava | 02:06:46.798 | 02:07:41.710 | 02:07:56.803 | 02:08:04.640 | 02:08:38.544 |
| Baskerville Biscotti | 02:08:38.641 | 02:09:31.938 | 02:09:47.046 | 02:09:52.242 | 02:10:28.555 |

For every run:

1. initial-wave authority and six provider creates completed;
2. generation 2 was accepted and the allocation was released;
3. attempt 2 restored six `WAITING` actions with six provider identities;
4. the public selector chose due `provider_reconciliation_cycle`;
5. the due set reduced from four actions to two;
6. SBE published revision-12 `provider_pending` evidence and exited 3 with
   `detached_provider_pending`; and
7. after the API heartbeat loop observed process completion, its stdout parser
   rejected the mixed stream and terminal-failed the job.

The approximately 34–36 second interval between native exit and API failure is
consistent with the wrapper's heartbeat polling interval. It is not evidence
of additional provider work.

## Exact provider-free reproduction

The reproduction used:

- the API virtual environment's installed SBE 0.4.59 package;
- the real public reconciliation CLI path through `closure.main()`;
- one scripted GET-only provider adapter returning `in_progress`;
- the production API `_ReconciliationStreamCapture.reconciliation_output`
  parser; and
- no provider network, create, R2 access, or retained QA workspace.

The exact emitted envelope classes were:

| Ordinal | Schema | Type/name | Canonical SHA-256 |
| --- | --- | --- | --- |
| 1 | `sbe.execution_event.v1` | `execution_event` / `provider.reconciliation_observed` | `785803eb5bb03422ceef3bfd8ea77649e06501e81cee8b212841301adf3a00c1` |
| 2 | `sbe.execution_event.v1` | `execution_event` / `run.detached` | `dff13ac8cdfd7aa5ae31b2de712e2d2e9bef0772772fbd20e03a0579ee41ee02` |
| 3 | `sbe.execution_event.v1` | `execution_event` / `checkpoint.committed` | `58cb491836395d3b49e85df2a288b3bdb4f14dfa57fda65e1454c0e8ddfa50e0` |
| 4 | `sbe.execution_event.v1` | `execution_event` / `native.result_published` | `4689bfea04aa8f7ae475a5f0ed909c259dcf06e57984a61795bcf24cb6924b2e` |
| 5 | `sbe.command_result.v1` | `command_result` / `astrowoof.provider_reconciliation_cycle_result.v0.2` | `ff6154b6f32eb5cc019a6f1d5885f382a5a0ebe77be4003ee145be88f396108a` |

The command exited 3, made exactly one scripted `GET`, and emitted ordinary
outcome `detached_provider_pending`.

Production-parser results:

- complete five-record stream: rejected at ordinal 1 with the exact field
  error seen in QA;
- unchanged ordinal-5 command result by itself: accepted as
  `astrowoof.provider_reconciliation_cycle_result.v0.2` with
  `detached_provider_pending`.

This proves that the ordinary result is not malformed and that the failure
occurs before result-schema validation.

## Source and release provenance

- SBE's stdout execution-event sink dates to `b21f3331` (2026-08-15).
- SBE reconciliation event emission dates to `c109892c` (2026-08-17).
- SBE 0.4.59 is tag target `e5127caea466b12340472eee48b2563abfd68650`.
- API commit `c1b4c3a05ea6e5d128650a98ed4a3d18b493320b` (2026-09-10,
  `fix: parse reconciliation terminal JSONL handoffs`) both added
  `--events-stdout-jsonl` to this route and added the every-line
  command-result check.

This history is not the proof by itself; the exact provider-free replay binds
the history to the observed failure.

## Closed correction boundary for joint review

The likely API correction is a closed demultiplexer:

- recognize and preserve/relay known `sbe.execution_event.v1` records only as
  diagnostics;
- recognize `sbe.command_result.v1` records only as transition authority;
- continue enforcing one ordinary reconciliation result, the existing closed
  result-schema set, and terminal-companion uniqueness/precedence;
- reject malformed, unknown, duplicate, or conflicting records explicitly;
- never implement an open-ended "ignore non-command lines" rule.

No SBE contract or runtime change is presently indicated. An SBE release would
need a separate demonstrated reason.

## Verification

- Exact installed-0.4.59 mixed-stream replay: reproduced.
- Command-result-only control: accepted.
- Existing API reconciliation parser tests: `5 passed, 37 deselected`.
- Provider operations: one scripted GET, zero creates, zero network.
- R2 operations: zero.
- QA/workspace mutations: zero.

## Voof-paws 1 questions

1. Does API agree that `c1b4c3a` introduced a closed-stream demultiplexing bug?
2. Can the three retained R2 reads be waived as causally unnecessary?
3. Should API own the correction and production-path regression while SBE
   supplies/qualifies the mixed-envelope fixture?
4. Is any additive SBE packaged fixture useful enough to justify a release, or
   can the existing installed 0.4.59 public command serve as the joint proof?
