# API review — promotion batch 7 collision qualification

## Decision

Approved to promote exactly these three Batch 7 modules from `provisional` to
`parallel_safe`:

- `test_sbe_v03.py`;
- `test_negative_authorization.py`; and
- `test_operator_retirement_contract.py`.

This approval is limited to the manifest classification change and its normal
runner/inventory regressions. It does **not** establish a general whole-suite
speed claim, alter serial release authority, or authorize later provisional
modules to move without their own evidence.

## Why the bounded proof is sufficient

The state-surface audit identifies owned temporary roots for every write in the
three modules. The only deliberate contention is local to the scenario that
proves it: the retirement module's workspace-local native lock. Its child
processes inherit the secret-scrubbed worker environment and use owned paths.
The v0.3 examples/resources and cached schemas are read-only inputs. No
database, network, provider, port, repository-write, fixed shared-output, or
ambient credential surface is introduced.

The approved collision matrix then ran two independent copies of every real
module, in three repetitions: 18 of 18 worker receipts were green with empty
stderr and no failures/errors. Every copy preserved its frozen inventory:

| Module | Tests / skips |
|---|---:|
| `test_sbe_v03.py` | 52 / 0 |
| `test_negative_authorization.py` | 20 / 0 |
| `test_operator_retirement_contract.py` | 26 / 2 |

That retains the important negative and contention assertions rather than
mocking them away: stale/race nonmutation and provider-I/O refusal, as well as
the operator retirement publication, replay, interruption-repair,
single-writer, and protected-sentinel behavior.

## Required next boundary

After only that manifest change:

1. run the manifest/inventory regression checks; then
2. run the repeated concurrent actual-manifest `parallel_only` stress proof;
   and
3. require exact matching identity, outcome, and manifest digests, with the
   complete expected test/skip inventory and empty stderr in both receipts.

Pause for the Batch 7 completion review after those receipts. Do not fold in
any other provisional promotion, semantic-closure movement, runtime/package
change, or release work.
