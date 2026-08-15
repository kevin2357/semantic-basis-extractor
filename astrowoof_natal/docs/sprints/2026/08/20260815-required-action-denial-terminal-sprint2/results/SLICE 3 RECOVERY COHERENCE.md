# Slice 3: Recovery and Lifecycle Coherence

## Outcome

Slice 3 adds a narrowly bounded reconciliation path for retained SBE 0.4.1
workspaces whose native providerless-denial evidence is complete and valid but
predates the run-level `run_transition` introduced in this sprint. It does not
provide a general snapshot override or allow consumers to bless changed bytes.

## Supported recognizer

Reconciliation is considered only when an action is durably
`DENIED_PROVIDERLESS`, its negative-authorization evidence has no
`run_transition`, and the workspace has no accepted delivery or competing review,
ambiguity, or policy-stop state. Every candidate must then satisfy all of these
conditions:

- the complete workspace snapshot is valid at its stable logical absolute path;
- provider identity, consumption, reported cost, and ambiguity evidence are absent;
- the denial reason is in the closed supported vocabulary;
- the exact v0.4.1 single-denial artifact, or exact recorded batch artifact and
  batch digest, matches native state;
- frozen SBE policy identifies at least one denied member as required; and
- the derived consequence is a deterministic required-action terminal stop.

Accepted delivery is preserved and optional-only legacy denials are not promoted
into terminal failures. Anything contradictory or outside this recognizer fails
closed and the workspace must be retained for review.

## Durable transition

The reconciler stages
`lifecycle/required-denial-terminal-reconciliation.json`, persists one new state
revision containing `required_denial_reconciliation` and the terminal transition,
promotes the artifact, publishes one complete snapshot, and validates it. The
artifact records the pre-mutation lifecycle observation, exact denial-artifact
descriptors, resulting revision, timestamp, and derived run transition.

Normal exact and bounded resume invoke this reconciler before entering any
provider-capable continuation. Normal closeout invokes it under the lifecycle
single-writer lock. A successful reconciliation therefore yields the same
`BUDGET_EXHAUSTED` or `POLICY_STOPPED`, terminal, quiescent, dependency-free state
as a new denial. Repeating reconciliation is byte-stable and nonmutating.

## Interrupted-write recovery

Failure injection covers interruption after:

1. reconciliation artifact staging;
2. authoritative state persistence;
3. reconciliation artifact promotion; and
4. snapshot publication.

Restart may complete only the declared reconciliation write set: `run.json`,
`public-run.json`, `spend-authorization-requests.json`, and the one reconciliation
artifact. An unrelated added or changed member causes snapshot validation to fail;
no automatic repair occurs. Bounded normal resume was also tested from an
interruption after state persistence and completed reconciliation without a
provider submission.

## Verification

Focused lifecycle command:

```text
python -m unittest \
  astrowoof_natal.tests.test_negative_authorization \
  astrowoof_natal.tests.test_batch_negative_authorization \
  astrowoof_natal.tests.test_bounded_lifecycle -q
Ran 49 tests in 22.401s
OK
```

Full repository command:

```text
python -m unittest discover -s astrowoof_natal/tests -p "test_*.py"
Ran 309 tests in 133.040s
OK
```

Provider operations: 0. Paid spend: `$0`. API key used: no.

## Gate assessment

The Slice 3 gate is satisfied: private/public state, inspection, quiescence,
closeout, exact replay, and bounded normal resume agree; retained evidence is
reconciled only through an exact provenance recognizer; every tested unsafe or
unrelated condition fails closed. CLI packaging, consumer examples, events, and
installed-interface qualification remain Slice 4 work.
