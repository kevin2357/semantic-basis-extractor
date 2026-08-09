# Slice 1 - Deterministic Fake and Smoke Correction

Status: complete; gate approval pending.

## Result

The patch remains inside the approved boundary. `closure.py` changes only fake
field generation; `smoke.py` changes only release-smoke reporting and cleanup
gating. Existing Batch-test scaffolding was updated for the renamed private
fake-value argument, and one focused regression module was added.

Fake values now derive from pass ID, separator-normalized relative path, field
path, and a file-local occurrence. They no longer depend on tree traversal
order or workspace root. Theme assignments retain deterministic four-way
balance using section-local ordering inside the stable theme-plan document.

Body uniqueness uses a 16-character alphabetic representation of SHA-256
nibbles (`a` through `p`). A 500-body regression proves every identity remains
distinct after the production `editorial_lint.words()` tokenizer and that the
production authoring-pass acceptance check accepts the set.

The smoke now performs delivery-only checks and completed-run cleanup only
after `DELIVERY_COMPLETE`. Otherwise it returns `status: fail`, records cleanup
as skipped, retains the original run and subject states plus available QA/lint
rejection evidence, and allows the CLI to write JSON and exit with its normal
failed-smoke code. Successful smoke still completes and verifies cleanup.

## Verification

- Focused new smoke/fake tests: 4 passed.
- Existing semantic-closure tests: 67 passed.
- Complete deterministic repository suite: 148 passed in 68.404 seconds.
- `git diff --check`: pass.
- Production provider/linter/workflow changes: none.
- Paid provider calls: zero.

Slice 2 may update patch coordinates, build the wheel reproducibly, audit it,
and run exact installed smoke on Windows and Linux only after this diff is
approved and committed.
