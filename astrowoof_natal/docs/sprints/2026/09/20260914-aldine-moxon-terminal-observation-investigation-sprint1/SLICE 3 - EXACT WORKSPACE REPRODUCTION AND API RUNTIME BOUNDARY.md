# Slice 3 — Exact Workspace Reproduction and API Runtime Boundary

## Decision

The exact retained generation-9 workspaces do not reproduce either live
`capture_or_preflight` failure when mounted at their contract-bound roots.
Moxon's full packet path succeeds through API request preflight. Aldine's
native capture intentionally resolves to a typed `contradictory_native_evidence`
absence status, and that status also succeeds through API envelope construction
and request preflight.

The common live failure is therefore not an SBE exact-reader, stable-root,
packet-builder, envelope, or deterministic request-preflight defect on the
retained bytes. Ownership returns to API's live runtime boundary after request
preparation, or to a deployed runtime/configuration difference not represented
by the exact source-and-workspace reproduction.

## Authorized custody

The owner authorized exactly one HEAD and one ETag-conditional bounded GET for
each pinned key in `API REVIEW - SLICE 2 AND PINNED R2 COORDINATES.md`.

| Pup | HEAD | GET | Bytes | Archive SHA-256 |
| --- | ---: | ---: | ---: | --- |
| Aldine | 1 | 1 | 5,108,295 | `707bd5ca64e5741a2949e5684bd6940d6fd6bac89dfe1d3312d16bc4276af695` |
| Moxon | 1 | 1 | 5,026,273 | `565f2047d01828a6d4c7bbbcefd3fdc51feb836ad44b474708913ebf28754d90` |

Both HEAD sizes, conditional GET sizes, archive digests, generation values,
and manifest inventory digests match the pinned coordinate packet. Operation
totals were HEAD 2, GET 2, list/write/delete 0. Archives, extraction roots,
access receipt, and diagnostic scripts remain outside Git in `C:\tmp`.

## Isolation

Each workspace was mounted read-only at its exact native logical root in an
ephemeral Docker container. SBE source, API source, and diagnostic code were
also read-only. The container used `--network none`, `--read-only`,
`--cap-drop ALL`, and `no-new-privileges`. No provider call, Better Stack
write, retry, resume, reconciliation, or workspace mutation occurred.

## Reproduction matrix

| Phase | Aldine v0.2 review | Moxon v0.1 delivery |
| --- | --- | --- |
| Exact native result read | `editorial_review` | `delivery` |
| Runtime evidence collection | typed `unsupported` | `delivery` |
| SBE capture construction | `contradictory_native_evidence` status | packet 1, projections 9, artifacts 9 |
| API envelope construction | success, 1 status event | success, 10 editorial events |
| API deterministic request preflight | success, 1,082 / 514 raw/compressed bytes | success, 53,548 / 7,744 raw/compressed bytes |

The two native branches are not internally equivalent. Aldine has a separate
bounded native-evidence contradiction worth classifying later, but it does not
explain the missing observation: the public contract converts it to a valid,
exactly bound capture status that API can envelope and preflight.

## Corrected phase boundary

API's `EditorialReviewObserver.observe_terminal()` labels its outer exception
handler `capture_or_preflight`, but that `try` region also includes
`post_editorial_review_request()`. The post helper sanitizes `httpx` timeout and
HTTP exceptions, while other caught outer-region `ValueError`, `TypeError`,
`KeyError`, `OSError`, or transport errors can still erase any partial outcome
and appear as `capture_or_preflight`.

Consequently, the live event does not prove that no HTTP attempt began. It
proves only that no post outcome survived the outer call. The exact offline
reproduction proves all deterministic work before the live post boundary.

## Next review gate

Stop for joint API/SBE review. The next investigation belongs on API's live
runtime/configuration side and should remain provider-free where possible:

1. split safe phases around target selection, client construction, editorial
   post, artifact preflight/post, and outcome assembly;
2. emit only exception class/fingerprint and phase—never URL, token, payload,
   authored content, or raw exception prose;
3. verify the installed API/SBE distribution pair and sanitized configuration
   shape in the deployed worker;
4. preserve best-effort, post-authoritative semantics and perform no live
   Better Stack write merely to diagnose the failure.
