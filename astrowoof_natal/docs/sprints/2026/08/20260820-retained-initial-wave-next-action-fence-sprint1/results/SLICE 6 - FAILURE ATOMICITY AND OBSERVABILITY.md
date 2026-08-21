# Slice 6 — Failure Atomicity and Observability

Status: implemented and provider-free qualified; awaiting review.

## Durable boundaries

| Injected boundary | Required result |
|---|---|
| stale request or invalid/partial grant | no native mutation; no provider call |
| after request/grant validation | no native mutation; no provider call |
| before durable constrained intent | no native mutation; no provider call |
| after durable constrained intent | six durable `SUBMITTING` actions; generic resume refused; no provider call by the interrupted invocation |
| provider return before identity persistence | durable ambiguity; no create replay permission |
| after each identity checkpoint | durable provider identity; later work is reconciliation-only |
| after final wave snapshot | complete detached checkpoint; stale constrained invocation refused; no duplicate create |

Authorization application and the all-member `SUBMITTING` intent are deliberately
one native mutation/checkpoint. There is no supported intermediate “authorized but
not intended” continuation state. This removes rather than documents an additional
crash window.

## Provider atomicity limit

SBE cannot atomically combine an OpenAI create with local identity persistence.
If the provider may have accepted a request but its returned identity is not
durable, SBE records ambiguity and refuses another create. Deterministic local keys
remain correlation evidence, not proof of provider idempotency.

## Diagnostics

Concise structured ✨🐶 logs now identify:

- external-authority request read start and selected request kind/count/digest;
- constrained fence request/grant identity and member count;
- durable intent revision;
- provider-I/O permission boundary; and
- generic/legacy/partial bounded refusal categories.

Lifecycle inspection continues to emit the redacted, failure-isolated
`lifecycle.branch_selected` event. Provider identity and waiting events remain
per-action. Logs and events are observational only; the request, grant, ledger,
snapshot, lifecycle inspection, and native result remain authoritative.

The constrained boundary additionally emits this closed ordered vocabulary:

1. `external_authority.request_selected`;
2. `external_authority.fence_validated`;
3. `external_authority.intent_committed`;
4. `external_authority.provider_create_permitted`; or
5. `external_authority.refused` when selection/validation cannot authorize create.

Sink exceptions are absorbed by `ExecutionEventEmitter`; they cannot change native
state, snapshots, authorization consumption, or provider behavior.

No log or event includes request payloads, protected subject data, authorization
documents, credentials, or complete bindings.
