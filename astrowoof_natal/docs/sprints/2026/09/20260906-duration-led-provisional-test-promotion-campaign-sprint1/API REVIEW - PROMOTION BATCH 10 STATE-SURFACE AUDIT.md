# API review — promotion batch 10 state-surface audit

## Decision

Approved for bounded collision qualification, and only for these five clean
candidates:

- `test_external_authority_public.py`;
- `test_post_fan_in_mixed_custody_slice4b.py`;
- `test_operator_disposition_reader_slice2.py`;
- `test_post_fan_in_retry_matrix_slice3.py`; and
- `test_polish_authority_handoff_qa.py`.

`test_post_fan_in_retry_matrix_slice0.py` is excluded from Batch 10 collision
and promotion until its obsolete historical witness is surgically removed from
routine discovery.

## Historical-witness disposition

Archive only
`test_ordinary_retry_cycle_can_republish_same_decision_without_progress` as
forensic characterization. Preserve its source/provenance alongside the
incident/sprint evidence, outside a discovered `test_*.py` surface. Its green
condition proves the old v0.5 defect, not a present safety invariant.

Keep the module's `_workspace` helper and its three current
compatibility/precedence tests intact and discoverable. Retain an explicit
archive record pointing to the current v0.7 regressions that prove the desired
fail-closed, append-only consumed-operation behavior. After that narrowly
scoped extraction, treat the remaining module as a fresh candidate with an
updated exact inventory; do not silently include it in this Batch 10 evidence.

## Why the five are eligible

The five approved modules account for only 5.549 frozen seconds and 26 tests.
Their writes and locks remain temporary-root owned; provider paths are injected
retrieval fixtures or explicit zero-I/O qualifications; CLI/log/availability
patches restore locally; and imported helpers/resources are read-only. The
stateful assertions—snapshot fences, exact-result/writer refusal, custody/local
work precedence, route parity, and zero-I/O polish authority—must remain
active in the real-module matrix.

## Collision gate

Run three repetitions of two independent copies per approved module in
controlled waves of at most six workers. Require exact inventories of 12/0,
1/0, 6/0, 3/0, and 4/1 tests/skips, no unexpected outcomes or coordinator
stderr, and no substantive assertion changes. Pause for a separate promotion
review before a manifest update or actual-manifest stress proof.
