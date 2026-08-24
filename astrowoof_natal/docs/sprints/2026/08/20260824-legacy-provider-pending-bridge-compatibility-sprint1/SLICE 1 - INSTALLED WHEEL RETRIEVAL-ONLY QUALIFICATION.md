# Slice 1 — Installed-Wheel Retrieval-Only Qualification

Status: complete; owner/API review pending before Slice 2

## Qualified artifact

- Distribution: `astrowoof-natal-authoring==0.4.16`
- Immutable tag: `astrowoof-natal-authoring-v0.4.16`
- Tag commit: `21705500a3aa6c5f3310a0aaee8aee8a71e4bdac`
- Wheel SHA-256:
  `56e26d82bb4689907dc830903721acf34a4c385557c7825c3ece19297f48d339`

The wheel was installed with `--no-deps` into a fresh virtual environment and
invoked through its generated public console executables from outside the source
package.

## Real command boundary

The test invoked:

```text
astrowoof-semantic-closure --run-dir RUN \
  --resume --provider openai \
  --provider-reconciliation-cycle \
  --observed-at 2026-08-24T15:00:00Z \
  --openai-base-url <scripted-loopback>/v1 \
  --max-transport-retries 0
```

The loopback adapter implemented only the provider HTTP boundary. Every GET
returned the exact requested Response ID with status `in_progress`. Any POST was
recorded as a contract violation and returned an error.

## Results

The first command cycle:

- selected four actions natively;
- issued exactly four distinct `GET /v1/responses/{id}` requests;
- issued no POST/create/submit/retry request;
- persisted four pending attempts and their new custody schedule;
- returned `detached_provider_pending` and the strict v0.2 cycle result;
- wrote and snapshot-bound the cycle artifact; and
- published a native `provider_reconciliation` result under SBE 0.4.16.

The installed `astrowoof-native-transition --latest` reader validated the complete
snapshot, bounded journal range, immutable result, retained checkpoint basis, and
publication receipt as one joined public view.

The second immediate command cycle correctly selected the remaining two originally
due actions. It issued exactly two further unique GETs, no POST, and published the
second bounded reconciliation checkpoint. This is the expected 4+2 behavior, not a
replay defect.

The third immediate command cycle returned `not_due`, performed no retrieval, and
left every authoritative workspace byte unchanged. It did not publish a new native
result because it created no checkpoint.

Each of these incompatible inputs was rejected by the public parser before file
loading or provider activity:

- spend authorization;
- spend reconciliation;
- legacy initial-wave authorization; and
- external-authority request plus aggregate grant.

All six Response paths were unique. Provider credentials were a local sentinel;
external network calls and provider spend were zero.

## Finding

The immutable 0.4.16 wheel already exposes the required retrieval-only bridge
mechanism for this frozen historical shape. Slice 1 found no runtime compatibility
gap and recommends proceeding to the broader replay/refusal/temporal matrix before
issuing the final `supported_now` decision.

