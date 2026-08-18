# Slice 0 — Four-Pipeline Baseline and Seam Inventory

Date: 2026-08-18
Provider operations created by this slice: 0
Result: pass; contract work may proceed after review

## Executive finding

The four pipelines share the intended six-pass editorial topology but do not share
one submission lifecycle:

| Pipeline | Current initial submission shape | Current detach shape | Required change |
|---|---|---|---|
| Exact interactive | Default `max_workers=6`; with prompt caching enabled, one cache-warmer pass completes first and the remaining five run in a thread pool | Threads remain inside `author()` polling until completion or timeout | Replace blocking author calls with complete-wave authorization, six concurrent creates, immediate ID commits, and detach |
| Bounded interactive | A plain ordered loop executes and completes one pass before entering the next | Each pass blocks inside provider execution | Introduce the shared six-create wave and detachable reconciliation |
| Exact Batch | One paid Batch round contains six pass members | Existing detach persists one File/Batch identity | Preserve and prove one-round authority; do not apply interactive reservation cardinality |
| Bounded Batch | One paid Batch round contains six pass members | Existing detach persists one File/Batch identity | Preserve and prove one-round authority; do not apply interactive reservation cardinality |

Exact interactive therefore already has editorial execution concurrency in part of
its legacy blocking path, but it does not have the production shape requested by
this sprint. It may deliberately serialize a cache warmer, and its worker threads
poll provider work rather than durably create and release the worker. Bounded
interactive is fully serial.

## Exact interactive seam

`author_pending_passes()` defaults from the CLI to six workers. When prompt caching
is enabled and all passes are fresh, it selects the smallest source archive as a
cache warmer and invokes it synchronously. Only after that pass closes does it
submit the remaining specs to a `ThreadPoolExecutor`.

Each `OpenAIResponsesProvider.author()` call combines all phases:

1. construct and persist the request;
2. invoke `before_submit`, which prepares or consumes one paid action;
3. POST `/responses`;
4. persist the background response marker;
5. invoke `provider_created`, which records the Response ID in the native ledger;
6. poll the Response in the same call until it completes or reaches the long
   response timeout; and
7. parse and return editorial output.

This coupling is the main seam to split. Existing thread-local active-action IDs
and a shared native state lock already demonstrate useful foundations, but the
current callback prepares authority lazily during provider execution. It does not
provide one complete wave preflight or a short create-only command boundary.

The exact default is consequently closer to:

```text
complete cache warmer + max(remaining five blocking author calls)
```

than either fully serial or the desired:

```text
authorize six + max(six create calls) + durable ID overhead + detach
```

Removing cache-warm serialization changes cost/cache behavior and must be recorded
as an intentional topology decision. Cache savings remain historical evidence, not
a sufficient reason to serialize a deck's initial editorial wave.

## Bounded interactive seam

`resume_bounded_run()` iterates `bounded["pass_ids"]` in order. For every unaccepted
pass, `_execute_stage()` calls `provider.execute()`, which delegates to the same
blocking Responses provider and does not return until that pass has provider output
or a pause/error. The next pass is not considered until the current pass is
accepted or exhausted.

The retained Kevin SBE 0.4.6 live run proves the production effect. Its six initial
provider identities were recorded at journal sequences 14, 28, 42, 56, 70, and 84.
The first-to-sixth identity span was 588 seconds. Consecutive identity gaps were:

```text
129.512, 131.212, 110.982, 111.941, 104.352 seconds
```

Those gaps correspond to waiting for each pass to finish before beginning the next
authorization/submission cycle. The evidence workspace and provider IDs remain
untouched.

## Exact and bounded Batch seams

Both Batch implementations already express initial fan-out correctly at the
provider transport level:

- one round builds six `/v1/responses` JSONL members;
- one File/Batch create produces one durable provider operation;
- one SBE paid action and API reservation bind the aggregate round;
- member identity, output, error, usage, and retry evidence remain subordinate to
  that round; and
- detach/reconciliation can proceed without a resident worker.

This sprint must not replace that with six Batch jobs or six API reservations. The
shared initial-wave identity may describe the six logical members, but transport
authority remains one Batch round.

## Existing provider-pending substrate

The released reconciliation path already provides important downstream machinery:

- known interactive Response retrieval is separated from submission;
- up to four due interactive actions are retrieved concurrently per bounded cycle;
- the provider request timeout is 15 seconds and provider-I/O wall-clock policy is
  20 seconds;
- known IDs cannot enter submission through reconciliation-only paths;
- exact and bounded adapters ingest completed results through route-specific logic;
- run-level inspection distinguishes local capacity from provider custody and
  consumer-authority retention; and
- snapshots, journal projection, immutable results, and receipts support
  fresh-worker restoration.

The missing substrate is on the front edge: prepare all six exact interactive
actions, validate complete API authority, perform create-only I/O concurrently,
and durably commit all returned IDs before detaching.

## Single-writer and crash implications

The existing `SpendController` uses a filesystem consumption lock, an in-process
state lock, thread-local active action IDs, and a state-revision compare before
submission. These are useful but are currently designed around one lazily prepared
callback per author call.

The new coordinator must avoid six concurrent calls each publishing a complete
wave-level workspace checkpoint. Provider I/O may overlap; native mutation must be
serialized. Each returned ID receives its own serialized ledger and journal
durability step immediately when that create returns—it must not wait for the other
five tasks. Only the aggregate wave-level snapshot, command result, and publication
receipt wait until all create tasks unwind and the coordinator has classified every
member outcome.

The irreducible provider gap remains per member: a process can fail after OpenAI
accepts a create but before SBE durably records its ID. That member becomes
ambiguous. Other members with durable IDs remain provider-bound, and members whose
create was provably never attempted remain authorized/unstarted. There is no
provider transaction spanning six Responses.

## Contract consequences for Slice 1

1. Interactive needs one versioned six-member wave prepare artifact and one
   digest-bound complete-wave authorization envelope.
2. The API transactionally owns the six-reservation set; SBE validates its complete
   exact evidence before any create.
3. SBE needs a create-only provider interface. Reusing blocking `author()` would
   retain worker capacity and fail the central requirement.
4. Per-member `SUBMITTING`, provider-ID, ambiguity, and untouched states must be
   expressible together without one global `active_action` assumption.
5. Native state writes remain single-writer even though provider create I/O is
   concurrent.
6. Existing inspection v0.3 and cycle-result v0.2 appear semantically sufficient,
   but strict schema additions may be needed for wave identity and per-action
   authorization. Slice 1 must decide versions explicitly.
7. The numeric create count is fixed at six. Per-create timeout and total cycle
   bound must be frozen after scripted create-latency measurement rather than copied
   blindly from retrieval policy.
8. Batch retains one round action/reservation and six member identities.
9. Slice 1 must explicitly remove full-response cache-warmer serialization, or
   demonstrate a nonblocking create-only warm-up with useful measured cache evidence.
   The latency barrier cannot survive as an implicit cost optimization.
10. Keep submission concurrency at six and released retrieval concurrency at four.
    They solve different problems; a completed wave may be ingested through two
    bounded retrieval subwaves.

## Focused test evidence

Command:

```text
python -m unittest \
  astrowoof_natal.tests.test_semantic_closure.TestSemanticClosure.test_passes_can_execute_concurrently_without_corrupting_ledger \
  astrowoof_natal.tests.test_semantic_closure.TestSemanticClosure.test_batch_service_authors_six_passes_and_records_discount \
  astrowoof_natal.tests.test_bounded_lifecycle.TestBoundedLifecycle.test_bounded_batch_authors_six_members_under_one_round \
  astrowoof_natal.tests.test_bounded_lifecycle.TestBoundedLifecycle.test_interactive_and_batch_converge_before_and_through_optional_stages \
  astrowoof_natal.tests.test_provider_pending_capacity.TestProviderPendingCapacityBaseline.test_four_due_retrievals_run_in_one_parallel_wave
```

Result:

```text
Ran 5 tests in 8.738s
OK
```

The tests prove existing exact fake-provider thread overlap, exact and bounded
six-member Batch rounds, bounded interactive/Batch output convergence, and released
parallel retrieval. They do not claim the current interactive submission path is
detachable.

Full baseline suite:

```text
python -m unittest discover -s astrowoof_natal/tests -p "test_*.py"
Ran 423 tests in 321.471s
OK (skipped=10)
```

## Slice 0 gate recommendation

Proceed to Slice 1 contract design. The shared seam should be a new bounded initial
wave coordinator above route-specific packet adapters and below lifecycle command
publication. It should reuse the released reconciliation substrate after provider
IDs exist and preserve Batch's one-round authority model.
