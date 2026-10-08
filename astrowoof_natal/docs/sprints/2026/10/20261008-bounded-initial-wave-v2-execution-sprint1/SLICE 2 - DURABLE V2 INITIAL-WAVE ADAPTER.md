# Slice 2 — Durable v2 Initial-Wave Adapter

## Implementation

`bounded_lifecycle.commit_bounded_initial_wave_v2_dispatch_intent()` is a
separate entry point from the ordinary external-authority v2 dispatcher. It
requires `initial_wave_admission`, re-inspects the exact checkpoint, validates
the v2 grant and six authorization documents, validates the stored bounded
wave/binding bundle/request bytes, and authorizes then begins submission for
all six members in their prepared semantic order.

It writes one `SUBMITTING` constrained intent before provider I/O. The intent
stores only a SHA-256 of its process-local capability. The raw capability is
kept in process memory keyed by workspace/request/grant; after process loss,
the adapter refuses a fresh submission rather than inventing a replacement
provider call.

`dispatch_bounded_initial_wave_v2_intent()` accepts only that exact pair and
delegates to `_execute_bounded_interactive_initial_wave()`. Thus it retains the
existing six-way parallel create, identity checkpoint, and ambiguity behavior.
It does not use the ordinary dispatcher’s lexical ordering or serial payload
resolver.

## Replay and failure boundary

- Repeating the exact commit returns the immutable intent receipt without
  rediscovering a now-stale pre-intent checkpoint and without provider I/O.
- A different request/grant after an intent exists is refused.
- A detached wave returns its existing result and makes no second create.
- Malformed or tampered workspace evidence refuses before intent creation.
- A process restart has no raw capability, so it cannot perform a new create;
  durable provider identity/reconciliation remains the only safe successor.

## Provider-free proof

`test_bounded_initial_wave_v2_contract.py` now proves:

1. one valid v2 grant produces exactly one semantic-order intent;
2. a fake bounded provider receives exactly the six expected creates;
3. commit and dispatch replay cause no duplicate create;
4. descriptor tamper, injected pre-intent failure, and duplicate documents
   fail closed before provider I/O.

## Public command envelope

`astrowoof-external-authority-v2` now recognizes
`initial_wave_admission` and performs commit and bounded dispatch within one
process. Its closed result schema is
`astrowoof.bounded_initial_wave_v2_command_result.v1`, deliberately distinct
from ordinary v2 results. It carries the run/checkpoint/request/grant/API
decision identities, semantic ordering, full initial-wave projection, durable
intent receipt, optional wave result, three explicit mutation/I/O/checkpoint
booleans, and a canonical `result_sha256`.

`checkpoint_published` is strictly per invocation: it is true only when that
command invocation made a durable checkpoint publication. Consequently an
exact replay has all three effect flags false. The public validator
`validate_bounded_initial_wave_v2_command_result()` and packaged schema reader
`read_bounded_initial_wave_v2_command_result_schema()` are the supported API
ingress surface; altered result bytes, effect claims, or digest refuse.

The outcome vocabulary is `pre_provider_refusal`,
`detached_provider_pending`, `exact_replay`, and
`ambiguous_custody_refusal`. A refusal is mechanically constrained to no
mutation, no provider I/O, and no checkpoint publication. A process restart
after intent cannot recreate a provider call; it returns the typed ambiguity
disposition instead.

## Installed-command evidence

The untagged local source wheel (`0.4.71`, SHA-256
`122a702c05bec119c5afed74710d9e5dcfff081f32ee9336827a4b0f594e4841`,
1,447,968 bytes) was installed into an isolated temporary venv. Its actual
`astrowoof-external-authority-v2` console command ran the bounded fixture with
`--provider fake` and produced:

- `detached_provider_pending`, exit 0, native mutation and provider-I/O true;
- `exact_replay`, exit 0, provider-I/O false; and
- a wrong-grant `pre_provider_refusal`, exit 3, mutation/I/O false.

The raw outputs are retained at
`C:\tmp\sbe-bounded-v2-installed-command-fixture.json` for the matching API
ingress fixture. This is provider-free fake transport only; it is not an
OpenAI request, a publish, or a deployment.
