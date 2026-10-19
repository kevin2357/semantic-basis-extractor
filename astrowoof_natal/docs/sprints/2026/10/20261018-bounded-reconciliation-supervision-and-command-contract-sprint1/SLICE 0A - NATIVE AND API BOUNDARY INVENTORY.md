# Slice 0A — native and API boundary inventory

**Completed, provider-free, 2026-10-18.** This is a source-and-focused-test
inventory, not proof that the complete repaired contract already exists.
Existing QA custody and evidence were not accessed or changed.

## Baseline and evidence

- The retained downloaded `astrowoof_natal_authoring-0.4.72-py3-none-any.whl`
  is 1,442,607 bytes; independently checked SHA-256 is
  `298273523a05c7a72cdd5404ca1727ef3f03c5c922785a7c5ba4da6f2990c364`.
  The focused tests below used the retained 0.4.72 installed environment;
  the wheel's prior install provenance is the release-lock evidence, not a
  fresh install independently proven in this slice.
- API's sprint background reports a synthetic, fake-provider native v2
  reconciliation success, not a successful real API command/ingress/checkpoint
  join. Its real QA evidence reports six native operations and six API
  reservations, which are separate custody records; this slice does not
  adjudicate their present state.
- Four focused provider-free tests passed against that installation in 25.983s:
  `test_reconciliation_observes_before_any_provider_get`,
  `test_request_arriving_during_get_suspends_after_response_checkpoint`,
  `test_bounded_reconciliation_retrieves_once_then_exhausts_local_work`, and
  `test_bounded_reconciliation_crash_checkpoints_resume_without_retrieval`.
  The first two exercise **exact**, not bounded, suspension. The other two
  exercise bounded retrieval/local recovery, not supervised bounded CLI/API
  integration. An initial sandboxed attempt failed on Windows temporary-directory
  permissions; the same tests passed with ordinary local temp access. No live
  provider call was made.

## Real command, transport and intake

1. API's `services/sbe_provider_orchestration.py` functions
   `build_sbe_provider_reconciliation_command` and
   `build_provider_reconciliation_command_sha256` assemble and bind ordered
   arguments including `--resume`, `--provider-reconciliation-cycle`,
   `--observed-at`, `--events-stdout-jsonl` and the paired supervision flags.
   Worker `worker/sbe_runtime.py::_advance_bounded_reconciliation` creates a
   prelaunch envelope, launches via the provider runtime and installs a callback
   to write the fence request.
2. The installed entry point is `astrowoof-run-bounded-natal`
   (`pyproject.toml`). Current `cli/bounded_run.py::build_parser` accepts
   `--events-jsonl` as a **file**, but not `--events-stdout-jsonl`,
   `--supervision-envelope` or `--suspension-control-root`. Its reconciliation
   branch prints a plain JSON object and does not provide a terminal-command
   callback. `--resume`, `--provider openai` and `--observed-at` are required;
   the branch refuses new spend/initial-wave/external authority inputs. A
   test's injected fake transport is not the same thing as public
   `--provider fake`, which this branch currently refuses.
3. API `_ReconciliationStreamCapture.reconciliation_output` accepts typed
   `sbe.command_result.v1` wrappers, plus recognized diagnostic events. It
   requires one ordinary v0.2 result **or** one suspension, rejects mixing
   suspension with ordinary/terminal, and permits at most one review or
   delivery companion. Thus the released bounded stdout is incompatible even
   if argument parsing were bypassed. Exact `cli/closure.py` already emits the
   typed wrapper and supports a paired supervision observer; that is a useful
   control, not proof that bounded is wired.
4. API `services/sbe_bounded_reconciliation.py::validate` checks the v0.2
   result, native identity, decision/successor snapshots, retrieval count and
   native inspection. Its downstream
   `services/sbe_provider_pending_lifecycle.py::validate` currently maps
   `bounded_natal` to `astrowoof.bounded_natal.authoring_run.v1`, whereas
   current bounded native inspection reports v2. A route-aware, profile-bound
   change is API-owned; relabeling v2 as v1 would be false.
5. Current API `_advance_bounded_reconciliation` publishes a result checkpoint,
   then reads a sealed native transition using `read_latest_sealed` before
   persisting it and observing economics. The stream parser can classify an
   exact terminal companion, but the bounded path does not yet prove it uses
   that exact selector. This is an important joint design/replay item, not
   proof that the observed economics mismatch was caused by this lookup.

## Native boundary and suspension facts

`reconciliation.py::reconcile_authoring_provider_cycle` explicitly refuses a
non-null observer for bounded interactive and bounded batch. Shared interactive
`reconcile_provider_cycle` already has writer-held pre-GET and post-response
snapshot callbacks, currently used for exact interactive. `reconciliation.py`
and `lifecycle_contracts.py` show the current interactive wave selects at
most four due operations, with up to four parallel retrievals; the configured
request timeout is 15 seconds. `executor.map` collects the whole wave before
response adoption/checkpointing. A fence arriving after the pre-wave callback
cannot cancel the wave, and a selected/queued GET can start after the fence;
do not read the 15-second timeout or configured wall limit as a hard
end-to-end child-exit guarantee.

The retrieval adapter uses GET against already identified operations, with no
request body and no transport retries. Native writes include response/action
evidence, state and snapshot; after the response checkpoint, bounded
`resume_bounded_run(..., reconciliation_only=True)` can perform route-local
continuation and can reach publication. The follow-on must be traced and
tested as local work, not described as "nothing happens after GET". New paid
create requires its existing separate authority; this inventory does not
prove arbitrary continuation is safe to run after a fence.

`native_suspension_runtime.py::NativeSuspensionControlObserver` validates
request/envelope, snapshot, run identity and current or supplied predecessor
basis, and records a local suspension result/receipt under the writer's
control. `native_suspension_contracts.py` names additional potential safe
points, but names alone do not establish that reconciliation calls them. The
shared observer uses its constructor's `observed_at` for request-expiry checking,
terminal precedence and evidence timestamps; API currently passes the launch's
fixed observation time. The validator rejects observation **after expiry**,
but does not require observation at/after request creation. Therefore launch
time is not evidence of actual fence-observation time, and a later observation
cannot safely infer freshness merely from that frozen time. This is a source
finding and a joint design issue, not a claim a specific QA fence was mishandled.

The existing post-wave callback supplies the wave's pre-retrieval checkpoint
basis as predecessor. If continuation adds further state changes, the original
anchor cannot simply be asserted to be the immediate predecessor: an approved,
verifiable ancestry or a narrower safe-point contract is needed. Local
snapshot persistence is not remote checkpoint publication. Native suspension
does not itself prove direct-child exit, lease revocation, remote durability,
slot release, provider cancellation, settled costs or no later external work.

## Independent economics finding

API `services/provider_economics_export_ingestion.py::_require_matches_publication`
compares the export's native run ID and snapshot SHA against the validated
publication. `sealed_publication_join_mismatch` identifies that comparison
failure, not which of those values differed or why. `observe` contains the
failure in a savepoint and reports unavailable; it is not lifecycle authority.
To investigate, capture safe expected/actual IDs/digests and the exact
export/publication selector and timing in synthetic joined replay; keep content,
provider credentials and paths out of diagnostics. A mismatch is not evidence
of CLI, accounting or provider failure without that join proof.

## Fixture to build after Gate A

Use a synthetic bounded v2, immutable-profile-bound workspace with six known
provider action identities and a deterministic fake transport; cycle through
multiple waves because one wave is limited to four. Include pending, completed
and failure responses, distinct response barriers for requests before/during/
after GET, durable snapshots, local continuation, terminal delivery and review,
and crash points. Exercise the actual installed CLI and API launch/collector/
ingestion with network disabled or a tightly controlled test-only fake transport;
do not silently relax the production `provider=openai` contract. Assert no
POST/paid-create and no duplicate create; compare exact provider IDs without
putting sensitive payloads in diagnostics. Preserve exact-route regression
controls. The full test matrix and unresolved choices are in Slice 0B.
