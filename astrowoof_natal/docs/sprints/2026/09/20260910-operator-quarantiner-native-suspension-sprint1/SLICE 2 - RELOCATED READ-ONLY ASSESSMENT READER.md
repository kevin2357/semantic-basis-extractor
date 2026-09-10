# Slice 2 — Relocated read-only assessment reader

Status: approved for API-host integration; release-gate coverage addition
incorporated.

## Outcome

SBE now has a dedicated relocated-checkpoint reader. It reuses the native
operator-disposition classifier without weakening the ordinary authoritative
workspace reader.

The new public entry point is
`read_relocated_operator_disposition_assessment(run_dir, authority=...,
assessed_at=...)`.

## Native fence

- The ordinary reader still requires the workspace at its original logical
  absolute path and takes the pre-existing native writer lock when available.
- The relocated reader does not acquire or create that lock. It accepts only an
  API-isolated immutable checkpoint copy under relocation authority.
- Provider I/O and availability discovery remain disabled.
- The authority now carries a required nullable `terminal_result_id`. `null`
  means no terminal-result read; a value permits only that exact result ID.

## Proofs performed before and after classification

- authority shape, digest, capability bits, and UTC window;
- exact native run identity;
- actual restored-root canonical digest;
- preserved original logical-root canonical digest;
- actual and original roots are distinct;
- snapshot schema and preserved logical root;
- exact member paths, byte sizes, and SHA-256 inventory.

The returned v1 relocated wrapper binds the unchanged native assessment to the
request, checkpoint, archive, inventories, both root identities, assessment
time, and authority digest. It declares zero provider I/O and zero workspace
mutation.

## Internal reuse boundary

Lifecycle inspection and retry-lineage inspection gained an internal optional
workspace-validator injection. Their public default remains the original exact
workspace validator. The operator classifier likewise has a private reusable
reader; the existing public reader is an unchanged-behavior wrapper around it.

## Focused qualification

- relocation contract, relocated reader, ordinary reader, and suite-manifest
  tests: 33 passed;
- lifecycle, retry-lineage runtime, and external-authority regression tests:
  22 passed;
- `git diff --check`: passed.

Coverage includes successful nonmutating relocated assessment, ordinary-reader
rejection at a relocated path, wrong restored-root identity, changed copied
bytes, expired assessment time, and attempted same-root authority.

Following API review, relocation-specific terminal-result coverage proves that
a signed non-null selector returns only its exact native result and that wrong
or missing result IDs fail closed without availability or latest-result
discovery.

## Next gate

API review should confirm the authority addition and reader semantics before the
paired API host-initialization/capture implementation and installed-wheel gate.
