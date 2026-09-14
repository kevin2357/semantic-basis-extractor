# Slice 0 — Corrected Log Coverage and Terminal Timelines

## Decision

Slice 0 is complete. Eight unfiltered 15-minute exports replace the truncated
two-hour file and provide complete current-cohort coverage. Aldine's fast
terminal review is explained by normal bounded progression; the common observer
failure remains independently unresolved.

## Export boundary

The original two-hour export reached Render's 1,000-record limit and stopped at
`19:08:05.978Z`. It contains neither current pup. The replacement manifest
covers `18:45–20:45Z` in eight non-overlapping windows. Every nonempty window is
below 1,000 structured events; the four intervening empty windows are retained
as legitimate zero-byte evidence.

Target filtering over the replacement files yields:

| Pup | Target-bound rows | First event | Last event | Worker cycles |
| --- | ---: | --- | --- | ---: |
| Aldine | 607 | `20:27:35.820Z` | `20:37:22.226Z` | 6 |
| Moxon | 572 | `20:29:31.769Z` | `20:41:28.945Z` | 7 |

## Aldine timeline

1. Initial wave prepared and submitted six provider actions.
2. Reconciliation joined all six provider results; assembly reached
   `FINAL_QA_FAILED` with one validation error and four lint findings.
3. Polish attempt 1 was prepared, separately authorized, submitted, joined, and
   remained `FINAL_QA_FAILED`.
4. Polish attempt 2 was prepared, separately authorized, submitted, joined, and
   recorded `POLISH_REJECTED` with two validation errors.
5. Lifecycle then reported no provider action, no eligible continuation,
   `retain_for_review`, and terminal closure.
6. SBE published exact v0.2 review result
   `nres_d0568048c5fc2d9cfd68d7c7` and receipt
   `nreceipt_39f8305f65dcfe9b36751f65` from invocation
   `ninv_f1ecd81445294d8ea90a840f`.
7. API observed that exact result but returned
   `unavailable / capture_or_preflight`; authoritative terminal closeout and
   resource release proceeded correctly.

The six-worker-cycle count is not the provider-attempt count. Aldine consumed
eight provider actions: six initial and two polish. The log does not support a
premature native closure hypothesis.

## Moxon timeline

1. Initial wave prepared and reconciled six provider actions.
2. Assembly entered `FINAL_QA_WARN`; one separately authorized polish action
   was submitted and joined.
3. Polish attempt 1 was accepted and produced `DELIVERY_COMPLETE`.
4. SBE published exact delivery result `nres_5a90fadd039f369c7303ecd3`.
5. The first API terminal attempt selected its bounded publication retry; the
   next attempt validated and accepted the same exact result.
6. API observed that result but returned
   `unavailable / capture_or_preflight`; reading publication, closeout, cleanup,
   and resource release remained authoritative.

## Residual investigation

Both independently legitimate terminal routes reach the observer with exact
result identity and fail before HTTP outcome classification. Slice 2's
post-rollout root and phase joins are now the central question. Aldine's native
terminal decision does not need correction based on current evidence.

No provider, R2, database mutation, retry, workspace mutation, Better Stack
write, or QA-state action occurred.
