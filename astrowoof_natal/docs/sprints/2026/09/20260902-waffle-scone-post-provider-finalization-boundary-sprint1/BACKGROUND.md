# Waffle/Scone Post-Provider Finalization Boundary — Background

## Purpose

Investigate the native failure that occurred after Waffle's completed provider
work and determine the smallest correct native/API contract change. This is
read-only investigation first; do not recover retained QA runs, call a
provider, alter R2, or release a package during Slice 0.

## Evidence artifact

An **unfiltered** Render SBE worker log export covering the two hours ending
approximately 2026-09-02T21:35Z is available locally:

`C:\tmp\sbe-worker-last-2h-20260902.txt`

It is divided into twelve labelled ten-minute windows to avoid Render's
per-query log-page limit. It contains no manual filtering; use the native run
IDs below to locate the relevant trace.

## Runs

| Pup | API run | Native run | Status |
| --- | --- | --- | --- |
| Waffle Wavelength | `d390e6da-60fd-4558-9f2d-8e211c5f5477` | `265612344da90275b3d2501166e5dedd3d62ab085fe1625ecb60102f1f892218` | Suspended mid-retry after finalization subprocess failure. |
| Scone Shannon | `3880c349-e144-4920-a155-45da977715e9` | `6b330550eb12b2fdd7786f7e814839d3b8e876977048b55a108e8e5556a81cec` | Terminal review-required comparator; do not assume same cause. |

## Exact active Waffle checkpoint coordinate

- API job: `d4cc704f-5917-4563-bbac-a877291c45c9`
- Latest active checkpoint: `4e2ed817-60a9-457f-913b-889bb40817f3`
- Checkpoint generation: `16`
- Checkpoint attempt: `929b08e3-c9ad-4111-b298-8106a1ba427f`
- State: `active`
- Contract: `astrowoof.sbe-workspace-checkpoint.v1`
- Compatibility identity:
  `astrowoof.qa.sbe0439-theme-advisory-pre-native-hold.v1`
- Storage: `qa` / `checkpoint` / `protected-operator`
- Object UUID: `55ec05d9-0cd2-4ebc-abe4-705f508fb147`
- Archive bytes: `4246846`
- Archive SHA-256:
  `fc38d94246d34a82399a94b38f5f48ee78f3bf8a35da08c227013675358e1e6b`
- Inventory SHA-256:
  `483f373477c4be76a75ac1d58054f671e283f3b101a5ddfde3c277d72db76625`
- Native status: `bounded-progressed_local`
- Logical restore path:
  `/work/runs/d390e6da-60fd-4558-9f2d-8e211c5f5477/sbe`

No credential, signed URL, or provider mutation authority is included.

## Observed sequence

1. Waffle completed eight reported actions: six initial authoring and two
   creative retries. Provider custody was zero.
2. SBE adopted the last result, accepted it, entered `AUTHORING_COMPLETE`,
   retired the external-authority-v2 intent, and selected `ordinary_resume`.
3. `finalize_subjects` began with `polish=True`.
4. The API child process raised `CalledProcessError`; API classified this as
   retryable `sbe.dependency.command_failed`. Repeated attempts followed.
5. QA SBE worker was suspended at `2026-09-02T21:27:35Z` while attempt 25 was
   active, preserving the boundary.

## Questions for SBE

- What exact native command/report/artifact fails after `finalize_subjects`?
- Is the outcome a genuine operational dependency failure, a typed editorial
  terminal/review result, or an unhandled native defect?
- What public, sanitized lifecycle/result surface should API consume to make a
  correct retry-versus-terminal decision without parsing logs or an exit code?
- What regression fixture covers this path alongside Scone's independently
  review-required terminal outcome?

## Guardrails

Read-only inspection only. Do not use the checkpoint to mutate Waffle, list
R2 broadly, make provider calls, or claim the worker. Keep all conclusions
specific to publicly evidenced native semantics.
