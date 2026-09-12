# Evidence

| Fact | Evidence | Authority |
| --- | --- | --- |
| Exact SBE checkpoint archive | `d5d942...882cc`, `14f286...7fafc`, 1,795,164 bytes | API checkpoint registry plus owner-authorized conditional HEAD/GET |
| Archive restoration | 387 members, 8,490,671 expanded bytes | Local checkpoint-archive verifier |
| Native snapshot comparison | 375 expected and 375 actual records; same map, differing ordered list | Exact released SBE 0.4.60 wheel against isolated local restore |
| Canonical-key comparison | `PurePosixPath(path).parts` exactly reproduces the retained 375-member Linux order; plain string and case-folded string ordering do not | Independent read-only SBE-side comparison |
| Failure text | `Relocated workspace snapshot is incomplete or changed` | Public relocated reader |
| Live custody | worker suspended; no operator request or quarantine mutation | API/Render operational boundary |

The first host-order divergence is at member 16, where Windows places a
lowercase `cards/` subtree before uppercase sibling files. The first
plain-string-versus-Linux component-order divergence is at member 198, where a
same-prefix `.zip` sorts differently from its sibling directory subtree.

## Slice 1 qualification

- Portable-order, duplicate, genuine-drift, relocation, checkpoint-repair, and
  manifest-runner suites: `46 passed`.
- The new regression module is registered in `test_suite_manifest.json`.
- Corrected source reads the exact retained Bodoni restore and validates its
  wrapper; all 387 files remain byte-identical before and after.
- No provider operation or external storage read occurred.
