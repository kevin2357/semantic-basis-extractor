# Evidence

- API worker logs show no observer completion or failure log for either target
  route.
- Didot completed delivery only after a single eligibility retry.
- Erasmus closed with the expected typed terminal-review result and no retained
  execution custody.

## Preliminary exact timeline

- Didot SBE publication at `2026-09-14T15:59:39Z`:
  - invocation `ninv_4049ced1f74647c3a56aba1e`;
  - result `nres_fd73a016721dcf725d6a5449`;
  - receipt `nreceipt_1d4f473bcd54f879e416ed93`;
  - native result v0.1 outcome `delivery_complete`;
  - exact `astrowoof.terminal_delivery_command_result.v0.1` emitted.
- Didot API first close: `provider_reconciliation` / `terminal_closed` at
  `16:00:12Z`, then retryable `terminal.publication.retry` at `16:00:13Z`.
- Didot API retry: `delivery_validation` / `delivery_accepted` at `16:00:41Z`,
  publication and closeout at `16:00:42Z`; no observer log.
- Erasmus SBE publication at `2026-09-14T16:10:50Z`:
  - invocation `ninv_2e71a7e0b2ce495cbfcf46f1`;
  - result `nres_68c273587d4363fe3d150cb9`;
  - receipt `nreceipt_a549e4b41eaa0ac8fe3f7329`;
  - native result v0.2 outcome `review_required`;
  - exact `astrowoof.terminal_review_command_result.v0.1` emitted.
- Erasmus first API close: `provider_reconciliation` / `terminal_closed` at
  `16:11:20Z`, non-retryable `native.terminal.review_required` closeout at
  `16:11:21Z`; no observer log.
- Erasmus later API close: `sealed_terminal_preflight` / `terminal_closed` at
  `16:12:38Z`, another non-retryable review closeout at `16:12:39Z`; no
  observer log.

Current source shows the Didot retry's delivery-validation result preserves no
sealed result ID. Current source also shows the Erasmus command-bearing close
should select ordinary-review observation, while a later sealed-preflight
review result alone does not satisfy that command-bound selection condition.

## Slice qualification summary

- Six current-source provider-free API tests passed: three transport/projection
  cases and three production-worker/observer cases.
- QA is bound to API `e412caf58dc4e47908559227ef69ecf37ba3ed23`
  and SBE-worker image digest
  `sha256:c4979464eeb15f45a3f814fd011ef525088af186ab0121e11c82d72b26c2bca1`.
- Both observer implementation commits are ancestors of that API revision.
- Erasmus attempts 11 and 12 are distinct claims with distinct attempt and
  lease identities; attempt 12 began after attempt 11's terminal-looking event
  sequence.
- Bounded QA persistence audit corrected the event-only interpretation:
  attempt 11 was durably `lease_expired`, not failed. Its command-bearing
  branch omitted `queue.fail()`, expired-lease collection scheduled attempt 12,
  and attempt 12 committed the final failure. No operator reactivation or R2
  inspection was involved.

## Export identities

| Export | Bytes | SHA-256 |
| --- | ---: | --- |
| `...-01.json` | 1,601,192 | `8537ba83385341c9ee873a5d6b95cc8808db15caea8920440ea1ab159f4b3a70` |
| `...-02.json` | 177,076 | `953f322ffd857633bf4aed92844787486e375ebbd39832ad3eb0c242f3875483` |
| `...-03.json` | 1,585,130 | `eaed07557de44b374c13df697d3129f1fbfef62a28b25c658d6301481a846d8d` |
