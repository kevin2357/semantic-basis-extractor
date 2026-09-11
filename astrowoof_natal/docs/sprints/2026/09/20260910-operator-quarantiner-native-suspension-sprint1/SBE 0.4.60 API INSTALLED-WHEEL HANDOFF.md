# SBE 0.4.60 API installed-wheel handoff

Status: ready for API consumer qualification; no tag or publication authorized.

## Immutable candidate

- release-lock commit:
  `350a8bf53582d2052093b6638f9ede97d8115a7d`
- tag target if later approved:
  `350a8bf53582d2052093b6638f9ede97d8115a7d`
- recorded `SOURCE_DATE_EPOCH`: `1789089592`
- canonical wheel:
  `C:\tmp\sbe-0460-final-350a8bf\wheel-one\astrowoof_natal_authoring-0.4.60-py3-none-any.whl`
- bytes: 1,383,825
- members: 310
- SHA-256:
  `618caee2c2f338cf868cfb024f764217c7b4ef4c83aff283b2bf78cd6e67d627`

Two clean archive builds from the exact lock commit reproduced these bytes.
The later commit containing this handoff is documentation-only and must never
be used as the release tag target.

## SBE qualification

- expanded focused matrix: 139 passed, 3 expected skips;
- corrected diagnostics/manifest gate: 25 passed;
- complete broad/full suite: 1,184 passed, 60 expected skips;
- wheel inventory and forbidden-member audit: pass;
- clean installed `pip check`, version/site-packages/export checks: pass;
- installed release smoke: pass;
- installed adversarial lifecycle QA: pass;
- installed operator-disposition QA: pass; and
- provider/network operations and spend: zero.

## Required API gate

Using only the exact wheel above, API should exercise its real request-isolated
checkpoint restore shape and ordinary `force=False` in-process SBE logging
setup. The gate must prove:

1. the relocated reader and closed pair validator are available from the
   installed wheel;
2. the exact authority-bound wrapper is accepted by API's writer;
3. wrong or missing identity/digest bindings fail closed;
4. SBE assessment events coexist with API stdout events under normal host
   initialization;
5. restored workspace bytes remain unchanged; and
6. provider calls, external network calls, retained-workspace access, and spend
   remain zero.

No API/Render mutation, live quarantine, capacity release, native suspension,
tag, or GitHub Release is authorized by this handoff.
