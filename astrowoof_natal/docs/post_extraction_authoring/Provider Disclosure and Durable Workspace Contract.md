# Provider Disclosure and Durable Workspace Contract

This document defines two pre-pin boundaries for Semantic Closure run schema
`astrowoof.semantic_closure_run.v0.9`.

## Provider-visible subject view

SBE retains complete normalized subject parameters and artifact provenance
locally. Paid OpenAI requests receive only this allowlist when present:

| Field | Disclosed | Editorial purpose |
| --- | --- | --- |
| `subject_id` | yes | stable subject association |
| `display_name` | yes | reader-facing address |
| `subject_type` | yes | dog/person grammar boundary |
| `gender` | yes | grammatical and editorial continuity |
| `pronouns` | yes | correct reader-facing references |
| `breed` | yes | dog-specific characterization where supplied |
| `birth_date` | no | no authoring requirement |
| `birth_datetime` | no | no authoring requirement |
| `birth_latitude` | no | no authoring requirement |
| `birth_longitude` | no | no authoring requirement |
| `birth_location` | no | no authoring requirement |
| `birth_date_precision` | no | no authoring requirement |

The allowlist is applied at the final provider boundary. Initial authoring and
creative retries remove protected lines from `DOG DETAILS.md`. Sparse polish,
qualitative critic, and qualitative candidate requests use the same minimized
subject object. Batch input is built from the already-minimized authoring
request. Persisted provider request artifacts therefore contain only this
provider-visible form.

Selected-card evidence is distinct from broader synthesis evidence. Ordinary
card authoring is bounded to the selected claim and its evidence. Summary and
whole-dog authoring may additionally use unselected claims, whole-chart
analysis, and the projected-term registry. Delivery provenance preserves the
input, resource, execution, QA, and delivery artifact identities; it does not
reinterpret summary-wide support as selected-card evidence.

## Durable workspace path and snapshot

Relocation and path rebasing are not supported for v0.9 runs. A resumable run
must be restored under the exact logical absolute path recorded in
`run.json.workspace_contract.logical_root`.

The complete snapshot boundary is every regular file below the run directory,
including state and spend files; extracted SBE outputs and pass archives; all
attempt requests, provider identifiers, responses, authored fields, and QA;
accepted workspaces; and final assembly, validation, lint, polish, critic,
candidate, delivery, and provenance artifacts.

Ephemeral lock files, atomic-write temporary files, and the snapshot manifest
itself are excluded. `workspace-snapshot.json` records the logical root plus
the relative path, byte count, and SHA-256 of every included member. Internal
provider/spend callbacks durably persist operator state, public state, and
authorization requests without publishing a complete-workspace attestation.
Only the coordinator publishes `workspace-snapshot.json`, after the current
transition has unwound and workspace mutations are quiescent. Resume fails
closed if the manifest is absent, its root differs, or the actual inventory
differs. A crash between an artifact write and the next coordinator checkpoint
is deliberately treated as an incomplete transition requiring native
inspection or recovery.

Concurrent interactive author workers atomically persist operator/public state
from their worker threads, but they cannot attest the whole directory while
peer workers are still creating files. The coordinator writes the complete
snapshot after all workers quiesce. Until then, the earlier manifest will not
match the newer state/artifacts, so a process crash fails closed instead of
resuming from a directory that was observed mid-write.

The same rule applies to optional paid stages. A polish, critic, or qualitative
candidate action may persist commitment, provider identity, waiting state, or
reported usage before all local result artifacts exist. That early ledger
durability is not a resumable workspace checkpoint. When a stage pauses for
external authorization, the exception first unwinds to the coordinator; the
coordinator then publishes the state-owned subject/attempt record, final and QA
artifacts, prepared request, ledger/public state, authorization request, and
snapshot as one restorable boundary.

### Constrained 0.2.1 polish-checkpoint recovery

The installed `astrowoof-repair-polish-checkpoint` command recognizes only the
proven SBE 0.2.1 boundary defect. Inspection is the default and does not mutate
the run. Apply mode requires an exact external authorization document and a
separate, byte-identical complete backup of the pre-repair workspace:

```text
astrowoof-repair-polish-checkpoint --run-dir <stable-path> \
  --authorization <attempt-2-authorization.json>
astrowoof-repair-polish-checkpoint --run-dir <stable-path> \
  --authorization <attempt-2-authorization.json> \
  --apply --backup-path <complete-backup> \
  --exclusive-owner-reference <api-lease-id> \
  --report <outside-run-report.json>
```

Apply requires an API-owned exclusive-lease reference and also acquires the
run's spend-consumption lock. The reference is an audit declaration, not an
SBE account-wide lease service; the API remains responsible for preventing any
other worker from mutating the run. The command accepts exactly three changed
final members—deck, validation report,
and lint report—and only when each byte sequence equals its retained attempt-1
counterpart. It also proves the reported attempt-1 Response identity, the
prepared attempt-2 request digest and external binding, and that attempt 2 has
no authorization, consumption, provider identity, or reported usage. Any
additional, missing, truncated, or conflicting evidence is refused. There is
no force, allowlist, relocation, or generic rehash mode.

Apply reconstructs the missing subject, partial attempt-1 result, and pending
attempt-2 record. A resumed `SUBMITTED` polish attempt is reused rather than
skipped or appended again. Repair preserves every existing ledger action and
accepted pass, atomically republishes
operator/public/authorization state, writes a complete snapshot, and validates
it before success. The output report must live outside the workspace so it
cannot create a self-referential snapshot member.

## Pre-pin qualification scope

Release qualification must continue to prove:

- projected-term registry merge, preservation, and closure validation;
- monotonic accepted-pass evidence across resume;
- distinct outcomes for provider waiting, warnings, review, spend
  authorization, hard budget exhaustion, ambiguous submission, and delivery;
- exact installed AGF 0.6 / SPC 0.10 identity propagation through projected
  input, claims, synthesis, authoring state, delivery provenance, and the
  installed-wheel smoke test.

Unknown-time claim suppression, variable basis sizes, Quick/Complete modes,
hierarchy redesign, and critic product policy are explicitly deferred.
