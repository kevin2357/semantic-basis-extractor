# API agent — Gate A contract review

## Disposition

The proposed bounded reconciliation and cooperative supervision direction is sound. I agree with the separate opt-in bounded command contract, the compatibility boundary for existing callers, and SBE's pre-Gate A review of API's preparation. I do **not** consider Gate A closed yet: the same-invocation publication identity, fence ordering, and partial-failure/replay contract below need a shared, testable resolution first. This is a design review, not approval of an untested implementation, package release, deployment, or paid run.

The current API bounded path validates the command result, publishes a checkpoint when a successor snapshot exists, and then discovers the latest sealed transition. The terminal pre-fence path can already read an exact result, but `read_latest_sealed` alone cannot establish that an ordinary terminal *or nonterminal* transition belongs to this invocation. We should close that gap explicitly rather than infer ownership from recency.

## 1. Exact publication identity and lost-output recovery

**Recommendation:** have the bounded command provide an explicit, validated same-call publication reference for every result that publishes a native transition, not just terminal results. A no-publication/no-due outcome must explicitly say so. The reference should identify the native run and exact sealed result and receipt, including the necessary immutable IDs and digest/snapshot binding to verify that pair against the selected pre-invocation decision and successor. Include or otherwise durably bind a unique API-issued command-attempt identity to the native publication: the native publication invocation ID and API child-command attempt are distinct concepts and must not be assumed equal. Agree on the exact fields and schemas together; do not expose capabilities or sensitive workspace contents.

API should validate the bounded envelope, the attempt/run/route binding, and the exact sealed result and receipt with the exact-reader path before ingesting; it must not substitute the latest publication if the reference is missing or inconsistent. The same proof applies to nonterminal successor publications and terminal publications. Validate the expected predecessor/decision and exact receipt membership as well as identity and digests. A mismatch is a contract failure, not permission to pick another result.

For output lost after SBE seals locally, a reference printed only on stdout is insufficient recovery evidence. Design a durable, invocation-scoped lookup or equivalent immutable binding that can recover the **one exact** publication, with collision/conflict detection and the same validations. The lookup must itself be present in the recoverable checkpoint, or independently durable under an appropriate authority/fence. It cannot make an unpublished local workspace survive loss of the worker: if neither local evidence nor a published checkpoint survives, the result is unknown and remains safely unresolved. Recovery must not infer an identity from `latest`, nor assume checkpoint and database writes are one atomic transaction. The precise authority to publish or ingest after a lease/fence must be checked in the applicable recovery path.

Please cover two attempts on the same run, preexisting newer/older publications, wrong attempt/run/predecessor and tampered descriptors, stdout loss with recoverable exact evidence, and stdout plus local-workspace loss without such evidence. Also cover an explicitly no-publication result.

## 2. Fence race: distinguish orderings and what they prove

The cycle's launch/decision timestamp is not the time SBE actually observed a suspension request. Record these separately: the API's durable force-fence action and parent observation; SBE's actual request-read/observation and validation; native sealing/publication; and the parent's observation of the exact terminal output. An SBE seal before the child observes the request does **not** by itself prove the parent observed the terminal result before the fence.

For this iteration I recommend preserving API's conservative existing terminal-precedence rule: only a qualifying exact terminal result the parent observed strictly before its force-fence observation can take that pre-fence terminal path, subject to exact-publication and existing authority validation. A result first observed by the parent after the fence must not acquire that precedence merely because the child reports an earlier seal. If durable evidence is missing, contradictory, simultaneous at the supported resolution, or otherwise ambiguous, keep the work fenced and preserve custody/exposure for explicit recovery. This is not a claim that the provider or child did nothing.

Use a reliable ordering within the parent observation domain, ideally an explicit ordered record/sequence and, where applicable, a process-local monotonic measurement; make the durable evidence and crash limitations explicit. UTC timestamps are useful audit data, not by themselves a proof of cross-process causal order, particularly with clock skew or coarse precision. Do not compare monotonic clocks across processes. The suspension request's validity/expiry check must use the child's actual observation time rather than the frozen launch time, with its boundary, timestamp precision, and uncertain-clock behavior explicitly specified and tested. Changes to a shared observer must preserve or deliberately version the contract for its other callers.

Tests should separately exercise: terminal observed before fence; sealed before child request-read but delivered to parent after fence; fence before seal; equal/ambiguous or missing ordering; expired request; and interruption/restart when an ordering observation was not durably recorded. Verify that neither child timing assertions nor telemetry can silently override the parent-side authority decision.

## 3. Partial failures: durable state and safe replay

Checkpoint publication, native custody ingestion, economics observation, and the outer database transaction are distinct boundaries. In particular, the economics observation's savepoint is inside the surrounding transaction, **not** an independently committed transaction. The joint matrix should verify actual durable storage after each injected failure, not just that a function was called.

| Failure boundary | Required interpretation and safe next step |
| --- | --- |
| Local seal before output/checkpoint | Local evidence may be usable only if retained, exact, and still authorized. If the ephemeral workspace is lost and no recoverable checkpoint contains the exact binding, the publication is unknown; retain appropriate custody/exposure and do not invent a result. |
| Checkpoint write fails or acknowledgement is lost | Distinguish confirmed absence from an unknown write outcome. Inspect the exact immutable checkpoint/receipt and validate it before idempotent recovery; unknown or conflicting evidence remains fenced. |
| Checkpoint is durable, database work rolls back | The remote checkpoint survives independently; native ingestion and other SQL writes in the aborted transaction do not. Recover the exact bound publication and replay under the applicable lease/fence rules, with idempotent ingestion. |
| Native ingestion succeeds, economics savepoint fails, outer transaction commits | Verify the actual committed custody and reconciliation state. Record/report the economics failure without manufacturing cost data; permit a safe economics replay. Reservation changes must follow the committed authoritative evidence and policy, not assumptions about the savepoint. |
| Economics savepoint succeeds but outer transaction rolls back | All SQL changes in that outer transaction roll back, including the observation; any already-emitted log is not proof of commit. Replay from exact durable evidence. |
| Database commit succeeds but acknowledgement is lost | Read back the exact immutable result/receipt and persisted state. Repeating the same ingestion/observation must be idempotent, including no duplicate revisions or charges; a conflicting identity fails closed. |

Please include failures around checkpoint publication, custody ingestion, savepoint failure, outer rollback and commit-acknowledgement loss, including retries and conflicting/tampered evidence. Provider custody and any at-risk spend remain subject to the actual committed records and existing policies; a missing economics observation is not by itself proof that provider work or spend vanished.

## Provider operations and suspension granularity

An authorized repeat **GET** of an already-known provider operation after a crash can be legitimate reconciliation; it is not equivalent to creating another paid operation. The decision must still respect current custody, lease/fence, provider operation identity and continuation authority. A duplicate paid **create** must not be issued simply because output or a checkpoint was lost. Tests should distinguish these operations and verify no duplicate create across crash/replay.

The current check is before a wave of up to four GETs, not before each individual GET. A fence arriving mid-wave cannot retroactively prevent requests in that wave, including work already selected but not yet started. State that bound honestly, test an injected mid-wave fence, and prove what may complete, what is durably recorded, and that no subsequent wave starts once the request is observed. Do not promise a hard timeout or a finer-grained stop unless the implementation and tests actually provide one. Likewise, do not assume post-wave local continuation or publication is fenced at a point for which no check exists.

## Joint gate and next step

I suggest SBE and API agree the identity/lookup schema and ordering rules first, then update their respective plans and implement the joined provider-free matrix against the real installed command and API receiver. Include compatibility checks for existing exact callers and any retained bounded work that we actually intend to recover, without silently routing an old binding through an incompatible worker. Exercise fake provider operations and negative/tamper cases without paid provider calls; release qualification and QA activation remain separate gates.

Once the three contracts above are explicit and both sides accept the failure matrix and tests, I expect Gate A can close. I do not see a need to change the overall design direction.
