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

## Slice 2 release policy

- API review: approved for package qualification.
- Candidate version: `0.4.61` (fresh and unreleased).
- Regression gate: focused matrix followed by the complete checked-in manifest
  suite, because snapshot inventory is shared persistence infrastructure.
- Alloy impact: none; portable ordering changes representation traversal only,
  not lifecycle or relational semantics.
- Retained-workspace gate: exact local Bodoni copy, public installed reader,
  pair validation, and byte-for-byte no-rewrite proof.

## Source regression receipt

- Focused matrix: `46 passed`.
- Complete manifest suite: `1,192` tests, `60` expected skips, zero failures,
  `1,600.308523` seconds.
- Test inventory SHA-256:
  `a65a1b0f50cab9902066571817e2db52b2ccf5ed4add76423451d2512f99f2bf`.

## Pre-lock candidate receipt

- Exact artifact source: `edeb38034c239b5b5ea22c4f0e58a89e33aa1632`;
  fixed `SOURCE_DATE_EPOCH=1789242555`.
- Two clean source exports produced byte-identical canonical wheels:
  `1,383,877` bytes, SHA-256
  `c71ee9717d128107ec09092018f280b3af50b4c569b63869f1b850388773dbcc`.
- Wheel inventories: 310 members, identical; no cache, test, or private
  checkpoint members.
- Clean install: SBE `0.4.61`, Semantic Projection Core `0.11.1`, and
  `pip check` passed after installing declared runtime dependencies.
- Installed release smoke: passed; resume reached `DELIVERY_COMPLETE` and the
  zero-action terminal-result identity remained null.
- Installed lifecycle smoke: passed with installed-runtime enforcement,
  snapshot validation, and route-parity resources present.
- Installed public relocated reader against the retained Bodoni generation-3
  checkpoint returned `provider_pending_known_identity`, `permitted`, and
  `known_provider_operation_pending`; authority/wrapper pair validation passed.
- All 387 retained-workspace files were byte-identical before and after.
- Provider operations and external storage operations: zero.

## Exact release-lock receipt

- Immutable release target:
  `477cfa2491f33377f1a873772c5e465c588f0741`.
- Exact commit epoch: `1789243472`.
- Source archive: 56,173,686 bytes, SHA-256
  `7b002bbbd334c8299dd1bbe9b5ae3977c28fad547858ac4df6d55f2ab053722f`.
- Two independent exact-lock builds produced byte-identical wheels: 1,383,877
  bytes, SHA-256
  `8dd151fced3fc7823ef914c7642798a977eca93d19b1136bf34da55b589ef723`.
- Wheel inventories: 310 members, identical; forbidden-member count zero.
- Clean exact-lock installation and `pip check`: passed.
- Exact-lock installed release and lifecycle smokes: passed.
- Exact-lock installed retained-Bodoni reader: expected assessment, valid
  authority/wrapper pair, and all 387 files unchanged.
- Provider operations, R2 reads, and live QA mutations: zero.
