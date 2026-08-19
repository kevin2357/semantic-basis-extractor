# Response Retrieval Diagnostic Contract

Contract: `astrowoof.response_retrieval_diagnostic.v1`

This closed artifact records one attempted read of one already-known OpenAI
Response. It is operational evidence only. It cannot authorize submission,
retry, cancellation, reservation release, spend settlement, delivery, or any
other lifecycle transition.

## Classification

- `completed`: the GET returned a well-formed matching Response whose retrieval
  is complete. `provider_status` may still say `failed`, `cancelled`, or
  `incomplete`; the word describes completion of the GET, not authoring success.
- `pending`: the matching Response reports `queued` or `in_progress`.
- `transport_warning`: the GET raised, returned malformed data, or returned an
  unsupported status. Existing provider custody and backoff remain in force.
- `identity_conflict`: a well-formed returned Response carries a different ID.
  Existing fail-closed review behavior remains in force.

Each diagnostic binds run/action IDs when it belongs to reconciliation, the
provider Response ID, fixed GET route identity, start/end/duration, normalized
provider status, and optional sanitized error metadata. Probe diagnostics use
null run/action IDs.

## Redaction threat table

| Input fact | Retained form |
|---|---|
| API key, Bearer token, authorization/cookie headers | Never retained; known patterns and exact configured key become `[REDACTED]` |
| Prompt, output, HTTP body, arbitrary exception object | Never retained |
| Exception text | Whitespace-normalized, redacted, and truncated to 512 characters |
| Error fingerprint | SHA-256 of sanitized exception class, HTTP status, and sanitized message |
| Endpoint | `GET /responses/{response_id}` and scheme/host/explicit port only |
| URL query or userinfo | Never retained |
| HTTP status | Optional integer when supported transport metadata exposes it |
| OpenAI request ID | Optional string when supported transport metadata exposes it |
| Response status | Normalized returned `status`, never the response body |

The sanitizer is a defense-in-depth boundary, not permission to pass arbitrary
secrets into exception messages. Diagnostic artifacts are included in the normal
workspace snapshot. Writes and cycle reduction remain single-writer even though
the provider GET calls are concurrent.

## Probe

`astrowoof-inspect-response` performs one GET through the same
`OpenAIResponsesProvider` transport construction used by reconciliation, with
transport retries disabled and a default 15-second request timeout. It accepts no
run directory and refuses an output path inside a recognized native run
workspace. Its JSON is diagnostic-only and must not be used as native run or API
financial authority.

