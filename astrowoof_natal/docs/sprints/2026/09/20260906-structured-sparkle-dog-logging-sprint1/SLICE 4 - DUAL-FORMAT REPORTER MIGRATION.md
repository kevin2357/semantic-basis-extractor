# Slice 4 — Dual-format reporter migration

## Result

The diagnostic run reporter now accepts historical pipe traces, structured
`astrowoof.sbe_worker_log.v1` records, and mixed files.

## Parsing precedence

1. Locate a complete JSON object after any Render/supervisor prefix.
2. If it declares the recognized SBE application-log schema/type, validate the
   complete closed record and consume only native JSON fields.
3. If it is an existing typed envelope, retain the prior envelope inventory.
4. Count any other complete JSON object as an unknown JSON record.
5. Otherwise, try the historical sparkle-dog pipe parser.

The structured `message` is never tokenized to override event, correlation, or
payload fields. Null remains null.

## Ordering and duplicates

Normalized events are ordered by their producer UTC timestamp and then source
line. Exact duplicate producer records are retained as observations—because
the reporter is diagnostic and cannot decide which relay observation to erase—
but their later source lines are listed in bounded duplicate coverage. This
makes duplication queryable without hiding evidence.

## Failure accounting

- A recognized but structurally/semantically invalid SBE v1 record is counted
  as malformed.
- A truncated JSON record containing the SBE marker is counted as malformed.
- A complete foreign JSON object is counted separately as unknown JSON.
- Existing execution/command envelopes remain separately inventoried.
- Counts and line-number inventories are bounded in the normalized trace.

## Privacy

Structured human-message prose is not copied into normalized events or report
artifacts. Payloads already passed the closed logging validator. A dedicated
sentinel proves raw human prose does not appear in JSON, Markdown, Mermaid, or
HTML reporter output.

## Evidence

The reporter, trace-observability, formatter, structured-contract,
execution-event, and both provider-free observability qualification suites
pass together: 56 tests, with two expected optional-schema skips.

This slice changes diagnostic parsing only. It does not change native state,
provider behavior, command results, or API authority.
