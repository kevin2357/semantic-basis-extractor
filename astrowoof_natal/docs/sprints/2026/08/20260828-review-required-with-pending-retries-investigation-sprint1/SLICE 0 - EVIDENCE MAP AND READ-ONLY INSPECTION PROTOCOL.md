# Slice 0 — Evidence map and read-only inspection protocol

## Status

Protocol frozen. Retained R2 bytes have not been accessed in this sprint. Slice 1
requires Voof-paws 1 review plus temporary read-only credential availability.

## Frozen subjects

| Subject | API run ID | Native run ID | Active generation | Archive bytes | Declared members |
| --- | --- | --- | ---: | ---: | ---: |
| Pippin von Waffle | `fbe8ada6-511d-469f-a9b6-31fe15835138` | `8fcce2334d4e717595cafe5af18bb6ee5d097270da362a6783a5fab2f5a8bb79` | 12 | 4,014,784 | 789 |
| Duchess Crumpet | `40783a32-e326-4605-8503-de8838152fc0` | `d436f2a008656d16bb8f1efbdb11342278ed808ad88acba3fdafef087d230268` | 13 | 4,054,594 | 796 |

The companion sprint previously verified both archive and complete inventory
identities against API-owned protected checkpoint rows. Those secret-bearing
storage references and full hashes were deliberately not committed. Slice 1 must
obtain the same exact references through a bounded local input supplied by the API
authority or repeat the protected metadata lookup. It must never select an object
from a bucket listing based only on similar size, name, recency, or generation.

## Required local input before any R2 GET

For each subject, a local, uncommitted inspection-authority document must contain:

- API run ID;
- native run ID;
- checkpoint ID and job ID;
- generation and active state;
- opaque storage object ID/reference;
- archive byte size and SHA-256;
- complete inventory SHA-256;
- checkpoint contract and compatibility identity;
- logical restore path; and
- storage environment, namespace, and protection class.

The inspection tool must reject missing fields, duplicate subjects, the wrong QA
environment/bucket, a non-active generation, an unexpected byte count/generation,
or a subject identity different from the frozen table above. The authority file
itself remains local and is deleted after the inspection receipt records only its
SHA-256 and nonsecret identities.

## Read-only operation boundary

Allowed remote operations are:

1. `HEAD`/stat of each exact opaque checkpoint object;
2. one `GET` of each exact object after size/digest expectations are loaded; and
3. no other R2 operation.

Forbidden operations include list-based object discovery, PUT, multipart upload,
COPY, DELETE, lifecycle changes, metadata rewrites, presigned publication, and any
API/SBE command that resumes, reconciles, repairs, denies, closes, or executes a
run. No OpenAI credential or provider transport is used.

The downloaded ZIPs are evidence copies only. They must be stored in a fresh local
temporary directory outside both repositories. The original R2 objects and API
checkpoint rows remain untouched.

## Archive and inventory validation

Before interpreting any member:

1. Verify downloaded byte count and archive SHA-256 against the protected authority
   input.
2. Parse the ZIP without extracting it into an executable workspace.
3. Reject malformed ZIPs, duplicate member names, unsafe paths, symlinks, absolute
   paths, path traversal, or members outside the checkpoint archive contract.
4. Require exactly one archive manifest.
5. Validate schema, checkpoint contract, compatibility identity, generation,
   predecessor identity, member count, total bytes, and inventory SHA-256.
6. Require the ZIP member set to equal the manifest-declared set exactly.
7. Verify byte size and SHA-256 for every member before reading any member as
   evidence.
8. Validate the restored logical-root and native run identity from declared native
   state. A mismatch refuses the entire subject.

No undeclared file, filesystem timestamp, ZIP ordering, or filename similarity may
be used as authority.

## Authoritative member evidence map

After whole-archive validation, inspection may read only declared members needed
for these questions:

| Question | Native evidence class |
| --- | --- |
| Run/profile/resource/route identity | `run.json`, public state, lifecycle and snapshot identity files |
| Paid action state and exact binding | spend ledger and authorization request/consumption records |
| Initial and retry pass lineage | pass assignments, authoring packets/state, retry feedback and accepted-pass records |
| Provider custody | durable provider IDs, call-entry/ambiguity evidence, reported usage/result records |
| Validation and editorial disposition | cards, validation reports, lint reports, pass-local QA and final-QA reports |
| Successor preparation | prepared request/binding records and native journal transitions |
| Public lifecycle projection | result index, sealed results, receipts, lifecycle/temporal inspection artifacts |

The exact member paths selected from each manifest are frozen in the local access
log before their contents are parsed. Content-bearing authored deck prose and full
prompts are not copied into reports. Where a report combines structural fields and
authored text, the inspector emits only closed codes, IDs, booleans, counts,
digests, paths, attempt numbers, and bounded technical diagnostics needed to
explain selection.

## Exact joins required

For every creative-retry row, the reconstruction must join:

- native run ID;
- native action ID;
- route, stage, pass ID, attempt number, and source/retry lineage;
- complete binding or binding digest;
- authorization request/reference and consumption/denial status;
- provider mechanism, call-entry state, durable provider identity, and reported
  result/usage where present;
- validation/rejection reason and successor action, if any; and
- API action/provider facts supplied separately by the API authority.

An unjoined action is `unresolved`; it is never silently assigned to the nearest
pass or inferred from ordering.

## Sanitization contract

Committed artifacts may contain:

- API/native/action/pass IDs already in the incident record;
- hashes and opaque provider response IDs where essential to custody joining;
- closed state, reason, scope, stage, route, attempt, and outcome values;
- timestamps and bounded durations;
- structural filenames, counts, and byte sizes; and
- short technical error categories with protected values removed.

Committed artifacts must not contain:

- R2 credentials or secret storage references;
- database credentials or connection strings;
- birth datetime, coordinates, location evidence, or other protected subject data;
- authored card/deck prose;
- full prompts, provider request/response payloads, authorization documents, or
  complete bindings;
- API keys, tokens, headers, or signed URLs.

A privacy sentinel scan must cover every generated report before it is staged.

## Access receipt

The Slice 1 receipt records:

- protocol and frozen-manifest SHA-256;
- authority-input SHA-256 but not its secret fields;
- exact subject/run/generation/archive/inventory identities;
- every accessed declared relative path plus its declared SHA-256;
- remote operation counts (`HEAD=2`, `GET=2`, all writes `0`);
- provider operation counts (`create=0`, `retrieve=0`);
- workspace/API/R2 mutation counts (`0`);
- cleanup result for downloaded archives, derived working files, and credentials;
- sanitized timeline/report hashes.

## Refusal posture

Any mismatch stops inspection for that subject. No alternate generation, nearby
object, predecessor checkpoint, newer checkpoint, or reconstructed hash is
substituted automatically. The result is a typed local refusal and a zero-write
receipt, followed by owner/API review.

## Confidence rubric

- **High:** directly joined authoritative native/API evidence with matching hashes.
- **Medium:** deterministic conclusion from complete authoritative inputs, but the
  decisive transition itself was not retained.
- **Low:** diagnostic trace or source-code inference without complete historical
  native inputs.
- **Unknown:** required evidence is absent or contradictory.

Each material conclusion in Slice 1 must carry one of these labels.

Every timeline claim must also carry a compact provenance pointer containing the
declared native relative path and member SHA-256, API row/action ID where
applicable, and evidence class (`direct`, `inferred`, `unknown`, or
`contradictory`). A paragraph-level bibliography or generic archive reference is
not sufficiently precise for a causal claim.

## Gate result

The procedure is safe to begin only after the exact protected checkpoint authority
inputs and temporary R2 credentials are available and Voof-paws 1 approves this
protocol. Merely having bucket credentials is not permission to enumerate or guess
the retained objects.
