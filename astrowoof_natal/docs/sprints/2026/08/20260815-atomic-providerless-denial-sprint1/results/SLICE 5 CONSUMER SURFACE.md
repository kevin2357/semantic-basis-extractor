# Slice 5 Consumer Surface

Status: complete; pending review and commit

## Installed interfaces

The batch operation is available through:

```python
from astrowoof_natal_authoring.lifecycle import deny_providerless_actions
```

and:

```text
astrowoof-authoring-lifecycle --run-dir RUN deny-providerless-batch \
  --request BATCH_NEGATIVE_AUTHORIZATION.json
```

The CLI supports the same default typed JSON result and optional external JSONL or
stdout-JSONL event transports as the existing lifecycle operations. Source-level
consumer tests invoke the documented CLI without importing implementation internals
and receive the v0.1 batch result.

## Event behavior

The API-approved policy is implemented:

- first application emits ordered per-action
  `authorization.denied_providerless` transitions, then one
  `authorization.denied_providerless_batch` result event;
- exact replay emits only the batch event with `idempotent_replay`;
- refusal emits only one optional batch event containing request digest, typed
  outcome, action count, and the same bounded outcome as reason category; and
- bindings, authority references, requests, and provider payloads never enter event
  data.

Event schema/catalog validation remains closed and versioned. Sink exceptions drop
events through the existing failure-isolated emitter and cannot affect the native
batch result. Tests prove all three first-application events may be dropped while
both action transitions and the complete snapshot still commit.

## Consumer handoff and migration

`docs/post_extraction_authoring/Authoring Lifecycle Consumer Handoff.md` now gives:

- the exact Python and CLI interfaces;
- API release conditions for successful member evidence;
- zero-release rules for every refused batch;
- packaged request/applied/replay/refusal fixture locations;
- request/result semantics and exact replay identity;
- terminal retained-workspace support;
- event behavior;
- interrupted-write retry rules and limitations; and
- migration from an inspect-once/sequential-single-denial loop to one batch call.

The original single-action operation remains documented and supported for genuine
one-action decisions.

## Provider-free installed-wheel qualification

A temporary source checkpoint wheel was built without dependency resolution and
installed into a fresh virtual environment outside the repository. The installed
smoke ran from `site-packages` and passed:

- packaged contract and batch-fixture loading;
- one legacy single-action denial;
- one two-action batch application;
- exact batch replay;
- approved event ordering;
- closeout/replay; and
- final complete snapshot validation.

The installed console help lists `deny-providerless-batch`. All four packaged batch
fixtures were enumerated through `importlib.resources`.

Temporary qualification wheel:

```text
astrowoof_natal_authoring-0.4.0-py3-none-any.whl
SHA-256 235e62f049a5c90b1645cbc8052d8a092d5af7275d59cf6ab6787d8765824bb3
```

This wheel is non-promoted evidence for the uncommitted Slice 5 source checkpoint.
It is not a release candidate, pin, tag, or published artifact.

## Gate evidence

- Focused batch/consumer/event/contract suite: 39 passed.
- Full repository suite: 294 passed.
- Installed lifecycle smoke: pass with `require_installed: true`.
- Installed batch fixtures: 4 present.
- Installed CLI batch subcommand: present.
- Provider operations: 0.
- Paid spend: $0.
- API key: not used.
