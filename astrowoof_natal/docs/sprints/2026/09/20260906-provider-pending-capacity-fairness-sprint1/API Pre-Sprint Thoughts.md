# API Pre-Sprint Thoughts

## Explicit outcome

First establish why paired runs that formerly appeared to share the one SBE slot after initial provider submission now appear serial. The concrete case is run A submitting an initial wave and apparently waiting on providers while run B does not receive a turn to submit its own wave.

The immediate investigation question is narrow: **what final capacity disposition did SBE return at the relevant provider-pending boundary, and did API honor that exact final result?** Do not begin with a general fairness redesign or presume the correct solution is a new disposition.

This is not a request to make SBE report `release_until_due` when provider/local work remains actionable. A false release would blur native scheduling truth with API policy and could permit unsafe concurrent progression.

## Preliminary evidence from the most recent successful pair

API joined the authoritative lifecycle records with SBE worker traces for Podium/Goldie and found two distinct facts:

1. **The final release path works.** Goldie's final persisted lifecycle inspection at 05:26:53 America/Denver returned `release_until_due`, due at 05:27:10. API released capacity, and Goldie's next cycle began around 05:27:13.
2. **Podium's earlier hold was not a final release ignored by API.** Through roughly 05:14--05:23, Podium repeatedly ended native cycles as `continue_local_cycle`, including `provider_reconciliation_due`, local fan-in, and external-authority continuation. Goldie began native work shortly after Podium closed out.
3. **An SBE trace snapshot is not necessarily the final command outcome.** `✨🐶` logs may expose an intermediate lifecycle inspection with `release_until_due` before subsequent work in that same invocation changes the final returned inspection. API must only schedule from the final schema-validated inspection it receives and records; it must not act on a log line.

This single pair proves neither that there was no regression nor that the earlier observed overlap was illusory. It only shows the need to compare exact final outcomes for an older overlapping cohort and a recent serial cohort before choosing a repair.

## Current API behavior relevant to native design

After SBE returns its final cycle result, API currently:

- releases capacity on the exact final `release_until_due` result;
- follows the distinct `await_external_authority` handling path;
- otherwise defers the owning SBE job for its ordinary roughly 15-second resume interval while retaining the allocation.

The queue then favors active allocation owners. Therefore a run that repeatedly returns `continue_local_cycle` can be reclaimed ahead of a peer that has never had capacity. This is why a peer can be delayed even though the owner has provider custody outstanding.

An API-only immediate-resume change would remove the 15-second gaps. It might improve throughput, but it would not by itself create the desired peer turn; it can cause the incumbent to finish its locally actionable work still faster.

## Investigation questions for the SBE companion plan

1. **Did SBE's final provider-pending output change?** Select one earlier overlapping pair and one recent serial pair. For the initial-wave boundary, reconstruct final command output, not merely intermediate `✨🐶` trace lines. Establish whether SBE returned `release_until_due`, `continue_local_cycle`, `await_external_authority`, or another disposition and branch reason.

2. **If the final outcome remained `release_until_due`, what API-visible resume/due data was bound?** Identify whether a change in due timestamp, provider-result timing, release safety predicate, or output schema explains a different API outcome.

3. **If the final outcome changed, what native state/topology made it change?** Determine whether it is intended (for example, results already due and actionable) or an unintended regression in inspection/selection behavior.

Only after those three questions have evidence-backed answers should the companion plan choose a runtime correction.

## Conditional design questions if investigation proves a remaining scheduling gap

1. **Can native SBE expose a final, closed, safe yield boundary after a bounded unit of work?** If the desired behavior is to yield after initial-wave submission or after a bounded reconciliation batch, that boundary must be final command output with the exact checkpoint/revision, pending-provider inventory, resume condition, and safe single-writer semantics.

2. **When is a yield semantically honest?** `release_until_due` must remain reserved for no currently actionable provider retrieval/local work. If SBE needs a different voluntary/cooperative fairness yield while work *is* actionable, it should have a distinct name and closed meaning rather than overloading that disposition.

3. **What is the smallest useful unit?** Candidates may include one initial provider-create wave, one reconciliation batch, or a completed local fan-in transition. The choice must avoid both unbounded monopolization and pathological yield/reclaim thrash.

4. **What resume information must SBE bind?** The handoff should not manufacture recovery or re-authorize work. It must retain exact provider identities, action keys, consumed/available evidence, checkpoint generation, and any external-authority request/binding necessary to resume safely.

5. **Which paths share the topology?** Initial waves, creative retries, polish, critic, candidate, ordinary reconciliation, and Batch/bounded operations may not all have the same safe yield point. Inventory source topology before broadening scope.

6. **How do we qualify this without providers?** A joint fixture/simulator needs a two-run/one-slot case: A submits a wave, waits safely; B performs useful initial submission; A resumes at due time; neither duplicate-submits, concurrently mutates a workspace, loses custody, or starves. Include immediately-due reconciliation and local-work-ready negative cases.

## Contract guardrails

- Do not make API infer fairness permission from SBE trace logging.
- Do not broaden `release_until_due` to cover immediate native work.
- Do not make capacity policy an alternate route around exact external-authority request validation or action/budget consumption.
- Do not alter provider result identity/custody merely because scheduling yields.
- A scheduler decision must not cause two native mutations for the same workspace to run concurrently.
- A separate voluntary-yield disposition, if needed, must be final, versioned, and explicit about successor/resume authority.

## Suggested first planning deliverables

- Joint terminology: provider quiescence, immediately actionable native work, cooperative fairness yield, and scheduler turn.
- A compact production trace timeline for Podium/Goldie joined against final persisted API decisions.
- Source topology of all candidate native branches and their current capacity dispositions.
- One proposed smallest safe cross-repo vertical slice with provider-free qualification and a two-run/one-slot trace.
- Explicit non-goals: live-run changes, provider calls, deployment, or reinterpreting historical SBE trace logs as authority.

This shell intentionally contains no `PLAN.md` yet. The next step is shared discovery and a jointly reviewed plan, not implementation.
