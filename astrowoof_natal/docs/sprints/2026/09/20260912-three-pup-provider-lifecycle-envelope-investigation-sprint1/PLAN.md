# Three-Pup Provider-Lifecycle Envelope Investigation — Plan

## Status

Closed after Slice 0 and Voof-paws 1. The investigation proved an API-owned
closed-stream demultiplexing defect. API accepted correction ownership, waived
all retained-workspace reads, and found no justification for an SBE runtime
change or release. The QA worker remained suspended throughout.

## Objective

Explain why Aldine Eclair, Ada Baklava, and Baskerville Biscotti all completed
their initial provider wave and then failed on the first due reconciliation
cycle with `SBE reconciliation envelope is unsupported`.

The investigation must distinguish:

1. valid native execution-event diagnostics;
2. authoritative native command-result envelopes;
3. API stream routing and consumer validation;
4. checkpoint/workspace state; and
5. release-pair compatibility.

No conclusion may convert a diagnostic event into transition authority or infer
a provider failure from the API's outer error classification.

## Preliminary evidence to preserve

The exported trace and current source already establish a narrow candidate
boundary:

- all three generation-2 workspaces restored as valid native v0.9 state with
  six `WAITING` initial actions and six durable provider response identities;
- the lifecycle selector chose `provider_reconciliation_cycle` because work was
  due, initially selecting four actions and later two as reconciliation made
  progress;
- SBE 0.4.59 published a native `provider_pending` result at revision 12 and
  produced an ordinary reconciliation result with
  `outcome=detached_provider_pending`;
- the API raised **envelope unsupported**, not **result schema unsupported**;
- API commit `c1b4c3a` added `--events-stdout-jsonl` to reconciliation and then
  required every captured stdout line to be a `sbe.command_result.v1` envelope;
- SBE's documented stdout JSONL transport emits typed
  `sbe.execution_event.v1` records as well as typed command-result envelopes
  when that flag is enabled.

This makes a stream-demultiplexing incompatibility the leading hypothesis:
the API may be rejecting a valid diagnostic execution-event record before it
reaches the valid command result later in the same stream. It remains a
hypothesis until Slice 0 captures the exact ordered stream and replays it
through the production consumer.

## Non-negotiable boundaries

- Provider-free throughout investigation and reproduction.
- No QA resume, retry, reconciliation, recovery, denial, settlement, or repair.
- No new provider creation, retrieval, or spend.
- No R2 listing, writes, alternate-object discovery, or mutation.
- If retained objects are used, access is limited to the three exact
  conditional HEAD/GET pairs authorized in `BACKGROUND.md`.
- Preserve exact release, invocation, result, receipt, action, response,
  checkpoint, and digest identities in evidence; sanitize content and prompts.
- Pause before runtime implementation even if the fault boundary appears
  obvious.

## Slice 0 — Freeze the transport and consumer boundary

### 0.1 Build three exact timelines

Parse the bounded Render export without editing it. For each run, record:

- API claim, lease, cycle start, checkpoint acceptance, defer/failure, and
  capacity release;
- native workspace fingerprint, lifecycle decision, selected/due action set,
  reconciliation progress, publication, command result, and CLI exit;
- the installed SBE version and available API revision/commit provenance;
- source ownership for each fact (`SBE diagnostic`, `SBE command result`,
  `API wrapper`, or `API persisted state`).

Use Denver time in the human-readable narrative and retain UTC timestamps in
the machine evidence.

### 0.2 Recover the ordered stdout envelope sequence

From trace evidence where possible, and otherwise from a provider-free local
reproduction using the released SBE 0.4.59 surface, capture the exact ordered
JSONL sequence emitted by:

```text
--resume --provider-reconciliation-cycle --events-stdout-jsonl
```

For each record, preserve only contract metadata:

- ordinal;
- `schema_version`;
- `envelope_type`;
- `event_name` or result schema;
- native run/invocation correlation;
- canonical digest.

Prove separately that the command emits a unique ordinary
`astrowoof.provider_reconciliation_cycle_result.v0.2` command result and that
any preceding/following `sbe.execution_event.v1` records are diagnostic only.

### 0.3 Exercise the production API parser provider-free

Feed the frozen ordered sequence to the actual
`_ReconciliationStreamCapture.reconciliation_output` implementation (or its
publicly testable production boundary) without rewriting the sequence.
Demonstrate which exact ordinal triggers the observed error and whether the
valid command result would be accepted when classified independently.

Negative controls must prove rejection of:

- malformed JSON;
- unknown envelope versions/types;
- unknown command-result schemas;
- duplicate ordinary command results; and
- conflicting terminal companions.

The proposed compatibility rule, if the evidence supports it, must remain
closed: recognize known diagnostic execution-event envelopes as non-authority,
and continue to validate command-result envelopes strictly. It must not become
"ignore every unknown line."

### 0.4 Release-pair history check

Compare the relevant SBE and API changes around the last known-good pair and
the deployed pair. Establish when:

- reconciliation began requesting stdout events;
- SBE began emitting each observed envelope class on that route; and
- the API reconciliation parser began accepting terminal companions.

Do not label the change causal merely because it is recent; bind it to the
provider-free reproduction.

### Slice 0 exit evidence

- Three frozen timelines.
- Ordered-envelope inventory and digests.
- Production-consumer reproduction of the exact failure.
- Owner classification: SBE emission defect, API consumer defect, release-pair
  skew, or unresolved.
- Explicit statement of provider-operation count and mutation count.

### Voof-paws 1

Joint review before R2 access or implementation. If the ordered stream and
production parser fully explain all three failures, reviewers should decide
whether checkpoint inspection adds any causal information. The already
authorized reads should not be performed merely because coordinates exist.

## Slice 1 — Conditional retained-checkpoint confirmation — waived

Voof-paws 1 found no material unanswered native-state question. API explicitly
waived all three authorized HEAD/GET pairs because generation 2 predates the
failed reconciliation subprocess and cannot prove its rejected stdout order.
This slice was not run.

For each approved generation-2 object:

1. perform one exact conditional HEAD;
2. compare ETag/version, size, and archive identity;
3. only on exact match, perform the one bounded GET;
4. validate archive and inventory SHA-256 before extraction; and
5. inspect only the state, snapshot/journal, action/custody, and public
   reconciliation/publication records needed for the stated question.

Compare all three checkpoints for the same six-action provider-custody shape.
Do not expect generation 2 to prove the later stdout sequence: it predates the
failed reconciliation attempt and API did not publish a successor checkpoint.

### Slice 1 exit evidence

- HEAD/GET access ledger and hashes, or a recorded decision that reads were
  unnecessary.
- Exact checkpoint/action/custody comparison.
- A clear statement of what generation 2 can and cannot prove.

## Slice 2 — Freeze correction ownership and regression shape — handed off

Slice 0 and API's reciprocal review froze the following API-owned handoff:

- the frozen mixed JSONL fixture;
- the first rejected diagnostic record;
- the independently valid ordinary command result;
- the closed allowlist and precedence rules;
- the three-run equivalence finding; and
- required production-path tests for reconciliation with diagnostics enabled
  and disabled.

No SBE defect was proven. API owns the closed demultiplexer and its
production-path regressions. The existing released SBE 0.4.59 public command
is sufficient joint evidence; no additive SBE fixture or release is required.

Any correction must preserve these invariants:

- execution events are diagnostic and never transition authority;
- command results remain closed, strictly validated, and uniquely selected;
- terminal companions retain their existing precedence and identity joins;
- unknown/malformed records fail closed with a typed classification;
- no provider operation is repeated merely because a consumer rejected the
  prior transport.

### Voof-paws 2 — implementation gate — not required in SBE

Voof-paws 1 already resolved owner and scope unconditionally. API will plan and
qualify its correction in its own sprint. Any later request for an additive SBE
fixture begins new, explicitly reviewed work rather than reopening this sprint.

## Disposition

- API-only parser/stream-routing correction and production-path qualification.
- No SBE code, schema, version, package, or release change.
- No retained R2 access performed.
- No QA resume, reset, deployment, or paid qualification performed by this
  sprint.
