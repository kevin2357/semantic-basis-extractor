# Slice 0 — Evidence map and read-only inspection protocol

## Status

Protocol frozen in principle; exact QA checkpoint coordinates and process-local R2
credentials are still required before access. This document authorizes no discovery
listing and no mutation.

## Exact target

The sole initial target is the active/frozen checkpoint belonging to API run
`f84b3524-659a-4b86-83b4-7deb5b7c59a6` and native run
`42407f1f4386eb0fcd387de9feb305a932d6626949dea247750f785bd1851920`.

The R2 object key must be derived from the authoritative QA checkpoint row as
`v1/checkpoint/<storage_object_uuid_hex>`. It must never be guessed from run or job
identity. Scone Ranger is not included in the initial access set.

## Required frozen coordinate packet

Before HEAD or GET, the API evidence must provide:

- checkpoint ID, job ID, attempt ID, and lease/fencing identity;
- generation/sequence and predecessor checkpoint ID;
- checkpoint contract and compatibility identity;
- storage environment, namespace, and object UUID/key;
- archive SHA-256, byte size, media type, protection class, and inventory SHA-256;
- storage creation time and provider version/ETag where available;
- logical restore path and native lifecycle status;
- source query/receipt identity and hash.

## Allowed remote operations

1. One exact `HEAD` for the frozen key.
2. One exact streaming `GET` for that same key if HEAD metadata exactly matches the
   coordinate packet.
3. No `LIST`, prefix scan, neighboring-object access, write, copy, delete, or
   lifecycle/provider operation.

If the coordinate packet identifies multiple checkpoint objects as independently
necessary, each additional HEAD/GET must be recorded and reviewed before access;
the default bound remains one object.

## HEAD validation

Require exact agreement for:

- bucket/environment and object key;
- `aw-contract = astrowoof.storage-receipt.v1`;
- `aw-sha256`, `aw-size`, `aw-media-type`, and `aw-protection` metadata;
- response byte size and content type;
- provider version/ETag when frozen.

Any mismatch stops the inspection without GET.

## Download and archive validation

- Stream into a fresh OS temporary directory outside all repositories.
- Enforce the configured maximum object size and the frozen exact byte size.
- Compute SHA-256 while streaming and refuse mismatch.
- Parse the checkpoint archive through the API checkpoint-archive reader or an
  equivalently strict read-only parser.
- Reject absolute paths, traversal, duplicate members, links, device entries,
  undeclared authority members, excess member count, or decompression bounds.
- Validate archive contract, compatibility identity, generation, predecessor hash,
  logical restore path, and complete inventory digest.

## Minimum member access set

After archive/inventory validation, inspect only:

- `run.json` and public run state;
- workspace snapshot/inventory;
- spend/action ledger and authorization-request projection;
- native journal and journal index/range evidence;
- native result index, exact results, and publication receipts;
- lifecycle/temporal/local-work/retry-lineage public artifacts;
- the affected pass's attempt metadata, provider identity marker, reconciliation
  record, response digest/status metadata, QA result, and retry feedback;
- binding-owned request/payload digests without reading prompt/payload content.

Do not extract or report authored deck/card text, prompt text, provider response
content, subject details, credentials, or unrelated pass workspaces.

## Required joins

Every affected-action fact must join:

- API run and native run;
- action ID and complete binding/binding digest;
- route, stage, pass, attempt, and retry attempt key;
- grant/request/document identities;
- native state revision and snapshot/archive identity;
- provider identity and journal/result record;
- API paid-action/admission/dispatch/intake identity where available.

Counts, timestamps, and log proximity are diagnostic only.

## Sanitized outputs

- Exact remote-access receipt with key, HEAD metadata hashes, downloaded archive
  hash, accessed member paths/hashes, timestamps, and side-effect counters.
- Chronological action/checkpoint timeline containing identities, states, digests,
  and closed reason codes only.
- Causal report with source/evidence pointers and confidence per conclusion.

Protected content and credentials must never enter committed files, stdout capture,
typed events, or handoff fixtures.

## Cleanup

After sanitized artifacts and their hashes validate:

- remove the temporary extracted workspace/archive;
- remove process-local credential variables;
- retain only bounded hashes/identities and sanitized findings;
- record cleanup success or exact failure without attempting an unsafe workaround.

## Refusal conditions

Do not proceed when the exact checkpoint row is unavailable, HEAD disagrees with the
row, archive/snapshot validation fails, logical/native identity differs, credentials
are absent, or the requested conclusion would require protected content outside the
declared member set.
