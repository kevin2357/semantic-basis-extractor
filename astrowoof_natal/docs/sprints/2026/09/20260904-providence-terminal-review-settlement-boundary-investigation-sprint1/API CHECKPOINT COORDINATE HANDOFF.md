# API checkpoint coordinate handoff

API supplied the requested immutable generation-12 coordinate packet at:

`C:\dev\github\astrowoof-api\docs\sprints\2026\09\20260904-providence-terminal-review-settlement-boundary-api-investigation-sprint77\providence-generation-12-checkpoint-coordinate.v1.json`

Its SHA-256 is
`99170231609c2f4db616192b3ea98a3b71e9faf4dd97afe2e58b84204f153d37`;
the adjacent `.sha256` sidecar records the same digest.

The packet is coordinates only and authorizes no R2 access. In particular:

- exact object: QA bucket `astrowoof-qa-artifacts`, key
  `v1/checkpoint/64f3af2fbe3544cdbbecc1f96bbfb792`;
- exact ETag/provider version, byte size, archive and inventory SHA-256 values
  are frozen in the packet;
- the final revision-79 snapshot SHA-256 is available from the invocation trace;
- no separate checkpoint-basis digest was persisted for that terminal revision.

The owner must separately authorize exactly one conditional HEAD and one
conditional GET before any R2 access. No listing, write, provider call,
reconciliation, settlement, repair, or retained-run mutation is authorized.
