# AstroWoof Natal Authoring 0.4.2 Known Limitations

- Filesystem persistence is a recoverable ordered protocol, not one atomic write
  spanning every workspace file.
- Provider-bound, consumed, reported, or ambiguously submitted actions cannot be
  denied or reconciled as providerless.
- Legacy reconciliation accepts only the exact recognized 0.4.1 evidence and known
  write set; it cannot bless arbitrary changed workspace bytes.
- A submitted providerless denial is final. Temporary API reservation delay must
  remain API-owned waiting and must not be expressed as a denial.
- Events are non-authoritative, redacted, failure-isolated observations.
- The operation does not mutate API reservations, capacity, leases, databases, or
  publication state.
- Batch size remains a fixed maximum of 32 actions.
- Bounded-Natal Batch provider authoring remains unsupported and
  `service_level=batch` is rejected.
