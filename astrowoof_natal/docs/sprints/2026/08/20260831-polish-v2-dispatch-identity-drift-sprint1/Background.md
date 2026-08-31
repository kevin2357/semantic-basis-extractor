# Polish v2 dispatch identity drift — investigation background

## Status and scope

**Status:** API-provided investigation packet; intentionally uncommitted.

**Scope:** provider-free inspection of one frozen QA SBE workspace and its
already-persisted public/API-side custody evidence. The QA SBE consumer was
suspended at 2026-08-31T02:00:02Z after the failing loop had reached attempt 17.
Do not resume it, reconcile, retry, create provider work, mutate the retained run,
write R2, or use a broad R2 listing as part of this investigation.

This is a narrow investigation into an apparent *same action, changed external
authority request identity* during the first observed post-authoring polish handoff.
It is not a request to recover this run.

## Downloaded Render trace export

The API agent exported the QA SBE worker's raw Render text log window spanning
cohort processing and suspension:

- `C:\Users\kevin\Downloads\qa-sbe-delerium-obstinate-20260831T0138Z-0200Z.render.log`

It is non-authoritative diagnostic evidence only. It contains the relevant
structured SBE trace events, command results, and retry-loop output for
2026-08-31T01:38:00Z through 2026-08-31T02:00:10Z. Treat it as a supplement to,
not a replacement for, the protected checkpoint and API custody records below.

## What happened

The fresh QA cohort was created with the ordinary live QA guard:

- USD 50 per run;
- USD 100 cohort;
- USD 150 rolling 24-hour;
- USD 49 for each active stage; and
- USD 0 for `qualitative_candidate`.

The focal run successfully traversed all of the following before the anomaly:

1. deterministic handoff;
2. six-member initial authoring fan-out;
3. initial result reconciliation;
4. one creative retry through v2 authorization, provider submission, and completed
   result reconciliation;
5. authoring completion, validation/lint, and entry into polish.

No polish provider request was created. The failure is at authorization dispatch,
not provider behavior or spend settlement.

## Exact retained-run coordinates

| Field | Value |
|---|---|
| Environment | `qa` |
| API run ID | `3ecc3cde-26f1-4f02-a0ec-96fd7fb0001a` |
| Reading ID | `43fca3dc-1ba8-4ca9-8003-cc8964756c4f` |
| Dog label | `Delerium of Dill ab8e8794` |
| SBE authoring run ID | `0d8958f1-3b9d-4ac9-83d8-9a1d337f9234` |
| Native run ID | `8756c0b6a642f85fa911557aeedf0b228dfbb3776ba070c3864a137632339091` |
| SBE execution job ID | `1c241872-0882-44b7-aaf4-cd1091af7b0f` |
| Logical restore path | `/work/runs/3ecc3cde-26f1-4f02-a0ec-96fd7fb0001a/sbe` |
| Compatibility identity | `astrowoof.qa.sbe0433-post-retry-authority-admission.v1` |
| SBE release | `0.4.33` |
| Storage environment / namespace / protection | `qa` / `checkpoint` / `protected-operator` |
| Worker state at freeze | job `retry_wait`, attempt 17; no active lease; stale active slot-1 allocation remains |

### Active checkpoint to inspect first

This is the exact active checkpoint after the creative retry was reported and the
polish authority was prepared/granted. It is the primary protected retrieval target.

| Field | Value |
|---|---|
| Checkpoint ID | `d0270152-7749-4c66-8aa4-58117e70d8b4` |
| Job / attempt / lease IDs | `1c241872-0882-44b7-aaf4-cd1091af7b0f` / `54e4e102-6e4e-4d66-8750-69dc6aee3688` / `24b22db2-e9f6-4a71-abbf-1785bc4d05fe` |
| Generation / sequence | `11` / `11` |
| State / native lifecycle status | `active` / `AWAITING_SPEND_AUTHORIZATION` |
| Opaque storage object UUID | `60c09a6f-1426-4c2a-a38e-77e8662aaac1` |
| Archive SHA-256 / bytes | `ec70409af469ea8fffb9217533a2173a8c206675a9949aa249f9ce4e1be92000` / `4779709` |
| Inventory SHA-256 | `dba64797a61449848bb378bba82e74491d5a0b6d2b02fd75bff81d790a37ca4c` |
| Checkpoint contract | `astrowoof.sbe-workspace-checkpoint.v1` |
| Storage contract | `astrowoof.storage-receipt.v1` |
| Provider version / ETag | `052b105050b4067d818814ae581d8b01` |
| Created / stored | `2026-08-31T01:52:58.655933Z` / `2026-08-31T01:52:59.927463Z` |

### Immediate predecessor for differential inspection

Retrieve only if it helps compare the pre-polish successful continuation against
the active authority checkpoint.

| Field | Value |
|---|---|
| Checkpoint ID | `00ae9580-5dc3-47c4-98a5-3e683a6d0618` |
| Job / attempt / lease IDs | `1c241872-0882-44b7-aaf4-cd1091af7b0f` / `35ead1ec-965f-4427-a450-3e6f63dbc6a5` / `bba9f311-ea1c-4c4e-bf77-c544cb429719` |
| Generation / sequence | `10` / `10` |
| State / native lifecycle status | `superseded` / `bounded-progressed_local` |
| Opaque storage object UUID | `dc2562e2-ad63-4b04-803b-a76a23f52e88` |
| Archive SHA-256 / bytes | `5b115ce782a508c95b6f9417e3241db40b46047af3f4754603f994ffe400808b` / `3781553` |
| Inventory SHA-256 | `54ed0a690fb58f2ad11698b9e5f5d886efaebf201fc1ac923a6a072c196019c0` |
| Checkpoint contract / compatibility identity | `astrowoof.sbe-workspace-checkpoint.v1` / `astrowoof.qa.sbe0433-post-retry-authority-admission.v1` |
| Storage environment / namespace / protection | `qa` / `checkpoint` / `protected-operator` |
| Provider version / ETag | `ebc7ecb26b412f7e38a4f49a1dcd03c5` |
| Created / stored | `2026-08-31T01:51:53.242904Z` / `2026-08-31T01:51:54.223972Z` |

## Exact polish authority evidence

The API-side records agree on the intended one-action authority:

| Field | Value |
|---|---|
| Polish action ID | `paid_c90cf4073c936d22e27e16ae` |
| Action record / authorization reference | `129550f8-6e18-4130-8a88-ce82b20ddc77` / same |
| Category / state | `polish` / `authorized` |
| Maximum authorized USD | `0.622175` |
| Provider operation ID | none |
| API awaiting-grant ID | `1b6eded7-061f-46e9-af99-15979f0608e7` |
| API v2 admission ID | `d956bf00-f4ad-4049-a343-756840a83553` |
| Frozen request SHA-256 | `07300bd27a5f61c592fc6fc7df1a7eee57bcd6bf9d333ca2b3b45a34e20b7fb2` |
| Grant SHA-256 | `bb3aea3813f914c57fa3ee21b3e215f59bf1239c63b50df32453a0504ac87796` |
| Checkpoint-basis SHA-256 | `d307b779e27717b27dd176eea658fc7e1e74a0ba7b2761fc02e81728d5114b4c` |
| Ordered action inventory | `["paid_c90cf4073c936d22e27e16ae"]` |
| Action immutable binding SHA-256 | `20c0572af490a8ef203cb2234e5917e11a65718ff5e425cf8bdadce7e350bf50` |
| Prepared state revision / route | `72` / `dog-245b6eaa-4d4a-4530-856d-ee1bed050ba1:polish:001` |

No v2 dispatch receipt exists for this admission. That is consistent with refusal
before provider I/O or normal receipt persistence.

## Observed trace sequence

All timestamps UTC. These are non-authoritative diagnostic logs; database records
above remain the custody source of truth.

1. `01:51:15` — creative retry result retrieved as `completed`; SBE reports
   `reconciliation_completed`.
2. `01:51:16` — SBE selects `ordinary_resume`; it records
   `authoring_attempt_ambiguous` for the same creative-retry action, then continues.
3. `01:52:22–01:52:24` — authoring finalization begins; validation succeeds;
   lint exits 2 with four findings; subject state becomes `FINAL_QA_WARN`.
4. `01:52:24` — polish action `paid_c90...` is prepared and SBE transitions to
   `AWAITING_SPEND_AUTHORIZATION`.
5. `01:53:03` — API persists the exact v2 grant shown above for request `07300...`.
6. `01:53:04–01:53:07` — during `external_authority_v2` dispatch, SBE logs an
   independently read request hash `a838af...`, then its structured
   `external_authority.request_selected` event names the API’s `07300...` request
   and matching grant. It then logs:
   - `intent_revalidation_deferred reason=action_state_or_custody_mismatch`
   - `command_refused ... reason=authorization_mismatch`

The trace also mentions a separate inspection request hash (`c5ac68...`) at the
same revision. Treat those trace hashes as a symptom to explain, not as an
authority substitute.

## Questions for investigation

1. Can the active checkpoint reproduce why a supposedly immutable external
   authority request acquires a different digest during dispatch without a
   different action, checkpoint basis, or provider operation?
2. Is the `authoring_attempt_ambiguous` after a successfully reconciled creative
   retry causally related, or merely a separate issue that changes the workspace
   state before polish?
3. Why is the action still `authorized` and the API grant still exact while the
   native v2 command rejects `action_state_or_custody_mismatch`?
4. Which contract/persistence/reader rule should prevent this drift, and which
   provider-free regression fixture can prove the repair? A fix must not make
   generic resume manufacture new authority or submit provider work.

## Guardrails

- Use precisely the active checkpoint HEAD/GET first; retrieve the predecessor
  only if necessary for a bounded differential comparison.
- Do not list the bucket, enumerate unrelated checkpoints, write R2, call OpenAI,
  resume workers, or mutate this run.
- Do not use trace output to override the persisted API action/admission/grant
  chain.
- Preserve the distinction between a stable historical diagnosis and any future
  recovery design. This sprint should explain and repair the general seam, not
  tailor a one-off resurrection command for Delerium.
