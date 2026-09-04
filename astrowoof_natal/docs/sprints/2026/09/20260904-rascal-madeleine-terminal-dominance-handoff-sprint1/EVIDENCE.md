# Evidence — terminal-dominance handoff

## Slice 0 — source and trace contract freeze (complete)

### Frozen conclusion

The Rascal and Madeleine facts map to one native control-flow seam:
`finalize_subjects()` may commit a delivery or final-QA-review conclusion, but
the surrounding production coordinator continues into work selection and
publishes a local-progress-shaped result.

This is not a provider, authority, retry, or optional-stage adoption failure.
No provider-free source evidence supports selecting new qualitative work after
the committed conclusion.

### Production paths mapped

| Entry path | Current post-finalization behavior | Risk |
| --- | --- | --- |
| Batch reconciliation | Calls `run_qualitative_review()` for a delivered subject. | Can prepare an optional action after delivery. |
| Interactive reconciliation | Calls `run_qualitative_review()` for a delivered subject, then writes `local_continuation`. | Explains Rascal-like new authority and Madeleine-like progress publication. |
| Direct authoring | Calls `run_qualitative_review()` for a delivered subject. | Same terminal-dominance violation outside reconciliation. |

### Existing lifecycle contract

`inspect_lifecycle()` already:

- recognizes delivery and final-QA failure/review statuses as terminal;
- suppresses completed-provider-evidence local fan-in for a terminal run; and
- states that nonblocking optional evidence must not reopen a delivered or
  terminal run.

The implementation must make the coordinator obey that existing meaning. It
must not reinterpret a terminal status label by itself.

### Important preserved boundary

`review_required` is not automatically a fully terminal handoff. A truthful
review result may retain durable provider custody. That case may retrieve and
account for the already-submitted provider work, but it must not create or
authorize new work. The terminal-dominance gate therefore needs exact
post-finalization custody/result evidence, not a bare status-string check.

### API consumer minimums to freeze before mutation

- exact sealed native result ID and result digest;
- receipt ID and digest;
- terminal outcome and reason;
- checkpoint/snapshot identity; and
- a post-cycle assertion distinguishing resolved custody/no-new-work from
  retained reconciliation custody.

### Scope and access record

No provider, R2, API, QA, or retained-workspace operation occurred. The source
review used only the local SBE checkout and the sprint's supplied trace facts.

## Slice 1 — terminal-dominance implementation (approved)

### Implemented boundary

- `finalization_conclusion()` derives `delivery_complete` or
  `review_required` from the durable subject-finalization record, not a status
  label.
- Direct authoring, exact interactive reconciliation, and exact Batch
  reconciliation persist finalization before considering qualitative work.
- A conclusion suppresses `run_qualitative_review()` in that invocation.
- Exact reconciliation omits the synthetic `local_continuation` result field
  when the just-adopted evidence completed finalization; Batch does the same
  for its result surface.
- Lifecycle capacity keeps retained provider custody ahead of terminal closure,
  but treats a finalization conclusion plus locally-created successor work as
  `retain_for_review` / `native_review_required`, not an ordinary resume.

### Regression evidence

Provider-free focused command:

```text
python -m unittest \
  astrowoof_natal.tests.test_terminal_dominance_slice1 \
  astrowoof_natal.tests.test_provider_pending_capacity
```

Result: **32 passed**. `git diff --check` passed for modified source and test
files. Slice 2 still needs the full production-shaped delivery, editorial
review, contradiction, and retained-custody matrix.

## Slice 2 — production-shaped coordinator matrix (ready for review)

The provider-free fixtures now execute the actual paths that had bypassed the
previous helper-level guard:

- the public direct authoring CLI reaches delivery without invoking a
  qualitative consumer, creating an action, emitting an authority request, or
  leaving a runnable local continuation;
- exact interactive response reconciliation retrieves one scripted completed
  response, commits delivery, and produces a `terminal` result without a
  `local_continuation`, new action, or authority request; and
- exact Batch reconciliation follows the corresponding 4+2-style coordinator
  boundary and has the same no-qualitative/no-new-work result.

The existing terminal-dominance contract cases additionally prove that a
finalization conclusion plus independently present local successor work is a
typed `retain_for_review` result, not `ordinary_resume`; existing
provider-pending capacity cases continue to prove that already-durable provider
custody is reconciliation-only rather than permission for fresh creation.

Focused command:

```text
python -m unittest \
  astrowoof_natal.tests.test_semantic_closure.TestSemanticClosure.test_direct_authoring_cli_does_not_select_qualitative_work_after_delivery \
  astrowoof_natal.tests.test_semantic_closure.TestSemanticClosure.test_exact_interactive_reconciliation_does_not_select_qualitative_work_after_delivery \
  astrowoof_natal.tests.test_semantic_closure.TestSemanticClosure.test_exact_batch_reconciliation_does_not_select_qualitative_work_after_delivery \
  astrowoof_natal.tests.test_terminal_dominance_slice1 \
  astrowoof_natal.tests.test_provider_pending_capacity
```

Result: **35 passed**, provider-free. `git diff --check` passed. No retained
QA, R2, API, or provider access occurred.

## Slice 3 — installed-candidate qualification (pre-release approved)

A clean candidate wheel was built from the current source:

```text
astrowoof_natal_authoring-0.4.45-py3-none-any.whl
SHA-256 7bcd5f8c604f5bb814ecc1b7f17744a21c1f636ff8170eda30ef3b97a3766459
```

It was force-installed into an isolated existing qualification environment;
the imported runtime resolved from that environment's `site-packages`, and
`pip check` reported no broken requirements. The packaged
`astrowoof-terminal-review-qa --detailed` command loaded its public v2
schema and completed its provider-free review/receipt/reconciliation continuity
receipt. That receipt discloses its exact result ID/digest, receipt ID/digest,
checkpoint-basis digest, and snapshot digest for the invocation:

- one scripted GET, zero POST/create, zero external network/spend;
- immutable terminal-review result and receipt validation;
- contiguous custody-only successor and providerless denial; and
- no remaining provider or local continuation after closeout.

API pre-release review approved a fresh patch version because `0.4.45` is
already immutable. The final `0.4.46` candidate was rebuilt twice with
`SOURCE_DATE_EPOCH=0`; the wheels are byte-identical:

```text
astrowoof_natal_authoring-0.4.46-py3-none-any.whl
SHA-256 c6155ed71428865faa49eaeaf3442f5f64bb670e2317b1ec6dfd0bda54dcbb14
```

The final wheel was force-installed into the isolated qualification environment
(`site-packages`, not the source checkout). `pip check` passed, its imported
version was `0.4.46`, and both public qualification forms passed. The detailed
v2 receipt has SHA-256
`9f0f1c7788e591fe869cdb75451b18f13d54dc8be7d276ca690aed9d14755545` and
binds the invocation-specific result, native receipt, checkpoint basis, and
snapshot identities. It exercised one scripted retrieval GET and zero
POST/create, external network, or spend.

The three terminal-dominance coordinator cases remain the focused source matrix
because package distributions intentionally do not ship the test suite. They
exercise the same installed public modules in the release qualification plan;
the final fresh-version gate will rebuild and rerun this matrix with the final
wheel identity recorded. No retained QA, R2, API, or real provider activity
occurred.
