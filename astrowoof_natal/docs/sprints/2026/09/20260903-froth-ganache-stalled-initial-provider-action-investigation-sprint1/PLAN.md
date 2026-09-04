# Froth / Ganache stalled initial-provider action investigation — plan

**Status:** Slices 0–2 complete; Slice 3 clean-wheel qualification passed
under candidate version 0.4.42 and awaits final release review. The initial
Slice 2 terminal-review proposal was withdrawn: Ganache's error is a legacy
theme-group assembly requirement, not a deck-validity condition. Read-only
checkpoint evidence confirms that Froth is ordinary retained provider custody.
No retained run has been resumed or mutated.

## Objective

Separate two superficially similar initial-wave stalls without resuming either
run, retrieving a provider response, or mutating retained state:

- **Froth:** determine whether its remaining `provider_created` action is
  ordinary retained provider custody, a stale API projection, or an SBE
  lifecycle/receipt mismatch.
- **Ganache:** establish why a completed initial action repeatedly re-entered
  reconciliation/local finalization until API retry attempt 64, and remove the
  dormant theme-group feature from final deck validity and delivery handling.

## Known trace facts (not transition authority)

- Froth (`ea226…92b78`) entered generation 7 after reconciliation with one
  retained provider action, no local continuation, and SBE's
  `release_until_due` disposition. At `21:12:16Z` it published a
  `provider_pending` result after the remaining provider response was still
  not due. This is consistent with live custody, not yet proof of its current
  provider state.
- Ganache (`41e6…472f`) had five `REPORTED` and one `WAITING` initial action.
  Its remaining provider ID `resp_01c199…` was retrieved as `completed` at
  `22:09:18Z`; SBE selected the corresponding local continuation and accepted
  pass 3. Final assembly then raised `AssemblyContractError`: the generated
  `ASSIGN THEME GROUPS.md` referenced unknown Interdogpendence chapter
  `grounded_companionship`.
- The CLI emitted no sealed typed result for that exception. API attempted to
  parse empty stdout, raised `CalledProcessError`, and classified
  `sbe.dependency.command_failed` as retryable. The same state was replayed.

Those observations establish a strong Ganache hypothesis, but the current
checkpoint/result/journal joins remain the native authority.

## Safety boundary

- Worker remains suspended.
- No resume, reconciliation, provider request, R2 write, repair, deletion,
  lease change, API database mutation, or new authority/provider work.
- Exact R2 `HEAD`/`GET` only after API provides an immutable coordinate packet
  and expressly authorizes the named objects. No listing.
- Logs are diagnostic evidence. Snapshot-validated workspace artifacts and
  sealed public results are the transition authority.

## Slice 0 — Freeze evidence and inspect current native truth

1. Preserve relevant trace excerpts with run/action/provider/result identity,
   timestamps, state revision, workspace fingerprint, selected branch, and
   subprocess outcome.
2. Request a minimal coordinate packet for each run's latest accepted
   checkpoint plus (if separate) the retained result/index object. Validate
   packet hashes before exact `HEAD`/`GET`.
3. Offline-validate archive/snapshot and inventory joins. For each action,
   record only safe identifiers and the native action state, provider identity,
   reconciliation outcome, local-work operation/consumption state, and any
   sealed result/receipt identity.
4. Establish independently:
   - Froth: whether the one provider-created action is still pending/due,
     completed-but-unadopted, ambiguous, or absent from the native inventory.
   - Ganache: whether the assembly failure is persisted as native review or
     merely escapes after an otherwise valid checkpoint; whether the same
     native checkpoint was replayed across API attempts.

**Completed evidence:** Both exact archives passed the one-HEAD/one-conditional-
GET identity checks and their declared archive inventories passed offline path,
member-size, member-hash, and aggregate-size validation. See `SLICE 0 -
CHECKPOINT FINDINGS.md`.

**Gate:** publish a fact/hypothesis matrix. Do not make a source change merely
because the trace has a plausible explanation.

## Slice 1 — Classify containment and the correct native/API boundary

For each confirmed condition, decide which component owns the correction:

| Condition | Expected disposition | Likely owner |
| --- | --- | --- |
| Froth provider action remains genuinely pending/not due | release capacity; later SBE-selected retrieval only | no runtime patch unless API routing disagrees |
| Froth evidence complete but native inventory does not join it | typed integrity/review, no create | SBE contract/runtime investigation |
| Ganache legacy theme artifact is malformed after final provider custody resolves | ignore the dormant artifact; complete ordinary finalization | SBE assembly/production workspace generation |

Specify any public contract addition narrowly: typed cause, pre/post snapshot,
action inventory/custody closure, and exact invocation/result identity. Do not
make logs authoritative and do not reintroduce theme-group runtime QA merely to
repair a historical artifact.

**API review constraints recorded:**

- Froth is explicitly out of SBE runtime scope. API will inspect its own
  due-time scheduling, queue-eligibility, and worker-claim trail; SBE must not
  add retries, receipt repair, or provider creation to compensate.
- Theme groups are a dormant, unimplemented filtering feature. They cannot
  participate in final deck validity, finalization disposition, delivery
  handling, advisories, or prompt-required work.
- Legacy `ASSIGN THEME GROUPS.md` artifacts remain tolerated for historical
  workspace compatibility but are ignored by assembly.
- New production split workspaces must not ask the model to create that
  artifact. Explicit test fixtures may still create one to verify that legacy
  content is ignored.
- The later reproduction must use no provider I/O and prove a malformed legacy
  artifact cannot force a generic retry or leak placeholder fields into output.

**Gate:** joint SBE/API review before source implementation.

## Slice 2 — Make the dormant feature structurally non-participatory

- Treat legacy `ASSIGN THEME GROUPS.md` as opaque retained compatibility data:
  assembly must neither parse nor validate it, and multi-pass assembly must not
  require it.
- Strip inactive registry/assignment fields from the delivered deck so stale
  `__LLM_FILL__` values cannot leak into output or trip the general placeholder
  invariant.
- Stop production split pass six from asking the model to create the inactive
  artifact. Keep the explicit builder flag only for historical/test-fixture
  compatibility.
- Prove a fully populated six-pass assembly succeeds with a deliberately
  malformed legacy artifact; prove no theme-group field appears in its deck or
  acceptance report; prove the generated production pass-six workspace omits
  the artifact and assignment language.
- Froth remains an API scheduling/capacity disposition, not an SBE fixture or
  runtime patch.

## Slice 3 — Qualification and review

Qualify source and, if the review approves a release, an installed wheel with
provider-free assembly fixtures. Confirm that the change is limited to dormant
theme-group handling and workspace generation; lifecycle, custody, provider,
and API result contracts are unchanged. Any release remains subject to a fresh
version, final artifact verification, and explicit owner approval.
