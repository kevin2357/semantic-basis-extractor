# AstroWoof Natal Authoring 0.4.1 Compatibility

## Runtime pins

| Component | Qualified release | Published SHA-256 |
| --- | --- | --- |
| Astrology Graph Foundry | 0.8.1 | `860c48793318c82c986b32664cd0f3fe97c4b1e02fb1e489561bc395c8b5a3ed` |
| Semantic Projection Core | 0.11.0 | `82290df44fe5697e87df2e27eb0aa4bab3b7954c66ce988efda0962964e1366d` |
| SBE release | 0.4.1 | recorded after final artifact qualification |

Python 3.11 or newer is required. SBE directly pins
`semantic-projection-core==0.11.0`.

All 0.4.0 exact-Natal and bounded-Natal routes remain compatible. The batch
providerless-denial operation is additive. Existing consumers may continue using
the unchanged single-action denial operation.
