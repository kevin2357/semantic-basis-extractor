# Slice 1 — Adversarial Trace Contract and API Handoff

Status: SBE candidate implemented and qualified; paused for joint schema and
authority review before executable adapters.

## Public contract

Schema identity: `astrowoof.lifecycle_adversarial_trace.v1`

Packaged schema: `lifecycle-adversarial-trace.v1.schema.json`

Supported Python surface:

- `read_adversarial_trace_schema()`
- `read_adversarial_trace_fixture(name)`
- `build_adversarial_trace_fixture(name)`
- `validate_adversarial_trace(trace)`
- `finalize_adversarial_trace(trace)`
- `canonical_adversarial_trace_bytes(trace)`
- `derive_adversarial_trace_id(trace)`
- `derive_adversarial_trace_sha256(trace)`

All are exported from `astrowoof_natal_authoring`. The Python validator is the
normative semantic validator and does not depend on optional `jsonschema`.

## Authority boundary

The trace is qualification evidence, not execution authority. It cannot authorize
provider work, mutate a native workspace, release API reservations, allocate API
capacity, or replace native results and publication receipts.

SBE owns the projected native facts and their interpretation. The API fixture owns
only modeled API run/job/lease/capacity/reservation facts. Provider state is a
scripted provider-free projection. Each resource remains visibly separated in the
trace.

The trace references public evidence only through kind, version, digest, and an
opaque fixture reference. It deliberately excludes provider request/response
payloads, prompts, raw provider IDs, workspace paths, credentials, and protected
subject data.

Native/API run references and starvation references must also use the closed
`fixture:` opaque-reference shape. Native reason codes and refusal reasons are closed
vocabularies, preventing a producer from hiding subject/provider/workspace material
inside otherwise free-form diagnostic strings.

## State and progress model

Each transition contains two identities:

- `raw_evidence_sha256` identifies the input evidence bytes represented at that
  step; and
- `semantic_fingerprint_sha256` identifies the closed native/API/provider facts
  that determine future modeled behavior.

A new timestamp, rewritten wrapper document, state revision, snapshot identity, or
raw digest is not semantic progress by itself. Future-fencing identities are carried
in the closed, lexically ordered `semantic_fences` inventory. The checkpoint-basis
fence is mandatory and must exactly match the materialized checkpoint basis;
additional action-inventory, authority-request, provider-custody, and publication
fences are retained when they determine future admissibility, stale-observation,
authority, replay, or publication behavior. The fingerprint hashes this explicit
semantic projection rather than observational revision/snapshot churn.

The closed classifications are:

- `productive`
- `legitimate_wait`
- `idempotent_replay`
- `stutter`
- `cycle`
- `refused`
- `contradictory_evidence`

Starvation is a separate multi-run witness. It is not flattened into a transition
classification.

`refused` is exactly equivalent to a disabled selected event with one closed refusal
reason. Every other classification requires an enabled event and null refusal reason.
`contradictory_evidence` remains an enabled observation of invalid materialized
facts—not an ordinary refusal.

`cycle` additionally requires a replayable recurrence witness containing the same
semantic fingerprint at an earlier logical step. A single identical before/after
transition without that earlier recurrence is `stutter`; an explicitly supported
nonmutating operation is `idempotent_replay`.

Materialized state and oracle classification are also separate. Legally reached and
historical states must be internally coherent. Deliberately synthetic invalid states
must declare the exact closed contradiction set produced by validation.

## Construction and time

`construction_class` is one of:

- `legally_reached`
- `historical_shape`
- `synthetic_invalid_state`

Every event advances one logical step. Simulated time changes only through an
explicit time event and uses canonical whole-second UTC `Z` form. This prevents
ordinary inspection or document publication from silently acting as elapsed time.

## Frozen route matrix

Both exact and bounded Natal are modeled. Response initial/retry/polish/critic/
candidate paths are supported. Batch initial and creative-retry paths are supported;
Batch optional stages remain explicitly refused. Closeout is supported as local
work with no provider mechanism. Unsupported combinations must be represented as
`explicitly_refused`, never silently omitted.

## Canonical fixtures

- `review-no-action-cycle.v1.json`: the historical Muffin reduction. Raw evidence
  changes while the semantic state recurs; a competing run supplies a distinct
  starvation witness.
- `provider-not-due-legitimate-wait.v1.json`: known pending provider custody with a
  declared due boundary; API fixture lease and capacity are released.
- `contradictory-command-custody.v1.json`: deliberately invalid reconciliation
  command without provider custody; exact contradiction is declared.

Packaged fixtures are compared byte-semantically with deterministic builders during
read. Fixture drift therefore fails closed.

## API consumption requirements

The API should ingest only a trace that passes both structural schema validation and
the public SBE semantic validator. It must not infer absent private evidence, treat a
trace as native authority, or use the fixture's API projection as a statement about
a deployed database.

The first composed vertical slice will use the historical Muffin trace to exercise
the API's actual production translator twice: once to demonstrate the historical
loop and once to prove the corrected typed non-local disposition releases capacity.
That executable adapter remains Slice 2 work and is intentionally not claimed by
this contract slice.

## Compatibility

Version 1 is closed-world. New keys, classifications, resource states, construction
classes, or route semantics require a new schema version unless they are already
represented by the frozen vocabulary. A fixture corpus update that changes an
existing fixture's digest is a consumer-visible change and requires coordinated
review.
