# Slice 1 — Relocation authority and wrapper contracts

## Result

Implemented the additive contract layer without changing ordinary workspace validation or assessment behavior.

## Public surfaces

- `build_relocation_authority()` / `validate_relocation_authority()`
- `build_relocated_assessment()` / `validate_relocated_assessment()`
- `canonical_root_sha256()`
- packaged authority and wrapper schema readers
- root-package exports for each surface

## Frozen behavior

- Authority and wrapper roots are closed exact-key documents.
- API request/run/job/checkpoint identities require canonical UUID strings.
- Native and compatibility identities use bounded opaque syntax.
- All digests require lowercase canonical SHA-256.
- Authority times and `assessed_at` require second-precision UTC `Z` RFC 3339.
- Authority windows require `issued_at < expires_at`.
- Wrapper construction requires `issued_at <= assessed_at <= expires_at`.
- Provider I/O and workspace mutation capabilities/assertions must be exactly false.
- Authority and wrapper digests cover all fields except their own digest using sorted compact UTF-8 JSON.
- The nested assessment must independently validate as disposition assessment v1 and match wrapper native identity.
- Repeating construction from frozen inputs is deterministic.

## Packaged schemas

- `operator-disposition-relocation-authority.v1.schema.json`
- `relocated-operator-disposition-assessment.v1.schema.json`

## Qualification

Focused authority/wrapper, root-export, suite-manifest, and ordinary assessment reader tests passed: 28 tests.

Covered failures include changed authority under stale digest, out-of-window assessment, positive mutation/provider capability, non-UTC time, and mismatched nested native identity.

### API review correction

`canonical_logical_root()` now performs platform-independent lexical normalization without filesystem access:

- POSIX roots are tagged and remain case-sensitive;
- Windows drive roots normalize separators, drive case, and path case;
- duplicate separators, `.` segments, and bounded `..` segments normalize deterministically;
- relative paths, UNC ambiguity, root escape, whitespace, and control characters are refused; and
- `canonical_root_sha256()` hashes only that canonical tagged representation.

Equivalent Windows spellings now produce one identity while meaningful POSIX case differences remain distinct.

`validate_relocated_assessment_pair()` was also added for API's durable intake. It revalidates both documents together, joins every shared authority/checkpoint/root field, and re-establishes the assessment-time freshness relationship.

## Unchanged boundary

No relocated reader exists yet. No native workspace is accepted at a relocated path by this slice. Ordinary assessment and every executable/mutating command retain their existing stable absolute-path requirement.

The next implementation slice may refactor private assessment machinery only after these public contracts are reviewed.
