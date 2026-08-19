# SBE 0.4.9 Known Limitations

- `astrowoof-deployed-qa` is topology and contract qualification, not a live
  provider integration test.
- Scripted provider identities in its receipt are not external provider evidence.
- The receipt is not production execution, scheduling, reservation, billing,
  delivery, or publication authority.
- The command intentionally stops Batch routes at provider-pending detach; it does
  not simulate provider billing reconciliation.
- Global reservations, quotas, circuit breakers, product policy, and billing
  reconciliation remain API-owned.
