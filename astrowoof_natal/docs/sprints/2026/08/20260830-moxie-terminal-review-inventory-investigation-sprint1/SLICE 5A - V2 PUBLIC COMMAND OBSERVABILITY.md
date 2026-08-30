# Slice 5A — v2 public-command observability

## Outcome

The supported `astrowoof-external-authority-v2` command now connects the
existing SBE application logger and typed execution-event runtime to its public
CLI boundary. This closes SBE's portion of control-room issue #7 without
changing lifecycle, authority, custody, provider, or command-result semantics.

## Public command behavior

The command now supports:

- `--log-level`, `--host-id`, and `--invocation-id` through the common
  `✨🐶` logging formatter;
- `--events-jsonl <outside-workspace-path>`; and
- `--events-stdout-jsonl`, when the authoritative command result is written to
  `--output` so stdout remains an event-only stream.

The command binds native run/status context, logs entry and final disposition,
and propagates one failure-isolated emitter through the v2 intent and dispatch
boundaries. A validated request produces the existing closed events for request
selection, fence validation, intent commit, provider-create permission,
provider identity, pending custody, and typed refusal.

The authoritative result remains the closed JSON document written to
`--output`. Neither logs nor events authorize or prove native mutation.

## Privacy and failure isolation

Events contain only the existing bounded safe correlations, digests, counts,
action/provider identities, selected command, and closed reason codes. They do
not contain prompts, request payloads, authorization documents, credentials, or
subject data. Text logs likewise report closed outcomes and counts rather than
exception messages that may contain protected input.

Event serialization or sink failure remains observational: it can drop an
event and emit a warning, but cannot change intent, dispatch, provider-call, or
command-result behavior.

## Cross-repository boundary

This slice makes SBE emit the missing v2 trace. API still owns:

- passing `--events-stdout-jsonl` for deployed v2 invocations;
- relaying or retaining bounded SBE stderr from reconciliation;
- durable diagnostic retention and operator presentation; and
- keeping supplementary diagnostics separate from authoritative state.

## Qualification

Provider-free focused matrix:

```text
python -m unittest -b \
  astrowoof_natal.tests.test_external_authority_v2_cli \
  astrowoof_natal.tests.test_ambiguous_provider_submission_runtime \
  astrowoof_natal.tests.test_moxie_terminal_review_inventory_slice3

Ran 20 tests in 42.003s
OK
```

The matrix proves ordered success events, typed refusal, exact replay and
ambiguity preservation, sink-failure isolation, protected sentinel absence,
Moxie adoption/refusal diagnostics, and zero real provider/network activity.
`py_compile` and `git diff --check` passed.
