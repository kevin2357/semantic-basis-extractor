# Known Limitations — SBE 0.4.23

- Provider submission and durable local identity persistence cannot be atomic.
- Anything after the durable call fence without one valid durable provider ID
  remains ambiguity/review-only.
- Historical v2 ambiguity lacks the phase proof required for reclassification.
- Pre-provider refusal is nonterminal but never implies automatic retry; fresh
  inspection and fresh external authority are required.
- Initial-wave v1 and ordinary Batch behavior are unchanged by this patch.
- API-global reservations, capacity, billing reconciliation, and product policy
  remain API-owned.
