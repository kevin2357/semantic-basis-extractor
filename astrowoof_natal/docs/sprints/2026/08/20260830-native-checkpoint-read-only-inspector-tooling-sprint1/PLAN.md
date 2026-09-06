# Plan — native checkpoint read-only inspector tooling

## Goal

Build and package a provider-free, local-only checkpoint inspector that turns a
supplied immutable archive into strict validation evidence and sanitized native
state/provenance projections without invoking any execution or recovery path.

## Status

Closed without implementation. This proposal is superseded by the structured
worker logging and decision-evidence observability delivered in later sprints.
If retained-workspace inspection again becomes a recurring need, start a fresh
tooling sprint from the then-current contracts and operational requirements.

## Non-goals

- R2/S3 access, object discovery, credential handling, or signed URLs.
- API database access or API job/action mutation.
- Native resume, reconciliation, repair, replay, denial, retirement, closeout,
  publication, or provider submission/retrieval.
- Declaring API capacity, lease, reservation, settlement, delivery, or product
  disposition.
- Emitting prompts, generated content, private payloads, authorization
  documents, or subject details.
- Automatically recovering or choosing a canonical retained run.

## Proposed public surfaces

### Python

- `verify_checkpoint_archive(...) -> CheckpointArchiveVerification`
- `inspect_restored_checkpoint(...) -> NativeCheckpointInspection`
- `inspect_checkpoint_archive(...) -> NativeCheckpointInspectionBundle`
- strict readers/validators for the verification receipt and inspection bundle.

### CLI

```text
astrowoof-checkpoint-inspect \
  --archive checkpoint.zip \
  --expected-archive-sha256 ... \
  --expected-inventory-sha256 ... \
  --output inspection.json
```

Optional controlled restoration:

```text
  --retain-restored-at EMPTY_DIRECTORY
```

Default behavior uses a managed temporary directory and removes it after the
inspection bundle is sealed. The CLI accepts no remote endpoint, credentials,
provider configuration, spend authority, or native execution options.

## Slice 0 — characterize existing validators and freeze the boundary

Inventory and compare:

- API checkpoint archive creation/restoration and bounds;
- SBE snapshot, journal, result, receipt, and checkpoint-basis validators;
- current public lifecycle/action/retry-lineage projections;
- incident-specific readers from Marmalade, Diffie/Hellman, Moxie, and similar
  retained investigations; and
- installed package constraints and optional dependencies.

Freeze decisions for:

- ZIP/archive compatibility and limits;
- logical workspace-root handling after local relocation;
- which validations can reuse current public functions without accidentally
  acquiring a writer or modifying bytes;
- whether the archive verifier lives in SBE, a shared package, or imports a
  narrowly extracted compatibility module;
- output privacy classification and bounded field vocabulary; and
- progress reporting for large archives without making logs authoritative.

Deliverables:

- validator reuse/gap matrix;
- threat and privacy model;
- proposed closed schemas with example sanitized documents;
- explicit proof that no execution/provider entrypoint is reachable.

Gate — Voof-paws 1: API reviews the input/output and ownership boundary before
schema implementation.

## Slice 1 — closed archive-verification contract

Define a versioned verification receipt containing only:

- archive SHA-256/byte count;
- manifest schema, checkpoint contract, compatibility identity, generation, and
  predecessor archive identity;
- inventory SHA-256, member count, and expanded byte count;
- applied path/type/count/size limits;
- boolean/closed validation outcomes;
- optional caller-supplied coordinate/reference digest; and
- inspector version and receipt digest.

The verifier must reject:

- absolute, parent-traversing, noncanonical, duplicate, or overlong paths;
- symlink, hardlink, device, directory, or other non-regular members;
- extra/missing members;
- malformed manifests or unsupported contracts/compatibility identities;
- member, inventory, size, archive, or predecessor identity mismatch;
- archive/member count or expansion-limit violations; and
- nonempty or unsafe retained extraction targets.

Add pure-Python strict validation independent of optional `jsonschema`, with
schema parity tests when `jsonschema` is present.

Gate — Voof-paws 2: freeze verification schema and compatibility behavior.

## Slice 2 — read-only native inspection contract

Define a closed inspection bundle with sections for:

- native run/revision/status/route/service-level identity;
- workspace snapshot identity and validation status;
- action inventory in native ledger order, using only public binding digests,
  stage, route, state, provider identity, evidence-presence flags, and custody;
- retry/pass lineage using stable attempt/action identities and sanitized state;
- lifecycle inspection/result index summaries;
- immutable result → receipt → snapshot → checkpoint-basis → journal joins;
- unresolved contradictions and unavailable evidence, using a closed vocabulary;
- optional API join results when a separate strict public action document is
  supplied; and
- privacy/operation counters proving zero provider and native mutation activity.

The bundle must distinguish:

- invalid evidence;
- unsupported evidence version;
- valid but incomplete historical evidence;
- internally contradictory native evidence; and
- external join mismatch.

For authority-handoff investigations, the bundle must additionally preserve the
distinction between request object identity and observation identity. It should
project request/inspection/checkpoint joins and native v2 intent membership
without emitting complete authorization documents or private request payloads.

It must not translate those into API queue/resource dispositions.

Gate — Voof-paws 3: API reviews the projection and contradiction vocabulary.

## Slice 3 — archive verification and contained restoration

Implement the verifier with bounded progress callbacks/events. Validate the
entire archive before making the restored directory visible. Use a temporary
sibling directory and publish the local extraction only after:

1. manifest validation;
2. exact declared-member-set validation;
3. per-member size/hash validation; and
4. total count/size validation.

On failure, remove only the inspector-owned temporary directory. Never overwrite
a nonempty caller path. The default managed-temporary mode cleans up after
inspection; retained mode records the selected local path but does not treat it
as the native logical root.

Tests cover malformed paths/types, duplicate entries, zip bombs/bounds, changed
bytes, interruption, cleanup isolation, and deterministic receipts.

## Slice 4 — native metadata and provenance inspection

Implement the inspection using read-only validation functions. Validate all
named results/receipts and bounded journal ranges. Preserve original logical
root identity while explicitly recording the local relocation as non-authority.

Add route/version matrices for:

- exact and bounded interactive;
- exact and bounded Batch where checkpoint contracts are compatible;
- lifecycle v0.5–v0.8;
- native result v0.1/v0.2 and current receipt compatibility;
- provider-pending, awaiting-authority, local-work, review, terminal, ambiguity,
  providerless denial, and mixed-custody workspaces; and
- historical unsupported versions, which fail closed or report a typed
  unsupported result without guessing.

Tests prove that protected payload sentinels never enter output, logs, exception
messages, or packaged fixtures.

Gate — Voof-paws 4: runtime/security review before CLI packaging.

## Slice 5 — installed CLI and qualification fixtures

Package:

- schemas, readers, and validators;
- the CLI entry point;
- small sanitized checkpoint archives spanning core state/custody cases; and
- a provider-free installed-wheel qualification command/receipt.

Qualification must prove:

- identical input produces byte-identical inspection bundles;
- temporary workspaces are cleaned;
- retained extraction refuses nonempty targets;
- no network/provider/credential code is reachable;
- no native state file changes;
- malformed archives and contradictory results fail closed;
- privacy sentinels never escape; and
- Moxie-shaped eight-native/seven-external inventory mismatch is detected when
  a public external join document is supplied.

Gate — Voof-paws 5: API consumer review of installed artifacts.

## Slice 6 — documentation and release decision

Document:

- operator workflow from authorized download to local inspection;
- authoritative versus diagnostic fields;
- safe attachment rules for incident reports;
- cleanup/retention expectations;
- examples of incomplete versus contradictory evidence; and
- explicit prohibition on treating inspection as recovery authority.

Run a risk-proportionate suite determined after implementation scope is known.
Freeze the new version before release testing, build reproducibly, run installed
qualification, and obtain separate owner approval before commit/tag/publication.

## Acceptance criteria

- A local checkpoint archive can be strictly verified and inspected with one
  supported installed command.
- Remote access and credentials are absent from the tool.
- Archive safety and every declared member identity are validated.
- Original native logical identity is preserved across local relocation.
- Native ledger, lifecycle, retry lineage, results, receipts, snapshots,
  checkpoint bases, and journal ranges are joined without native mutation.
- Outputs are closed, deterministic, bounded, sanitized, and independently
  validatable.
- Unknown/contradictory evidence never becomes a guessed scheduling decision.
- The inspector performs zero provider work and exposes no recovery operation.

## Review pauses

- Before schema work: public boundary and ownership.
- Before runtime: verification and inspection schemas.
- Before packaging: runtime/security/privacy review.
- Before release: installed consumer qualification and explicit owner approval.
