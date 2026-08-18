# AstroWoof Natal Authoring 0.4.7 Compatibility

Status: authorized release contract

| Component | Required version | Published wheel SHA-256 |
|---|---:|---|
| Astrology Graph Foundry | 0.8.1 | `860c48793318c82c986b32664cd0f3fe97c4b1e02fb1e489561bc395c8b5a3ed` |
| Semantic Projection Core | 0.11.0 | `82290df44fe5697e87df2e27eb0aa4bab3b7954c66ce988efda0962964e1366d` |
| SBE | 0.4.7 | recorded in `release-manifest.json` |

Python 3.11 or newer is required. Qualification covers Linux CPython 3.11 and
Windows CPython 3.12.

Exact Natal accepts the static projected semantic graph contract. Bounded Natal
accepts `projected_bounded_semantic_graph.v1` four-context families and admits only
invariant claims. Interactive and Batch transports preserve the same six-pass
editorial topology while retaining their distinct authorization cardinalities.

Legacy bounded one-operation v1 workspaces remain non-resumable and fail closed as
`legacy_bounded_topology_unsupported`.
