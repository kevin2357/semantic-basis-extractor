# API review — Slices 2–3

## Decision

The narrow custom coordinator is the right current choice. I approve the
overall Slice 2–3 direction and the decision not to adopt `pytest-xdist`:
the measured custom two-worker route is faster while retaining the project’s
closed manifest, per-worker roots, credential discipline, serial tail, and
reproducible receipt. No API/SBE lifecycle or release-contract concern was
found.

Before beginning Slice 4, please make the following two corrections.

## Required correction 1 — sanitize AstroWoof-namespaced credentials

`run_test_suite.py` currently removes generic `DATABASE_URL`, `OPENAI_API_KEY`,
`RENDER_API_KEY`, `ASTROWOOF_R2_*`, `AWS_*`, `CLOUDFLARE_*`, and `RENDER_*`.
That leaves realistic inherited names such as:

- `ASTROWOOF_DATABASE_URL`;
- `ASTROWOOF_OPENAI_API_KEY`; and
- any other secret-bearing `ASTROWOOF_*` value outside the current R2 prefix.

That conflicts with the plan’s explicit provider-free/database-free parallel
environment invariant. The worker environment should deny the specific known
AstroWoof secret names and/or apply an allowlist for the non-secret AstroWoof
test configuration it truly needs. Add direct tests with seeded
`ASTROWOOF_DATABASE_URL` and `ASTROWOOF_OPENAI_API_KEY` proving neither reaches
a shard subprocess. Continue to preserve the local test settings that are
actually non-secret and necessary.

This is a test-runner isolation correction only; it must not alter normal
package/runtime environment handling.

## Required correction 2 — reconcile the module inventory count

The checked-in manifest currently classifies exactly 129 discovered
`test_*.py` modules: 38 parallel-safe, 55 provisional, and 36 serial-only.
Several planning/log sections still state 128. Update those narrative counts
and retain the manifest validator as the authority.

## Slice 4 guardrails confirmed

- Run repeated exact identity/outcome comparisons, including the serial tail.
- Inject one deterministic failure per parallel shard and preserve its exact
  reproduction command in the aggregate receipt.
- Prove worker roots do not cross-write and repository release outputs remain
  untouched.
- Keep wheel construction, installed qualification, package inventory, release
  evidence, provider/R2/Render/QA activity, and all live work serial and out of
  this runner.
- Do not change CI or the release playbook until Voof-paws 2 evidence is
  reviewed.

With the two corrections above incorporated and focused tests green, SBE is
approved to begin Slice 4.
