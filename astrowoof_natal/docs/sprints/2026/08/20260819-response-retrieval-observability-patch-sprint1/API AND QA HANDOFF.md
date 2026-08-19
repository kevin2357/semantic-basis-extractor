# API and QA Handoff

## Surgical probe

Set the same API-key and base-URL configuration used by the worker, then inspect
one durable Response ID:

```console
astrowoof-inspect-response --response-id resp_...
```

Optional controls:

```console
astrowoof-inspect-response \
  --response-id resp_... \
  --api-key-env OPENAI_API_KEY \
  --openai-base-url https://api.openai.com/v1 \
  --timeout-seconds 15
```

The command performs exactly one GET, disables transport retries, prints only the
closed sanitized diagnostic, and does not open or mutate an SBE run. A zero exit
means the probe itself produced a valid diagnostic; consumers must inspect
`outcome` rather than treating process success as provider success.

## Durable run evidence

Interactive reconciliation now writes one artifact per attempted action under:

```text
lifecycle/provider-reconciliation/<action-id>.attempt-<ordinal>.json
```

The cycle record contains `diagnostic_artifacts` entries with action/attempt ID,
logical path, bytes, and SHA-256. These artifacts are covered by the workspace
snapshot. Existing lifecycle state, custody, backoff, and cycle-result vocabulary
are unchanged.

Never use these diagnostics to infer that a provider operation may be resubmitted
or that API reservation/financial authority may be released. Provider IDs,
provider evidence, native lifecycle results, and API-owned ledgers retain their
existing authority.
