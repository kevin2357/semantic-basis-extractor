# AstroWoof Natal Authoring 0.4.10 Release

Status: qualified immutable artifact; publication authorized

## Summary

SBE 0.4.10 adds durable, sanitized observability for interactive OpenAI Response
retrieval without changing provider custody, retry/backoff, spend authority,
lifecycle status, or delivery semantics.

Each attempted reconciliation GET now produces a snapshot-covered
`astrowoof.response_retrieval_diagnostic.v1` artifact. It records native and
provider identities, safe endpoint identity, timing, normalized provider status,
HTTP status and OpenAI request ID when available, and a bounded sanitized error
classification/fingerprint. Credentials, headers, query secrets, prompts, outputs,
and raw response bodies are excluded.

The release also adds:

```console
astrowoof-inspect-response --response-id resp_...
```

This installed-wheel probe performs exactly one read-only GET through the same
OpenAI provider transport/configuration construction used by reconciliation,
disables retries, and prints only the closed diagnostic. It accepts no run
directory and carries no native, spend, retry, reservation-release, or delivery
authority.

## Qualification

- Focused/directly affected source tests: 100 passed.
- Two fixed-epoch wheels: byte-identical.
- Exact installed-wheel API, CLI/schema, one-GET scripted probe, and packaged
  resource inspection: pass.
- Wheel boundary: 125 entries, 74 resources, no tests/bytecode, `py.typed` present.
- Real provider GETs/submissions/spend: 0 / 0 / USD 0.

The wheel is 843,325 bytes with SHA-256
`e27a4ea740f8492672f059209dbd743432cf3fd9bdcbf91e12a17a4be2ff437e`.

