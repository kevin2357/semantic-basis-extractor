# AstroWoof Natal Authoring 0.4.0 Candidate Compatibility

## Runtime pins

| Component | Qualified release | Published SHA-256 |
| --- | --- | --- |
| Astrology Graph Foundry | 0.8.1 | `860c48793318c82c986b32664cd0f3fe97c4b1e02fb1e489561bc395c8b5a3ed` |
| Semantic Projection Core | 0.11.0 | `82290df44fe5697e87df2e27eb0aa4bab3b7954c66ce988efda0962964e1366d` |
| SBE candidate | 0.4.0 | `4fb7a114ae4866475778d36b677d170499a5558e0f1a854aeb88616b9c6c8c84` |

SBE requires Python 3.11 or newer and directly pins
`semantic-projection-core==0.11.0`. SPC requires `jsonschema>=4,<5`. AGF 0.8.1 is
the preferred compatible producer of the bounded wire identities accepted here.

## Supported routes

- Exact Natal remains supported with `legacy_atomic.v1` as the unchanged default.
- Exact `axis_aware.v1` is experimental and opt-in.
- Bounded Natal accepts only `projected_bounded_semantic_graph.v1` from all four
  exact supported Woofmapping contexts and produces only invariant claims.
- Exact and bounded artifacts cannot be mixed.
- Bounded Batch authoring is not implemented. `service_level=batch` fails before
  execution so interactive Responses work cannot be mispriced as Batch.

Operator run v0.9, spend ledger v0.1, public state v0.1, lifecycle inspection,
providerless denial, closeout, and stable-logical-absolute-path snapshots remain
the common operational authority for both routes.
