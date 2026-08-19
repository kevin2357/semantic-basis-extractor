# SBE 0.4.11 API Consumer Handoff

No public lifecycle or artifact schema changes are required for adoption.

Workers may pass `--host-id` and `--invocation-id` for correlation and select
verbosity with `--log-level`. Logs go to stderr; stdout remains reserved for each
command's existing machine-readable result. The default format is documented in
`docs/post_extraction_authoring/Application Logging.md`.

Logs must remain observational. API-owned PostgreSQL/R2 state, reservations,
capacity, billing, public delivery, and SBE's validated native artifacts retain
their existing authority.
