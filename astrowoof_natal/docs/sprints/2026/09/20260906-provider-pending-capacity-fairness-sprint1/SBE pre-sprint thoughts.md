# SBE Pre-Sprint Thoughts

## Purpose

Determine why paired QA runs once gave run B its initial fan-out within roughly
one to two minutes, while later peers waited five to nine minutes and the recent
Podium/Laurel pair waited until the incumbent terminal boundary. Provider-bound
overlap did not vanish absolutely; prompt peer access degraded.

The first objective is causal reconstruction, not a fairness patch. We need to identify whether the observed change came from native disposition, final-result transport, API capacity handling, queue selection, configured timing, or simply a different provider-completion topology.

## What the locally available SBE traces establish

Across several earlier paired windows, run B began initial fan-out while run A still had unresolved reconciliation or fan-in work:

- 2026-09-02: run A began its wave at 06:30:49 America/Denver; run B began at 06:38:44; run A continued until approximately 06:51.
- 2026-09-03 morning: run A began at 07:18:15; run B began at 07:26:13; run A did not reach review until approximately 07:37.
- 2026-09-03 afternoon: run A began at 15:02:11; run B began at 15:07:19; run A still had reconciliation activity after 15:12.

The create bursts themselves were not concurrent: each six-member initial wave completed its provider-create boundary in roughly two to four seconds. The overlap occurred after detachment, while provider custody and reconciliation for both runs coexisted.

The locally retained Podium/Laurel window is much more serial:

- Podium initial wave: 03:28:32 America/Denver.
- Podium terminal command result: 03:36:54.
- Laurel initial wave: 03:37:40.

This proves that overlapping provider custody is supported historically. The
regression to investigate is increasing peer time-to-first-submit, culminating
in one terminal-boundary-serialized witness; it is not a claim that all overlap
vanished. It does not prove a specific cause.

## Native lifecycle behavior observed

SBE does emit `release_until_due` when retained provider operations are known and none is currently due and no local work is ready. In Podium's trace this occurs, for example, after reconciliation at 03:31:33 and 03:32:21 America/Denver.

SBE also emits `continue_local_cycle / provider_reconciliation_due` when immediately actionable retrieval work remains. A concrete shape is six due actions with a four-member reconciliation cap:

1. the invocation selects four due actions;
2. those four may remain pending;
3. two unselected actions remain due now;
4. the final inspection therefore cannot honestly claim `release_until_due`.

SBE similarly emits `continue_local_cycle / local_work_ready` when completed provider evidence needs deterministic native adoption or fan-in.

These are materially different from provider quiescence. Changing either to `release_until_due` would misstate native truth.

## Leading hypotheses

The hypotheses should be tested rather than ranked by preference:

1. **Final-disposition change.** Older overlapping runs may have returned a final `release_until_due` at a boundary where recent runs return `continue_local_cycle` because more results are immediately due, local work is ready, or topology/version behavior changed.
2. **Capacity-owner preference.** API may correctly preserve an allocation for `continue_local_cycle`, then repeatedly reclaim the incumbent ahead of a never-started peer.
3. **Defer/continue mismatch.** API may interpret `continue_local_cycle` as retaining capacity while still applying a nonzero ordinary defer. Native says “work is actionable now,” but the worker sleeps while continuing to exclude its peer.
4. **Intermediate-versus-final confusion.** A trace-visible `release_until_due` can be superseded by later work within the same invocation. Only the final returned and validated inspection is scheduling authority.
5. **Timing/topology rather than code regression.** Faster provider responses may make work due or locally consumable on nearly every recent turn, leaving fewer genuine quiescent windows than older cohorts had.
6. **Configuration or queue-policy drift.** Capacity count, resume interval, allocation selection priority, or wakeup behavior may have changed independently of SBE.

## Native contract position

`release_until_due` must remain a statement that no native/provider operation is actionable before a bound due time. It must not be overloaded as a cooperative scheduler yield.

If fairness requires a run to surrender capacity while safe, actionable work remains, the system needs one of:

- a distinct final, closed cooperative-yield disposition carrying checkpoint and resume authority;
- an API-owned turn policy at a boundary already proven safe for exclusive workspace access; or
- a different bounded native work unit that reaches an honest existing disposition sooner.

The correct choice depends on exact final-output and queue evidence.

## Required investigation

### Cohort comparison

Select at least one older overlapping pair and one recent serial pair. For each invocation, join:

- API run/job/allocation/lease identity;
- native run and checkpoint identity;
- final returned lifecycle schema/version;
- final capacity disposition, reason, local-work inventory, provider custody, and resume time;
- queue defer/release and next-claim times;
- supporting SBE trace observations, labeled non-authoritative.

Do not compare only create timestamps or intermediate lifecycle log lines.

### Source map

Trace the complete production path for:

- initial-wave detachment;
- provider reconciliation with more due actions than the per-cycle cap;
- provider reconciliation with all operations not due;
- completed-evidence local fan-in;
- external-authority wait;
- terminal/review closeout;
- API capacity release, retained allocation, ordinary defer, and claim ordering.

### Timing verification

Measure configured and observed values separately. In particular, establish the actual deployed ordinary resume interval; older local traces show near-minute gaps in some cohorts, while current API notes describe approximately fifteen seconds.

## Candidate solutions to evaluate only after evidence

1. Immediate same-owner continuation for genuinely actionable native work.
2. Fair scheduler turn selection after a safe API/native command boundary.
3. A new explicit cooperative-yield contract after a bounded unit of native work.
4. Adjusting the reconciliation batch size or draining due retrievals within one invocation.
5. A hybrid: prompt bounded progress, followed by a certified yield when custody remains but exclusive local mutation is no longer active.

Each option must be evaluated for peer time-to-first-submit, total cohort makespan, wakeup punctuality, mutation exclusion, custody preservation, and duplicate-create safety.

## Provider-free proof target

A two-run, one-slot production-boundary fixture should demonstrate:

1. A submits exactly one six-member initial wave and detaches.
2. B receives a turn and submits its own exact initial wave while A retains provider custody.
3. A resumes at or before its lawful due boundary.
4. Due retrieval and local fan-in are neither mislabeled as quiescent nor starved.
5. No workspace has concurrent writers.
6. No request, grant, authorization, provider create, retrieval, adoption, or consumed operation is duplicated.
7. Crash/reclaim and exact replay preserve the same outcome.

Use the real queue/runtime/native adapters wherever practical; a toy scheduler is insufficient evidence.

## Non-goals

- No provider calls or live QA mutations.
- No reinterpretation of trace logs as authority.
- No weakening of external-authority or custody joins.
- No assumption that every stage shares the same safe yield boundary.
- No runtime correction before the older-versus-current final-output comparison is complete.
