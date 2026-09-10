# API technical approval — 0.4.57 packaged fixture canonicalization

Date: 2026-09-10

## Review conclusion

API approves the `0.4.57` corrective release candidate for owner tag and
publication, subject to the stated release-lock procedure.

The candidate addresses the API broad-suite failure at the correct boundary:
the packaged fixture bytes and catalog digests now share an explicit LF byte
policy rather than relying on the host's checkout conversion behavior. This is
a packaging/resource-identity correction, not a relaxation of catalog
validation or a runtime/lifecycle change.

## Evidence reviewed

- Candidate source commit: `9158e89`.
- Candidate wheel: 1,375,422 bytes; SHA-256
  `957f677d46ad01a7a7243e79db611c14fb63763868056aae971d9d50642abc1c`.
- `.gitattributes` explicitly pins `*.json text eol=lf` while retaining the
  repository's general text policy.
- All nine digest-bearing catalog fixtures were checked; source, both
  `core.autocrlf` archive modes, wheel, and installed-package bytes agree.
- Two candidate wheel builds are byte-identical. Installed focused
  qualification, provider-free adversarial QA, release smoke, and public
  catalog-reader checks pass.
- The six changed API-facing digests are limited to values whose prior API/SBE
  identity was accidental CRLF checkout bytes. Case order, owners, evidence
  references, assertions, parsed JSON values, and the other three fixture
  digests remain unchanged.

## Required API follow-up

API must not update its frozen `_CASE_SPECS` digest values while still pinned to
`0.4.56`: doing so would intentionally reject that immutable historical
release. After `0.4.57` is tagged and published, API will consume the exact
released wheel, update the six listed expectations from the handoff, and rerun
the previously failing vertical slice plus the broader release gate.

No API deployment, Better Stack delivery, provider work, or lifecycle change is
approved by this package-release approval.
