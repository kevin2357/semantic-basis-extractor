# Log

- 2026-09-10: Sprint opened on clean `main` for Baskerville and Hopper. Scope is
  the existing assessed-quarantine production boundary only. The historical
  failed attempt is explicitly unrecoverable after QA database/R2 reset; Slice 0
  will reconstruct current behavior with genuine provider-free generated
  evidence and will not claim historical causal reproduction.
- 2026-09-10: No Baskerville/Hopper workspace access, R2 access, provider work,
  quarantine execution, process termination, cleanup, or runtime mutation has
  been authorized or performed by this sprint.
- 2026-09-10T19:27:22.727Z: API submitted exact operator request
  `02de1a55-b137-499d-9fb4-c327a7fe3116`. The runner returned `refused` with
  `disposition_assessment_unavailable`. It did not quarantine Baskerville or
  release her capacity. This reproduces the remembered external failure
  signature, but does not yet classify the unavailable-assessment seam or
  explain why Baskerville originally became stuck.

