# AstroWoof Natal Authoring 0.4.13 Release

Status: qualified and authorized for immutable publication

## Summary

SBE 0.4.13 corrects the lifecycle classification used after an interactive
six-member initial authoring wave has durable provider identities but no ordinary
local work. Lifecycle inspection v0.4 now exposes a closed `execution_branch`:

- provider-only work is not reported as local continuation;
- not-due work releases capacity until the native lower bound;
- already-due work directly selects the provider-reconciliation cycle; and
- SBE retains ownership of the bounded next retrieval subset.

The API invokes only the supported run-level command and never reconstructs a
provider operation from action IDs.

## Qualification

- API contract and implementation review: approved.
- Focused lifecycle, bounded-route, contract, event, and consumer suites: pass.
- Installed-wheel provider-pending qualification: pass.
- Six scripted creates and six scripted retrievals in bounded 4+2 cycles: pass.
- Installed-wheel release smoke: pass.
- Fixed-epoch double build: byte-identical.
- Provider network calls/submissions/spend: 0 / 0 / USD 0.

Wheel SHA-256:
`4798758f0420d43276efce50c1611db222fba1dc1c2b9446319efe82b089e8f9`.
