# Background — durable operator hold and verified quarantine companion

## Status

**Closed — 2026-09-23.** This companion completed cross-repository review and
SBE-side discovery. It identifies no truthful SBE-wheel process-inventory or
post-redeploy absence capability: the API worker and Render platform own those
facts. No SBE runtime code, schema change, wheel build, provider work, R2
access, Render operation, or live QA mutation occurred.

## Product decision

The teams are intentionally stepping away from the previous end-to-end force-fence choreography as the near-term public operator workflow. That route attempted to make a cold Render one-off capture one exact active API attempt/lease/child identity, fence it, coordinate a cooperative stop or worker replacement, and complete a final quarantine.

Live QA showed the timing premise is too brittle for an ordinary operations tool: suspending the SBE service blocks future admission but does not stop a child already running; the delayed exact force-fence then correctly refused a stale child identity rather than mutating the wrong work.

The replacement model is deliberately simpler:

1. API persists a sticky **operator hold** on an exact run/job.
2. API denies all **future** ordinary claims and API-side provider/resource grants for that held run. It makes no statement about work already approved or currently running.
3. SBE-owned tooling inventories and stops work it can truthfully associate with that run, then produces a bounded receipt whose unknowns remain explicit.
4. API verifies that receipt and separately finalizes the run as `operator_quarantined`, releasing capacity only then. An explicit audited emergency/manual path handles unresolved cases.

The aspirational fully automatic choreography may be revisited later, but is not the current product gate.

## Completed API work

API slices 0–1 were committed and pushed at:

- API commit: `b83c9ef4` — `feat: add durable operator admission hold`
- Migration: `20260923_0092_add_operator_run_holds.py`
- Focused qualification: **120 passed** provider-free/API tests.

The API now owns `operator_run_holds`, one immutable/sticky relation per run/job. The hold records actor, reason, environment, canonical request digest and hold time. Same intent is idempotent; changed intent refuses.

The `astrowoof-operator sbe-operator-hold` command is the current operator ingress. It explicitly warns that it does not stop existing work or release capacity.

API checks the hold before future ordinary authority creation:

- queue/SBE-capacity claims, including failed-SBE recovery claims;
- initial-wave and external-authority v2 grant creation;
- new paid-action reservation, authorization, and provider-operation recording.

The hold deliberately does **not** revoke an active lease, kill a process, change a current provider-created action, release capacity, fabricate a native outcome, or mutate workspace custody.

## SBE discovery outcome

SBE reviewed what it can truthfully attest from the held run's durable identity
without accepting an API-supplied PID or stale child identity. The answer is
bounded: the SBE wheel can cooperatively report facts from its own active
invocation, but does not own the worker-wide child table, worker boot/restart
lifecycle, API queue, or Render container retirement. A cold SBE command cannot
truthfully assert that another worker container has no child running.

The requested later receipt may distinguish at least:

- `stopped`: SBE can associate current work and prove its stop outcome;
- `already_exited`: SBE can associate prior work and prove it had exited;
- `not_found`: no current SBE-associated work can be found, without claiming that no historical/native/provider work exists;
- `ambiguous`: association or safe stop cannot be proven.

The existing native supervision handoff remains useful cooperative evidence, but
it cannot become worker-wide post-redeploy proof. The appropriate finalization
receipt is API/worker/platform-owned and joins: the durable hold, final child
admission refusal, new-worker readiness, new-boot child-ledger inventory, API
queue/admission state, and Render old-boot retirement/no-overlap readback.
SBE should not invent a process-group, provider-settlement, or service-wide
absence assertion merely to produce a convenient success value.

## Non-negotiable invariant

After API accepts a valid finalization, other eligible runs must be able to progress normally. A held run may retain capacity only while stop proof is open and that unresolved posture must be operator-visible; it must never silently strand capacity indefinitely.

## Evidence and references

- API sprint plan: `C:\dev\github\astrowoof-api\docs\sprints\2026\09\20260923-durable-operator-hold-manual-quarantine-sprint115\PLAN.md`
- API hold contract: `C:\dev\github\astrowoof-api\docs\sprints\2026\09\20260923-durable-operator-hold-manual-quarantine-sprint115\SLICE 0 - OPERATOR HOLD CONTRACT.md`
- API implementation: `C:\dev\github\astrowoof-api\docs\sprints\2026\09\20260923-durable-operator-hold-manual-quarantine-sprint115\SLICE 1 - API ADMISSION HOLD IMPLEMENTATION.md`
- Stale-target QA witness: `C:\dev\github\astrowoof-api\docs\sprints\2026\09\20260923-provider-pending-lifecycle-contradiction-capacity-starvation-sprint114\testcases\Q5-004-pause-first-full-quarantine\RESULT.md`
- Earlier API/SBE lifecycle context: `C:\dev\github\astrowoof-api\docs\sprints\2026\09\20260921-worker-replacement-lifecycle-control-sprint111\PLAN.md` and `C:\dev\github\astrowoof-api\docs\sprints\2026\09\20260921-quarantiner-admission-freeze-graceful-completion-sprint112\PLAN.md`

## Log

- 2026-09-23: companion sprint created. API has completed only the durable future-admission hold. No SBE implementation request has yet been frozen.
- 2026-09-23: reviewed the API hold implementation and worker launch surface.
  The existing hold guards queue selection and authority creation, but the
  mandatory parent child-admission seam needs a final held-run refusal before
  `Popen` so a pre-hold lease cannot launch after containment.
- 2026-09-23: closed with no SBE package change. For the alpha manual route,
  an operator-authorized SBE-worker redeploy is the defensible broad stop
  action; API must collect worker/platform evidence before capacity release.
