# Pre-Sprint Huddle

## Shared objective

Explain, with final authoritative evidence, why paired QA runs formerly overlapped their provider-bound portions while recent pairs appear effectively serialized behind one SBE capacity owner. Then select the smallest safe correction that improves peer time-to-first-provider-submission without weakening native truth, provider custody, external authority, or workspace single-writer exclusion.

This is an investigation gate. Neither repository should implement a fairness change until the older-overlapping and recent-serial timelines are joined at the final command/result and API queue/allocation boundaries.

## Materials considered

- `API Pre-Sprint Thoughts.md`
- `SBE pre-sprint thoughts.md`
- Locally retained ✨🐶 worker traces covering multiple paired cohorts
- Current SBE lifecycle/capacity reducer
- Current API cycle-result and capacity-release/defer paths

## Reactions to both initial-thoughts documents

### Where the documents agree

Both documents now support the following:

1. `release_until_due` is a native quiescence claim, not a generic fairness hint.
2. SBE must not publish it while retrieval is already due or deterministic local fan-in is ready.
3. Intermediate ✨🐶 lifecycle inspections are diagnostic observations; the final returned, schema-validated inspection is the scheduling authority.
4. API currently releases capacity for an exact final `release_until_due` and treats `continue_local_cycle` differently.
5. Repeated `continue_local_cycle` results can let an incumbent capacity owner outrank a peer that has never received a slot.
6. Merely making incumbent continuation faster may improve makespan but does not prove fairness.
7. Any correction must preserve exact request/grant/action bindings, provider custody, checkpoint identity, replay safety, and one writer per workspace.
8. A two-run/one-slot provider-free production-boundary qualification is required.

The initial disagreement—“SBE forgot to release” versus “API ignored a release”—is therefore not the current evidence-backed question. The open question is whether recent native topology legitimately presents continuous actionable work, and what safe bounded-turn rule should apply if it does.

### SBE reaction to the API initial thoughts

The API note usefully supplies the authoritative half SBE traces cannot establish:

- Goldie's final persisted `release_until_due` was honored.
- Allocation-aware claim selection favors an existing owner.
- Other final outcomes use an ordinary defer while the allocation remains owned.
- A trace-visible release can be superseded before the command returns.

SBE agrees that these facts rule out a blanket “API ignores `release_until_due`” diagnosis.

Two items require exact verification during Slice 0:

1. The API note describes an approximately 15-second ordinary resume interval. Several older local traces show approximately 40–60 seconds between retained-owner reconciliation cycles. This may be historical configuration drift, queue latency, or a different measured interval. Record configured and observed timing for each comparison cohort.
2. The API note refers to Podium/Goldie, while the locally retained paired files and editorial inventory include Podium/Laurel. Freeze API run ID, native run ID, subject, log window, and deployment version before joining evidence so names or cohorts are not accidentally conflated.

SBE also agrees that immediate continuation is not automatically a fairness improvement. It can reduce dead time while allowing the incumbent to monopolize the slot more efficiently.

### API-facing reaction to the SBE initial thoughts

The SBE note adds concrete historical proof that provider custody—not initial create execution—overlapped between paired runs.

The precise wording matters:

- Observed six-create bursts are individually short and have not been shown to overlap each other.
- Earlier run B did begin its fan-out while run A still had provider custody, reconciliation, or fan-in outstanding.
- The desired recovered property is therefore overlapping provider-bound run lifetimes and bounded peer access—not necessarily simultaneous provider-create calls.

The SBE source behavior also explains why some final `continue_local_cycle` results are honest. With six actions due and a four-action reconciliation cap, one invocation can query four while two remain due and unqueried. A final `release_until_due` would be false. Likewise, completed provider evidence may make local fan-in immediately ready.

This shifts the likely design question from “change the boolean/disposition” to “define a safe scheduling turn after bounded progress.”

## Frozen terminology

- **Provider quiescence:** Provider custody exists, but no retrieval or native local work is actionable before a bound due time.
- **Immediately actionable native work:** Due retrieval, completed-evidence adoption/fan-in, or another exact local operation that can advance native truth now.
- **Capacity ownership:** API's durable right for one run/job to occupy scarce SBE execution capacity.
- **Scheduler turn:** One bounded opportunity for a run to execute at a safe exclusive-workspace boundary.
- **Cooperative fairness yield:** A possible future explicit handoff while additional work remains actionable. It is not `release_until_due`.
- **Create-burst overlap:** Two runs concurrently crossing provider-create calls. This has not been established or requested.
- **Provider-lifetime overlap:** Run B submits its wave while run A still retains provider operations or unfinished fan-in. This existed in older traces and is the practical target.

## Joint causal questions

### Question 1: Did final native output change?

For one older overlapping pair and one recent serial pair, recover each relevant command's final:

- lifecycle schema/version;
- checkpoint/revision identity;
- capacity disposition and reason;
- provider-custody inventory;
- local-work inventory;
- due action IDs and earliest resume time;
- selected command/branch;
- external-authority request presence;
- SBE artifact/runtime version.

If historical final command output is unavailable, state that evidence ceiling explicitly and select the strongest available API-persisted record.

### Question 2: Did API handling or scheduling change?

For the same commands, join:

- job, attempt, lease, and allocation IDs;
- capacity limit and allocation owner;
- result-ingestion timestamp;
- release or defer operation;
- configured retry/resume interval;
- queued `available_at`;
- next selected job and claim timestamp;
- reason the incumbent or peer won selection.

### Question 3: Was the changed behavior legitimate topology?

Determine whether recent runs had:

- more responses completing near the first due boundary;
- remaining unselected due actions after the four-member cap;
- more immediate local fan-in/retry/polish work;
- external-authority continuation;
- fewer genuine no-work-until-due intervals;
- a changed SBE/API version, reconciliation policy, capacity configuration, or queue priority.

### Question 4: Where is the first safe fairness boundary?

Inventory whether a peer turn is safe after:

- initial-wave provider identities are all durable;
- one bounded reconciliation batch is checkpointed;
- completed evidence is atomically adopted;
- an external-authority request is durably published;
- a final `release_until_due`;
- another existing command boundary.

A fairness turn must never permit concurrent writers for the same workspace or create alternate authority for native/provider work.

## Slice 0 evidence plan

1. Freeze one older overlapping cohort and one current serial cohort by all public identities and deployed versions.
2. Produce a single chronological table containing final SBE result, API persistence, capacity mutation, defer/release, and next claim.
3. Place intermediate trace observations in a separate supporting column.
4. Compute:
   - peer time-to-first-submit;
   - incumbent time holding allocation;
   - useful native execution time;
   - retained-owner sleep time;
   - provider-lifetime overlap;
   - due-time wakeup lateness.
5. Identify the first row where cohort behavior diverges.
6. Pause for joint review before selecting a design.

## Conditional solution matrix

| Option | Likely benefit | Principal risk/question |
|---|---|---|
| Immediate incumbent continuation | Removes sleep while actionable work exists | May worsen peer fairness |
| API scheduler turn at an existing safe boundary | No new native disposition if exclusion is already proven | API must not infer native resumability or allow concurrent workspace use |
| Explicit cooperative-yield contract | Closed, auditable cross-repo semantics | New contract/version and more implementation scope |
| Drain more due retrievals per invocation | Fewer retained/deferred cycles | Longer incumbent monopolization; bounded-I/O policy changes |
| Bounded progress then certified yield | Balances progress and peer access | Requires precise progress budget and replay-safe resume |

No option is approved yet.

## API follow-up reactions after reviewing the huddle

### Alignment

The huddle's revised target is the correct one: recover **provider-lifetime overlap** where it is safe, rather than require simultaneous initial provider-create bursts or prematurely choose a generic fairness mechanism. The prescribed Slice 0 join is the necessary gate before either repository changes runtime behavior.

The distinction between a final returned inspection and a trace-visible intermediate inspection is especially important. API can only release or retain capacity from the final schema-validated result it has durably ingested. A trace line may explain why a later final result changed, but can never itself authorize a capacity mutation.

### API-specific corrections and evidence rules

1. **Freeze identities before interpretation.** The huddle correctly notes a Podium/Goldie versus Podium/Laurel naming discrepancy. Slice 0 must use a manifest with API run ID, native run ID, reading/subject label, worker resource, log-export window, API commit/image, SBE wheel version, and timezone. Names alone are not adequate join keys.

2. **Separate three elapsed-time categories.** A large gap between final lifecycle records is not necessarily a generic API defer. Record separately: (a) native command execution duration, (b) queue `available_at`/configured defer interval, and (c) post-availability claim latency. The API default ordinary continuation interval is approximately 15 seconds, but historical 40--60 second gaps may be dominated by native execution, queue polling, or historical deployment configuration. The data must decide.

3. **Treat allocation priority as a mechanism, not a diagnosis.** API's active-allocation preference explains how an incumbent can reclaim capacity after a retained defer. It does not prove that the incumbent should have yielded, or that it prevented the peer from claiming after a lawful release. Slice 0 should record the eligible-run set at each claim and the exact reason the selected job was eligible.

4. **External authority is neither automatically quiescent nor automatically monopolizing.** Record its final disposition, successor identity, and whether capacity was actually held/released. Do not fold `await_external_authority` into either provider quiescence or immediate local work without the exact final lifecycle result.

5. **The older comparison cohort is essential.** The recent successful pair proves API honored at least one final `release_until_due`; it cannot explain the earlier observed overlap. The planned older-versus-recent comparison is therefore a required causal test, not supplementary historical color.

### Minimum API artifacts for the investigation gate

API should prepare, without state mutation:

- a normalized event table keyed by native run, attempt, final-result/event identity, and timestamp;
- capacity allocation and lease lifetime joins, including release/defer operations and queue availability;
- job claims/attempts for both peer runs, including the selection state immediately preceding each claim where retained data permits it;
- exact application configuration/worker image facts relevant to capacity count and resume timing; and
- a clearly labelled evidence ceiling for historical fields that were not persisted.

If this table shows a final `release_until_due` followed by an incumbent reclaim while a peer was eligible, that is an API scheduling/release defect. If instead it shows continuous final `continue_local_cycle` work, the next question is whether an existing safe command boundary can legally yield a peer turn; it is not evidence to overload `release_until_due`.

### Approval for next step

Approved to proceed with the huddle's Slice 0 provenance and divergence analysis only. No runtime scheduling, SBE disposition, reconciliation-cap, live-run, or deployment change is implied by this approval.

## API Sprint 58 boundary hypothesis

### Owner recollection and falsifiable claim

The owner recalls that effective serialization first became noticeable shortly after API Sprint 58's terminal-result-first lifecycle handoff. This is a useful, falsifiable boundary hypothesis--not a causal conclusion. The investigation should test whether the change was introduced by Sprint 58 itself, by an adjacent deployment/configuration change, or merely coincided with a changed native/provider topology.

The two repository-history anchors are exact:

| Boundary | Git commit | America/Denver time |
|---|---|---|
| Sprint 58 `PLAN.md` created | `31237f6e369fb411732769bb9675a03b599897e3` | 2026-08-30 04:07:55 MDT |
| Sprint 58 `LOG.md` last updated | `bc5873f590a0de0154754c0a74f52dcb7a04f045` | 2026-08-30 06:07:59 MDT |

The intended comparison population is the last four live test runs before the first timestamp and the first four live test runs after the second timestamp.

### Current evidence ceiling: requested eight-run table cannot yet be truthfully populated

The current QA database was reset after this period. A read-only query found **no** `generation_runs` before 2026-08-30 04:07:55 MDT. Its first surviving rows after the second boundary are from 2026-09-04, so they are not valid immediate-post-Sprint-58 comparison candidates.

API attempted to export QA SBE worker logs from 2026-08-29 10:07:55Z through 2026-08-31 12:07:59Z in 15-minute windows:

`C:\tmp\sprint58-boundary-qa-sbe-worker-logs-20260829T100755Z-to-20260831T120759Z.txt`

This first attempt is **not a complete archive**: its unpaced 201-request loop triggered Render throttling in 149 windows, beginning at 2026-08-29 21:37:55Z. It must not be used to conclude that logs were unavailable before that point or that the observed August 31 events were the first events in the source window. A paced, resumable re-export is required before this source can support the boundary hypothesis.

The partial file happens to contain three post-boundary native starts, but no surviving API-run-ID correlation needed to populate the requested eight-run table:

### Paced re-export result

API then completed a fresh, paced 30-minute-window export with no Render CLI throttling:

`C:\tmp\sprint58-boundary-qa-sbe-worker-logs-paced-20260829T100755Z-to-20260831T120759Z.txt`

All 101 requests completed without a CLI `error listing logs: too many requests` failure. The raw log contains historical provider-side “too many requests” responses; those are events emitted by the workload, not failures of this export. The clean windows spanning Sprint 58's 2026-08-30 10:07:55Z--12:07:59Z cutover are empty. The first nonempty retained window begins at 14:37:55Z (08:37:55 MDT), after the exact cutover. Thus the original before/after cohort is genuinely unavailable from this worker resource's current retention, but four later native/API joins are now recoverable as contextual, not causal, examples.

| Position | API run ID | Native run ID | Start | Stop | Status |
|---|---|---|---|---|---|
| Pre 1 | not recoverable from current QA DB / incomplete log export | -- | -- | -- | evidence unavailable pending paced re-export |
| Pre 2 | not recoverable from current QA DB / incomplete log export | -- | -- | -- | evidence unavailable pending paced re-export |
| Pre 3 | not recoverable from current QA DB / incomplete log export | -- | -- | -- | evidence unavailable pending paced re-export |
| Pre 4 | not recoverable from current QA DB / incomplete log export | -- | -- | -- | evidence unavailable pending paced re-export |
| Post 1 | `9bbc2acc-4f78-436e-9a19-c617d7397fac` | `612ca77bca4dc64419a236b9000f3a1641ab181d6ff139a9238b0d2e07d25ad2` | 2026-08-30 09:40:15 MDT | 2026-08-30 09:53:16 MDT (last observed) | first recovered run after retention gap; not immediate cutover evidence |
| Post 2 | `b39c8b14-d0c7-440a-b5b8-bd4bb0d85205` | `53bacbe893fa722a50a251111d9263a7c703da28c088b30fcdc9ff3798a8dea4` | 2026-08-30 12:43:20 MDT | 2026-08-30 13:01:45 MDT (last observed) | recovered contextual run |
| Post 3 | `76c883b5-6a01-4025-8b12-f6d9ed0b8519` | `8c7446005d39963dfb562bc7d4985de9d124b0fed9ee05d90a347ff27a57714d` | 2026-08-30 12:44:58 MDT | 2026-08-30 12:50:58 MDT (last observed) | recovered contextual run |
| Post 4 | `ae32b064-c946-43aa-b157-56b0b336adb7` | `90efb386a228801ddafb4907da19216d85b8a0456a55298618b076de0c6e3400` | 2026-08-30 19:47:26 MDT | 2026-08-30 19:51:09 MDT (last observed) | recovered contextual run |

These rows are deliberately **not** offered as plausibility confirmation. They document the current evidence ceiling and prevent later readers from confusing later same-day contextual traces with the exact August 30 before/after cohort. “Last observed” is not an authoritative terminal/stop time.

### Next lawful evidence source

To test the hypothesis, locate a retained immutable source that contains both API and native identifiers for the actual late-August runs: a pre-reset database backup/export, an archived API worker log, a dated qualification state file, or a sprint artifact already carrying those joins. Do not infer missing run IDs from dog names, deployment dates, or native trace order. Once such a source is identified, replace the eight evidence-ceiling rows above with the exact IDs and start/stop times, then perform the final-outcome/capacity join specified by Slice 0.

## Joint acceptance target

A provider-free production-path qualification must prove:

1. Run A submits six initial actions exactly once and detaches with durable identities.
2. Run B obtains a bounded turn and submits six initial actions exactly once while A remains provider-bound.
3. A resumes no later than its lawful due boundary.
4. Due retrieval and local fan-in advance without being mislabeled as quiescent.
5. No two commands mutate the same workspace concurrently.
6. No provider create, retrieval, action consumption, authority grant, or local operation is duplicated.
7. Crash/reclaim and replay retain the same custody and scheduling result.
8. Neither run can starve indefinitely under a deterministic clock and bounded scheduler.

## Scope guardrails

- Provider-free; no live QA/R2/provider mutation.
- Logs inform reconstruction but never grant transition authority.
- No false `release_until_due`.
- No scheduling shortcut around v1/v2 external authority.
- No assumption that Batch, bounded, critic, candidate, polish, and initial-wave paths share a fairness boundary.
- No implementation before the Slice 0 divergence point is evidenced and jointly reviewed.
