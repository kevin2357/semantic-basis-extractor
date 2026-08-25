# Known Limitations — SBE 0.4.21

- This release exports durable native observations; it does not implement API
  persistence, dashboards, calibration, or account-authoritative billing.
- Provider compute duration remains null unless explicitly reported. SBE-observed
  provider-pending wall time includes scheduler and polling delay.
- Retrieval detail retains the first 16 references plus an overflow count.
- `legacy_unknown` cohorts are reportable but excluded from automatic calibration.
- Legacy bounded v1 workspaces fail closed.
