# Bembo/Morris runtime-capture TypeError investigation

## Purpose

Two fresh QA terminal witnesses reached the API terminal-observer boundary after
SBE `0.4.61`. Exact terminal authority was selected on each route and the
observer entered capture, but the installed native runtime-capture call returned
a caught `TypeError` before envelope construction, Better Stack preflight, or
any HTTP request.

This is a read-only SBE investigation. Its first goal is to reproduce and
classify the exact inner `TypeError` against pinned retained evidence; no API,
provider, R2, Better Stack, queue, lifecycle, or retained-workspace mutation is
authorized by this background.

## Witnesses

| Pup | API run | Native run | Exact terminal result | Route | Terminal outcome |
| --- | --- | --- | --- | --- | --- |
| Bembo Brioche | `c77f8bfe-6c8b-4612-8dcd-de76d7d5822b` | `a1523be35ee0d47fa5e471fc6dc8b4bd6ee5b3d8959ba591b7b720cf4977d3e0` | `nres_a83f5a0c2946e06876d7e79c` | delivery | succeeded / delivery published |
| Morris Madeleine | `f679b5af-8dcb-4db5-a79b-72c67fac4f6f` | `b374742b24ec55c5f04dec878e663cdc4bf8d86d4e476542fdde5ff224651220` | `nres_3f628ce39fa7673b7c141a25` | review | `native.terminal.review_required` |

Both terminal operations completed normally and released capacity. Neither
observation created a packet, longitudinal artifact, request preflight, or
Better Stack HTTP call.

## Raw worker-log export

Unfiltered SBE-worker Render export: Sunday 14 September 2026 20:20–21:20
America/Denver (Monday 15 September 2026 02:20–03:20 UTC), in ten-minute files:

`C:\\tmp\\astrowoof-sbe-worker-logs-20260914-2020-2120-denver`

- `sbe-worker-01-0220Z-to-0230Z.json` — 230 raw records.
- `sbe-worker-02-0230Z-to-0240Z.json` — 868 raw records.
- Files 03–06 are empty because both terminal paths ended before 02:40Z, not
  because an export failed.

The Render CLI output is raw concatenated JSON objects, not an array. Neither
nonempty file reached Render's 1,000-record cap.

The nonempty exports have been parsed as concatenated Render JSON objects and
frozen as follows:

| File | Bytes | Records | First/last record UTC | SHA-256 |
| --- | ---: | ---: | --- | --- |
| `sbe-worker-01-0220Z-to-0230Z.json` | 638,490 | 230 | 02:27:50.447Z / 02:29:59.838Z | `230ebd8c50e4161b0485ed7be2f285d34da30f8a1a8bc24ba20940801874d0e0` |
| `sbe-worker-02-0230Z-to-0240Z.json` | 1,780,950 | 868 | 02:30:00.045Z / 02:39:54.337Z | `41aa024ed3570c58aff8491cb9c088c4701b41907ee1a27debf3859e032a597e` |

Files 03--06 are zero-byte files with the canonical empty SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## Established boundary

For both witnesses API emitted observer selection with exact authority present,
then capture `entered`, then capture `failed` with
`failure_kind=capture_or_preflight` and `failure_exception_class=type_error`.
The wrapper returned `unavailable` and zero artifacts. No envelope, preflight,
or post phase occurred.

Most importantly, the capture event's API-side workspace digest equals SBE's
independently logged logical-root digest for that same run:

| Pup | Matching digest |
| --- | --- |
| Bembo Brioche | `8d924a9bf4d41931be78dd844686ff0353c0cd6dd90144e6ffa84c5097b19e41` |
| Morris Madeleine | `ec1ae981f99ac42c29d411dc84bf36d4badcdfeab0dcc57c706f4fc885ead689` |

So the caller passed SBE's own logical workspace-root string. This is not a
relocation, stale-root, or wrong-path defect. The leading hypothesis is an
internal runtime-capture data-shape/operation seam while interpreting otherwise
valid native evidence.

## Initial source map and hypotheses

The observed call is `build_editorial_review_runtime_capture(workspace,
result_id)`, supplied by the installed SBE package. The path passes through
`read_eligible_editorial_result(...)`,
`collect_editorial_review_runtime_evidence(...)`, then runtime packet building
in `editorial_review_runtime.py`.

The API observer safely catches `OSError`, `ValueError`, `KeyError`, and
`TypeError` but intentionally logs only the normalized class, not exception
prose or a traceback. The exact expression is therefore not recoverable from
the safe event alone.

Inspect without assuming guilt:

- live native state/result/receipt field shape differing from fixtures;
- initial/pass or optional-stage evidence translation;
- a collection, digest, or path operation receiving an invalid in-memory type.

The common `TypeError` across delivery and review makes a root-path fault
implausible; a shared evidence-reader or packet-builder assumption is the
stronger starting point.

The matching class does not yet prove one shared failing expression. Morris's
review route evaluates action-disposition joins that Bembo's delivery route
skips. What is shared and proven is the pre-envelope capture region and the fact
that packet assembly's internal typed-status guard was not observed to return.

## Requested Slice 0

1. Freeze source/trace provenance and map the exact installed runtime path.
2. Decide whether retained checkpoints require a separately authorized bounded
   coordinate plus HEAD/GET read; do not list/discover objects.
3. Reproduce provider-free where possible, or define the smallest exact
   read-only reproduction that distinguishes field-shape candidates.
4. Report the exact failing operation and evidence condition before proposing
   implementation, package, or release work.

## Safety / non-goals

No provider work, resume, retry, repair, reconciliation, queue mutation, R2
write/listing/cleanup, Better Stack change/replay, or retained-workspace
mutation is authorized.
