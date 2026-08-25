# Evidence

## Incident facts supplied by API

- Two fresh exact-Natal runs completed and reconciled their initial six-member
  waves.
- Temporal lifecycle selected ordinary v2 external authority only after provider
  dependencies reached zero.
- Both next-action invocations sealed `request_payload_digest_mismatch` before
  provider I/O; no blocked-action provider identity or ambiguity exists.
- API retained its request, grant, authorization, custody, and spend evidence.

## Pre-implementation source evidence

- Ordinary exact request binding: `closure.py` computes
  `request_sha256 = spend_digest(payload)` from the complete payload.
- Ordinary exact persisted display artifact: `OpenAIResponsesProvider.author()`
  replaces the workspace prompt in `openai-request.json` with a fixed placeholder
  and writes the actual prompt to adjacent `openai-workspace-prompt.txt`.
- Initial-wave preparation additionally writes the exact private payload, explaining
  why that path does not exhibit the same missing-evidence shape.
- Current v2 resolver searches JSON request artifacts and accepts only a direct
  canonical digest match; it does not reattach the separately persisted prompt.

## Slice 0 production-path result

- Test:
  `test_external_authority_v2_payload_digest_recovery_slice0.py`
- Result: 1 passed.
- Complete payload user content: three ordered `input_text` blocks.
- Cache metadata: breakpoint annotations on blocks one and two.
- Persisted prompt: flattened segment text only; block boundaries and annotations
  are not retained in that file.
- Persisted redacted JSON digest differs from the binding as expected.
- The pre-patch resolver returned the exact incident outcome:
  `request_payload_digest_mismatch`.
- Rebuilding with the original production segment map reproduces the complete
  payload and binding digest exactly.
- Bounded ordinary interactive representation: complete request persisted; defect
  not reproduced and runtime expansion not justified.

## Slice 1 payload persistence and compatibility result

- New exact actions: one direct private artifact plus one exact action-owned
  content reference; no recursive discovery.
- New bounded direct requests: existing full request bytes preserved and referenced
  without changing bounded request construction.
- Historical compatibility: exact 0.4.23 creative retries only, pinned to the
  retained v0.9 run identity and the exact installed resource-set identity.
- Negative mutations passed for path escape, changed prompt, wrong placeholder,
  and incompatible resources. Unreferenced duplicate payload bytes are ignored.
- Focused result: 47 passed.

## Slice 2 refusal-to-fresh-authority result

- First invocation: the real resolver reads the real lossy 0.4.23 artifact shape
  and returns `pre_provider_refusal / request_payload_digest_mismatch`, provider
  I/O `not_attempted`.
- Exact old invocation replay: identical refusal evidence, zero create.
- Fresh inspection: distinct v2 request digest over the successor native basis.
- Fresh grant: historical payload rebuilt and bound exactly; one scripted POST.
- Fresh exact replay: zero additional POST.
- Original refusal history: retained unchanged as the prefix of append-only dispatch
  history.
- Same-hash source archive outside the restored workspace: typed refusal before
  reading it as reconstruction authority.
- Combined focused result: 57 passed.

Slice 2 gate status: complete and subsequently API-approved.
Provider/network/spend activity: 0.
Retained QA access/mutation: 0.

## Slice 3 installed-wheel evidence

- Candidate version: `0.4.24`.
- Focused source result: 59 passed.
- Installed payload-recovery receipt: pass; one scripted create, zero external
  calls, zero spend, exact refusal and replay assertions all accepted.
- Generic installed release smoke: pass; `DELIVERY_COMPLETE`, 50 cards, four
  summaries, accepted final QA, cleanup complete.
- Reproducible wheel SHA-256:
  `eae1206e54e83e4f874de0595a8d2c616fc11a3980ba91f228d34e3186a27404`.
- `git diff --check`: clean apart from informational Windows line-ending notices.

Status: Slices 0–3 complete; final release review pending.
