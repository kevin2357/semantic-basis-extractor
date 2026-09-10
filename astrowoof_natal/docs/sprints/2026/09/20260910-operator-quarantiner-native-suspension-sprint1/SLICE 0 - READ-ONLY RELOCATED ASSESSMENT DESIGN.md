# Slice 0 — Read-only relocated assessment design

## Decision

Add a dedicated read-only relocated-assessment surface. Do not weaken `validate_workspace_snapshot()`, add `ignore_path`, or change the meaning of `astrowoof.operator_disposition_assessment.v1`.

The new surface should return an additive wrapper:

```text
astrowoof.relocated_operator_disposition_assessment.v1
  relocation authority and evidence
  + unchanged astrowoof.operator_disposition_assessment.v1
```

This preserves v1 custody/posture semantics and makes the changed evidence-view provenance explicit to every consumer.

## Why a wrapper instead of assessment v2

The native custody classification does not change merely because exact checkpoint bytes are read elsewhere. Reissuing the entire assessment as v2 would duplicate a mature closed contract and encourage two classification implementations.

The wrapper instead binds:

- one validated relocation authority;
- one exact relocated evidence view; and
- one otherwise ordinary v1 assessment document.

The nested v1 document remains independently valid. Consumers that do not understand the wrapper cannot accidentally treat a relocated directory as executable authority.

## Relocation authority

Proposed schema: `astrowoof.operator_disposition_relocation_authority.v1`.

Required closed fields:

| Field | Owner | Meaning |
| --- | --- | --- |
| `schema_version` | contract | exact authority version |
| `operation` | contract | fixed to `read_operator_disposition_assessment` |
| `request_id` | API | durable operator request identity |
| `api_run_id` | API | caller run identity |
| `job_id` | API | exact checkpoint-owning execution job |
| `native_run_id` | joined | expected native run identity |
| `checkpoint_id` | API | exact active checkpoint row |
| `checkpoint_generation` | API/archive | exact positive generation |
| `checkpoint_contract` | API/archive | fixed supported SBE checkpoint contract |
| `compatibility_identity` | API/archive | exact installed-worker compatibility identity |
| `archive_sha256` | API/archive | exact downloaded and verified archive bytes |
| `inventory_sha256` | API/archive | exact canonical archive member inventory |
| `original_logical_root_sha256` | API/native join | digest of recorded logical restore path |
| `restored_root_sha256` | API/SBE join | digest of the actual isolated assessment root |
| `issued_at` | API | timezone-aware authority creation time |
| `expires_at` | API | bounded assessment window |
| `provider_io_permitted` | contract | must be `false` |
| `workspace_mutation_permitted` | contract | must be `false` |
| `authority_sha256` | canonical document | digest over all preceding fields |

UUID syntax should be required for API request/run/job/checkpoint identities. Native run and compatibility identities retain their existing bounded opaque syntax. Digests are lowercase canonical SHA-256.

The authority is not a cryptographic delegation token. It is an exact typed handoff inside the installed API/SBE trust boundary. Its value is closed identity binding, replay diagnosis, and prevention of ambient “this directory looks copied” permission.

### Canonical digest and time rules

- Root digests use the existing canonical normalized logical-root string representation, never raw OS-dependent spelling. Supplied and observed roots are canonicalized before comparison and hashing.
- `issued_at`, `expires_at`, and `assessed_at` are canonical UTC RFC 3339 instants. Timezone-naive or non-UTC values are rejected.
- SBE validates `issued_at <= assessed_at <= expires_at` before the fenced read and validates freshness again after it.
- `authority_sha256` covers canonical JSON for every authority field except itself: sorted keys, UTF-8, no insignificant whitespace, and no NaN/Infinity.
- API creates `request_id` once. The same request ID may replay only the same canonical authority digest; changed authority or checkpoint generation requires a new request ID.

## API proof and SBE proof remain distinct

### API proves before invocation

- checkpoint row belongs to the exact run/job;
- checkpoint is the selected active checkpoint;
- generation, contract, compatibility identity, logical restore path, payload SHA, and inventory SHA are present and exact;
- downloaded archive receipt and bytes match persisted SHA/size;
- archive extraction validated its manifest, members, sizes, and digests;
- target directory is the exact fresh request-owned location; and
- authority timestamps and digest are canonical.

### SBE proves during invocation

- authority shape, digest, operation, expiry, and negative capabilities are valid;
- actual root digest equals `restored_root_sha256`;
- `run.json` native run equals `native_run_id`;
- state and snapshot both declare the same original logical root;
- that logical-root digest equals `original_logical_root_sha256`;
- snapshot schema, exact member inventory, and every member digest validate against the relocated bytes;
- the workspace remains byte-identical throughout the fenced read;
- lifecycle, terminal evidence, custody class, posture, and next actions satisfy existing v1 rules; and
- no native member is created, modified, or deleted.

SBE cannot derive the original ZIP byte identity from extracted files and must not pretend to do so. `archive_sha256`, checkpoint row identity, and archive inventory identity remain explicitly caller-proven evidence carried into the wrapper.

## Read-only validation primitive

Do not modify the ordinary executable validator. Introduce a separate internal primitive conceptually equivalent to:

```python
validate_relocated_workspace_snapshot(
    actual_root,
    state,
    expected_original_root_sha256=...,
    expected_actual_root_sha256=...,
)
```

It should share snapshot inventory/digest machinery with `validate_workspace_snapshot()` but replace only the physical-path equality assertion with the two exact digest joins. All other snapshot checks remain equal or stricter.

The ordinary validator continues requiring:

```text
actual root == workspace_contract.logical_root == snapshot.logical_root
```

The relocated validator requires:

```text
state logical root == snapshot logical root
sha256(state logical root) == authority original-root digest
sha256(actual root) == authority restored-root digest
actual root != state logical root
```

Requiring inequality prevents accidental use of relocation authority as an alternate ordinary-reader mode.

## Public reader shape

Prefer a separate root-level public function:

```python
read_relocated_operator_disposition_assessment(
    run_dir,
    relocation_authority,
    *,
    terminal_result_id=None,
    assessed_at,
)
```

The ordinary `read_operator_disposition_assessment()` signature and behavior remain unchanged.

`assessed_at` is required caller-supplied canonical UTC time. API freezes it for deterministic qualification and supplies the immediate live assessment time in operation. It participates in the wrapper digest and cannot be silently rebound on replay.

`terminal_result_id` remains an optional exact selector only when already bound by the API request and relocation authority. It never enables latest-result or availability discovery. Without an exact selector, nested v1 may classify only from immutable evidence already permitted by ordinary v1 semantics; otherwise the relocated reader refuses.

The relocated reader may share private classification helpers, but its control flow must never call a mutating command or create the ordinary writer lock. If existing lifecycle inspection requires a writer-fence posture, the relocated mode must explicitly report assessment-only exclusive access based on the already isolated immutable copy; it must not claim ownership of the authoritative writer fence.

## Wrapper result

Proposed top-level fields:

- `schema_version`;
- `authority_sha256`;
- `request_id`;
- `native_run_id`;
- `checkpoint_id`;
- `checkpoint_generation`;
- `archive_sha256`;
- `inventory_sha256`;
- `original_logical_root_sha256`;
- `restored_root_sha256`;
- `assessment_mode` fixed to `relocated_read_only_checkpoint`;
- `assessed_at`;
- `provider_io_performed` fixed to `false`;
- `workspace_mutation_performed` fixed to `false`;
- `assessment` containing exact v1; and
- `wrapper_sha256`.

The nested assessment's native custody class and quarantine posture remain the only SBE classification authority. Wrapper metadata does not upgrade or override them.

`wrapper_sha256` covers canonical JSON for every wrapper field except itself, including `assessed_at` and the complete nested v1 assessment, using the same canonicalization rules as the authority digest.

## Freshness and replay

- Authority must be unexpired when assessment begins and ends.
- Duplicate byte-identical authority against unchanged bytes returns a byte-identical semantic result when `assessed_at` is caller-supplied/frozen for qualification.
- Same `request_id` with a changed authority digest is contradictory and must be refused by API admission; SBE validates each supplied document but does not own the durable replay registry.
- Any changed checkpoint, archive, inventory, native run, original root, or restored root requires a fresh authority.
- A successful relocated assessment is evidence for the exact checkpoint only. It says nothing about a later authoritative workspace generation.
- A valid nested v1 `prohibited` or `unsupported_or_inconsistent` posture is still a successfully produced assessment wrapper. Malformed, contradictory, expired, or unproven relocation evidence is a reader refusal. API must preserve that distinction in operator diagnostics.

## Capability fence

Relocation authority is accepted only by the dedicated relocated assessment reader. It is not an accepted argument to any executable or mutating public command.

Provider-free qualification must prove the relocated root is rejected by:

- semantic closure/resume;
- provider reconciliation and dispatch;
- local-work consumption;
- native transition/result publication;
- operator retirement;
- cooperative suspension; and
- checkpoint publication.

No result/receipt is published into the relocated workspace. The wrapper is returned to API for durable storage with the operator request.

## Failure matrix

| Case | Required result |
| --- | --- |
| authority absent or malformed | refuse before classification |
| authority digest mismatch | refuse |
| wrong/expired operation window | refuse |
| actual root digest mismatch | refuse |
| actual root equals authoritative logical root | use ordinary reader; relocated reader refuses |
| state/snapshot logical roots disagree | refuse |
| original-root digest mismatch | refuse |
| native run mismatch | refuse |
| unsupported checkpoint or compatibility contract | refuse |
| archive/checkpoint claims malformed | refuse |
| member missing, added, or changed | refuse |
| bytes change during assessment | refuse |
| unsupported lifecycle evidence | valid v1 prohibited/unsupported assessment only where existing semantics allow; otherwise refuse |
| observer/logging failure | assessment behavior unchanged |

No failure may fall back to ordinary path discovery, latest checkpoint/result discovery, or inferred identity.

## Privacy and observability

Use the existing safe `workspace_fingerprint` methodology. Add relocation mode and authority/wrapper digests to bounded assessment logs if the active logging sprint's contract supports them.

Never log either raw path, archive/storage coordinates, full authority, full assessment, workspace members, subject content, or exception prose containing paths.

## Cross-package qualification gate

The release pair must include one real integration path:

1. API constructs a genuine SBE workspace through supported writers.
2. API creates and verifies its real checkpoint archive.
3. API persists/represents the exact checkpoint row evidence.
4. API restores through `restore_checkpoint_archive()` into its real request-specific target shape.
5. API builds the relocation authority from the exact restore result and checkpoint evidence.
6. The installed SBE wheel reads the relocated assessment.
7. API validates the wrapper and nested v1 assessment.
8. A dry-run admission accepts a permitted fixture without applying quarantine.
9. Before/after inventories prove zero workspace mutation; provider/network/spend counters remain zero.

The existing fake-restore/fake-reader tests remain useful unit tests but cannot satisfy this gate.

## Ownership ruling

- API owns checkpoint/archive receipt truth, request identity, restore isolation, freshness, replay registry, and later quarantine mutation.
- SBE owns relocated snapshot validation, native evidence interpretation, custody classification, and truthful refusal.
- The wrapper records both evidence classes without collapsing them.

## Slice 0 conclusion

The design is implementable as an additive assessment-only capability. It preserves the stable absolute-path contract for every executable workspace and introduces no SBE mutation authority.

Pause for API and owner review before freezing JSON schemas or implementing the reader.
