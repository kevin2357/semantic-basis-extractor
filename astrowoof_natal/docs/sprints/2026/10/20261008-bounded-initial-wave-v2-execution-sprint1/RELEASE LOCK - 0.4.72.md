# Release lock — AstroWoof Natal Authoring 0.4.72

This record freezes the intended release candidate. The commit containing this
file is the intended annotated-tag target, subject to rebuilding and installed
qualification after that commit. Publication and its evidence are separate.

## Immutable identities

| Item | Value |
| --- | --- |
| Artifact-source commit | `986e05ea04fc31419d6c0e240ce05d7ba3baa980` |
| Release tag | `astrowoof-natal-authoring-v0.4.72` |
| Fixed `SOURCE_DATE_EPOCH` | `1791479232` |
| Wheel | `astrowoof_natal_authoring-0.4.72-py3-none-any.whl` |
| Qualified wheel SHA-256 | `298273523a05c7a72cdd5404ca1727ef3f03c5c922785a7c5ba4da6f2990c364` |
| Wheel size | `1,442,607` bytes; 330 members |
| Resource-set SHA-256 | `38ee3bf6464a14f9e00c0b79d97764627fe758b452ff9520f27c92b1126c0688` |
| SPC | `semantic-projection-core==0.11.1` |
| Bounded profile | `astrowoof.bounded_natal.live.stable_facts.v3` |
| Profile SHA-256 | `5ccdbac1d8b81b9099fa7689f08460c30a2563192b4c766587ea190bfb05caed` |
| Prompt release | `astrowoof.authoring.bounded_stable_facts.v3` |
| Prompt SHA-256 | `737bb2cb64e426b281a12a88578b7831473b228d2b40a7fdb2c8c7ad5fa1b0e6` |
| Worker descriptor SHA-256 | `440d4475d4b746833f45bc9a4efc53d220fca636476ca6f8d626f4259b201cf8` |
| Profile catalog SHA-256 | `039fd08ea77f105cb52ae9376e7e3907b3ff130d258f6afccafc375f609d1982` |
| Prompt catalog SHA-256 | `d827e2d7cc1aa7fbc4c4f62b3624dda0d30b7afce6bd709bac71523d6006851e` |

The original unpublished `dadd3969…` candidate is superseded after the broad
suite exposed an exact-route regression; the fix was included before the
successful complete rerun. The replacement was built twice from independent
Git archives with `core.autocrlf=false`, `core.eol=lf`, and the fixed epoch;
the wheels and member bytes matched and packaged text contained no CRLF.
The intended publication artifact is the retained exact wheel at
`C:\tmp\sbe-0.4.72-regression-candidate\canonical-wheel-a\astrowoof_natal_authoring-0.4.72-py3-none-any.whl`.

## Qualification and scope

The broad/full regression gate was selected because the change affects native
authority and lifecycle. At artifact source `986e05ea`, the manifest runner
using Python 3.12 ran 1,267 cases with 62 skips, no failures or errors, in
1,345.694 seconds. Receipt: `C:\tmp\sbe-0472-canonical-broad-suite-receipt.json`.
Changes since that source commit are sprint documentation only; the broad suite
was not repeated for this documentation-only lock.

Candidate installed `pip check`, generic smoke and provider-free adversarial
qualification passed; see [the precheck](RELEASE%20PRECHECK%20-%200.4.72.md)
and its retained receipts. API's joined installed-wheel grant, command,
receipt, replay and altered-grant test passed for the exact candidate; its
expanded provider-free crash-custody matrix has 28 cases, with limitations
recorded by API. API approved package release of this exact SHA in its sprint
128 `API GATE D - 0.4.72 PACKAGE RELEASE REVIEW.md`; the owner authorized
release. No API approval transfers to a different wheel hash.

Relational-model impact: this release adds a separate bounded initial-wave v2
authority/execution path with six ordered actions and preserves ordinary v2
and exact-route boundaries. This release relies on executable contract and
joined/failure-injection tests; no new Alloy claim or model run is asserted.

This release does not itself authorize or attest QA/production deployment,
profile activation, paid provider work, live alert qualification, real R2
outages, or an exhaustive exact-route crash matrix. Bounded provider behavior
remains subject to separate controlled live QA; this change addresses authority
and execution rather than changing authoring prompt content.
