# Historical one-off test programs

These programs are preserved as investigation evidence from the August 31,
2026 partial-reconciliation snapshot-mutation investigation. They are
intentionally stored with `.py.txt` extensions outside the package test tree.

They are not evergreen regression tests:

- `partial_reconciliation_snapshot_mutation_slice0.py.txt` characterized the
  historical moving-workspace failure shape.
- `partial_reconciliation_wheel_battle_slice2.py.txt` compared the immutable
  SBE 0.4.35 and 0.4.36 wheels under explicitly supplied environment controls.

Running either program through ordinary test discovery is incorrect. The
wheel-battle program in particular depends on historical wheel installations
and `SBE_WHEEL_BATTLE_*` environment variables. The durable conclusions and
artifact identities remain recorded in the sprint evidence documents.
