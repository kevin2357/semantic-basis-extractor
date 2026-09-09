# Slice 3D — Native-result version runtime discovery

Runtime mapping found a fixture-provenance error, not a structural schema gap.

- Successful ordinary delivery is published as
  `astrowoof.native_execution_result.v0.1`.
- Interactive terminal editorial review is published as
  `astrowoof.native_execution_result.v0.2`.
- Both use `astrowoof.native_publication_receipt.v0.1`.

The packet schema already carries these as explicit strings and does not require
one false shared version. The accepted fixture is therefore corrected to v0.1,
the closeout fixture remains v0.2, and both use the canonical receipt name.
The runtime builder must dispatch through the exact-result reader's validated
version rather than infer result semantics from the packet outcome.

This correction changes no lifecycle, custody, transport, or provider behavior.
Runtime construction remains paused for narrow provenance review.
