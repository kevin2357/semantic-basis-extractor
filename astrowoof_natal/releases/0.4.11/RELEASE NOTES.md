# AstroWoof Natal Authoring 0.4.11 Release

Status: published and verified

## Summary

SBE 0.4.11 adds conventional Python application logging across the principal
exact/bounded, interactive/Batch, spend, reconciliation, lifecycle,
snapshot/publication, editorial, delivery, closeout, and repair paths.

Supported CLIs keep machine-readable results on stdout and emit human-facing logs
to stderr. The default line begins with `✨🐶` and includes UTC time, level, host,
native run, invocation, Python function, and current-state context. `--log-level`
selects verbosity, while embedding applications may replace normal stdlib handlers
and formatters.

Logging is non-authoritative and deliberately excludes credentials, prompts,
authored output, raw provider bodies, Batch JSONL, and protected subject data. No
lifecycle state, spend rule, provider behavior, or public artifact contract changes.

## Qualification

- Focused product tests: 70 passed.
- Final formatter tests: 3 passed.
- Source compilation and diff hygiene: pass.
- Provider requests/submissions/spend: 0 / 0 / USD 0.

Detailed scope and evidence are in the 20260819 operator-observability sprint.

The immutable tag points to `80c817ecb40cd47103b3f28389a26c9100937104`.
GitHub reports the published wheel as 852,245 bytes with SHA-256
`a2339d3302fd8dede54be52de948909992ab1db3d0366befbc457d1f8e035fa2`,
matching the qualified artifact. This post-publication evidence does not move the
tag.
