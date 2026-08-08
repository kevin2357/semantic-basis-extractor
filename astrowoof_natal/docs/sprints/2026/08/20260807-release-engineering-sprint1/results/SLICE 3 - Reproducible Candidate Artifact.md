# Slice 3 — Reproducible Candidate Artifact

## Result

Slice 3 passes and awaits gate approval. The approved distribution version is
now `0.2.0`. Two corrected candidate builds are byte-identical:

- filename: `astrowoof_natal_authoring-0.2.0-py3-none-any.whl`;
- size: 623,605 bytes;
- SHA-256: `799307597fb33e5717112e0c772983bca2dd78bd193b999a5286e4476f2b4ea4`.

These are candidate artifacts outside Git, not published release assets.

## Reproducible build

Both builds used CPython 3.12.13, setuptools 83.0.0, wheel 0.47.0, pip 26.0.1,
and `SOURCE_DATE_EPOCH=1786156755`. They were emitted into separate directories
outside the checkout and matched byte-for-byte.

## Package allowlist

The complete 40-member wheel consists only of:

- 16 allowlisted `astrowoof_natal_authoring` Python source members, including
  the two CLI modules;
- 19 resources selected by the explicit `pyproject.toml` package-data classes
  (`authoring`, `contracts`, `fixtures`, `references`, and `schemas`); and
- five standard `.dist-info` metadata members.

There are no absolute or parent-traversal paths and no unexpected member
class. Sprint workspaces, repository docs, generated run artifacts, provider
payloads/responses, authorization records, snapshots, caches, bytecode, logs,
and environment files are absent.

## Protected-reference finding

The first audit correctly rejected two otherwise reproducible wheels because
the required Kevin editorial gold reference still carried six protected birth
and location values. Excluding the whole reference would remove runtime
behavior, so only those values were cleared (`""` or `null`); semantic and
editorial content was preserved. A release-contract regression now freezes
that sanitized boundary.

The two replacement builds above contain none of the audited exact datetime,
coordinates, location, secret markers, or API-key signatures. The rejected
pre-fix wheels are not candidates.

## Resource identity and verification

- resource count: 19;
- aggregate resource SHA-256:
  `439c8771fe7944ddb1b5b83465b7d2f76f252340624f1b85c85f9278fba55404`;
- ZIP integrity: pass;
- complete repository suite after sanitization: 140 passed;
- focused release-contract suite after adding the regression: 13 passed;
- `git diff --check`: pass;
- live provider calls: zero.

The exact candidate wheel is ready for Slice 4 clean-installed deterministic
qualification after this gate. No tag or publication occurred.
