# AstroWoof Natal Authoring 0.4.5 Compatibility

## Runtime pins

| Component | Qualified release | Published/candidate SHA-256 |
| --- | --- | --- |
| Astrology Graph Foundry | 0.8.1 | `860c48793318c82c986b32664cd0f3fe97c4b1e02fb1e489561bc395c8b5a3ed` |
| Semantic Projection Core | 0.11.0 | `82290df44fe5697e87df2e27eb0aa4bab3b7954c66ce988efda0962964e1366d` |
| SBE release | 0.4.5 | `9b5f1ce0336c791ec4fde906ccd2e8deeac3abc6bc9eac49e94f2c7ea62e71b4` |

Python 3.11 or newer is required. SBE directly pins
`semantic-projection-core==0.11.0`.

All 0.4.4 extraction, authoring, spend, lifecycle-inspection, provider-
reconciliation, denial, snapshot, delivery, and closeout contracts remain
compatible. Native transition journal/result/receipt contracts v0.1 are additive
consumer surfaces introduced in 0.4.5.

The new terminal-first ingestion path requires 0.4.5 artifacts and explicit result
identity. Historical workspaces without a valid journal/result/receipt publication
must not be inferred into the new contract from exit code, stderr, logs, or mutable
private state.

Supported provider routes remain exact Natal Responses, exact Natal Batch, and
bounded-Natal Responses. Bounded-Natal Batch remains explicitly unsupported.
