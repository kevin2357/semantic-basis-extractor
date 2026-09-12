# Hokusai relocated-assessment refusal investigation — Background

## Purpose

Investigate one post-`0.4.60` QA execution of SBE's public relocated operator-disposition assessment. This is a read-only, provider-free investigation. It grants no workspace mutation, provider access, recovery, resume, reconciliation, or repeat operator action.

## Exact live boundary

| Fact | Value |
| --- | --- |
| Pup / API run | Hokusai Hamantaschen / `00667fb9-c068-415e-a045-8d4059ac549e` |
| API SBE job | `3c1dc0cd-3169-4542-8f9b-40305d8dcf3b` |
| authoring / native run | `331d5f68-a236-438e-8168-b1c4bf93d6ca` / `06931bef20441d0ce8b76adb01404279d821327b0c2f9ccf04d7d078f2cce05c` |
| operator request | `e80e824c-fe88-4753-9f55-d2ff42aeb1c0` |
| durable result | `refused` / `disposition_assessment_unavailable` |
| persisted safe detail | `SBE relocated operator disposition assessment is invalid` |

API proved checkpoint restore completed and emitted `operator_quarantine.assessment_started` with `restore_outcome=isolated_restored`. The next event was `operator_quarantine.refused`. This puts the failure inside the public SBE reader/pair-validator or API's strict intake of its returned shape, after restore and before custody classification. The runner was correct to fail closed; no Hokusai provider/spend/workspace/capacity mutation occurred.

The generic safe detail arises because API maps an SBE reader or validator `TypeError`/`ValueError` to the same closed error. Do not infer a specific failure reason from it.

## Local log evidence

Unfiltered SBE worker log export, outside Git:

`C:\tmp\sbe-worker-cohort-and-quarantine-20260912T0945Z-1050Z.jsonl`

Window: `2026-09-12T09:45:00Z` through `2026-09-12T10:50:00Z`; bytes: 3,051,088. Filter with Hokusai's IDs above. It is non-authoritative trace evidence.

Related bounded operator trace, also outside Git:

`C:\tmp\operator-hokusai-quarantine-service.jsonl`

## Checkpoint coordinate packet

The API checked-in catalog returned:

- checkpoint: `b7ceea14-cb07-4366-b944-31bceb2c5159`, generation `4`, active;
- object: `v1/checkpoint/957a1c32cf724c7ea087fa4abf5ab236`;
- archive SHA-256: `79b771d0ce02a7c1e20fb6d177e4ac0ae62f1f5608bfb877c0480762792cde86`;
- inventory SHA-256: `6351e48ca7e6ad27a45d4d38dc4d0bf7861a900f1e822add1df0360ddd982d3b`;
- size `4,019,115` bytes;
- catalog logical restore path `/work/deterministic-domain`.

No ETag/version is available from PostgreSQL. These coordinates are **not** authorization for R2 HEAD/GET/listing, extraction, or alternate discovery. If exact object inspection remains necessary after local/provider-free reproduction, request a separately explicit one-HEAD/one-GET authorization.

## Live custody context

At refusal, the SBE job was `retry_wait` with no active lease/capacity. The pre-pause trace shows six initial actions were created; one had reconciled and five provider-local dependencies remained. The SBE worker is suspended; do not resume it.

## Boundaries

- Preserve the stable executable-path invariant.
- Do not introduce an `ignore_path` option or general relaxed workspace reader.
- Do not make a relocated copy executable, mutable, publishable, or capable of provider I/O.
- Do not change `0.4.60` runtime behavior until a provider-free reproduction identifies an exact closed boundary.
