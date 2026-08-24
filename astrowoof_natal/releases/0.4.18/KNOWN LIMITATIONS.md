# Known Limitations — SBE 0.4.18

This release does not change provider limits, pricing, spend-policy semantics,
or the API-owned cross-run reservation policy. A retained workspace whose
evidence is internally contradictory must still fail closed for review rather
than being reconstructed from diagnostics.
