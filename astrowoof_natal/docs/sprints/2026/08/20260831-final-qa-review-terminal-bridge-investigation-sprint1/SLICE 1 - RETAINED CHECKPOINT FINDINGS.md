# Slice 1 — retained checkpoint findings

## Decision

Generation 18 is sufficient. Generation 17 is not needed.

The retained checkpoint proves an internally contradictory native scheduling
projection:

- outer run status: `FINAL_QA_REQUIRES_REVIEW`;
- subject state: `FINAL_QA_WARN`;
- polish action `paid_6ee06e41562c351b58b53865`: authorized, consumed,
  provider-bound, unreported, and awaiting its first reconciliation;
- live ordinary-v2 dispatch intent: `PROVIDER_PENDING`;
- durable provider operation:
  `resp_0adb36622d328d79006a953081340087d0ad61989d37af4f6f`;
- provider retrieval attempt count: `0`;
- provider resume boundary: `2026-08-31T07:43:12Z`; and
- sealed terminal-review result: absent.

This is not a valid terminal handoff that API merely misunderstood. SBE made a
provisional final-QA warning terminal-looking while retaining real polish
provider custody. The API's strict terminal-lifecycle refusal exposed that
contradiction.

## Protected access record

The approved generation-18 object was accessed with exactly:

- `HEAD`: 1;
- `GET`: 1;
- bucket listing: 0;
- writes/deletes: 0; and
- provider calls: 0.

The first `HEAD` revealed that R2 returned the expected ETag with HTTP quoting.
The manifest was corrected to preserve that exact representation, and the GET
was then performed without a second HEAD. The final access manifest SHA-256 is
`a066d66ae3fcce3624a4f14b875a168c394238a45b138ed6657344611d3b6681`.

The downloaded archive matched:

- object key `v1/checkpoint/19224c980c0c4a6291206d36e712f88c`;
- byte count `5303567`;
- archive SHA-256
  `a53a6a916a530381af500121882a6dd40ce638af974fd261d1c26f09c3e37eb1`;
- inventory SHA-256
  `bda5e1bd10527ed454b636a0a1442284f1d39b5e4f43552bb6e086b675ee1717`;
- checkpoint generation `18`; and
- predecessor archive SHA-256
  `f6fefcaa96c066d039111ad9eaa38c1e9d9cd51597362f6ef810670f617a37dd`.

API's production restore boundary validated archive safety, inventory hashes,
1022 members, and 22,723,480 uncompressed member bytes before inspection.

## Exact native join

The restored `run.json` is
`astrowoof.semantic_closure_run.v0.9`, revision `104`, native run
`23087de39dfa3d6211dc0d012dee469088c1dfa94eb1337953ad8cfb4f63009d`.

The polish action's complete public binding remains joined to the live intent:

- stage `polish`;
- route
  `dog-d29f44b2-6e9d-41f0-845c-0b1f5ad8bcee:polish:001`;
- request SHA-256
  `342fb4e9e995a4a6ad8999d9ed6bf168657933799b7bdfb45fe8c4c202e20f5a`;
- authorization reference `ed9711a1-c11c-4c59-891a-c9d3be060542`;
- consumption revision `101`; and
- provider identity exactly equal to the intent's sole provider operation.

The native-result index contains fourteen historical v0.1 results, all
`provider_pending` or `awaiting_external_authority`. It contains no Glimmer
terminal-review result. That absence agrees with the logs: the v2 dispatch
returned `detached_provider_pending`; the later API inspection failed before a
terminal closeout command ran.

## Causal source seam

`persist_state()` always calls `update_run_status()`. During intent commit, the
polish action moves through authorization/submission and the v2 intent becomes
durable. The reducer nevertheless derives `FINAL_QA_REQUIRES_REVIEW` from the
subject's provisional `FINAL_QA_WARN`, because it has no precedence for
authorized/submitting/provider-bound ordinary polish custody. Once derived, its
preservation clause retains the review status across later identity persistence.

The v2 executor validates the pre-intent inspection, but after persisting the
intent it does not verify that the resulting checkpoint remains nonterminal
before provider call-entry. Public lifecycle inspection then correctly treats
the outer status as terminal and refuses to project provider reconciliation.

The narrow defect therefore has two native faces that should be corrected
together:

1. active ordinary polish custody must outrank provisional final-QA review in
   run-status reduction; and
2. v2 dispatch must fail closed before provider I/O if its newly committed
   checkpoint is terminal or otherwise contradicts its dispatch intent.

The existing provider identity remains reconciliation-only. Nothing in this
finding authorizes a new provider call, denial, recovery, or retained-workspace
mutation.

## Voof-paws 2 questions

1. Approve generation 18 as sufficient and waive generation 17 access.
2. Approve the mixed-custody invariant above for Slice 2 contract freeze.
3. Confirm that API should retain strict refusal of terminal lifecycle bytes;
   SBE should publish coherent provider-custody truth instead of asking API to
   reinterpret a terminal label.
