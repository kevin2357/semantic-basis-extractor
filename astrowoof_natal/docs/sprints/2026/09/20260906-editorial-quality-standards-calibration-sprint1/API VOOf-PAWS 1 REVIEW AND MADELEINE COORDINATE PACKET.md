# API Voof-paws 1 review and Madeleine coordinate packet

Status: approved for the exact bounded read below.  Prepared from read-only QA
PostgreSQL metadata on 2026-09-06.  No R2, provider, run, queue, or workspace
mutation occurred while preparing this packet.

## Review outcome

The four-run manifest is identity-consistent with authoritative API records.

- Doughmeat's generation 11 checkpoint ID, object UUID/key, ETag, archive bytes,
  archive SHA-256, and inventory SHA-256 all match the current API checkpoint
  record and the locally hash-verified archive recorded in the access ledger.
- Macaron's corresponding generation 11 fields likewise match authoritative API
  records and its locally hash-verified archive.
- Frisbee's corresponding generation 11 fields likewise match authoritative API
  records and its locally hash-verified archive.
- Madeleine is the only cohort member without a local archive.  The manifest's
  conclusion that it is the only member requiring a new retained-object read is
  therefore correct.

The three reused archives must not be downloaded again.  Their existing local
archive hashes are evidence for later replay, not an authorization to expand the
campaign.

## Exact Madeleine packet

| Field | Exact value |
| --- | --- |
| API run | `98d2819f-4807-4f13-9b73-9bc8e8d2e1f5` |
| native run | `064c17a411af2df9670372d1e6d1cf71880d2f1c0d5d92b0682e3da751696965` |
| checkpoint ID | `85fcca2a-f9e0-4bdc-837c-f764abb2416c` |
| job / attempt | `43048de5-ebe5-4b3f-bec8-5d1bc1e31835` / `aa86d602-2443-457b-997e-27963d606ea0` |
| sequence / generation | `9` / `9` |
| checkpoint contract | `astrowoof.sbe-workspace-checkpoint.v1` |
| storage receipt contract | `astrowoof.storage-receipt.v1` |
| storage environment / namespace | `qa` / `checkpoint` |
| storage object UUID | `3a43e623-d580-435c-b452-916896964d6d` |
| exact R2 object key | `v1/checkpoint/3a43e623d580435cb452916896964d6d` |
| provider version / ETag | `"3bd3ddfbf9eae8af6f65a54eae1cea8d"` |
| archive bytes | `4,686,611` |
| archive SHA-256 | `d76e358134e38380092420c77887faed1ec64d84ae5c98821ac1356703a52e56` |
| inventory SHA-256 | `9b81f9caa7b76cd39e236f5a3df5134703023a3c0c4c6224e4eadeefe583dfc2` |
| media / protection | `application/vnd.astrowoof.checkpoint+zip` / `protected-operator` |
| compatibility identity | `astrowoof.qa.sbe0445-intent-retirement.v1` |
| logical restore root | `/work/runs/98d2819f-4807-4f13-9b73-9bc8e8d2e1f5/sbe` |
| native lifecycle status | `bounded-progressed_local` |
| fencing identity | `9d085aee-aea3-4c7b-965b-a24552917715` |

### Terminal result and receipt join

The latest durable native receipt is stored in API, not as an additional R2
object to retrieve:

| Field | Exact value |
| --- | --- |
| receipt row ID | `92f30f3b-c827-4cad-a996-39d010abd134` |
| result ID / SHA-256 | `nres_4c48e5b8d7148cda9cf04c9c` / `4c48e5b8d7148cda9cf04c9ca3329dafc937b412324920f62e1f6eb7e10e979f` |
| native outcome / cause | `review_required` / `final_qa_requires_review` |
| command / route | `provider_reconciliation` / `exact_natal` |
| receipt ID / SHA-256 | `nreceipt_9fe2fe86644e06f8affa3a60` / `9fe2fe86644e06f8affa3a6005e3f169d3cf9ee010835725229783cd48325b42` |
| receipt checkpoint-basis SHA-256 | `fa4cf54dacdc66090579d8c7c25dbe1f06eda9169442ccff1ecbc2a945fa3d62` |
| receipt snapshot SHA-256 | `d0d27f94646dac435b3330995c6ce15d77e3d8fa5bf3dd453765f7c3d115b787` |

The receipt checkpoint-basis digest is intentionally recorded separately from
the named generation-9 archive SHA-256.  They are not equal.  This packet does
not claim that equality or manufacture a terminal-checkpoint relationship; the
bounded archive inspection must establish which retained members join the final
validation and receipt lineage.

## Authorization envelope

SBE is authorized to perform exactly the following against only the named
Madeleine object above:

1. one conditional `HEAD`, requiring the recorded ETag, size, archive SHA-256,
   storage contract, and protection metadata to match; then
2. at most one bounded `GET`, only if that `HEAD` matches, limited to
   `4,686,611` bytes and verified against archive SHA-256
   `d76e358134e38380092420c77887faed1ec64d84ae5c98821ac1356703a52e56`.

This authorizes no bucket listing, prefix scan, alternate-object discovery,
additional GET, write/delete, provider action, reconciliation, recovery, or
retained-run/API mutation.  A HEAD mismatch or digest/size mismatch is a typed
evidence failure and closes this access envelope.
