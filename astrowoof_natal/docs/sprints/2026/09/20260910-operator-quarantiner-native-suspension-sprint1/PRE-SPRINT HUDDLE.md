# Pre-Sprint Huddle — Nice Quarantine Before Emergency Suspension

## Revised framing

The operator quarantiner has two materially different modes.

The **nice path** asks SBE for a read-only, snapshot-valid disposition
assessment and proceeds only when that assessment proves ordinary native work no
longer needs local scheduling capacity. AstroWoof attempted this path once
against a retained-native run, but the operator runner did not receive a valid
public assessment. The detailed transcript is no longer retained, so the cause
is unclassified.

The **not-so-nice path** begins with a durable API stop fence and may culminate
in exact supervised process termination when the native invocation cannot
cooperate. It preserves an interrupted or ambiguous posture and may require
later native inspection or reconciliation. It is not a broadened version of the
nice assessment and must not imply clean native suspension, cancellation,
terminalization, provider release, or workspace cleanup.

This distinction changes the recommended sprint sequence. Before freezing a
new suspension protocol, recreate and classify the failure of the existing nice
path. A package, subprocess, restore, identity, timeout, or stdout-adapter defect
may be preventing an already-valid contract from working operationally.

## Comparison with API Sprint 90

API's draft Sprint 90 is well aligned with the native design assessment. Its
strongest improvement is sequencing: Slices 0–2 investigate the current control
surface and assessed-quarantine failure before Slice 3 freezes a new joint
suspension contract.

The following API conclusions should be adopted here:

- the historical assessed-quarantine failure remains unclassified rather than
  presumed to be a semantic SBE refusal;
- existing safe refusals must not be weakened to make the operator path appear
  more useful;
- a durable API fence must remain useful even when no valid SBE assessment or
  suspension result is available;
- one bounded QA experiment may be valuable only after deterministic failure
  coverage exists and with separate owner authorization;
- pre-native hold truthfulness is related API work but is not a native
  suspension-result problem;
- cooperative suspension and forced interruption require distinct evidence and
  must lead to distinct operational postures.

Two wording/ownership refinements are recommended for joint review:

1. API queue claims and lease renewal are API-owned fence boundaries. SBE does
   not observe those operations; it observes an exact suspension request at
   enumerated native safe points.
2. Cooperative SBE suspension and API exact-process hard-stop should be separate
   implementation sub-slices. They have different authorities, failure modes,
   and qualification evidence even though the final API admission joins them.

API Sprint 90's `BACKGROUND.md` also still says there is no implementation plan
although a draft `PLAN.md` now exists; that is editorially stale, not a design
problem.

## First question: why did the nice path fail?

The existing public SBE surface is intentionally narrow:

- `astrowoof.operator_disposition_assessment.v1`;
- snapshot-valid read-only assessment;
- exact workspace and lifecycle evidence;
- no provider authority or mutation;
- strict `native_prior_action_required` and `prohibited` outcomes;
- canonical JSON output from the installed CLI.

The historical workspace, checkpoint, database state, and R2 object were
destroyed by the ordinary QA reset. The lost attempt could have failed at
several independent seams, but its exact cause is no longer reproducible from
native state:

| Failure class | Example | Owner of initial evidence |
| --- | --- | --- |
| restore/configuration | wrong retained root, missing packaged resource, incompatible installed pair | API runner plus installed SBE CLI |
| invocation | wrong executable/module, arguments, environment, working directory, timeout | API runner |
| native eligibility | valid typed prohibition or prior-action requirement | SBE assessment |
| native read | malformed, contradictory, or unsupported workspace evidence | SBE assessment/diagnostic stderr |
| serialization | valid assessment built but absent or malformed on stdout | SBE CLI |
| adapter | canonical assessment emitted but rejected, truncated, or misparsed | API subprocess adapter |
| identity join | assessment valid but bound to a different checkpoint/workspace/request | API admission plus SBE identity fields |
| lifecycle mutation | assessment valid but target changed before execution | API writer fence/admission |

Without the transcript and workspace, none should be privileged as the likely
answer. The first useful result is a provider-free matrix that can distinguish
all of them through the real production boundary using a new genuine
SBE-generated fixture. That can reproduce the remembered symptom in current
code; it cannot prove which failure occurred historically.

## Required provider-free reproduction boundary

Callback-level tests are insufficient. The reproduction should exercise:

```text
retained-workspace-shaped fixture
  -> exact API restore/input preparation
  -> installed astrowoof-operator-disposition-assessment process
  -> real stdout/stderr capture and timeout behavior
  -> API parser and identity validation
  -> dry-run quarantine admission/refusal
```

At minimum, cover:

- one valid permitted assessment;
- one valid `native_prior_action_required` result;
- one valid prohibited/unsupported result;
- process starts but emits no assessment;
- malformed or truncated JSON;
- valid JSON with wrong contract, run, workspace, checkpoint, or assessment
  digest;
- nonzero exit with bounded sanitized stderr;
- process timeout;
- workspace/checkpoint identity changes between attempts;
- installed-package/resource mismatch;
- successful duplicate read producing byte-identical assessment.

Every cell remains provider-free and mutation-free. A semantic refusal is a
successful assessment outcome, not an invocation failure.

## Bounded retry position

A small fixed retry may be appropriate for failure before a semantic assessment
exists—for example process startup, transient restore visibility, or bounded
subprocess failure. It must obey all of these rules:

- exact workspace/checkpoint identity is pinned before the first attempt;
- identity is revalidated before every retry;
- any identity change ends the operation rather than restarting the budget;
- a valid permitted, prior-action, or prohibited assessment is conclusive and
  never retried;
- malformed identity-bearing output is retained diagnostically but does not
  authorize mutation;
- retry count and total wall-clock budget are fixed and recorded.

Retry is resilience around obtaining an assessment. It is not polling until
SBE changes its answer.

## Proposed bounded QA experiment

After the deterministic matrix and any resulting correction are reviewed, one
live QA exercise can separate the remaining layers:

1. Create or select one owner-authorized ordinary QA target under an explicit
   cost ceiling.
2. Wait for exact retained native evidence and a stable posture; do not infer
   eligibility from outer API status.
3. Pause ordinary worker progress through the approved operational mechanism.
4. Preserve API/PostgreSQL diagnostics, matching SBE logs, exact workspace and
   checkpoint identities, and operator request state.
5. Run the installed read-only SBE assessment independently against the restored
   exact workspace and retain stdout, stderr, exit code, duration, and digest.
6. Run the API operator preflight/dry-run and compare its interpretation with
   the independently captured assessment.
7. Execute `sbe-quarantine-run` at most once, and only if the target and
   assessment remain exact and eligible.
8. Stop at the first conclusive outcome: completed quarantine, typed native
   refusal, missing/malformed/timed-out assessment, or identity change.

The independent CLI read before API dry-run is important. It distinguishes an
SBE producer/eligibility failure from an API invocation/parser/admission failure
without broadening authority.

This experiment requires separate owner approval for cohort/spend, worker pause,
the exact execute operation, and any later cleanup or reset. It is diagnostic,
not a substitute for deterministic fixtures and not authority to test hard-stop
behavior on a live paid run.

## Revised native sprint sequence

### Slice 0A — Existing assessment producer and CLI inventory

Map the v1 reader, validation, packaged resources, CLI stdout/stderr/exit
behavior, workspace/checkpoint identity, and all native reasons an assessment
may be unavailable or refused.

### Slice 0B — API restore, invocation, and admission handoff

Jointly map how the operator runner restores the workspace, selects the installed
SBE executable, sets the working environment, captures streams, applies
timeouts, validates identity, and admits a permitted assessment.

### Slice 1 — Nice-path provider-free reproduction matrix

Exercise the real installed CLI and API subprocess boundary across the failure
classes above. Classify the historic failure only if evidence supports it;
otherwise record which current failure shapes reproduce and which do not.

### Slice 2 — Narrow correction and bounded experiment

Correct only the proven seam. Rerun focused installed and cross-repo tests. Then,
if still useful and separately authorized, perform the one bounded QA exercise.

### Slice 3 — Residual-gap decision

State exactly which active/ambiguous postures remain impossible for assessed
quarantine. Use that evidence to decide the minimum cooperative suspension
contract rather than treating the full initial design as predetermined scope.

### Later slices — Cooperative suspension and hard-stop containment

Freeze and implement the additive exact request/result pair only for residual
cases. Implement API process supervision separately. Join their evidence at the
capacity-release boundary, preserving interrupted/ambiguous custody whenever a
clean native result is absent.

## Native role in the not-so-nice path

SBE may be essential after a forced stop, but it should not own arbitrary
process killing or broad cleanup. Its useful responsibilities are bounded:

- cooperatively observe a stop request at safe lifecycle seams when possible;
- persist exact checkpoint, action, provider, result, receipt, and local-work
  facts before exit;
- emit a closed suspension result when those facts are provable;
- read and classify surviving durable native evidence after interruption;
- provide a typed inspector or recovery operation for a named unresolved
  posture;
- refuse to infer missing call-entry, provider, checkpoint-publication, or
  receipt identity.

API/operator supervision owns the durable fence and termination of the exact
process. Cleanup is a later typed operation admitted from retained evidence. A
kill must never automatically delete a workspace, clear provider/spend custody,
release semantic authority, or manufacture terminal state.

## Updated recommendation

Retain the broader native-side design assessment as the architectural hypothesis
for Control Room issue 18, but do not treat all of it as approved implementation
scope. The next concrete work should be the existing assessed-quarantine
inventory and production-boundary reproduction.

If that work finds a mundane CLI, packaging, restore, or parser defect, fix and
exercise the nice path before adding new lifecycle vocabulary. If it proves the
nice path is functioning as designed but cannot safely handle an active target,
the evidence will define the exact residual contract needed for cooperative
suspension and hard-stop containment.
