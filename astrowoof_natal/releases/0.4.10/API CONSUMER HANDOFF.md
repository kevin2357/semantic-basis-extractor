# SBE 0.4.10 API Consumer Handoff

The public diagnostic contract is
`astrowoof.response_retrieval_diagnostic.v1`. Reconciliation artifacts live at:

```text
lifecycle/provider-reconciliation/<action-id>.attempt-<ordinal>.json
```

The snapshot-covered cycle record binds them by action/attempt identity, logical
path, bytes, and SHA-256. Existing lifecycle inspection and cycle-result contracts
remain unchanged.

Diagnostic outcomes describe the GET boundary:

- `completed`: retrieval completed; inspect `provider_status` for provider success
  versus `failed`, `cancelled`, or `incomplete`;
- `pending`: matching Response is `queued` or `in_progress`;
- `transport_warning`: HTTP/transport/protocol/malformed/unsupported-status issue;
- `identity_conflict`: a well-formed Response returned a different ID.

Diagnostics are non-authoritative operational evidence. They never authorize
resubmission, API reservation release, billing settlement, capacity release,
delivery, or publication.

For a surgical QA check, configure the same API key/base URL as the worker and run:

```console
astrowoof-inspect-response --response-id resp_...
```

Process success means a valid sanitized diagnostic was produced; consumers must
inspect `outcome`. The command performs one GET with retries disabled and does not
open or mutate a native workspace.

Detailed redaction and interpretation rules are in the sprint's
`RESPONSE RETRIEVAL DIAGNOSTIC CONTRACT.md` and `API AND QA HANDOFF.md`.

