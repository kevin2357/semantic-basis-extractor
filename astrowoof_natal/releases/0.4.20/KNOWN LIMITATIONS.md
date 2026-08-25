# Known Limitations — SBE 0.4.20

- Ordinary external-authority v2 Batch dispatch is deliberately deferred.
- Provider identity-less interruption after `CALL_ENTERED` is conservatively
  ambiguous and requires review; local deterministic keys are not provider
  idempotency evidence.
- API remains authoritative for global admission, reservations, capacity, leases,
  product policy, and billing reconciliation.
