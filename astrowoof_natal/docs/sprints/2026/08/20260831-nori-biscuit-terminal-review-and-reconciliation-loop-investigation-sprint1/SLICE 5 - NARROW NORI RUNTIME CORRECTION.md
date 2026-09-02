# Slice 5 — narrow Nori runtime correction

## Implementation

The ordinary exact-interactive coordinator now distinguishes its two real
consumer boundaries:

- the authoring-pass checkpoint continues to seal authoring and creative-retry
  operations immediately;
- a local operation whose advertised stages are entirely optional/finalization
  stages is retained until `finalize_subjects()` runs; and
- the existing finalization checkpoint then performs the unchanged strict
  progress commit.

After a successful progress commit, the coordinator reloads the writer-owned
`run.json` checkpoint into its in-memory state. This preserves cumulative
`consumed_operation_keys` through later status/result publication.

The implementation adds no new command, contract version, authority, provider
operation, or status.

## Qualification result

The new public-boundary regression invokes real `finalize_subjects()`, real
`polish_subject()`, real completed-response artifact adoption, and real
`SpendController` settlement. Provider transport raises if invoked.

It proves:

- the completed polish action becomes `REPORTED`;
- the prior polish operation key enters cumulative consumed history;
- the operation cannot reappear in the successor;
- no `local_work_progress_contradiction` is sealed;
- the resulting custody-final editorial review is truthful; and
- provider create/retrieval count is zero.

Adjacent controls preserve creative-retry behavior, malformed/interrupted
adoption behavior, mixed custody, and not-due custody.

Focused evidence: 43 tests passed across the Nori/Biscuit reproduction,
Moxie adoption matrix, final-QA mixed-custody matrix, and post-fan-in runtime
modules. Diff hygiene passed; Git emitted only its existing LF/CRLF advisory.

## Explicit non-scope

- no Biscuit-shaped runtime workaround;
- no retained workspace execution or recovery;
- no API disposition implementation;
- no Batch or bounded-route claim; and
- no release preparation yet.
