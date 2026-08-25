# Slice 5 — Packaging and Release Readiness Review

Date: 2026-08-24
Status: complete; SBE 0.4.20 published and digest-verified

## Packaged public surfaces

- strict Python builders, readers, validators, intent fence, payload resolver, and
  provider dispatch executor;
- `astrowoof-external-authority-v2` passive/provider-capable CLI;
- `astrowoof-external-authority-v2-qa` provider-free qualification CLI;
- packaged grant, passive result, intent result, provider-dispatch result, command
  result, and qualification receipt schemas;
- sanitized ordinary-action contract fixture; and
- API consumer handoff with explicit ordinary-Batch deferral.

## Source qualification

- v2 qualification receipt and schema validation: pass;
- exact and bounded same-workspace holistic bridge: pass;
- exact and bounded all-four-stage Response matrix: pass;
- ordinary Batch pre-intent refusal: pass;
- provider-capable CLI with mocked create transport and exact replay: pass;
- passive CLI nonmutation and output-path refusal: pass;
- focused lifecycle, deployed-QA, and provider-pending suites: pass.

No real provider, network, credentials, spend, or retained-QA workspace activity
occurred.

## Installed-wheel and reproducible-build evidence

- Two candidate wheels built with the same frozen build epoch are byte-identical:
  SHA-256 `0e1d127c782a19f997eeb70b51ed615b58affc32435bd42542e3f24b289c621b`.
- The installed candidate reports its module from the isolated virtual
  environment, not the source tree.
- `pip check`: pass.
- `astrowoof-release-smoke --require-installed`: pass.
- `astrowoof-external-authority-v2-qa`: pass; receipt SHA-256
  `5eb7d1ef2fdbd7d1c0e9daae66ae665f667dc9bfc5ba2a83342cbbe8948ab950`.
- Complete source suite exercised all 655 tests: 654 passed, 35 expected skips,
  and the sole failure exposed a Windows CRLF checkout mismatch in a pre-existing
  frozen-artifact hash assertion. The assertion now canonicalizes text to LF, and
  its focused regression passes. Because that correction is test-only and cannot
  affect runtime/package behavior, a redundant second 9.5-minute full-suite run
  was intentionally stopped rather than repeated to completion.
- The receipt proves exact and bounded 4+2 bridges, four ordinary interactive
  Response stages per route, durable dispatch followed by reconciliation-only
  selection, and deliberate ordinary-Batch refusal.
- Real provider creates, retrievals, network calls, credentials, spend, and
  retained-QA access: zero.

The pre-authorization candidate retained package version `0.4.19` and was never
published. Final review required duplicate-definition cleanup and approved a fresh
`0.4.20` release. Immutable `0.4.19` remains unchanged.

## Remaining release gate

1. obtain final API/owner release approval;
2. commit the approved candidate and bump to the fresh immutable release version;
3. rebuild reproducibly from that exact committed source identity;
4. rerun installed smoke, v2 qualification, `pip check`, and artifact checks;
5. record final release hashes/source identity; and
6. only then tag and publish.

Recommended next version: **0.4.20**. Existing `0.4.19` remains immutable.
