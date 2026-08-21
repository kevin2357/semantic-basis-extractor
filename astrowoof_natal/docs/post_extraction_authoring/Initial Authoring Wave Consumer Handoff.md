# Initial Authoring Wave Consumer Handoff

## Supported boundary

Fresh exact- and bounded-Natal interactive authoring use one six-member initial
wave. The six members remain independently prompted paid actions, but the API must
authorize the exact complete wave before SBE creates any provider operation.

| Artifact | Identity |
|---|---|
| Prepared wave | `astrowoof.initial_authoring_wave.v1` |
| API wave authorization | `astrowoof.initial_authoring_wave_authorization.v1` |
| Aggregate create result | `astrowoof.initial_authoring_wave_result.v1` |
| Complete binding bundle | `astrowoof.initial_authoring_wave_binding_bundle.v1` |
| Joined authority inputs | `astrowoof.initial_authoring_wave_authority_inputs.v1` |

These contracts do not replace lifecycle inspection v0.3, reconciliation-cycle
result v0.2, the native transition journal/result/receipt, or the six ordinary
member spend authorizations. They bind initial-create topology; existing native
contracts remain authoritative for custody, scheduling, terminal meaning, and
publication.

`prepared_wave.run_id` is the SBE-native run identity. In AstroWoof API persistence
it binds exactly to `SbeAuthoringRun.native_run_id`; it is not
`GenerationRun.id`. Both identifiers exist during one product pipeline run and are
not interchangeable.

## API adoption sequence

1. Start or resume the supported exact/bounded runner until SBE publishes the
   prepared wave, binding bundle, and six `PREPARED` spend actions.
2. Call `read_initial_wave_authority_inputs(run_dir)` or
   `astrowoof-initial-wave-contract --initial-wave-inputs --run-dir <run>`. SBE
   validates the complete snapshot, both documents, and their exact join before
   returning either.
3. Persist the returned prepared wave and bundle, verify both native run IDs equal
   `SbeAuthoringRun.native_run_id`, then atomically reserve the
   exact complete six-action set in API-owned storage. A partial API reservation set
   must not cross the SBE execution boundary.
4. Create six ordinary member authorization documents by copying the exact complete
   binding from each ordered bundle member. Then create the wave-level
   authorization with `build_wave_authorization()`. Persist all seven documents.
5. Resume with `--initial-wave-authorization` and exactly six ordered
   `--spend-authorization` arguments. SBE validates the complete set before any
   provider create or authorization consumption.
6. Ingest the immutable native result/receipt before interpreting command exit.
   Validate lifecycle inspection and persist mapped API state transactionally.
7. Release the worker slot when inspection says `release_until_due`; retain every
   listed provider-custody action and consumer-authority action.
8. Reclaim on or after `resume_not_before`. Never poll early and never use the wave
   result alone as scheduling authority.

The API remains authoritative for cross-run reservations, account/global quotas,
circuit breakers, entitlements, billing reconciliation, capacity records, and
public product state. SBE remains authoritative for its native workspace, exact
action bindings, provider identities, snapshot, journal, result/receipt, and
semantic progression.

## Authority cardinality

- **Interactive:** six paid SBE actions and six API reservation members, bound
  together by one all-or-none initial-wave reservation set.
- **Batch:** one paid SBE action and one API reservation per Batch round. Its six
  logical members are audit/settlement evidence beneath that round and must not be
  multiplied into six global reservations.

Both remain bounded by immutable run spend authority. Switching transport does not
change editorial pass membership, request semantics, or validation authority.

## Create and crash outcomes

- `provider_bound`: the exact Response ID is durably checkpointed; reconcile only.
- `authorized_unstarted`: SBE has positive evidence create was not attempted.
- `create_refused`: the provider definitively refused creation without accepting an
  operation.
- `ambiguous_submission`: acceptance may have occurred but no provider identity is
  durable; fail closed and retain API authority.

Before any POST, SBE checkpoints all six actions as `SUBMITTING`. It then checkpoints
each returned ID individually. There is still an irreducible provider atomicity gap
between provider acceptance and local ID persistence. Deterministic request keys are
correlation material, not proof of OpenAI idempotency. The API must never turn an
ambiguous member into retry authority automatically.

## Packaged consumer resources

- `contracts/initial-wave-contracts.v1.schema.json`
- `contracts/initial-wave-result.v1.schema.json`
- `contracts/initial-authoring-wave-binding-bundle.v1.schema.json`
- `contracts/initial-authoring-wave-authority-inputs.v1.schema.json`
- `fixtures/initial_wave/prepared-wave.v1.json`
- `fixtures/initial_wave/wave-authorization.v1.json`
- `fixtures/initial_wave/six-id-detach.v1.json`
- `fixtures/initial_wave/partial-ambiguity.v1.json`
- `fixtures/initial_wave/exact-binding-bundle.v1.json`
- `fixtures/initial_wave/bounded-binding-bundle.v1.json`

Python consumers may import from the package root:

```python
from astrowoof_natal_authoring import (
    build_wave_authorization,
    read_initial_wave_authority_inputs,
    preflight_wave_authorization,
    read_initial_wave_fixture,
    read_initial_wave_schema,
    validate_initial_wave,
    validate_initial_wave_result,
    validate_initial_wave_authority_inputs,
    validate_initial_wave_binding_bundle,
    validate_initial_wave_binding_bundle_against_wave,
    validate_wave_authorization_document,
)
```

Provider-free CLI exports are available as:

```text
astrowoof-initial-wave-contract --fixture prepared
astrowoof-initial-wave-contract --fixture authorization
astrowoof-initial-wave-contract --fixture six-id-detach
astrowoof-initial-wave-contract --fixture partial-ambiguity
astrowoof-initial-wave-contract --schema wave
astrowoof-initial-wave-contract --schema result
astrowoof-initial-wave-contract --schema binding-bundle
astrowoof-initial-wave-contract --schema authority-inputs
astrowoof-initial-wave-contract --fixture exact-binding-bundle
astrowoof-initial-wave-contract --fixture bounded-binding-bundle
astrowoof-initial-wave-contract --initial-wave-inputs --run-dir <restored-run>
```

The run-specific operation is provider-free and read-only. An `--output` path must
resolve outside the run workspace. It returns one content-bound closed wrapper with
both `prepared_wave` and `binding_bundle`; a snapshot, document, digest, or join
failure returns neither. The API must not reconstruct either document from
`run.json`, `spend-authorization-requests.json`, packet files, or logs.

Unsupported versions, extra fields, changed digests, reordered/missing members, and
aggregate/member conflicts fail closed.

## Lifecycle examples after create

| Phase | Authoritative or adoption evidence |
|---|---|
| Awaiting complete wave authority | prepared-wave fixture plus inspection v0.3 |
| Six-ID detach | `six-id-detach.v1.json`, then inspection v0.3 |
| Partial ID / ambiguity | `partial-ambiguity.v1.json`, native result/receipt |
| Pending / not due / reclaim | reconciliation policy v0.2 and cycle fixtures |
| Batch round | bounded route-parity traces and Batch native action evidence |
| Deterministic fan-in | ordinary native journal/result/receipt progression |
| Pass-local retry | route-parity trace; a new exact retry action, not wave replay |
| Final QA/review | native terminal result and immutable publication receipt |
| Delivery | delivery manifest/provenance plus terminal native result/receipt |

`provider.identity_recorded` and `provider.waiting` events repeat once per durable
interactive member identity. `run.detached`, `checkpoint.committed`, and
`native.result_published` describe the aggregate command boundary. Events are
redacted, failure-isolated observations; they are never authority and must not be
used to reconstruct missing native facts.

## Consumer safety rules

- Read HTTP/API status from API-owned persisted state, never a live worker
  filesystem.
- Ingest validated SBE public/native evidence transactionally before releasing an
  API worker lease.
- Worker-slot release never implies provider-custody or reservation release.
- A completed Response may settle one member, but deterministic fan-in waits for
  every required pass outcome.
- Do not parse private `run.json`, subprocess log text, packet directories, or event
  order as a substitute for public contracts.
- Legacy serial/timing-free workspaces are not silently reinterpreted as v1 waves.
## External authority continuation fence

For current interactive initial-wave admission, consumers must use lifecycle
inspection v0.5's embedded `external_authority_request` and provide one exact
`astrowoof.external_authority_grant.v1` plus the six complete ordered ordinary
authorization documents. A prepared wave is not create permission. Generic resume
against an awaiting, authorized, or submitting wave fails closed.

SBE commits all six `SUBMITTING` actions and one constrained submission intent
under native single-writer ownership before provider I/O. Provider-return/identity
persistence remains an irreducible provider atomicity gap and becomes ambiguity,
not replay permission. See the current sprint's
`EXTERNAL AUTHORITY CONSUMER HANDOFF.md` and run the installed, provider-free
`astrowoof-external-authority-qa` command when qualifying a worker image.
