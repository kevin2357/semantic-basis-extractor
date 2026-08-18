# API Agent Slice 4 Review and Response

## Decision

The separate immutable publication receipt is accepted. It correctly resolves the
result/snapshot content-hash cycle while retaining the exact historical snapshot
manifest and checkpoint-basis document needed to validate a specified prior result.
The narrow `native-publication-receipts/` exclusion is appropriate; no broader
inventory exception is acceptable.

The normal result, complete snapshot, then receipt ordering is correct. The
provider/native outcome coverage and route-neutral finalizer are also approved.

## Required publication hardening

Immediately after each `write_workspace_snapshot(run_dir)` and before calculating
the snapshot SHA-256 or calling `_publish_receipt`, call:

```python
validate_workspace_snapshot(run_dir, state)
```

This applies to both:

1. the ordinary publication path; and
2. the one-orphan repair path.

`write_workspace_snapshot` constructs a manifest but does not itself validate that
the manifest agrees with all workspace members. The immutable receipt must only seal
a complete snapshot that has passed the existing full workspace validation. The
reader's later validation of the *current* live snapshot is not a substitute for
establishing that fact at the time the historical receipt is published.

Please add a focused regression test covering a malformed/incomplete snapshot write
that is refused before a receipt is created. Existing receipt-tampering and orphan
recovery coverage remains valuable and should stay unchanged.

## API handoff condition

After that correction, API Slice 3 can consume result + bounded journal range +
publication receipt as its strict ingestion input. The API will retain the external
receipt identity and canonical content alongside its own PostgreSQL receipt; it will
not infer snapshot authority from a mutable latest index.

No API runtime, database, provider, R2, or paid action is authorized by this review.
