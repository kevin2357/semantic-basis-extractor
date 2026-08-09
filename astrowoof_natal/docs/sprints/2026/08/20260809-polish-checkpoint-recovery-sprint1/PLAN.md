# Polish Checkpoint and Recovery Sprint

```yaml
status: planning
created: 2026-08-09
owner: semantic-basis-extractor
affected_release: astrowoof-natal-authoring 0.2.1
proposed_patch_release: 0.2.2
execution_authorized: false
live_run_mutation_authorized: false
paid_provider_work_authorized: false
publication_authorized: false
```

## Outcome

Correct SBE's durability boundary so every externally visible provider/spend
pause has one self-consistent, complete, restorable workspace checkpoint.
Provide a narrowly constrained, provenance-preserving inspection and repair
procedure for the affected 0.2.1 acceptance run without resubmitting provider
work or treating arbitrary changed bytes as trusted.

This sprint directory is planning only. It does not authorize source changes,
test execution that mutates the acceptance run, repair execution, authorization
consumption, OpenAI access, version changes, tagging, pushing, or publication.

## Trigger and confirmed evidence

The affected run is retained outside this repository at:

```text
C:\dev\github\astrowoof-api\.acceptance\domain-worker-run-20260808\sbe-run-2
```

It uses SBE 0.2.1 and run ID
`5ad1153d835177111d61fa1da80375e97b69015404d060b374c89997f93de5e2`.
Read-only inspection established:

- all six authoring passes are accepted;
- polish action 1 is `REPORTED` with durable Response ID
  `resp_0ab43a322b5839de006a785f8e04848194a5e41e056e9bcfc0` and reported
  estimated cost 16,644 micro-USD;
- polish action 2, `paid_0d941d208206a4d8b0349f91`, is `PREPARED`, has
  no recorded authorization, provider ID, consumption, or reported usage;
- the external action-2 authorization exactly matches its complete binding;
- the snapshot has 876 declared members with no missing or additional
  authoritative member;
- exactly the final deck, validation report, and lint report differ;
- each differing final file is byte-identical to its retained native polish
  attempt-1 output; and
- `run.json` has no persisted subject record because the authorization pause
  interrupted `finalize_subjects` before its final `subjects` assignment.

No file in the retained run was changed during diagnosis. No provider request
was made and no authorization was consumed.

## Root-cause hypothesis to prove in tests

`save_state()` currently combines atomic run/public/authorization-request
persistence with `write_workspace_snapshot()`. Spend callbacks call it from
inside provider and polish orchestration. The main-thread check is therefore
not a sufficient quiescence condition: nested callbacks also run on the main
thread while request markers, response artifacts, QA reports, final copies,
and subject records are still evolving.

At a polish retry boundary, `polish_subject()` mutates its local subject record
and final files, but `finalize_subjects()` publishes that record into
`state["subjects"]` only after `polish_subject()` returns. An
`AwaitingSpendAuthorization` exception bypasses that assignment. This permits
a ledger/public state that advertises a prepared next action while the operator
state and workspace snapshot describe different moments.

The sprint must reproduce the observed mixed checkpoint before choosing the
final implementation. It must also audit the adjacent provider-ID and response
reconciliation boundaries; the plan must not assume that fixing only three
file copies is sufficient.

## Required invariants

1. **One checkpoint authority.** A published snapshot represents a quiescent
   coordinator boundary, not merely the latest nested state write.
2. **Ledger durability remains early.** Provider acceptance, operation IDs,
   commitment, consumption, reported usage, and ambiguity state remain durable
   at the earliest safe moment even when the workspace is not yet checkpointed.
3. **No blind retry.** Existing provider IDs are polled/reconciled without new
   commitment or submission. Missing provider identity after `SUBMITTING`
   remains machine-distinguishable ambiguity.
4. **Prepared means restorable.** Before exposing
   `AWAITING_SPEND_AUTHORIZATION`, the preceding attempt result, QA artifacts,
   final files, subject state, prepared request, ledger, public state, and
   authorization request are represented by one validated checkpoint.
5. **Monotonic evidence.** Repair and resume may add evidence but may not erase
   accepted authoring, provider IDs, reported usage, spend events, or QA history.
6. **Fail closed.** Unexplained differences, incomplete evidence, mismatched
   bindings, or an already-consumed/submitted next action refuse repair.
7. **Single writer.** Checkpoint publication and repair require the same
   exclusive run ownership expected of normal execution.
8. **No arbitrary rebase.** A repair tool may accept only named, derivable
   transition shapes whose changed bytes are proven by retained SBE evidence.

## Proposed design

### Split persistence from checkpoint publication

- Introduce an internal state/ledger persistence operation that atomically
  writes `run.json`, `public-run.json`, and authorization requests without
  claiming the complete directory is quiescent.
- Introduce an explicit coordinator checkpoint operation that publishes those
  state files and `workspace-snapshot.json` only after mutations settle.
- Ensure a stale or absent checkpoint during an in-flight transition fails
  closed with a machine-readable recovery classification instead of looking
  like an unexplained user workspace edit.
- Preserve the stable-logical-absolute-path and complete-snapshot contract.

### Make polish state durable before it can pause

- Install the subject record into `state["subjects"]` before entering resumable
  polish and mutate the state-owned record thereafter.
- At a next-attempt authorization pause, unwind to the coordinator, persist the
  complete attempt result and ledger, and publish the snapshot before exiting.
- Keep action binding to the exact request digest and prepared revision; do not
  silently regenerate or substitute an authorization after repair.

### Harden provider interruption and reconciliation

- Test interruption before provider creation, after provider acceptance but
  before ID persistence, after ID persistence but before local marker
  persistence, while polling, after response persistence, after cost
  settlement, during QA generation, and during checkpoint publication.
- Preserve the documented irreducible provider atomicity gap and ambiguity
  classification.
- Demonstrate that recorded response work is retrieved, never re-created, and
  that polling creates no new spend commitment.

### Constrained 0.2.1 repair

Provide an installed-runtime command with dry-run default and an explicit
apply mode. For the supported polish-boundary shape it must:

- require exclusive ownership and a complete copy/backup declaration;
- compare every authoritative member against the recorded snapshot;
- allow only the exact final deck/validation/lint mismatch set;
- prove those bytes equal retained attempt outputs;
- verify response ID, action state, request digest, profile/run identity,
  reported cost, and the unused next action plus authorization binding;
- reconstruct missing subject/attempt state from native artifacts or replay a
  deterministic local transition without creating provider work;
- emit a machine-readable repair plan and before/after hash report;
- atomically persist repaired monotonic state and a complete new snapshot; and
- validate the repaired snapshot before declaring success.

The tool must never accept a generic `--force`, arbitrary member allowlist, or
"rehash current directory" mode.

## Slices

### Slice 0 - Frozen forensic model and executable reproduction

- Preserve the original acceptance run as read-only external evidence.
- Record a compact redacted mismatch/action/state report in sprint results.
- Add a synthetic regression reproducing response reconciliation, partial
  polish improvement, final-file replacement, preparation of attempt 2, and
  failed restored resume.
- Confirm whether the initial observed timing race is the same defect or a
  separate concurrent-checkpoint problem.
- Freeze the exact changed production surfaces and recovery preconditions.

Gate: approve the reproduced failure, root cause, and implementation boundary.

### Slice 1 - Quiescent checkpoint architecture

- Separate internal state/ledger persistence from complete checkpoint
  publication.
- Persist the state-owned subject record before resumable polish begins.
- Route every normal authorization, detach, waiting, ambiguity, review, and
  delivery exit through an explicit coordinator checkpoint.
- Add state/snapshot revision linkage and machine-readable incomplete-
  transition diagnostics if needed without weakening legacy fail-closed rules.
- Run focused polish, spend, snapshot, and public-state tests.

Gate: approve the production durability diff and state-contract consequences.

### Slice 2 - Provider interruption and boundary failure injection

- Inject failure on both sides of provider submission, provider-ID recording,
  marker persistence, response reconciliation, settlement, final copy, next
  action preparation, run-state persistence, and snapshot publication.
- Prove no duplicate paid submission when a durable provider ID exists.
- Prove ambiguous submission remains blocked when provider acceptance cannot be
  established.
- Prove prepared authorization remains exact and single-use after restore.
- Run the complete deterministic repository suite and `git diff --check`.

Gate: approve recovery semantics and the complete regression matrix.

### Slice 3 - Constrained repair tooling and documentation

- Implement dry-run inspection and explicit repair for the proven 0.2.1 polish
  checkpoint shape.
- Add positive tests from a synthetic fixture and refusal tests for every
  unexplained mutation, missing artifact, identity mismatch, altered binding,
  or used/submitted next action.
- Update the durable workspace, spend authorization, provider enforcement, and
  semantic closure consumer documentation.
- Publish a field-level description of what repair changes and preserves.

Gate: approve the repair command and documentation before it touches any copy
of the acceptance run.

### Slice 4 - Acceptance-run dry run and repaired-copy validation

- Make a complete immutable backup or verified copy outside Git.
- Run inspection/dry-run against a separate working copy only.
- Compare the generated repair plan with the frozen forensic model.
- After explicit per-run approval, apply repair to the copy, validate every
  member and monotonic ledger invariant, then test resume only to the existing
  authorization boundary without consuming action 2 or contacting OpenAI.
- Produce compact redacted evidence; do not commit the run or provider payloads.

Gate: separately authorize any repair of the canonical retained run and any
subsequent provider-connected resume.

### Slice 5 - Patch artifact and consumer handoff

- If prior gates approve release, set final patch coordinates and build the
  wheel twice reproducibly.
- Audit the wheel and clean-install the exact artifact on Windows and Linux.
- Run deterministic installed smoke plus the offline repaired-checkpoint
  regression.
- Prepare API-worker pin, recovery advisory, compatibility delta, checksums,
  and release manifest.
- Tag, push, and publish only after a separate explicit publication approval.

Gate: independently verify any published artifact without moving its tag.

## Test matrix

Minimum required coverage:

1. exact synthetic reproduction of the observed polish retry boundary;
2. subject-state persistence across `AwaitingSpendAuthorization`;
3. checkpoint member equality after attempt-1 final replacements;
4. prepared action/request/authorization digest stability after restore;
5. existing Response ID retrieval with zero create calls;
6. ambiguity when submission outcome lacks durable provider identity;
7. failure injection at every state/file/snapshot boundary listed above;
8. concurrent or overlapping checkpoint publication refusal;
9. repair dry-run and apply success for the exact supported shape;
10. repair refusal for additional, missing, truncated, or altered evidence;
11. monotonic accepted evidence and reported spend before/after repair;
12. complete deterministic repository suite; and
13. exact-wheel installed smoke on Windows and Linux if release proceeds.

No live OpenAI request is required to implement or qualify the correction.

## Controls

- Follow `docs/sprints/README.md` and pause at every slice gate.
- Do not mutate, resume, re-snapshot, or clean the original acceptance run
  during Slices 0-3.
- Do not consume the prepared action-2 authorization.
- Do not issue POST, GET, cancel, or delete requests to OpenAI during this
  sprint unless separately and explicitly authorized; the planned tests use
  fake transports and retained local evidence.
- Never print or commit prompt bodies, protected subject data, API keys,
  authorization secrets, full provider responses, or the acceptance workspace.
- Preserve the immutable 0.2.0 and 0.2.1 tags and published assets.
- Do not weaken snapshot validation, spend binding, single-writer enforcement,
  ambiguity classification, or provider disclosure to make recovery pass.
- Stop for a plan revision if repair requires accepting bytes not derivable
  from retained SBE-native evidence.

## Exit criteria

- every provider/spend exit publishes one validated quiescent checkpoint;
- a restored checkpoint resumes without duplicate paid work;
- polish attempt results and subject state survive the next authorization
  boundary;
- provider-ID interruption paths remain fail-closed and reconcilable;
- the constrained repair tool accepts the exact proven 0.2.1 shape and rejects
  unexplained variants;
- repaired state preserves all accepted authoring, provider, spend, QA, and
  provenance evidence monotonically;
- the existing action-2 authorization remains unused unless separately
  authorized after repair;
- focused and complete deterministic tests pass; and
- consumer documentation clearly defines checkpoint, restore, repair, and API
  ownership responsibilities.

## Planned result records

Each completed slice will add `results/SLICE N - <name>.md` and compact redacted
JSON where useful. `LOG.md` will record approvals, commits, test commands,
failure-injection outcomes, repair hashes, and any plan revision. Large or
sensitive acceptance artifacts remain outside Git.
