# SBE 0.4.11 Compatibility

- Python: 3.11 or newer.
- Direct dependency: Semantic Projection Core 0.11.0.
- Qualified upstream identities remain AGF 0.8.1 and SPC 0.11.0.
- Exact/bounded, interactive/Batch, lifecycle, capacity, spend, snapshot,
  diagnostic, and native-transition contracts are unchanged from SBE 0.4.10.
- New operational CLI options: `--log-level`, `--host-id`, and
  `--invocation-id` on the instrumented production commands.
- Ordinary application logs are stderr observations, never consumer authority.
