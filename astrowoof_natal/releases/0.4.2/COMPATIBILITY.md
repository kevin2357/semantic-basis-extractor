# AstroWoof Natal Authoring 0.4.2 Compatibility

## Runtime pins

| Component | Qualified release | Published SHA-256 |
| --- | --- | --- |
| Astrology Graph Foundry | 0.8.1 | `860c48793318c82c986b32664cd0f3fe97c4b1e02fb1e489561bc395c8b5a3ed` |
| Semantic Projection Core | 0.11.0 | `82290df44fe5697e87df2e27eb0aa4bab3b7954c66ce988efda0962964e1366d` |
| SBE release | 0.4.2 | `cb63b4ff8a014a1e5848071a52c280bd14c2b69293388b1c2576a5e9940f7366` |

Python 3.11 or newer is required. SBE directly pins
`semantic-projection-core==0.11.0`.

All 0.4.1 exact-Natal, bounded-Natal, spend, snapshot, delivery, and providerless
denial operations remain compatible. Negative-authorization requests remain v0.1.
New successful single and batch results are v0.2; v0.1 results remain supported as
historical reader evidence.
