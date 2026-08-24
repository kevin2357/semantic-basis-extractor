# API Consumer Handoff — SBE 0.4.17

Use `astrowoof-natal-authoring==0.4.17` for the audited retained-provider bridge.

The supported retrieval-only command remains:

```text
astrowoof-semantic-closure --run-dir RUN --resume --provider openai \
  --provider-reconciliation-cycle --observed-at <canonical UTC instant>
```

The API supplies the trusted observation instant and invokes only the run-level
command. SBE validates the complete snapshot and native inventory, selects the
bounded due subset, performs GET-only retrieval, and publishes native evidence only
when a reconciliation checkpoint exists.

For a binding/native-run contradiction:

- result outcome is `review_required`;
- provider retrieval count is zero;
- no `result_checkpoint` or native transition publication exists;
- authoritative workspace bytes remain unchanged; and
- optional diagnostic event `execution.failed` carries reason
  `provider_binding_integrity_mismatch`.

The result outcome is authority; the event and logs are diagnostic only. The API
must retain the workspace for review and must not reinterpret refusal as permission
to submit or retrieve provider work.

The validated consistent-inventory behavior remains four GETs in the first due
cycle, two in the next due cycle, and a nonmutating `not_due` replay thereafter.

