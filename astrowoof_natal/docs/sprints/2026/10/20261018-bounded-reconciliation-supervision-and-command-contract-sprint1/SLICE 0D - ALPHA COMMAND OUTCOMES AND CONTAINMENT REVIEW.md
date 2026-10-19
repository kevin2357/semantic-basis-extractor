# Slice 0D — concrete alpha command, outcomes and containment

**2026-10-18 · historical Gate A proposal; not implementation evidence.**
API's subsequent approval and SBE's matching sign-off close Gate A on the
refined contract and shared fixture definitions; see the SBE plan.
The companion refinement and outcome-table corrections in the API sprint's
`SBE AGENT - SLICE 0D REFUSAL AND CLOCK RESPONSE.md` supersede any contrary
wording below. In particular, early integrity refusal needs its own typed
companion; unproven terminal-companion exceptions are not accepted.
The subsequently agreed alpha clock policy in API sprint 129's
`SBE AGENT - GATE A ALPHA SHARED HANDOFF AND FIXTURES.md` supersedes older
calls below for a proven skew bound or mandatory refusal merely because the
cross-host relationship is unmeasured. Gate A and executable fixtures remain
open.
This follows [Slice 0C](SLICE%200C%20-%20ALPHA%20SAME-CALL%20HANDOFF%20AND%20CONTAINMENT.md)
and API's `API AGENT - SLICE 0C SCOPE REVIEW.md`. It makes the remaining
choices concrete without restoring the deferred automatic crash-recovery work.
Gate A is open until API and SBE agree the final executable fixtures, clock
policy and containment behavior. No provider calls or live state changed.

## 1. Proposed installed command and transport

Use the ordered bounded argv and synthetic digest fixture in API sprint 129's
`SBE AGENT - GATE A ARGV AND DECISION EVIDENCE.md`: executable, `--run-dir`,
`--resume`, `--provider-reconciliation-cycle`, `--provider openai`,
`--service-level interactive`, `--observed-at`, the four immutable profile
references, `--events-stdout-jsonl`, `--supervision-envelope`, and
`--suspension-control-root`. Validate caller-supplied provider/service, saved
profile, workspace, route and operation mechanism before mutation or I/O.
Current bounded CLI does not yet accept the last three options or the new
transport. Hash/launch the same argv; the profile/manifest and envelope remain
independently validated. Exact route stays unchanged.

Propose a closed JSONL stream using existing `sbe.command_result.v1` wrappers
(`schema_version`, `envelope_type: command_result`, `result`). Valid existing
`sbe.execution_event.v1` diagnostics are non-authoritative. For the ordinary
path there is exactly one `astrowoof.provider_reconciliation_cycle_result.v0.2`
and, **only if the same call made a fresh publication**, exactly one new
publication companion. For a newly published native delivery or terminal review,
also include exactly the matching existing terminal command-result companion;
for nonterminal publications there is no terminal companion. For verified
no-publication outcomes there is no publication or terminal companion.
Cooperative suspension emits exactly one validated suspension command result,
with no ordinary/publication/terminal result. Reject missing, duplicate, mixed,
unknown, truncated, oversized or wrong-schema authority records; diagnostics
and exit code alone are never success. Freeze exact line order with the real
API collector; preserve truthful parent observation timing and do not claim an
earlier terminal observation merely because the child sealed earlier.

The **proposed**, not-yet-existing, closed publication companion schema is
`astrowoof.bounded_reconciliation_publication_command_result.v1`, with exactly:

```text
schema_version, supervision_invocation_id, envelope_sha256, command_sha256,
native_run_id, native_invocation_id, result_id, result_sha256,
receipt_id, receipt_sha256
```

It contains no capability, lease token, path or provider payload. SBE must
construct it from the actual just-completed publisher return and validated
prelaunch envelope; API checks those values against the exact child, run,
route/profile, saved invocation and the named native result/receipt. A
supervision ID copied into output is not authority. The existing publisher can
repair an unsealed journal or reuse a terminal result; unless same-call
freshness is established, emit no fresh-publication companion and leave the
case unresolved. A new result contract for arbitrary crash reconstruction is
not an alpha requirement. The old terminal companions must match the same
result/receipt and cannot substitute for the generic nonterminal companion.

## 2. Proposed outcome / checkpoint / exit table

Source evidence: `lifecycle_contracts.py:164` lists seven v0.2 outcomes;
`reconciliation.py:430–575, 880–927, 1765–1807, 2110–2127` constructs them
and conditionally publishes; current `cli/bounded_run.py:391–420` exits **0
for cycle outcome `terminal`, 3 for other returned cycle outcomes**. The
table proposes preserving that process-level mapping for this successor.
The current code and its legacy plain JSON are not yet this stream contract.

| Cycle outcome | Current checkpoint evidence to support | Proposed outer exit and publication/companion rule | API handling |
| --- | --- | --- | --- |
| `not_due` | No `result_checkpoint`; no cycle record or changed workspace. | 3; ordinary only; no publication or terminal companion. | Validate no GET/change; schedule only under ordinary current authority. Lost output remains unknown. |
| `detached_provider_pending` | Retrieval cycle artifact and snapshot, when returned by real response cycle. | 3; ordinary + exact same-call publication if freshly sealed; no terminal companion. | Preserve known pending custody; continue only under valid lease/fence and timing policy. |
| `progressed_local` | Cycle artifact/snapshot, including local-evidence branch. | 3; ordinary + exact same-call publication if freshly sealed; no terminal companion. | Validate evidence and local state; no implicit permission for new paid work. |
| `awaiting_external_authority` | Either an existing snapshot-file artifact on an already-waiting branch, or cycle artifact after local continuation. | 3; ordinary + exact same-call publication if freshly sealed; no terminal companion absent a separately specified, fixture-proven exception. | Preserve custody; any later paid request needs the separate authority gate. |
| `terminal` | Snapshot-file artifact when already terminal, or cycle artifact after local continuation. | 0; ordinary + same-call fresh publication + matching delivery/review companion **only when actual sealed outcome and schema require it**. Existing earlier terminal reuse is unresolved, not a fresh handoff. | Validate exact terminal result/receipt and applicable fence; no terminal inference from cycle text alone. |
| `review_required` | An early binding-integrity refusal can have **no checkpoint**; other review branches return snapshot-file or cycle artifact. | 3; ordinary plus the proposed closed integrity-refusal companion for the specific early branch; no publication or terminal companion. A checkpointed branch requires exact fresh publication; include terminal-review companion only if the actual result is the terminal-review publication. | Preserve review/custody; a missing checkpoint is not success or proof of no provider exposure. |
| `unsupported` | Existing snapshot-file artifact or cycle artifact depending on route/local continuation. | 3; ordinary + exact fresh publication if made; no terminal companion absent a separately specified, fixture-proven exception. | Retain capacity/custody as indicated by validated native inspection; do not invent success. |
| cooperative suspension | Separate existing suspension checkpoint/result/receipt, not a cycle result. | Propose 0; one suspension command result only. | Verify exact request, local evidence, direct-child exit and API authority/checkpoint; uncertain or missing proof remains fenced. |
| parser error, unexpected exception, contradictory or incomplete stream | No assumed checkpoint/publication state. | Any non-contract exit/stream: no success inferred. | Preserve custody, block unauthorized continuation and surface unresolved state. |

The companion's own existing `exit_code` field is **not necessarily the
bounded process exit**: `build_terminal_review_command_result` embeds `2`,
while the current bounded cycle uses 0/3 for its own outer outcome. API must
validate each field against its own schema, not equate them. Any unlisted or
unproven combination is refused/contained. API must independently verify the
early no-checkpoint branch's cause/identity rather than accept arbitrary
`review_required` + missing checkpoint; decide the smallest closed evidence
needed before implementation. In particular, no-GET claims need an executable
fixture, not an inference merely from absent output.

`reconcile_provider_cycle` selects at most
`maximum_due_actions_per_cycle = 4`, and its thread pool has at most 4 workers
(`lifecycle_contracts.py:67–76`, `reconciliation.py:575–675`). This is one
bounded interactive cycle/wave, not a promise to finish all six actions in one
cycle; a six-operation fixture must require further authorized cycles.

## 3. Clock and fence: actual topology and narrow proposal

- The operator-side `SbeForceFenceService.admit` calculates the fence's
  `grace_deadline` as its own `datetime.now(UTC) + grace_seconds` unless a
  `now` is injected (`services/sbe_force_fence.py:70–85, 189`). The operator
  invokes it through `operator.py`; the existing runbook uses an operator
  runner, so that process is not necessarily on the SBE worker host.
- The worker parent prepares its own envelope grace deadline and, when it
  observes the fence, builds the suspension request using its current UTC;
  request expiry is the **minimum** of the parent-envelope and persisted
  fence deadlines (`sbe_native_supervision.py:169–173, 260–272`). The same
  worker parent launches the SBE child and writes the control file.
- Therefore parent/child generally share the worker-host clock on this path,
  but the persisted fence deadline can originate on a different process/host.
  Source code alone does not establish actual clock namespaces, synchronization,
  error bound or behavior under wall-clock steps. Do not assume zero skew.

Agreed alpha direction: new versioned child observation samples UTC at the safe point and
preserves it on replay; never treat the frozen launch timestamp as a later
observation. Keep the previously discussed strict request interval for the new
version while preserving old exact/historical validation. Retain the existing
operator-origin deadline, assuming services' UTC clocks are reasonably
synchronized. Their skew is unknown and unbounded by evidence: the effective
deadline can be earlier or later and is not a guaranteed hard cutoff. Do not
invent a skew constant, extend grace, or require an attestation as an alpha
precondition. Expired, malformed or detectably contradictory timing and
ordering remain contained; test detectable clock steps without claiming all
steps or cross-host skew are detected. The agreed tradeoff is documented in
the shared handoff; precise executable fixtures and sign-off remain open.

The parent must not treat child publication/seal time as evidence that it
observed a terminal result before a fence. API may use its existing ordering
evidence only where it actually proves strict order for the exact child/fence;
equal/missing/contradictory or lost evidence stays fenced. A universal new
parent journal is not a prerequisite, but safe containment still must be proved.

## 4. Containment tests: actual state, not just logs

API and SBE's joint provider-free tests must inspect the durable run/job,
lease/fence or applicable hold, paid-action/provider IDs, reservations and
capacity where applicable **after** each failure; an exception or emitted log
alone is not proof. Include:

1. Lost or malformed output after known provider GET, after result seal and
   before/after receipt; invalid/missing direct-child evidence; old terminal
   returned by repair/replay. Assert no latest-result attribution, no success,
   no unauthorized continuation or duplicate paid create, and no invented
   provider settlement or reservation release.
2. Crash/unknown acknowledgment around remote checkpoint, native ingress,
   economics savepoint and outer SQL commit. Check actual persisted outcome;
   idempotent replay only with independently established exact committed
   evidence and applicable authority. Missing proof remains unresolved.
3. Fence before wave and while a fake GET is blocked, including all four
   admitted GETs and the post-response checkpoint; no next wave after a valid
   observation, and no successful acknowledgment for a killed/hung child.
4. Record the actual operator-facing signal and exact run/job identity; test
   whether a durable hold/fence really prevents a new child/admission. Test
   whether the documented manual hold/redeploy/finalization preconditions are
   met for each relevant state. If not, the correct outcome is investigate or
   leave held; no automatic stop, capacity release or provider settlement is
   assumed. If existing API paths do not contain a case, smallest API-side
   correction is required before qualification.
5. Wrong route/profile, missing/invalid checkpoint and valid no-checkpoint
   review, duplicate/unknown output records, privacy, changed argv/receipt,
   old exact-route and historical observer behavior. Use the exact candidate
   wheel and real API archive/restore/collector paths with fake providers.

## 5. Proposed next steps

API: review the outcome/exit/companion table, the minimally closed publication
companion, its early-refusal evidence, clock rule and containment assertions;
confirm which API validators/state transitions need changes. SBE: incorporate
any agreed corrections and specify small implementation slices. Both sides
freeze executable positive/negative fixtures and agree Gate A before production
implementation. Exact candidate, release, deployment and paid canary remain
separate gates. This document deliberately does not declare any of them done.
