# Plan — SBE worker trace observability

## Status

Slices 0–6 complete in source. Slice 7 packaging/release evidence is in
progress. Owner authorized autonomous progress through review pauses unless a
contract decision or material issue arose.

## Objective

Make SBE's restored basis, native state, selected transition, durable
publication, and public command outcome understandable from bounded sanitized
`✨🐶` worker traces, reducing routine reliance on retained-workspace downloads.

## Success criteria

For representative exact and bounded interactive flows, an operator can use
the SBE trace alone to determine:

- the exact safe identity of the restored checkpoint/snapshot;
- the validated lifecycle/result contract version and selected branch;
- action, custody, local-work, retry-lineage, and dispatch-intent posture;
- whether provider creation/retrieval and native mutation occurred;
- which durable artifact/result/checkpoint was returned to API; and
- the typed reason for refusal, review, ambiguity, pending, local work,
  terminal result, or ordinary success.

The same tests prove no protected data appears and logging failures do not alter
authoritative behavior.

## Non-goals

- Making logs or structured events transition authority.
- Replacing lifecycle, authority, result, receipt, or checkpoint contracts.
- Reconstructing API-global lease, slot, reservation, billing, or queue facts.
- Building the full R2/native checkpoint inspector in this sprint.
- Auditing deterministic-worker or API logging implementation.
- Redesigning the entire structured-event taxonomy.
- Logging full payloads, prompts, bindings, provider bodies, or subject data.
- Accessing or mutating retained QA workspaces.

## Frozen principles

1. Log validated truth; do not implement a parallel lifecycle reducer.
2. Emit a workspace fingerprint only after restore/snapshot validation.
3. Emit a decision summary only after the corresponding public artifact passes
   its supported validator.
4. Emit a publication summary only after durable persistence succeeds.
5. Emit exactly one best-effort exit summary for every public CLI path.
6. Unknown is distinct from absent, false, zero, or unavailable.
7. Sink failure is isolated from all authoritative behavior.
8. Inventory detail is bounded and deterministic with explicit overflow.
9. Provider-custody, local-work, authority, review, and terminal facts remain
   distinct; status labels are never used as inferred permissions.
10. Existing `✨🐶` formatting remains the human-searchable entry point.

## Candidate standard prefix/context

Continue the centralized format in `application_logging.py`:

```text
✨🐶 timestamp | level | host_id | run_id | action_id | module.function : message
```

The audit may add a compact invocation/command correlation field if existing
context cannot distinguish concurrent or repeated commands. It must not add
high-cardinality subject or payload information.

## Required safe projections

### Workspace fingerprint

- `native_run_id`
- route/contract identity
- state revision
- checkpoint generation/object identity when available
- logical-root identity/digest, never a private absolute path
- snapshot/checkpoint-basis/archive/inventory digests when available
- installed SBE and SPC compatibility identity
- validation outcome

### Decision summary

- lifecycle/result schema version
- selected command/branch/capacity disposition/reason
- ordered action count and bounded IDs/digests
- counts by action state, stage, and custody class
- retained provider response IDs/statuses and SBE-selected due subset
- local-work operation IDs/keys and consumed-lineage summary
- retry predecessor/successor lineage summary
- live/retired/completed/ambiguous v2 intent identity
- terminal/review result, receipt, and predecessor/successor identities
- explicit validated readiness/custody/publication assertions

### Side-effect/publication summary

- provider create/retrieve counts for this invocation
- authority consumption count
- mutation/publication booleans
- pre/post revision and snapshot/checkpoint digests
- sealed artifact/result/receipt IDs and digests

### Exit summary

- command and invocation correlation
- typed outcome/reason
- exact returned artifact/result identity
- numeric exit code
- whether stdout/output-file bytes are authoritative
- sanitized exception class/fingerprint when applicable

## Slices

### Slice 0 — trace coverage and source-boundary audit

Inventory all supported production-facing SBE commands and the real internal
boundaries they use:

- semantic closure/resume;
- lifecycle inspection and local-work inspection;
- provider reconciliation;
- external-authority v1/v2;
- initial-wave and bounded paths;
- terminal-review/native-transition availability;
- operator retirement and supported repair commands; and
- installed qualification commands where they exercise production paths.

For each, record:

- current workspace-entry/fingerprint visibility;
- current branch/decision visibility;
- provider call before/after visibility;
- mutation/publication visibility;
- exception-handler visibility;
- CLI exit visibility;
- text versus structured-event coverage; and
- whether API actually relays/retains the trace.

Create a provider-free characterization showing at least one current public
handoff where the returned artifact is valid but the trace lacks enough safe
facts to reconstruct the selected state/branch.

Deliverables:

- `SLICE 0 - TRACE COVERAGE AND HANDOFF MAP.md`
- coverage matrix tied to exact source functions
- focused characterization test
- updated `LOG.md` and `EVIDENCE.md`

**Voof-paws 1:** review the matrix and freeze the first-release command scope.

### Slice 1 — sanitizer, bounded projection, and fingerprint contract

Design one internal observability helper layer that:

- accepts already-validated public/native projections;
- normalizes safe scalar identities;
- summarizes ordered inventories deterministically;
- explicitly represents unknown/unavailable/truncated values;
- sanitizes exception messages and endpoint identities;
- emits through standard Python logging; and
- cannot throw into authoritative control flow.

Freeze the workspace fingerprint and decision-summary field vocabularies. This
is a diagnostic internal contract, not an API-consumable authority schema.

Tests must cover:

- canonical determinism;
- bounded inventory overflow;
- protected payload/path/credential/subject sentinels;
- malformed optional metadata;
- sink/formatter failure isolation; and
- absence of complete bindings, documents, prompts, or provider bodies.

Deliverables:

- helper implementation and focused tests
- `SLICE 1 - TRACE SUMMARY AND FINGERPRINT CONTRACT.md`

**Voof-paws 2:** approve the privacy boundary and exact fingerprint semantics.

### Slice 2 — workspace acquisition and checkpoint publication visibility

Wire the workspace fingerprint into supported public entrypoints immediately
after snapshot/restoration validation and before selection/mutation.

Wire publication summaries after successful durable snapshot/checkpoint/result
publication. Prove pre/post identities distinguish:

- read-only inspection;
- not-due no-op;
- local mutation;
- provider retrieval checkpoint;
- result/receipt sealing; and
- publication failure.

Never log raw restored paths or R2 credentials/URLs. If R2 generation/object
identity is unavailable to SBE, log `unknown`; do not synthesize it from paths.

### Slice 3 — lifecycle, local-work, retry, and custody decision summaries

Add validated summaries at:

- lifecycle v0.5/v0.7/v0.8 and temporal v0.6 selection;
- provider-custody precedence and bounded due-subset selection;
- local fan-in/adoption and consumed-operation transitions;
- retry-lineage conflict/refusal;
- prepared authority selection; and
- review/terminal/unsupported dispositions.

Regression scenarios must include the previously difficult shapes:

- completed evidence plus prepared successor;
- pending custody plus separate local work;
- retry-lineage conflict under retained custody;
- no-custody terminal review; and
- provisional review status plus live provider custody.

### Slice 4 — authority, provider I/O, reconciliation, and intent traces

Complete before/after visibility for:

- constrained external-authority request/grant validation;
- writer-fenced intent commit;
- provider call entry, returned identity, ambiguity, and refusal;
- reconciliation GET start/result/duration/status/request ID;
- v2 intent retirement; and
- exact replay/no-duplicate behavior.

Use sanitized endpoint identity only. Never log request payloads, credentials,
headers, provider bodies, or complete authority documents.

### Slice 5 — terminal result, receipt, successor, and CLI-exit summaries

Emit trace summaries for:

- terminal/review result sealing;
- terminal-result availability discovery;
- custody-only successors and immutable predecessor continuity;
- typed review/refusal versus terminal completion; and
- every public CLI exit path in the selected release scope.

A sealed typed result returned by the invocation must be named directly and
must outrank the numeric exit code in the explanatory trace. Availability-based
discovery remains clearly labeled as recovery/preflight evidence.

### Slice 6 — holistic provider-free trace qualification

Build a provider-free qualification that captures trace output for exact and
bounded representative routes and validates:

- workspace fingerprint appears before the first decision;
- decision summary agrees with the returned validated artifact;
- mutation/publication summary agrees with durable bytes;
- exit summary names the exact returned artifact and outcome;
- provider-pending, local-work, authority, refusal, ambiguity, review, and
  terminal-result branches are distinguishable;
- protected sentinels never occur;
- inventory truncation is explicit and stable;
- failing logger/event sinks do not alter authoritative bytes or provider-call
  behavior; and
- the emitted evidence is sufficient to reconstruct the selected branch and
  custody/progress posture without opening the workspace.

The qualification should produce a concise closed receipt containing only
test identities, trace hashes/counts, privacy assertions, and zero-provider-I/O
evidence. The receipt is qualification evidence, never runtime authority.

**Voof-paws 3:** API reviews real captured trace samples for operational utility
and confirms which lines are relayed/retained in deployed workers.

### Slice 7 — packaging, playbook, and release gate

- Package any qualification command/resources added by the sprint.
- Document log levels, filtering by `✨🐶`, correlation workflow, and escalation
  from logs to public artifacts to the R2 inspector.
- Add a short operator playbook with examples for the major branch families.
- Run the risk-proportionate focused/broad/installed-wheel matrix agreed at the
  final review pause.
- Record exact wheel, source, SPC, and qualification identities.
- Confirm no real provider, spend, R2, or retained-QA activity.

**Voof-paws 4:** final API/owner release review before commit, tag, or publish.

## Compatibility and release posture

- No public lifecycle/status/authority/result semantics should change.
- Existing public schemas remain frozen unless implementation discovers that a
  currently required safe identity is unavailable through any validated public
  projection. Such a discovery pauses the sprint for contract review.
- Text changes are operationally visible and should be treated as additive,
  non-authoritative diagnostics.
- Structured events may be enriched only through an existing compatible closed
  event contract. Otherwise record a follow-up for the structured-event audit.
- This work warrants a fresh immutable SBE patch release because deployed
  worker behavior and installed qualification change.

## API handoff expectations

API should be able to correlate each SBE invocation using:

- API job/attempt and subprocess invocation identity;
- SBE native run and workspace fingerprint;
- exact returned artifact/result ID and digest;
- SBE branch/outcome/reason; and
- API's independently logged mapper, custody, lease, and scheduling decision.

API must not parse free-form message prose as transition authority. Structured
public artifacts remain the only supported consumer boundary.
