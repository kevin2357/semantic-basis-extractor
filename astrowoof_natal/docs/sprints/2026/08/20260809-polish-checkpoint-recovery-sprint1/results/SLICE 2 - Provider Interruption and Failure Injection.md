# Slice 2 - Provider Interruption and Failure Injection

Status: complete; gate approval pending.

## Result

The provider-response boundary now preserves the narrowest available native
reconciliation evidence without claiming provider exactly-once semantics.
After a successful Responses POST, SBE validates the returned ID and writes the
attempt-local `openai-background-response.json` marker before persisting that
identity in the spend ledger. A restored `SUBMITTING` action with a matching
marker records that identity and performs GET-only reconciliation. It neither
creates another response nor adds another commitment.

Recording the same provider identity twice is idempotent. A marker identity
that conflicts with the ledger identity is durably classified as
`AMBIGUOUS_PROVIDER_SUBMISSION` and blocks automatic progress. Failure after
provider acceptance but before SBE receives and durably records an ID remains
the irreducible provider/local-state atomicity gap. Deterministic request keys
are correlation evidence, not proof that resubmission is safe.

Local failure while installing polished final files or QA results now stops the
polish loop after recording `POLISH_ERROR`; it cannot silently prepare or
submit another paid attempt. An interrupted coordinator checkpoint remains
fail-closed: if state persistence succeeds but snapshot publication fails,
native snapshot validation refuses resume until the coordinator republishes a
complete checkpoint.

## Failure matrix

- before submission: exact prepared authorization remains required;
- submitted without durable provider identity: machine ambiguity, no retry;
- Response returned before ledger-ID persistence: native marker survives and
  ambiguity is recorded if persistence fails;
- restored `SUBMITTING` plus matching marker: ledger identity attachment and
  GET-only reconciliation;
- repeated matching identity: idempotent;
- marker/ledger identity conflict: persisted ambiguity and refusal;
- polling recorded provider work: no new action or commitment;
- reported response: usage and estimate settle on the existing action;
- final-copy/QA installation failure: attempt records `POLISH_ERROR` and stops
  before another paid attempt;
- next authorization boundary: Slice 1 coordinator unwind checkpoints the
  settled prior attempt before exposing the prepared action;
- state persisted but snapshot publication interrupted: restored validation
  fails closed until a complete checkpoint is republished.

Existing tests continue to cover exact request binding, one-time authorization
consumption, Batch request-digest stability, background retrieval, ambiguous
transport outcomes, and atomic state replacement failure.

## Verification

- Focused spend and semantic-closure suites: 91 passed in 64.528 seconds.
- Complete deterministic repository suite: 157 passed in 77.297 seconds.
- Fake transports only; OpenAI requests and incremental spend: zero.
- Prepared acceptance authorization consumed: false.
- Retained acceptance run read or mutated during this slice: false.
- Provider atomicity qualified rather than overstated: yes.

Next action: approve the recovery semantics and regression matrix before the
Slice 2 commit and Slice 3 constrained repair tooling.
