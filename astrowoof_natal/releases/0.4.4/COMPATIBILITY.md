# AstroWoof Natal Authoring 0.4.4 Compatibility

## Runtime pins

| Component | Qualified release | Published/candidate SHA-256 |
| --- | --- | --- |
| Astrology Graph Foundry | 0.8.1 | `860c48793318c82c986b32664cd0f3fe97c4b1e02fb1e489561bc395c8b5a3ed` |
| Semantic Projection Core | 0.11.0 | `82290df44fe5697e87df2e27eb0aa4bab3b7954c66ce988efda0962964e1366d` |
| SBE release | 0.4.4 | `ee98db9512a5d0bb7082ef1e4b92ab5923bac9bbb88014f2a35fbfceeee2e6bd` |

Python 3.11 or newer is required. SBE directly pins
`semantic-projection-core==0.11.0`.

All 0.4.3 extraction, authoring, spend, denial, snapshot, delivery, and closeout
contracts remain compatible. Lifecycle inspection v0.3 and reconciliation result
v0.2 are required for route-parity capacity decisions. Inspection v0.2/v0.1 and
cycle result v0.1 remain historical evidence and must not authorize the new route
behavior.

Timing-free retained 0.4.3 Batch workspaces fail closed. Existing bounded 0.4.3
Responses workspaces are accepted only when their timing and route evidence satisfy
the strict current contract.

