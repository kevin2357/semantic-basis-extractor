# Gutenberg / Hypatia Editorial Capture Handoff Investigation

## Objective

Jointly determine why the first live QA cohort after editorial-review capture rollout produced no Better Stack capture events. Native behavior and API terminal outcomes are already authoritative; this sprint only investigates the exact native handoffs/capture inputs needed for best-effort observation.

## Runs and immutable checkpoint coordinates

### Gutenberg Ganache — terminal editorial review

- API run: `7487145f-f23f-4629-b322-95123cc7c8f6`
- Native run: `0485e36ce81311d08e7ba47f614f1e653e2871a48ac9d332b04269127998996c`
- Checkpoint ID / generation: `141aac6c-017b-4977-a189-522c9c36eba4` / `9`
- Storage object ID: `de5d4868-b311-45f4-b2bf-515c7f79fed4`
- R2 object key: `v1/checkpoint/de5d4868b31145f4b2bf515c7f79fed4`
- Archive SHA-256: `6def3f552485eff2a92266d1d2c96b24d657222c793d8acacdb92e6b49040dc3`
- Inventory SHA-256: `cffa82bf48ed17d5d5de48eefbf61192ba440df0d4a31ba9c2c9e02c03182724`
- Archive bytes: `5,037,928`
- Logical restore root: `/work/runs/7487145f-f23f-4629-b322-95123cc7c8f6/sbe`
- Exact result: `nres_07686011f6203f77fb590e0e` / SHA-256 `07686011f6203f77fb590e0ec03410bd35c86b8509977082b7c7c3663a5814fd`
- Publication receipt: `nreceipt_4f0d04f075359b55e1fed511` / SHA-256 `4f0d04f075359b55e1fed511005e1ab9e3fab6b37c80ceabc96a7c3d5586496f`

### Hypatia Honeycake — successful delivery

- API run: `b42ffae4-1b4f-41e3-b578-772ac659cb20`
- Native run: `36cec78b587129108aa3ad19d503827c6b305fca345de0f634442205fda01016`
- Checkpoint ID / generation: `debdc7a2-b2e3-49d5-bbd7-ffb50d122d1e` / `9`
- Storage object ID: `ae296ad6-996e-4c5d-971e-b9cddd26e6cd`
- R2 object key: `v1/checkpoint/ae296ad6996e4c5d971eb9cddd26e6cd`
- Archive SHA-256: `9c9a1e76e49940b8ae8206d6adc58c8a720cb826bb7e8d1a4876ccc024a019b2`
- Inventory SHA-256: `0b923679283a5aff3c907da8cf3fa22513fe80b78c2e69c60c6e91011ed91796`
- Archive bytes: `5,057,929`
- Logical restore root: `/work/runs/b42ffae4-1b4f-41e3-b578-772ac659cb20/sbe`
- Exact result: `nres_dc1080caa04fd6b4302b0d8e` / SHA-256 `dc1080caa04fd6b4302b0d8eb4fe90236f498fd5d729136da4fa324ddaf4422d`
- Publication receipt: `nreceipt_1e3bfaec883c7a6155d76281` / SHA-256 `1e3bfaec883c7a6155d76281df5dce05b761c6a0f40e7e932190c0a70c3cf02b`

## Render log export

Unfiltered SBE worker logs covering both runs:

`C:\tmp\sbe-worker-gutenberg-hypatia-20260910T1639-1653Z.jsonl`

The export covers `2026-09-10T16:39:00Z` through `16:53:00Z`, is 2,178,673 bytes, and includes both the transient Hypatia `terminal.publication.retry` and eventual `delivery_accepted` closeout.

## API framing

- Gutenberg terminated with `native_terminal_review_required` after a clean local review branch. The current API observer needs the invocation-specific `terminal_review_command_result.result_id`; its completion/failure log is absent.
- Hypatia delivered successfully after a retry. Current API code only calls the observer on delivery when a `sealed_terminal_result_id` survives to publication; the normal fresh-delivery route apparently did not provide one.
- The first retry raised `PublicationEligibilityError: SBE-accepted delivery authority is required`. It recovered on a subsequent delivery-validation invocation, but this ordering must be characterized rather than normalized as expected behavior.

## Requested SBE work

1. With the above pinned evidence, determine whether each native invocation/result actually carried the intended closed command-result handoff and, if not, the narrowest producer-side omission.
2. Distinguish exact ordinary delivery, terminal-review, and retry/delivery-validation command shapes. Do not manufacture a latest-result fallback.
3. Confirm whether the first Hypatia publication attempt is an expected predecessor/authority timing boundary or a contract/runtime violation.
4. Do not mutate retained workspaces, invoke providers, reconcile, resume, repair, or replay.

If exact archive inspection is needed, request explicit bounded one-HEAD/one-GET authorization for each named object; no blanket R2 authorization is granted by this document.

