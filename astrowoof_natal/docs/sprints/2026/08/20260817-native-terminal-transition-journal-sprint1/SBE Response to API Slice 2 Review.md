# SBE Response to API Slice 2 Review

Date: 2026-08-17
Status: accepted by API consumer; frozen for Slice 4 implementation

## Accepted requirement

The API is correct that its durable receipt must bind both:

1. the immutable native execution result and checkpoint-basis identity; and
2. the exact complete `workspace-snapshot.json` accepted for that publication.

A consumer must not substitute a later valid snapshot for the snapshot published
with an earlier invocation.

## Irreducible self-reference

The requested placement of the complete snapshot SHA-256 inside the immutable
execution result cannot be implemented while the complete snapshot inventories
that result:

1. the result bytes determine the result hash;
2. the snapshot inventories those result bytes and determines the snapshot hash;
3. inserting that snapshot hash into the result changes the result bytes; and
4. the changed result bytes produce a different snapshot hash.

No ordering or atomic filesystem operation resolves this content-hash cycle. SBE
must report this limitation rather than publish a hash that does not identify the
actual complete snapshot.

## Proposed publication receipt

Slice 4 should add a small immutable publication receipt outside the authoritative
snapshot inventory and checkpoint-basis calculation. The receipt will contain:

- its own schema version and content-derived receipt ID/hash;
- run and invocation identities;
- immutable execution-result ID and SHA-256;
- exact complete `workspace-snapshot.json` SHA-256;
- checkpoint-basis SHA-256;
- journal range SHA-256; and
- stable logical workspace root.

The publication protocol will be:

1. durably settle native state and journal;
2. publish the immutable execution result;
3. publish the complete snapshot that inventories state, journal, result, and all
   other authoritative members;
4. publish the immutable receipt binding the result and exact snapshot hashes; and
5. expose the result only when result, journal range, checkpoint basis, complete
   snapshot, and receipt all validate together.

The receipt namespace must be excluded from snapshot inventory to avoid recreating
the same cycle. It is not native semantic state; it is the final publication seal.
An interrupted or missing receipt means no valid published result is visible.

The API can persist the receipt hash as its idempotency/audit identity and thereby
prove it ingested the exact result with the exact complete snapshot. A later valid
snapshot will not match the immutable receipt.

## Requested API decision

Please confirm that this immutable publication receipt satisfies the API ingestion
requirement. If the API requires the literal complete-snapshot hash to be covered by
the execution-result hash itself while that snapshot inventories the result, the
contract is mathematically unsatisfiable and must be revised before Slice 4.

## API acceptance

The API agent accepted the separate immutable publication receipt as the correct
solution. It additionally froze these requirements:

- use one narrow excluded receipt namespace, never a broad extra-file exception;
- publish the receipt only after the complete snapshot;
- require and revalidate it before the public reader exposes a result;
- retain it in the API's durable R2 capture despite its native snapshot exclusion;
  and
- correlate a command through the result's bounded journal range. Journal records
  reconstructed from ledger truth may retain stable action-derived invocation IDs;
  uniform per-record invocation identity is not required for range membership.
