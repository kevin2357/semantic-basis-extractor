# Final-QA review terminal bridge — investigation background

## Scope

Read-only, provider-free investigation of the fresh QA run **Glimmer von Gloss**.
The purpose is to establish whether `FINAL_QA_REQUIRES_REVIEW` is a legitimate
native editorial terminal and, if so, why the API/SBE bridge subsequently invoked
another ordinary SBE cycle that failed with `SBE temporal lifecycle is terminal`.

This is not a recovery or mutation request. Do not resume, reconcile, retry,
retire, release, create provider work, write R2, or use broad R2 listing.

## Observed outcome

The cohort began normally under QA profile
`astrowoof.qa.sbe0434-stale-retry-dispatch-retirement.v1` and SBE 0.4.34.
Glimmer completed the initial six-member wave and two creative retries. Its
first polish action was authorized and consumed by SBE's constrained v2
dispatch. The trace proves that one polish provider operation was created and
its response identity, `resp_0adb36622d328d79006a953081340087d0ad61989d37af4f6f`,
was durably recorded while the outer native status was already
`FINAL_QA_REQUIRES_REVIEW`.

At 2026-08-31T07:43:34Z, the SBE worker recorded:

- `sbe.cycle.failed`
- `reason_code=sbe.contract.provider_lifecycle`
- `contract_detail=SBE temporal lifecycle is terminal`
- `retryable=false`

The corresponding API generation run and execution job are failed. The worker
lease and capacity allocation were released. One API reservation remains
active/unreported. The corresponding SBE action is authorized and consumed,
with durable provider identity; it must be treated as reconciliation-only
custody evidence, not as providerless work or permission to recover the run.

The active generation-18 checkpoint instead records native lifecycle status
`FINAL_QA_REQUIRES_REVIEW`. That is evidence that the native authoring pipeline
may have reached a normal editorial review terminal before the bridge made its
extra continuation attempt. Predicate Paws, the cohort's other run, independently
reached `terminal_closed` / `native.terminal.review_required`, further supporting
that terminal review is a normal native outcome class.

## Exact Glimmer coordinates

| Field | Value |
|---|---|
| API run ID | `f056cdb2-8954-492f-8dde-4f644aa2ee6a` |
| Reading ID | `57005e09-655e-4455-84c6-7b08d8fedbd9` |
| SBE authoring-run ID | `19880aa5-786e-473e-b7eb-e9994911e919` |
| Native run ID | `23087de39dfa3d6211dc0d012dee469088c1dfa94eb1337953ad8cfb4f63009d` |
| SBE job ID | `955afa91-82d2-469e-9127-20322dbba84e` |
| Logical restore path | `/work/runs/f056cdb2-8954-492f-8dde-4f644aa2ee6a/sbe` |
| Profile / compatibility identity | `astrowoof.qa.sbe0434-stale-retry-dispatch-retirement.v1` |
| SBE release | `0.4.34` |

### Primary active checkpoint (inspect first)

| Field | Value |
|---|---|
| Checkpoint ID | `44ffb561-c2ff-4dc9-8868-f8a40f4bd5e5` |
| Attempt / lease IDs | `e4976ad3-64bd-4fe1-8ced-1e8bc28ee482` / `5af75c2c-e5ff-4153-87fa-ee95a351e93b` |
| Generation | `18` |
| State / native lifecycle status | `active` / `FINAL_QA_REQUIRES_REVIEW` |
| Storage object UUID | `19224c98-0c0c-4a62-9120-6d36e712f88c` |
| Archive SHA-256 / bytes | `a53a6a916a530381af500121882a6dd40ce638af974fd261d1c26f09c3e37eb1` / `5303567` |
| Inventory SHA-256 | `bda5e1bd10527ed454b636a0a1442284f1d39b5e4f43552bb6e086b675ee1717` |
| Checkpoint contract | `astrowoof.sbe-workspace-checkpoint.v1` |
| Storage environment / namespace / protection | `qa` / `checkpoint` / `protected-operator` |
| Provider version / ETag | `cb0606da5dbd0a66c612b53d80dc1f31` |

### Immediate predecessor (retrieve only if needed)

Generation 17 was `AWAITING_SPEND_AUTHORIZATION` and was superseded by the
generation-18 checkpoint above. It is the bounded comparison point for whether
the terminal transition itself correctly retired the pending polish request.

| Field | Value |
|---|---|
| Checkpoint ID | `1f70d2da-0b72-41a6-9445-2c8a5ac7cf47` |
| Storage object UUID | `3d17aa6c-3737-43f1-ba3a-0b8de784cb31` |
| Archive SHA-256 / bytes | `f6fefcaa96c066d039111ad9eaa38c1e9d9cd51597362f6ef810670f617a37dd` / `5302945` |
| Inventory SHA-256 | `362b50b42fa4e0aaf3320c9eaa10d4f9fb2df44a1a26c5f30ef705d18d3cf923` |
| Native lifecycle status | `AWAITING_SPEND_AUTHORIZATION` |

## Required questions

1. Is `FINAL_QA_REQUIRES_REVIEW` the intended native terminal for an editorial
   final-QA failure/review outcome?
2. Does the generation-18 workspace expose a terminal result/closeout, or does
   it preserve provider-bound polish custody requiring reconciliation?
3. Why did SBE's invoked ordinary cycle reject as terminal rather than publish a
   native terminal result that the API could ingest cleanly?
4. Should provisional final-QA review remain nonterminal while polish is
   provider-bound, and what exact transition may terminalize after that custody
   has been reconciled and adopted?
5. What exact public terminal artifact and regression fixture are needed so the
   API never attempts continuation after an SBE review terminal?

## Evidence boundaries

Authoritative API custody currently establishes: Glimmer is failed; its job,
latest attempt, lease, and capacity allocation are all terminal/released; the
six initial and two creative retry actions are reported; one polish action is
authorized and consumed with durable provider identity but remains unreported;
its active global reservation is USD 0.617853. SBE traces are diagnostic only.

Use one exact HEAD and one exact GET for generation 18 if protected checkpoint
inspection is required. Do not retrieve generation 17 unless it answers a
specific documented differential question.
