# Known Limitations — SBE 0.4.25

- V0.7 local-work members are SBE-selected evidence for a run-level command; they
  are not independently executable API tasks.
- The current concrete operation vocabulary covers proven exact/bounded interactive
  post-fan-in work. Batch remains governed by its existing round contracts and
  fails closed where equivalent local work cannot be proven.
- The provider submission/identity-persistence atomicity gap remains unchanged and
  fail-closed after provider call entry.
- SBE does not assert API-global reservation, capacity, lease, admission, billing,
  entitlement, or publication facts.
- API deployment requires a matching v0.7 consumer update and fresh release-pair
  qualification before a new paid QA cohort.
