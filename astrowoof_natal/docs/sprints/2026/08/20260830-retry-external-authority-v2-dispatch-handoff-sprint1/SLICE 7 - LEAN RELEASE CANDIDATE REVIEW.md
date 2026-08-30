# Slice 7 — Lean release-candidate review

## Candidate

- Version: `0.4.31`
- Dependency: `semantic-projection-core==0.11.1`
- Wheel: `astrowoof_natal_authoring-0.4.31-py3-none-any.whl`
- Size: 1,111,586 bytes
- SHA-256: `6bb587c9cd5cd0ef8bf767a677450fbaf7fcd9bf3be655ef68584e279a03f0d9`
- Artifact source commit: `3709f18d1b8c15c6030173868e175110a7894c51`

Two controlled post-commit builds produced byte-identical wheel bytes. The later
release/evidence-lock commit contains only release records and is intentionally
distinct from the artifact source commit above.

## Scope

This patch adds one read-only, snapshot-validating discovery boundary for exact
sealed native-transition-result availability. It does not change lifecycle
selection, provider submission or retrieval, spend authority, native mutation,
terminal-result semantics, or retained-run recovery.

## Installed evidence

- Generic installed release smoke: pass.
- Packaged availability schema and root reader exports: pass.
- Availability CLI `none_available`: pass.
- Availability CLI `available`: pass, joined to a sealed exact result.
- Terminal-review qualification: pass against the corrected `0.4.31` receipt.
- Installed dependency identity: SPC `0.11.1`.

## Full-suite record

The full suite was intentionally run once. It completed 905 cases in 947.198
seconds: 857 passed, 47 expected skips, and one failure. The failure was a
deterministic release-identity fixture mismatch: the packaged terminal-review
qualification still named already-published `0.4.30` after `pyproject.toml` had
been advanced to `0.4.31`.

The fixture version and its canonical receipt digest were corrected. The affected
focused suite then passed 30 tests with two expected optional-schema skips, and
the corrected final wheel passed the installed terminal-review qualification,
generic release smoke, and both new availability outcomes. By explicit owner
direction, the full suite was not repeated and this record does not call it green.

## Safety statement

Qualification was provider-free and did not access or mutate retained QA, resume
a worker, perform recovery, create/retrieve provider work, spend funds, deploy, or
change API state.

## Gate

Paused for explicit owner and API approval before commit, annotated tag,
publication, and post-publication download verification.
