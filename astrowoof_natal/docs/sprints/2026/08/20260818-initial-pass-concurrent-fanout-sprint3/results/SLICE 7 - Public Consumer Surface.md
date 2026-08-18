# Slice 7 — Public Consumer Surface

## Result

The initial-wave contract is now a supported installed-wheel consumer boundary.
Consumers can validate/export the prepared wave, complete API authorization, six-ID
detach result, and partial-ambiguity result without importing private route modules,
reading `run.json`, invoking a provider, or parsing subprocess logs.

## Public Python and CLI

The package root exports provider-free builders, validators, and installed-resource
readers for the three v1 contracts. The new
`astrowoof-initial-wave-contract` command exports each validated fixture or schema.
Unsupported versions, extra fields, digest changes, incomplete/reordered action
inventories, and aggregate/member conflicts fail closed.

The route runners retain their established execution seam:

```text
--initial-wave-authorization WAVE-AUTHORIZATION.json
--spend-authorization MEMBER-1.json ... MEMBER-6.json
```

Complete authority preflight remains before provider creation and authorization
consumption.

## Packaged resources

- Combined prepared-wave/authorization JSON Schema.
- Aggregate result JSON Schema.
- Prepared exact-Natal wave fixture.
- Complete wave-authorization fixture.
- Six-provider-ID detached result fixture.
- Partial known-ID / ambiguity result fixture.
- Contract-catalog and lifecycle-smoke registration.
- Hash-bound Slice 7 consumer-review manifest.

The API handoff maps those resources to existing inspection v0.3,
reconciliation-cycle v0.2, route-parity, journal/result/receipt, final-QA, and
delivery evidence. It explicitly distinguishes six interactive reservation members
from one Batch-round reservation.

## Event and disclosure boundary

The wave reuses existing closed event names. Per-ID
`provider.identity_recorded`/`provider.waiting` events are non-authoritative,
redacted observations; aggregate detach/checkpoint/result events remain the command
boundary. No new event vocabulary was necessary.

Provider-visible subject minimization remains unchanged and revalidated. Protected
birth datetime, coordinates, location, and evidence do not enter authoring, retry,
polish, critic, or candidate requests.

## Qualification

- Public wave/lifecycle/journal/event/disclosure suite: 69 passed in 3.216 seconds.
- Wave/public/proposal suite after strict validator expansion: 23 passed; eight
  optional JSON-Schema-library checks skipped because `jsonschema` is not a runtime
  dependency. Runtime closed validators and installed-resource readers passed.
- Source lifecycle smoke: pass.
- Built wheel SHA-256:
  `30b91c0d422e1a1e1fd14e1019cc0b9e4bb33b576f00b071b4cf2ffd3132b583`.
- Fresh venv installed-wheel Python import/validation: pass.
- Installed `astrowoof-initial-wave-contract` fixture export: pass.
- Installed lifecycle smoke with `--require-installed`: pass.
- Provider operations and paid spend: zero.

## Review gate

This slice pauses for API review before Slice 8 joint/cross-platform qualification.
The review manifest status remains `awaiting_api_review` until that review is
recorded.
