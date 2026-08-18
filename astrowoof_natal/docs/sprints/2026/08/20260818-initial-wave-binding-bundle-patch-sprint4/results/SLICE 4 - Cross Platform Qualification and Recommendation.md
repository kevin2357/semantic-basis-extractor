# Slice 4 — Cross-Platform Qualification and Recommendation

Status: complete; awaiting final Kevin/API review and separate release authorization

## Recommendation

Recommend the joined initial-wave authority-input contract for a fresh immutable
`0.4.8` release. The qualification wheel still identifies itself as `0.4.7`,
which is already immutable; it is evidence for the post-0.4.7 source boundary and
must not replace or alter the published 0.4.7 artifact.

## Reproducible candidate

Two independent builds from source commit
`34de4798be76482dbb9f39a9fd59561bea9f81fe` used fixed epoch `1787090323` and
were byte-identical:

| Property | Value |
|---|---|
| Wheel | `astrowoof_natal_authoring-0.4.7-py3-none-any.whl` |
| Bytes | 828,375 |
| SHA-256 | `f15d0afc9fd4eaac6c0a48c78af4c0787fef696ecc55a158be5778047e633b1e` |
| Entries / packaged resources | 118 / 71 |
| `py.typed` | present |
| Tests / bytecode in wheel | 0 / 0 |

The strict binding-bundle and joined authority-input schemas plus exact/bounded
fixtures are present in the wheel. The pinned SPC 0.11.0 dependency remains
SHA-256 `82290df44fe5697e87df2e27eb0aa4bab3b7954c66ce988efda0962964e1366d`.

## Test gates

- Full source suite: 469 tests in 338.064 seconds; 449 passed and 20 expected
  environment-dependent tests skipped.
- Strict Linux contract/bundle/round-trip suite: 36 passed without skips.
- Windows CPython 3.12.13: `pip check`, lifecycle smoke, release smoke, and
  installed exact/bounded joined-reader/CLI qualification passed.
- Network-isolated Linux CPython 3.11.15: the same installed gates passed.
- The API-shaped round trip sources every complete binding from the public bundle;
  mismatch cases invoke zero provider creates.
- Provider operations: 0. Spend: USD 0.

## Compatibility and residual limits

- This additive patch introduces no lifecycle states, transition-oracle changes,
  editorial changes, or provider-transport changes.
- Batch authority cardinality and behavior remain unchanged.
- API still owns atomic reservation of the exact six-member wave, ordinary
  authorization documents, cross-run policy, and billing authority.
- Legacy workspaces without the bundle fail closed at this public operation.
- The provider acceptance/local identity-persistence atomicity gap is unchanged;
  identity-less interrupted submission remains ambiguous and fail-closed.

Machine-readable evidence is in
[`slice4-qualification.json`](slice4-qualification.json).

## Release gate

The sprint exit criteria are satisfied. Version bump, exact-source 0.4.8 rebuild,
release-record lock, annotated tag, GitHub publication, and authenticated asset
verification require explicit authorization after final Kevin/API review.
