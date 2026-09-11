# Slice 3 — Relocation capability fence

Status: API reviewed and approved; implementation complete.

## Outcome

The relocation authority remains exclusive to
`read_relocated_operator_disposition_assessment()`. It is not accepted by any
resume, reconciliation, local-work, publication, retirement, or snapshot-write
surface. A relocated assessment copy therefore remains evidence for a bounded
read and cannot become an executable workspace merely because its bytes and
authority are valid.

## Executable and mutation matrix

The provider-free regression constructs a valid authoritative workspace,
writes its snapshot, copies it byte-for-byte to a distinct physical root, and
then proves the following against the relocated copy:

| Surface | Required result |
| --- | --- |
| semantic-closure resume | stable logical-root refusal; no byte change |
| provider reconciliation | stable logical-root refusal before provider I/O; no byte change |
| local-work commit | stable logical-root refusal; no byte change |
| native result/receipt publication | stable logical-root refusal before journal, snapshot, result, or receipt writes |
| retirement-request construction | not retirement-eligible; no byte change |
| relocation authority reuse | unsupported by every executable or mutating signature |

The public package also continues not to export the internal snapshot writer or
nonexistent checkpoint-publication/native-suspension capabilities.

## Publication correction exposed by the matrix

Native result publication previously performed full workspace validation only
after refreshing the snapshot. That sequence is necessary for legitimate
authoritative publication because native state may have changed immediately
before publication, but it also meant a relocated copy could reach pre-snapshot
writes before the logical-root mismatch was detected.

The publication entrypoint now checks the durable
`stable_logical_absolute_path` root invariant immediately after reading native
state and before any write. It deliberately does not perform the full member
digest check there; full validation remains after publication refreshes the
snapshot. This preserves ordinary publication semantics while making the
relocated-path refusal pre-mutational.

## Qualification

- Slice 3 capability-fence module: 3 passed.
- Suite-manifest, native-transition, and operator-retirement regressions:
  64 passed, 2 skipped.
- The new Slice 3 module is registered in `test_suite_manifest.json`.
- Provider calls made by the capability matrix: zero.

## Next gate

API approved the assessment-only boundary, the byte-preservation matrix, and
the publication pre-write stable-root correction. That approval does not grant
native suspension, forced termination, provider reconciliation, resume,
retirement, or any other mutation authority to a relocated copy. See
`API REVIEW - SLICE 3 RELOCATION CAPABILITY FENCE.md`.

Pre-release qualification may now begin when authorized. After publication,
the final cross-package gate must use the released installed wheel with API's
real isolated checkpoint restore shape and `force=False` in-process logging.
It must prove the relocated reader is available, produces the closed wrapper,
and that API's writer accepts only the exact bound result. No pre-release work
was started while recording this approval.
