# Evidence — Frisbee/Hype Prepared-Polish Authority Handoff

## Slice 0 conclusion

Frisbee and Hype expose the same native contradiction. SBE deliberately elected
and durably prepared a first polish action from `FINAL_QA_WARN`, but the public
lifecycle reducer simultaneously treated that warning as an already committed
terminal-review conclusion. Terminal dominance then suppressed the ordinary-v2
external-authority request that the prepared polish action required.

This is an SBE control-flow/meaning seam. It is not evidence of an API request
ingestion failure, a provider failure, or a missing generic polish request
builder.

## Frozen invariant for review

- A genuinely committed terminal conclusion remains dominant over all later
  optional-stage selection and authority preparation.
- `FINAL_QA_WARN` is provisional when SBE has elected enabled polish and has a
  durable nonterminal polish attempt/action awaiting a typed disposition.
- Such a prepared ordinary interactive polish action must expose exactly one
  ordinary-v2 external-authority request.
- A warning with no elected or pending polish may remain a non-dispatching review
  closeout.
- API must never manufacture the missing request or use generic resume to create
  provider work.

## Slice 1 correction

The exception is not triggered by a generic prepared action. It requires a
complete subject-local identity join from the same subject's current `SUBMITTED`
polish attempt, through its exact `paid_action_id`, to one exact providerless
`PREPARED` ledger action whose binding names the matching polish route and
interactive service. Batch, bounded, stale, mismatched, unrelated, authorized,
provider-bound, consumed, and terminalized evidence remain fail-closed under
terminal dominance.

The positive public inspection now selects `await_external_authority` and emits
exactly one ordinary-v2 request containing the matching polish action ID.

## Provider-free characterization

- `test_prepared_polish_is_currently_hidden_by_review_conclusion`
- `test_warning_without_elected_polish_remains_review_closeout`

The focused Slice 1 and existing terminal-dominance matrix passes: **9 tests**.
The adjacent lifecycle and persisted-polish-pause checks pass: **8 tests**.

## Slice 2 packaged public surface

- Command: `astrowoof-polish-authority-handoff-qa`
- Receipt: `astrowoof.polish_authority_handoff_qualification.v1`
- Schema resource:
  `contracts/polish-authority-handoff-qualification.v1.schema.json`
- Source qualification receipt: **pass**
- Focused qualification and neighboring-stage audit: **21 tests passed**
- Packaged schema parity: exact negative-case and check-name vocabularies are
  enforced independently of the Python validator; both schema-only mutations
  are rejected.

## Slice 3 release-bound regression gate

- Candidate version was frozen as **0.4.49** before the release-bound suite.
- Expanded focused matrix: **37 passed**.
- Packaged schema/public subset: **13 passed**.
- Broad/full suite: **1,052 passed, 3 expected skips**, in 921.962 seconds.
- `git diff --check`: clean for the complete intended release diff.
- The remaining gate is deterministic double-build and isolated installed-wheel
  qualification of the exact committed candidate.

## Activity boundary

- External provider calls: **0**
- R2 reads/listing/writes: **0**
- Retained QA mutation or recovery: **0**
- Runtime implementation changes: exact provisional-polish identity join and
  durable attempt/action provenance only
- Release activity: candidate preparation only; no tag or publication
