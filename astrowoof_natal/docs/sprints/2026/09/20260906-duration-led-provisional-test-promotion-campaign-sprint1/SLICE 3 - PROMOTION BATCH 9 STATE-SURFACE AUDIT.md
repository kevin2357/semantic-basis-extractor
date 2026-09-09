# Slice 3 — promotion batch 9 state-surface audit

## Scope and decision

Audit the next five remaining leaders in the frozen provisional-duration
inventory. Their compact duration and owned state justify the larger adaptive
cohort. All five may advance to bounded collision qualification; none is
promoted by this document.

| Module | Frozen seconds | Tests | Audit disposition |
|---|---:|---:|---|
| `test_review_required_pending_retries_investigation_slice2.py` | 1.691 | 4 | collision candidate with shared fixture inheritance and workspace-local thread lock |
| `test_spend_enforcement.py` | 1.683 | 18 | collision candidate with injected provider transports and process-local patches |
| `test_external_authority_empty_inventory_investigation.py` | 1.585 | 13 | collision candidate with helper import, logger capture, and event sinks |
| `test_lifecycle_closeout.py` | 1.546 | 10 | collision candidate with interruption recovery and package-resource validation |
| `test_checkpoint_repair.py` | 1.419 | 8 | collision candidate with dry-run/apply and exact-backup filesystem surfaces |

The cohort represents 7.924 seconds of the original provisional tail and 53
tests with no expected skips.

## Review-required pending retries

- Every scenario owns its temporary run root. The runtime reproduction uses a
  process-local `SpendController`, `threading.Lock`, and extracted shared
  fixture class whose mutable products remain caller-owned.
- Its v0.7 duplicate-route case is retained backward-contract evidence, not a
  request to recreate duplicate provider work: distinct request bindings may
  share a route, while the real runtime case proves one exact attempt/action is
  reused before transport.
- The provider object is configured with a placeholder key, but execution stops
  at the exact spend callback before any transport call.
- Module-level imports and state are process-local. No environment, cwd,
  subprocess, database, port, network, repository write, or fixed output path
  was found.

Disposition: advance to collision qualification. Preserve custody precedence,
v0.7 compatibility, modality-independent review projection, exact retry/action
reuse, and zero provider I/O.

## Spend enforcement

- Mutable ledgers and every persisted controller/provider case use owned
  temporary roots and workspace-local locks.
- Provider-facing behavior is exercised only through injected `NoCalls`,
  failing, completed, and retrieval transport doubles. Their call lists are
  instance-local and prove exact POST/GET/no-call behavior without network I/O.
- Persistence-failure patches restore through context managers. Module-level
  `sys.path` insertion and helper state are process-local.
- No environment, cwd, subprocess, database, port, network, repository write,
  or fixed shared output was found.

Disposition: advance to collision qualification. Preserve exact authorization,
budget, commitment, ambiguity, durable-marker ordering, reconciliation, and
provider-call-count assertions.

## External-authority empty inventory

- All lifecycle documents, snapshots, requests, and refusal artifacts are
  caller-owned beneath temporary roots. The imported public-authority fixture
  module supplies builders but no import-time mutation or shared output.
- Event sinks are in-memory/process-local. `assertLogs` and the one lifecycle
  helper patch are restoring context managers; sink-failure cases explicitly
  prove diagnostic loss cannot alter authority results.
- No provider transport, environment, cwd, subprocess, database, port, network,
  repository write, or fixed output path was found.

Disposition: advance to collision qualification. Preserve the exact positive
predicates, typed refusal distinctions, diagnostic non-authority, lexical
action-set joins, snapshot race refusal, and mutation failures.

## Lifecycle closeout

- Every closeout, staged artifact, delivery, crash injection, and recovery case
  is rooted in an owned temporary workspace. Byte comparisons exclude only
  workspace-local lock files.
- Schema/example resources and the imported validator are read-only. The
  module-level source-path insertion is process-local.
- Event emitters and failing sinks are instance-local and preserve the native
  result across diagnostic loss.
- No environment, cwd, subprocess, database, port, external network, provider
  I/O, repository write, or fixed shared output was found.

Disposition: advance to collision qualification. Preserve durable/idempotent
closeout, delivery bytes, interruption repair, mutation refusal, exact provider
custody, decision-basis correlation, and event-loss independence.

## Checkpoint repair

- Fixture construction, repair candidates, native artifacts, authorization,
  and the mandatory backup all live under an owned temporary root.
- `shutil` operations copy only within that root. Dry-run and refusal cases
  prove nonmutation; apply requires a distinct exact backup before writing.
- Module-level source-path insertion is process-local. No environment, cwd,
  subprocess, database, port, network, provider I/O, repository write, or fixed
  shared output was found.

Disposition: advance to collision qualification. Preserve exact polish repair,
dry-run/apply separation, unexplained-mutation refusal, authorization/provider
identity joins, retained-attempt integrity, and backup requirements.

## Next boundary

No pre-collision repair is justified. Run three repetitions with two
independent process copies of each candidate in controlled waves capped at six
simultaneous workers. Require exact per-copy inventories of 4, 18, 13, 10, and
8 tests; zero skips; empty failure/error sets; no coordinator stderr; and all
substantive assertions unchanged. Then pause for the separate promotion
decision before any manifest change or actual-manifest stress proof.

This audit grants no production/package change, semantic-closure movement, or
blanket qualification of the remaining provisional tail.
