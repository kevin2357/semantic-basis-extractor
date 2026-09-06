# Slice 2 — Battle of the Wheels result

## Result

The immutable SBE 0.4.36 wheel defeats the immutable SBE 0.4.35 wheel on the
exact historical worker-save/sibling-response-tree boundary.

| Wheel | Exact fixture outcome |
| --- | --- |
| 0.4.35 | worker `save_state()` enters sealed-result reading, validates the moving whole workspace, and raises the Kardamom `ValueError` |
| 0.4.36 | worker persistence completes; the coordinator publishes the complete successor snapshot; the predecessor review result remains byte-identical and readable |

This proves that 0.4.36 already removed Kardamom's immediate crash path. It is
not, by itself, a release or deployment recommendation; interruption and typed
replay semantics remain the next contract gate.

## Identical test body

`test_partial_reconciliation_wheel_battle_slice2.py` performs the following
against each installed wheel:

1. constructs the same production-shaped exact-Natal workspace;
2. publishes and seals an immutable v0.2 review result;
3. creates one 30-member sibling pass response tree outside the state lock;
4. invokes real `closure.save_state()` from a worker thread;
5. records the wheel-specific behavior; and
6. for 0.4.36, lets the coordinator publish the successor, validates the
   complete snapshot, reopens the predecessor result, and proves its bytes did
   not change.

The fixture makes no provider call and does not inspect retained QA data.

## Artifact identities

- SBE 0.4.35 wheel SHA-256:
  `830a4cd9288628c399a79f9d255edbb49caa5ab608046af6f12cfec8bbe34cfb`
- SBE 0.4.36 wheel SHA-256:
  `a76157d5342cb3b72a88b0b04fe8f3b549b8941b46d92d268182cbf934e8d826`

Both wheels were installed into separate local targets with `--no-deps`; the
test asserted the imported package version before exercising the boundary.

The same module also executes two real `author_pending_passes()` continuations
with `max_workers=1` and `max_workers=2`. It compares normalized complete pass
truth, attempt/QA states, every accepted-workspace relative file digest, run
status, and the complete action inventory. The projections are identical; the
concurrent provider records a peak of at least two while the serial control
records one.

Finally, the module constructs the production-shaped post-retrieval boundary:

- four provider-bound actions;
- two completed response artifacts already durable under reconciliation;
- two actions retaining pending provider custody;
- a sealed immutable v0.2 review predecessor; and
- two completed passes selected for real concurrent `author_pending_passes()`
  adoption through a reconciliation-only `SpendController`.

On 0.4.35 that boundary raises the historical snapshot error. On 0.4.36 both
completed passes become accepted, both pending actions remain pending, no
transport call occurs, the successor snapshot validates, and the sealed
predecessor remains exactly readable.

## Commands and outcomes

```text
SBE_WHEEL_BATTLE_VERSION=0.4.35
SBE_WHEEL_BATTLE_EXPECT_FAILURE=1
Ran 3 tests — OK

SBE_WHEEL_BATTLE_VERSION=0.4.36
SBE_WHEEL_BATTLE_EXPECT_FAILURE=0
Ran 3 tests — OK
```

“OK” for 0.4.35 means the test observed the expected historical failure;
“OK” for 0.4.36 means it observed the expected safe worker/coordinator split.

## Paws point 2 decision boundary

The reproduction gate is complete. Contract design must now decide whether to
qualify the already-shipped 0.4.36 worker/coordinator split as the correction,
or add a narrow explicit fence/result. Remaining requirements are:

- terminal-review status/result preservation;
- pending-provider custody;
- interruption before and during coordinator publication;
- typed review versus affirmatively safe replay; and
- absence of any new provider create or redundant retrieval.

The mixed-custody, terminal-result immutability, and no-I/O cases now pass. The
remaining work is specifically interruption classification and public typed
replay/review evidence.

Current tests written after 0.4.36 cannot be indiscriminately run against that
historical wheel: at least one now expects later custody-successor semantics.
Those cross-version semantic differences must not be misreported as evidence
for or against this snapshot-race correction.
