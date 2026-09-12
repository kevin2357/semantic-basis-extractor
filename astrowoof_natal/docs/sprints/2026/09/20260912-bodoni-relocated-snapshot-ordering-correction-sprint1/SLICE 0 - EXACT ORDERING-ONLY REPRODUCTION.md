# Slice 0 — Exact ordering-only reproduction

## Result

The retained, hash-verified Bodoni generation-3 checkpoint proves a pure
cross-platform ordering defect in SBE `0.4.60` snapshot inventory validation.

- Expected and actual inventories each contain 375 records.
- Relative path sets are identical.
- Every corresponding byte size and SHA-256 is identical.
- Host-ordered lists first differ at index 16.
- The archive SHA-256 is exactly
  `d5d94241314e084e0c8375b0de31f432a934689929ad90bc4891abdcd4d882cc`.

The implementation sorts host-native absolute `Path` objects before converting
them to relative POSIX paths. Windows therefore applies different comparison
semantics than the Linux authoring host.

## Canonical ordering decision

Three candidate comparisons were checked against all 375 retained records:

| Key | Retained Linux order |
| --- | --- |
| Windows host `Path` | differs at index 16 |
| plain relative POSIX string | differs at index 198 |
| case-folded relative string | differs |
| `PurePosixPath(relative).parts` | exact match |

The component tuple is the compatible portable key. It preserves historical
Linux `Path` ordering, including a directory subtree beside a same-prefix
`.zip`, while removing the restored host's case/path semantics.

## Corrected-source retained control

Against the retained local restore, the candidate source:

- returns native custody `provider_pending_known_identity`;
- returns quarantine posture `permitted` and reason
  `known_provider_operation_pending`;
- validates the relocation authority/wrapper pair; and
- leaves all 387 restored files byte-for-byte unchanged.

No R2 access, provider operation, live runner action, or retained-workspace
mutation occurred.

