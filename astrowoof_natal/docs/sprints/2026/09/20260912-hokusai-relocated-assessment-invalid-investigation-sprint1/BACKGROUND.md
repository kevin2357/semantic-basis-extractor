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

## Corrected checkpoint coordinate packet

The original API catalog query selected by run and therefore returned the
deterministic-domain job's active checkpoint. It was not the checkpoint restored
by the operator runner. A subsequent exact job-bound join established:

- exact SBE checkpoint: `c1726aeb-f091-45d4-956a-4f628bb96439`, generation
  `3`, active;
- checkpoint and `SbeAuthoringRun` root:
  `/work/runs/00667fb9-c068-415e-a045-8d4059ac549e/sbe`;
- archive SHA-256:
  `6d6a9ebdb6dfcf6172d41c06107c89fbeadd86efeb068fdd208d78af6b189626`;
- inventory SHA-256:
  `2ee271fcbec0b326568975aec2c002cb9a0029d49b2135bb0b1fb999cfd2e204`.

SBE's frozen trace records native durable root
`/work/runs/workspace-5d5294a3-6d1d-4fe4-9a36-c0e2b067414a/sbe`. The two roots
are not canonically equal. API used its API-run root to construct relocation
authority, and SBE correctly refused it at original-root binding.

No ETag/version is available from PostgreSQL. These coordinates are **not**
authorization for R2 HEAD/GET/listing, extraction, or alternate discovery. No
object inspection is materially needed after the exact job-bound join.

## Live custody context

At refusal, the SBE job was `retry_wait` with no active lease/capacity. The pre-pause trace shows six initial actions were created; one had reconciled and five provider-local dependencies remained. The SBE worker is suspended; do not resume it.

## Boundaries

- Preserve the stable executable-path invariant.
- Do not introduce an `ignore_path` option or general relaxed workspace reader.
- Do not make a relocated copy executable, mutable, publishable, or capable of provider I/O.
- Do not change `0.4.60` runtime behavior until a provider-free reproduction identifies an exact closed boundary.
