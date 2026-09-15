# Slice 0 — Native Join Surface and Digest Domain

## Finding

Static source tracing isolates one review-only leading candidate before any
retained read. Terminal-review result v0.2 seals each action disposition's
`binding_sha256` over the closed projection returned by
`terminal_review_contracts._binding()`. Editorial runtime capture instead
recomputes the comparison digest over the complete ledger `binding` mapping.

The closed terminal projection contains:

- `action_id`;
- `stage`;
- `route`;
- `request_sha256`;
- `profile_sha256`;
- `maximum_output_tokens`;
- `commitment_micro_usd`; and
- `price_book_version`.

A real ledger binding also carries fields outside that projection, including
`service_level` and `prepared_state_revision`. Canonical hashing is therefore
deterministic in both places but over different objects.

## Finite contradiction matrix

| Candidate | Applies to both review witnesses | Bypassed by delivery control | Verification |
| --- | --- | --- | --- |
| top-level result/receipt/run mismatch | possible | no | exact pinned identities and public reader |
| state revision or checkpoint-basis mismatch | possible | no | archive state/result/receipt join |
| runtime release/profile/resource provenance | possible | no | archive state/result join |
| duplicate/missing ledger action | possible | no | ledger inventory |
| disposition action ID missing/duplicate | review-only | yes | v0.2 result inventory |
| closed-projection digest versus complete-binding digest | review-only | yes | three-way digest comparison per action |
| optional initial-deck digest | witness B only | no | retained deck and state digest |

The digest-domain candidate uniquely explains the observed route split without
requiring two independent witness defects: delivery capture does not enforce
terminal-review `action_dispositions`; both failed witnesses do.

## Existing test gap

The focused synthetic review test constructs a reduced fake binding and hashes
that same dictionary into a fake disposition. It proves mismatch rejection but
does not reproduce a real producer-generated v0.2 disposition paired with a
full ledger binding. Consequently it cannot expose disagreement between the
producer's projection and the capture consumer's recomputation.

## Gate A ruling

Proceed with the two authorized exact reads. For every referenced action,
calculate the sealed disposition digest, complete-binding digest, and producer
projection digest. Do not infer the live cause from source alone, and do not
alter runtime code before retained proof and provider-free reproduction.
