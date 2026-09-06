# API Joint Review — SBE Slices 0–1

## Disposition

**Approved with one reframing refinement.** SBE's Slices 0–1 correctly replace
the unsupported claim that provider-lifetime overlap vanished at Sprint 58 with
the narrower, evidence-backed problem: peer time-to-first-submit degraded over
later cohorts and eventually reached a terminal-boundary wait.

The Sprint 58 API/SBE changes are an appropriate **negative control**, not the
leading regression boundary. API's independent source audit agrees: the final
Sprint 58 commit `bc5873f` changed only the terminal-review QA fixture/test and
version/docs. The earlier Sprint 58 production commits tightened sealed-result
identity/preflight, but did not alter ordinary nonterminal capacity disposition,
provider-pending release, queue defer, full-pool eligibility, or the native
four-action reconciliation bound.

## Deployment and witness check

The September 2–3 witnesses are post-Sprint-58 deployments:

| Witness period | Deployment/source evidence | Sprint 58 ancestry conclusion |
| --- | --- | --- |
| Sep. 2 overlap | QA rollout trace binds the fleet to API `f5b4f9b` | `bc5873f` is an ancestor of `f5b4f9b`. |
| Sep. 3 morning overlap | The SBE 0.4.40 intake/launch era is represented by API `299a1dd` and its rollout records | `bc5873f` is an ancestor of `299a1dd`. |
| Sep. 3 afternoon overlap | The later 0.4.41 intake/rollout era is represented by `0aba8d1` and descendants | `bc5873f` is an ancestor of `0aba8d1`. |

The exact API image digest for every historical SBE log line is not retained,
so this is a deployment-era/ancestry conclusion rather than an invented
per-event image join. It is nevertheless sufficient to reject a strict
post-Sprint-58 loss-of-overlap theory.

## Narrow replay boundary

Use two bounded comparisons, in this order:

1. **Negative control:** parent of Sprint 58 terminal preflight versus its
   release tree, with the same nonterminal final cycle result and explicit
   terminal-result absence. The expected result is identical ordinary
   provider-pending capacity behavior. Add a sealed-result case only to prove
   terminal precedence remains intact.
2. **First post-overlap scheduler-touching candidate:**
   `d451a88fdfa3dac5125ffe0ca462618097e8423b` (parent) versus
   `8c389b39857f9c6f8a2974b152bacdb0319307e7`.
   This is the first commit after the September 3 overlap witnesses that
   changes `ExecutionQueueService` and `SbeReadingWorker` capacity handling.
   Its intended scope is retry-ceiling terminal cleanup, so it is *not*
   presumed to explain healthy provider-pending serialization. The replay must
   show whether it changes the two-run/one-slot result at all; a no-difference
   result removes it cleanly.

No configuration mutation was found in the same interval for
`sbe_worker_resume_seconds`, SBE slot-limit code/configuration, active-run
eligibility, or the ordinary `release_until_due` release service. Preserve the
one-slot and 15-second ordinary-resume configuration in replay; do not
introduce a configuration theory without an immutable manifest/deployment fact.

If comparison 2 is equal for the healthy provider-pending topology, do not
attribute terminal-delivery commits by title. Freeze a source range
`299a1dd..e783078`, then test only an observed final-result/queue predicate
that differs in that range. If no such predicate affects the fixture, classify
the historical cause as unproven and move directly to the present-day policy
question rather than performing a speculative commit-by-commit archaeology.

## Required joined fixture shape

The API Slice 0 source map agrees with SBE's fixed semantics:

- API schedules only from the exact final validated result, never an
  intermediate trace event.
- `release_until_due` remains a native no-work-before-exact-time assertion;
  it cannot become a fairness signal.
- `continue_local_cycle / provider_reconciliation_due` with two unqueried due
  actions after a four-action bounded retrieval is actionable and must retain
  that truth.
- `continue_local_cycle / local_work_ready` is likewise not provider
  quiescence.
- Full-pool active-owner eligibility is an existing single-writer/custody
  safeguard. It is the mechanism through which an incumbent may exclude a
  peer, not itself evidence of when a lawful turn boundary exists.

For Slice 2, use real API queue/capacity/lease/defer selection and validated
public SBE result documents where practical. Record native duration, final
ingestion time, `available_at`, allocation owner, eligible set, next claim,
and due-time wakeup lateness separately. The test must prove no duplicate
provider work and no concurrent same-workspace writer before it can recommend
any fairness policy.

## API/SBE ownership and next gate

SBE owns a truthful final lifecycle state and any new safe-turn fact; API owns
durable queue/capacity selection. API must not infer a cooperative yield merely
from elapsed time, provider identity, or a diagnostic trace.

I approve SBE to begin Slice 2 as the provider-free characterization/replay
work described above. No runtime policy or public contract change is approved
until the joined replay identifies either a real divergence or the evidence
that existing closed facts are insufficient for bounded peer access.
