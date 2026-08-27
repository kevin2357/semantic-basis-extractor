# SBE 0.4.26 Known Limitations

- The bounded campaigns are deliberately finite and fixed-seed; they are not a
  proof over an unbounded state space.
- The historical starvation path is explicitly a `historical_shape`, not a claim
  that the corrected production worker still exhibits the defect.
- Qualification receipts describe tested evidence only. They do not grant API
  capacity, leases, reservations, spend, billing settlement, or publication.
- API deployment and pinning require a separately qualified worker-image/runtime
  combination.
