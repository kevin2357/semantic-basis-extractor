# Slice 1 — first-batch state-surface audit

## Decision summary

The two dominant provisional modules are both viable collision-qualification
candidates, but for different reasons and with different rollout risk.

- `test_bounded_lifecycle.py`: **advance to collision qualification without a
  production change**. Its writes are owned by per-test temporary roots and its
  provider/network surfaces are fakes. Internal concurrency is behavior under
  test, not an isolation defect. Cross-test helper imports and import-time
  `sys.path` mutation are maintenance debt, but process-isolated runner workers
  prevent them from becoming shared cross-worker state.
- `test_waffle_scone_finalization_slice0.py`: **advance to collision and
  resource-contention qualification, but do not promote merely because it is
  filesystem-isolated**. It inherits the semantic-closure fixture and runs the
  full packaged finalization qualification twice. Its 118–147 second duration
  may therefore compete heavily for CPU/disk with other shards even though its
  writable roots are private. Promotion is useful only if broad wall time
  improves or at least does not regress materially.

Neither module changes manifest classification in this slice.

## Candidate 1 — bounded lifecycle

### Timing value

- samples: 122.434, 121.750, 144.843 seconds
- median: 122.434 seconds
- share of provisional isolated time: approximately 23.5%
- tests: 39

### State-surface inventory

| Surface | Finding | Disposition |
|---|---|---|
| Filesystem | Every test uses an owned `TemporaryDirectory`; state, snapshots, archives, denial artifacts, and checkpoints remain under that root. | likely isolated |
| Repository/package writes | None found. Source fixtures are read-only. | safe |
| Provider/network | Scripted/fake providers use the invalid `.invalid` endpoint and local transports; no real provider call is intended. | safe, retain secret scrubbing |
| Database/ports | No database or listening-port surface found. | safe |
| Environment/cwd | No environment or cwd mutation found. | safe |
| Import state | Import-time `sys.path` insertion and helper imports from three other test modules. | maintenance debt; process isolation contains cross-worker effects |
| Shared fixtures | One class-level compiled bounded artifact is created and read by cases. Tests pass it into newly owned run roots; no mutation of the shared artifact was found. | verify with self-collision and randomized neighbors |
| Threads/locks | Internal `ThreadPoolExecutor`, scripted transport lock, and mixed-route concurrency test. | behavior under test; do not mock or serialize away |
| Time/randomness | No explicit sleep or wall-clock dependency in this module. Due instants are fixture values. | likely deterministic |
| Logging | Not logging-sensitive in the manifest; event-sink failure is asserted through state/behavior rather than captured INFO output. | quiet posture retained |
| Subprocess/build/release | No subprocess, build, wheel, or publication activity. | safe |

### Required collision probes

1. Run two independent instances of the whole module concurrently in separate
   worker roots, three repetitions.
2. Run it beside `test_provider_pending_capacity.py` and
   `test_external_authority_execution.py`, whose helpers it imports.
3. Run it beside a representative existing parallel-safe CPU-heavy module.
4. Compare exact test/outcome identities to the isolated result and check for
   residue beneath both owned roots.
5. Record wall time and CPU pressure; its internal fan-out must not starve the
   sibling shard enough to erase the scheduling benefit.

No repair is presently justified. If collision exposes only import hygiene,
move helpers to an explicit non-discovered support module; do not weaken the
internal concurrency assertions.

## Candidate 2 — Waffle/Scone finalization witness

### Timing value

- samples: 117.633, 146.773, 122.645 seconds
- median: 122.645 seconds
- range: 29.140 seconds, materially noisier than ordinary modules
- tests: 6

### State-surface inventory

| Surface | Finding | Disposition |
|---|---|---|
| Filesystem | Four direct temporary-root uses; packaged qualification also creates its own prefixed `TemporaryDirectory`. | isolated |
| Repository/package writes | None found. Packaged schema/resources are read-only. | safe |
| Provider/network | Uses `FakeAuthoringProvider`; qualification records zero real create/network/spend. | safe, retain secret scrubbing |
| Database/ports | None found. | safe |
| Environment/cwd | No environment or cwd mutation found. | safe |
| Import state | Imports `SemanticClosureFixture` from the 196 KiB serial-only test module. | undesirable coupling; process isolation prevents cross-worker collision |
| Shared fixtures | Inherits the expensive process-local compiled packet. Each worker process builds its own copy. | isolated but resource-heavy |
| Patching | Scoped patches of CLI argv/stdout and production functions; no patch escapes its context. | likely isolated |
| Time/randomness | Uses fixed timestamps; no sleep or random source. | deterministic |
| Logging | One test captures the production logger locally; module is not globally logging-sensitive. | verify under sibling activity |
| Qualification | Calls the full finalization-boundary qualification twice, rebuilding multiple complete workspaces. | principal duration/contention source |
| Subprocess/build/release | No subprocess or build/publish action. The word “packaged” refers to installed resource shape, not a wheel build. | safe |

### Required collision probes

1. Run two independent instances concurrently, three repetitions, checking
   exact result IDs/digests and absence of leaked protected sentinel text.
2. Run beside `test_semantic_closure.py` to prove independent process-local
   fixtures and quantify duplicate compilation/resource pressure.
3. Run beside another qualification-heavy provisional module.
4. Capture isolated versus paired wall times. Reject promotion if contention
   makes the critical path slower despite state isolation.
5. Preserve both calls to the public qualification unless a later test-only
   refactor proves they cover duplicate assertions. Duration alone does not
   authorize removing either.

The approved semantic-closure support extraction can later remove the direct
test-to-test fixture import, but this candidate need not wait for that purely
for safety. It should wait if collision evidence shows duplicated packet
construction is the reason parallel execution loses time.

## First-batch recommendation

Use these two modules as the entire first collision batch. Do not add the next
eight Pareto modules until attribution is clear.

- Prefer `test_bounded_lifecycle.py` as the first promotion candidate if its
  three collision repetitions preserve exact outcomes and acceptable wall time.
- Treat `test_waffle_scone_finalization_slice0.py` as an evidence-driven second
  candidate: isolation looks adequate, but its resource profile may make
  promotion counterproductive on the current laptop.
- Make no test-only repairs before a collision actually demonstrates a failing
  surface.
- Keep semantic-closure support extraction as a separate serial-equivalence
  workstream, as required by the approved paws-point review.

## Next gate

Slice 2 may run the defined provider-free collision probes and change manifest
classification only for candidates whose exact outcomes and resource behavior
pass. Any source/helper refactor or semantic-closure extraction must be
separately attributable and must retain the approved identity-equivalence
fences.
