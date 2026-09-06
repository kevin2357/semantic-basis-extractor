# Slice 0 — Evidence Manifest and Source Map

## Result

Slice 0 establishes a real peer-latency degradation, but it falsifies a strict
API Sprint 58 cutoff. A retained post-Sprint-58 pair fanned out only 97 seconds
apart, and provider-lifetime overlap continued on September 2 and September 3.
Later pairs show progressively longer peer waits, culminating in Podium/Laurel,
whose peer did not fan out until after the incumbent terminal command result.

The remaining investigation is still justified. It must study increased
peer time-to-first-submit rather than claim overlap disappeared absolutely, and
locate the first code/configuration boundary that reproduces the degradation.

## Evidence manifest

| Evidence | Local source | Authority and limit |
|---|---|---|
| September 2 overlap | `C:\tmp\sbe-worker-render-last-2h-20260902.log` | SBE trace evidence; proves native activity timing, not API allocation mutation |
| September 3 morning overlap | `C:\tmp\sbe-worker-last-2-hours-puff-20260903.log` | SBE trace evidence; proves provider-bound lifetime overlap, not claim rationale |
| September 3 afternoon overlap | `C:\tmp\astrowoof-qa-sbe-worker-logs-20260903T1919Z-to-2319Z.txt` | SBE trace evidence; proves later run fan-out began while peer reconciliation continued |
| Podium/Laurel serialization | `C:\tmp\podium-laurel-sbe-20260906T0915-0930Z.jsonl`, `...0930-0945Z.jsonl`, `...0945-1000Z.jsonl` | Recent SBE trace evidence; does not independently prove API eligibility/selection cause |
| Sprint 58 partial export | `C:\tmp\sprint58-boundary-qa-sbe-worker-logs-20260829T100755Z-to-20260831T120759Z.txt` | Incomplete due to Render throttling; not suitable for absence claims |
| Sprint 58 paced export | `C:\tmp\sprint58-boundary-qa-sbe-worker-logs-paced-20260829T100755Z-to-20260831T120759Z.txt` | Complete paced request set; relevant cutover windows are empty |
| API Sprint 58 history | API commits `31237f6` through `bc5873f` | Exact source history and documentation |
| SBE companion | SBE commit `3709f18`; release `0.4.31` | Exact source history; availability-reader addition |

All times in this document are America/Denver unless suffixed with `Z`.

## Behavioral witnesses

| Witness | Run A fan-out | Run B fan-out | Run A activity after B fan-out | Classification |
|---|---:|---:|---:|---|
| September 2 | 06:30:49 | 06:38:44 | through approximately 06:51 | provider-lifetime overlap |
| September 3 morning | 07:18:15 | 07:26:13 | through approximately 07:37 | provider-lifetime overlap |
| September 3 afternoon | 15:02:11 | 15:07:19 | reconciliation after 15:12 | provider-lifetime overlap |
| Podium/Laurel, September 6 | 03:28:32 | 03:37:40 | Podium terminal at 03:36:54 | effective serialization |

The paced boundary export additionally contains a post-Sprint-58 pair with
initial-wave starts at 12:43:31Z and 12:45:08Z on August 30: a 97-second gap.
That is the strongest surviving approximation to the owner's earlier
“within about a minute” behavior. Later retained pairs show gaps of roughly five
to nine minutes. The regression signal is therefore increasing peer latency,
not a binary transition from overlap to no overlap.

These rows do not claim overlapping create bursts. Each initial six-member create
burst was short. The older property was that a peer obtained capacity and
submitted while the incumbent still retained provider-bound work.

## Identity correction

The recent local witness is Podium/Laurel. Earlier notes that name Podium/Goldie
must not be joined to it without exact API and native IDs. Subject labels are
descriptive only and are not authority.

## Historical evidence ceiling

- The current QA database has no surviving pre-Sprint-58 generation runs.
- Render Hobby retention no longer contains the immediate before/after window.
- The paced export rules out CLI throttling as the reason those exact cutover
  windows are empty.
- Four later August 30 runs in the paced export are contextual, not immediate
  boundary evidence.
- No exact historical API allocation/lease/eligible-set table can now be built
  for the desired eight-run population.

This ceiling is final unless a separately retained immutable database backup or
API log archive is identified. No missing IDs will be inferred.

## SBE production source map

### Initial provider creation

`initial_wave.py` freezes six initial members, permits at most six concurrent
creates, and durably persists returned provider identities. The create boundary
is independent from later capacity scheduling.

### Bounded reconciliation

The initial-wave contract limits due retrieval selection to four members per
cycle. `temporal_lifecycle.py` derives `due_action_ids` from provider actions
whose `resume_not_before` is due and selects at most four. When unselected due
actions remain, `provider_reconciliation_due / continue_local_cycle` is truthful.

### Provider quiescence

When custody remains but no action is due and no local work is ready, lifecycle
inspection publishes `release_until_due` and an exact `not_before`. That is a
native no-work-until-time assertion.

### Completed evidence and fan-in

Completed provider evidence becomes deterministic local work. Until that work
is durably consumed, SBE may publish `local_work_ready /
continue_local_cycle`. It cannot truthfully call the state quiescent.

### External authority and terminality

External-authority and terminal/review branches use their own closed
dispositions. Neither may be collapsed into provider quiescence. A sealed result
can dominate later selection, but its discovery does not define fairness.

## API production source map

### Claim and allocation

`ExecutionQueueService.claim_next_sbe_capacity()` delegates to `_claim_next()`.
When active allocations fill the configured pool, `_claim_next()` restricts
eligible run IDs to current allocation owners. The source comment identifies
this as protection against capacity head-of-line deadlock.

The behavior originated before Sprint 58 (`dc4cae0`, August 24). It therefore
cannot alone explain a loss of overlap after September 3, although it is the
mechanism by which retained ownership can exclude a peer.

### Exact provider-pending release

`SbeProviderPendingCapacityReleaseService` accepts only a validated final
`release_until_due`, defers the job until the native due time, and releases the
run allocation atomically. This permits another run to acquire the slot.

### Ordinary continuation

A final `continue_local_cycle` becomes `local_continuation_required=true`.
Ordinary handling defers the job while preserving its run-level allocation.
With a full pool, the next claim is limited to existing owners.

### Terminal preflight

Sprint 58 added exact terminal-result availability discovery immediately after
workspace preparation and before legacy bridging/lifecycle selection. A found
sealed result enters exact terminal ingress. Explicit absence continues the
ordinary selector.

This can shorten or correctly terminate a run, but does not change the
nonterminal provider-pending release or allocation-selection predicates.

## Timing categories

Future replay and traces must record separately:

1. native command execution duration;
2. configured queue defer (`available_at - disposition time`);
3. post-availability claim latency;
4. total allocation ownership duration.

The previously observed 40–60-second gaps cannot be called the configured defer
without these joins. Current documentation's approximately 15-second ordinary
defer is a separate value.

## Slice 0 conclusion

1. SBE still has truthful quiescent and actionable-work distinctions.
2. API still has a retained-owner exclusion mechanism when capacity is full.
3. Sprint 58 did not edit that mechanism or the provider-pending release path.
4. A 97-second post-Sprint-58 pair and later overlap disprove a strict immediate
   cutoff.
5. The evidence suggests progressive degradation from near-overlap to five-to-
   nine-minute gaps and finally a terminal-boundary wait; the exact first
   divergence remains open.
6. Slice 1 should use Sprint 58 as a negative control and identify later commits
   for the API-side replay candidate set.
