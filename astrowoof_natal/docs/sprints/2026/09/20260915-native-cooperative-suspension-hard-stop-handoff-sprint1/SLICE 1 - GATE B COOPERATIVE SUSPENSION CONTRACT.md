# Slice 1 — Gate B cooperative-suspension contract

## Status

**Gate B clarification incorporated; ready for the shared Alloy spike.** This freezes a closed v1 protocol for
exact interactive ordinary-v2 dispatch and response reconciliation only. It
does not authorize implementation, signaling, process termination, capacity
release, live execution, provider work, R2 access, or workspace mutation.

Initial-wave fan-out, legacy direct authoring, bounded routes, and Batch are
explicitly unsupported by v1.

## Ownership model

API owns the durable force fence, pre-launch supervision identity, control-root
creation, request publication, process observation/termination, worker lease,
execution-capacity accounting, run allocation, and later resolution admission.

SBE owns validation and observation of an exact cooperative request at a native
safe point, serialization with native mutation, checkpoint/custody truth,
native suspension result and receipt publication, and refusal or ambiguity when
those facts cannot be proved.

The public join is:

```text
API force fence
  + pre-launch supervision envelope
  + exact cooperative request
  + exact SBE suspension result/receipt when available
  + exact API child-exit observation
  -> resource-specific API resolution
```

No member is sufficient by itself.

## Contract family

v1 introduces four separately validated documents:

1. `astrowoof.native_supervision_invocation.v1` — API-created private launch
   envelope.
2. `astrowoof.native_suspension_request.v1` — API-created canonical control
   request.
3. `astrowoof.native_suspension_result.v1` — SBE-created public native result.
4. `astrowoof.native_suspension_receipt.v1` — SBE-created immutable publication
   receipt.

An optional
`astrowoof.native_suspension_command_result.v1` is the exact stdout/output-file
transport envelope. It names the result and receipt returned by this invocation
and cannot use availability/latest-result discovery.

All schemas are closed. Unknown versions, keys, enum members, missing evidence,
and inconsistent joins fail closed.

## 1. Pre-launch supervision envelope

API creates and persists the envelope before `Popen` and supplies it to the
child through a dedicated CLI argument. Required fields:

| Field | Rule |
| --- | --- |
| `schema_version` | exact `astrowoof.native_supervision_invocation.v1` |
| `supervision_invocation_id` | random immutable API identifier; distinct from logging and native-publication invocation IDs |
| `launch_generation` | positive monotonic generation for the exact job/attempt |
| `api_run_id`, `job_id`, `attempt_id`, `lease_id` | nonempty exact API identities |
| `lease_token_sha256` | digest only; plaintext forbidden |
| `native_run_id` | exact expected SBE run identity |
| `worker_boot_id` | exact worker-process boot identity |
| `command_kind` | closed to `external_authority_v2_dispatch` or `provider_reconciliation` in v1 |
| `command_sha256` | canonical digest of executable plus ordered arguments and authority-document digests; secrets excluded before hashing |
| `executable_workspace_root` | canonical absolute authoritative SBE workspace root used by this child |
| `executable_workspace_root_sha256` | canonical digest over that absolute root identity |
| `control_root` | canonical absolute, request-isolated control root outside the executable workspace |
| `control_root_sha256` | canonical digest over that absolute control-root identity |
| `created_at`, `launch_not_after`, `grace_deadline` | UTC instants with strict ordering |
| `force_fence_id`, `force_fence_sha256` | exact admitted API fence binding |
| `envelope_sha256` | digest of every preceding canonical field |

The envelope is immutable. API may append PID, process-group, start-marker, and
exit observations to its own supervision ledger; those are not edits to this
document and are not native authority.

The existing environment/logging `ASTROWOOF_INVOCATION_ID` is diagnostic only.
The native publication invocation ID remains separately minted by SBE. Neither
may substitute for `supervision_invocation_id`.

## 2. Control-root capability

### Layout and ownership

- API creates one fresh control root per supervision invocation before launch.
- Its canonical absolute path is outside and not nested beneath the executable
  workspace, any relocated assessment root, and other invocation roots.
- The child receives the envelope path and control root explicitly; it performs
  no directory discovery or parent traversal.
- API is the only writer to the request channel. SBE treats it as read-only.
- The v1 request filename is fixed as `native-suspension-request.v1.json`.
- API publishes by writing a sibling temporary file, flushing/closing it, and
  atomically replacing the fixed request filename on the same filesystem.
- Multiple request files, unexpected regular files, links/reparse points,
  directories in place of the file, or identity changes are conflicts.

### Validation order

Before opening or parsing the request, SBE must:

1. validate that the current run root is the stable authoritative executable
   workspace, not a relocated assessment;
2. canonicalize the envelope's executable and control roots;
3. prove current executable-root identity equals the envelope;
4. prove the control root equals the envelope's exact absolute identity and
   digest;
5. prove the roots are disjoint and the control root is request-isolated; and
6. reject unsupported route/command or expired launch identity.

A relocated copy therefore cannot learn or exercise the request capability even
when its bytes and checkpoint authority are otherwise valid for assessment.

The control channel grants only permission to read and validate the one fixed
cooperative-suspension request. It grants no arbitrary command, provider,
workspace, publication, retirement, reconciliation, shell, or cleanup power.

## 3. Cooperative suspension request

Required fields:

| Field | Rule |
| --- | --- |
| `schema_version` | exact `astrowoof.native_suspension_request.v1` |
| `operation` | exact `cooperative_suspend` |
| `request_id`, `idempotency_key` | nonempty immutable API identities |
| `supervision_invocation_id`, `launch_generation`, `envelope_sha256` | exact launch-envelope join |
| `force_fence_id`, `force_fence_sha256` | exact durable-fence join |
| `api_run_id`, `job_id`, `attempt_id`, `lease_id`, `native_run_id` | exact repeated target identities |
| `command_kind`, `command_sha256` | exact command binding |
| `executable_workspace_root_sha256`, `control_root_sha256` | digest-bound capability identities; raw paths are not repeated |
| `admission_checkpoint_basis_sha256` | exact checkpoint observed by API while atomically admitting the force fence and publishing this request; it is an anchored predecessor, not an observation-time equality gate |
| `actor_id`, `reason_code`, `environment` | audit-safe values; no free-form secrets or subject content |
| `emergency_containment_confirmed` | exact `true` |
| `requested_at`, `expires_at`, `grace_deadline` | UTC instants; request must be fresh and cannot extend the envelope grace |
| `request_sha256` | canonical digest over all preceding fields |

An exact duplicate is idempotent. A second differing request for the same
supervision invocation is `suspension_refused/request_conflict`. A request for
an earlier launch generation is stale and must never affect the current child.

Absence means continue ordinary behavior; malformed, conflicting, or identity-
mismatched presence means fail closed before further provider/local work and
attempt to publish a typed refusal only when the native publication boundary is
itself safe.

The child receives the immutable envelope-file path and canonical control-root
path through two dedicated ordered CLI arguments. It opens only the exact
envelope at that canonical location and then applies the control-root validation
order above. An envelope digest alone is not path authority. Argument
substitution, a byte-valid envelope at a different location, and path/digest
disagreement all fail closed.

The request's admission checkpoint is an immutable lineage anchor. When SBE
later observes the request, normal already-authorized work may have published a
successor checkpoint. SBE may honor the request only if the observation-time
checkpoint is the same checkpoint or a validated contiguous successor in the
same authoritative run/workspace lineage. Missing, contradictory, forked, or
non-successor evidence refuses or produces the applicable ambiguity; SBE never
synthesizes the lineage.

## 4. Observation safe points

v1 observes requests only in exact interactive ordinary-v2 paths:

### Dispatch

1. after writer acquisition and workspace/envelope validation;
2. after complete intent/prepared-create checkpoint;
3. immediately before provider POST;
4. immediately after provider return and before identity persistence; and
5. after provider identity checkpoint and before another action.

### Response reconciliation

1. after writer acquisition and workspace/envelope validation;
2. before each due provider GET;
3. after retrieved response evidence is durably written;
4. before local adoption;
5. after adoption/checkpoint and before successor selection; and
6. before native result publication/command handoff.

The observer runs under the coordinator's existing serialization. It cannot be
called from an OS signal handler or in the middle of arbitrary file writes.
Once a valid request is observed, this invocation may perform only the bounded
persistence/publication needed for the suspension result; it may not select a
new action or begin new provider work.

Provider polling can stop only between HTTP operations. If a transport call is
blocked past the grace deadline, API may separately terminate the exact child;
without a native result that remains an API interruption with native/provider
ambiguity.

## 5. Native suspension result

The SBE result binds:

- `schema_version`, `result_id`, and canonical `result_sha256`;
- exact request ID/digest and complete supervision-envelope identity;
- exact native run and authoritative logical workspace-root digest;
- `observed_at`, `safe_point`, and supported route/command;
- pre-observation and post-publication checkpoint identities/revisions/digests;
- closed provider boundary and local-work posture;
- ordered action/custody inventory using existing public native joins;
- ordinary-result precedence evidence;
- closed outcome/reason; and
- exact receipt identity/digest after receipt construction.

### Closed outcomes

| Outcome | Meaning |
| --- | --- |
| `suspended_checkpointed` | Request observed; required native facts and a new exact checkpoint/result/receipt were durably published |
| `suspended_quiescent_no_checkpoint_change` | Existing checkpoint already represented the exact safe boundary; result/receipt binds it without inventing mutation |
| `suspension_deferred` | Request was observed but the current bounded operation must settle before a truthful result can be produced; includes a closed reason and upper bound when known |
| `suspension_refused` | Identity, freshness, capability, route, custody, or safe-point requirements failed |
| `provider_boundary_ambiguous` | Provider call entry or returned identity cannot be proved durably |
| `checkpoint_publication_ambiguous` | Native state may have changed but exact checkpoint/result publication cannot be proved |

### Provider boundary

Closed values are `not_entered`, `known_provider_identity`,
`completed_provider_evidence`, and `entry_or_result_ambiguous`. Known provider
evidence includes exact action/provider-operation joins; ambiguity cannot carry
a fabricated provider identity.

### Local work posture

Closed values are `none`, `durable_pending`, `completed_unadopted`,
`adopted_checkpointed`, and `ambiguous`.

The result explicitly does **not** assert process exit, API lease or capacity
release, run-allocation release, provider cancellation, spend settlement,
terminalization, or cleanup authority.

Every `suspension_deferred` result also carries one closed continuation mode:
`continue_to_named_safe_point`, `exit_after_result_publication`, or
`await_separate_api_action`. The first names the next permissible safe point
and its bounded deadline; the latter two prohibit ordinary continuation. API
must not infer child exit or any resource release from a deferred result.

## 6. Publication and command-result precedence

Suspension publication reuses the existing native writer, journal, checkpoint,
result-index, sealed-result, and receipt discipline. The suspension result is a
new additive public type, not a reinterpretation of lifecycle status.

The exact command-result envelope binds `supervision_invocation_id`,
`native_publication_invocation_id`, result ID/digest, receipt ID/digest,
checkpoint digest, outcome, and exit code. It is written to the configured
authoritative output and may also be emitted on stdout under the existing CLI
transport rules.

Precedence is strict:

1. a valid ordinary terminal/delivery result committed before suspension
   observation remains authoritative and is returned unchanged;
2. otherwise, an exact suspension result produced by this invocation outranks
   exit code and diagnostic logs;
3. API availability/latest-result discovery is not permitted for ordinary
   command handoff; and
4. process exit without an exact result is interruption evidence, never a
   reconstructed suspension result.

## 7. Append-only evidence and replay

The API force fence remains immutable. Each SBE suspension result names its
request/envelope predecessor. Each later API process observation or resolution
names the immediately preceding evidence digest. No record changes the original
request, fence, or ambiguity in place.

Exact replay returns the same result/receipt identities and performs no provider
or workspace mutation. A stale or conflicting replay refuses. Restarted workers
cannot honor a prior control root or request because worker boot, invocation ID,
generation, command digest, and control-root identity no longer all join.

## 8. API resource-resolution matrix

| Evidence | Worker execution | Run allocation | Provider/spend/workspace/native custody |
| --- | --- | --- | --- |
| Fence only / authority revoked | busy or unknown | retain | retain |
| Valid SBE suspension result, child exit unknown | busy or unknown | retain | retain according to reported native posture |
| Exact envelope-bound child exit, no SBE result | may reclaim worker execution only | retain | retain as ambiguous |
| Valid SBE suspension result + exact child exit | may reclaim worker execution | separate named policy; default retain | retain unless a separate exact operation is authorized |
| Stale/mismatched/contradictory process identity | do not reclaim | retain | retain |
| Prior ordinary terminal/delivery result + exact child exit | may reclaim worker execution | ordinary API settlement policy | consume exact ordinary result; do not substitute suspension semantics |

The SBE result supplies native facts but never authorizes an API release.

## 9. Failure and race matrix required before implementation

Provider-free fixtures must cover:

- request absent, exact, duplicate, conflicting, expired, wrong generation,
  wrong worker boot, wrong command, wrong run/checkpoint, and corrupt digest;
- admission checkpoint C1 followed by a valid contiguous safe-point checkpoint
  C2, plus missing, forked, contradictory, and non-successor C2 cases;
- control-root relocation, nesting, replacement, link/reparse ambiguity, and
  unexpected members; envelope/control CLI argument substitution; and a
  byte-valid envelope at the wrong canonical location;
- stop before intent, after intent, before POST, after possible POST/before ID,
  after ID, before GET, after GET/before adoption, after adoption, before
  publication, and after ordinary result publication;
- parent crash before request, during atomic publication, after publication,
  and after child result but before process observation;
- child restart, PID reuse simulation, stale control root, and exact replay;
- publication failure before checkpoint, after native mutation, after result,
  and after receipt;
- unrelated run/workspace/control root/process isolation; and
- zero provider calls for every provider-free qualification cell.

Malformed, conflicting, or unsupported control input prohibits all **new**
native/provider work for the fenced invocation. If SBE cannot safely publish a
refusal, API's durable fenced ambiguity remains authoritative; rejection of the
control input never selects ordinary retry, reconciliation, or successor work.

## 10. Unsupported v1 behavior

If the envelope command/route is initial-wave, legacy direct, bounded, or Batch,
SBE must refuse before parsing a suspension request or performing provider/local
work. API retains the force fence and ambiguity. It must not retry the same
unsupported cooperative operation as though it were transient.

No signal handler, raw PID, Render service restart, relocated assessment, or
generic latest-result reader is a v1 fallback.

## Gate B decision requested

API/SBE/owner review should confirm:

1. the four-document identity split and exact field ownership;
2. the canonical absolute control-root binding and validation order;
3. the v1 route restriction;
4. result taxonomy and ordinary-result precedence;
5. append-only replay/resolution semantics;
6. worker-execution-only reclamation after exact child exit; and
7. the provider-free race matrix.

Only an affirmative joint Gate B review authorizes Slice 2 contract fixtures
and readers. Runtime safe-point integration remains separately gated after
those packaged contracts are reviewed.
