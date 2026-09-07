# Log — duration-led provisional test promotion campaign

## 2026-09-06 — campaign initialized

- Created a separate campaign rather than expanding the active runner
  qualification sprint.
- Established duration-led review priority with isolation still requiring
  independent proof.
- Preserved test semantics, protected observability, provider-free execution,
  deterministic receipts, and serial release authority as hard boundaries.
- Planned an evidence-dependent number of small promotion batches rather than
  promising that all provisional modules will become parallel-safe.
- Added a non-blocking architecture slice for evolving the manifest into a
  pipeline-, tier-, resource-, and execution-profile-aware source of truth for
  both conservative local execution and future distributed CI. The runner's
  project-specific isolation semantics remain authoritative; a future CI
  platform supplies capacity and orchestration rather than replacing them.
