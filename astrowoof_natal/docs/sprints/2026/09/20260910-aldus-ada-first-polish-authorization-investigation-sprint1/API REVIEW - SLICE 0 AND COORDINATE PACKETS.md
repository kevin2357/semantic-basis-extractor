# API Review — Slice 0 and Coordinate Packets

## Review

Approved: Slice 0 correctly treats the shared first-polish boundary as a
cross-source question, rather than inferring ownership from trace vocabulary.
The separation is particularly important here:

- Ada's provider-reconciliation v0.1 publication is API-persisted and proves
  only an `awaiting_external_authority` result/cause, not a consumable request;
- Aldus's v0.2 ordinary-authoring/terminal-review publication was rejected by
  API before `sbe_native_execution_receipts` persistence, so it cannot be
  described as a sealed API receipt.

The two coordinates are published beside this review:

- `ada-generation-6-checkpoint-coordinate.v1.json`
- `aldus-generation-11-checkpoint-coordinate.v1.json`

They are derived from API-owned checkpoint and receipt metadata only. Where a
logical-root digest is not durable at that boundary, the packet explicitly
records `null` plus its reason rather than fabricating a value.

Their SHA-256 values are recorded in `checkpoint-coordinate-packets.sha256`.

## Access decision

The packets themselves grant **no** R2 access. If Kevin separately approves
the proposed Slice 1 boundary, SBE may perform exactly one conditional `HEAD`
and one bounded conditional `GET` against each named object, pinned to the
included version/ETag and archive digest. The allowed extraction remains
limited to the archive safety/inventory metadata and the named final-QA,
first-polish, result/receipt, request/refusal, and binding evidence necessary
to answer Slice 0's questions.

No listing, alternate discovery, provider operation, resume, recovery,
reconciliation, or workspace mutation is authorized.
