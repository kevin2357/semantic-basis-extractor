# Log

- 2026-09-14: Opened as the SBE companion to API Sprint 97 after both QA runs
  reached accepted delivery but Better Stack observation remains unconfirmed.
  Raw unfiltered Render exports and all immutable run coordinates are recorded
  in `BACKGROUND.md`. No native/runtime change has been made.
- 2026-09-14: Parsed both nonempty exports completely. Both exact terminal-
  delivery handoffs survived the publication retry and entered the observer.
  Both returned `capture_or_preflight` before any HTTP outcome, narrowing the
  investigation to local SBE capture construction or API request preflight.
  Expanded the investigatory plan through the joint pre-implementation gate.
- 2026-09-14: Completed Slice 0 and provider-free Slice 1. SBE accepted-polish
  capture and exact/fail-closed status tests passed (`3 passed`); API's complete
  editorial observer/preflight module passed (`15 passed`). The checked-in
  fixtures do not reproduce either live failure. Stopped before Slice 2 for
  exact-coordinate review and separate owner authorization; no retained
  workspace or external system was accessed.
- 2026-09-14: API supplied an owner-authorized coordinate/read receipt and two
  hash-verified local archives. Exact-path reproduction found both inventories
  complete, but API's stated checkpoint roots differ from the native durable
  roots recorded in `run.json`. The former reproduces snapshot-validation
  failure; the latter yields complete delivery captures (`1` packet, `8`
  projections, `9` artifacts each). Assigned correction ownership to API and
  stopped at the joint implementation-review gate. No runtime code, provider,
  publication, lifecycle, or QA state was changed.
- 2026-09-14: API approved the Slice 2 finding and accepted correction
  ownership. Closed the SBE investigation with no runtime, package, schema,
  test-manifest, or Alloy change. API will preserve the exact native durable
  workspace root through initial terminal publication and publication retry,
  while SBE's strict root validation remains unchanged.
