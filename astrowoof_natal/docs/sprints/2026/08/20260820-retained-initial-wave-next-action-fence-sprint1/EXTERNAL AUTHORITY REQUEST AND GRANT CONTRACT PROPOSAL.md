# External Authority Request and Grant Contract Proposal

Date: 2026-08-20  
Status: Slice 1 proposal; API schema review required before runtime implementation

## Decision

Lifecycle inspection v0.5 will make the exact provider-capable next action public.
It adds two required, mutually exclusive nullable fields:

- `external_authority_request`: a complete request that the API can validate,
  reserve, and answer without reading native implementation files;
- `external_authority_refusal`: a closed native refusal when SBE cannot safely
  identify one exact request.

The API answers a request with one all-or-nothing
`astrowoof.external_authority_grant.v1`. A grant is an authorization input, not a
provider result and not permission to bypass SBE's revalidation. The existing six
ordinary per-action `astrowoof.provider_spend_authorization.v0.1` documents remain
the member authorities whose complete bytes and references are bound by the grant.

## Packaged contract identities

- lifecycle inspection: `astrowoof.authoring_lifecycle_inspection.v0.5`;
- request: `astrowoof.external_authority_request.v1`;
- native refusal: `astrowoof.external_authority_refusal.v1`;
- API grant: `astrowoof.external_authority_grant.v1`;
- schema resource: `external-authority-contracts.v1.schema.json`.

The schema is closed-world. Cross-array equality, canonical ordering, digest
construction, and exact document joins are additional semantic validation rules;
JSON Schema alone cannot express them.

## Lifecycle v0.5 branch matrix

| Native decision | `execution_branch` | Request | Refusal | Provider create |
|---|---|---|---|---|
| Exact public action inventory needs API authority | `command=await_external_authority`, `reason_code=spend_authorization_required`, `eligible_now=false`, `action_ids` exactly equal the request's ordered IDs | object | `null` | Only after a matching grant and all native checks |
| SBE cannot prove one exact safe inventory | `command=none`, `reason_code=native_review_or_ambiguity`, `eligible_now=false`, empty `action_ids` | `null` | object | Forbidden |
| Ordinary local continuation | existing v0.4 values | `null` | `null` | Not decided by this surface |
| Provider reconciliation | existing v0.4 reconciliation values | `null` | `null` | Forbidden; retrieval only |
| Terminal or no continuation | existing v0.4 terminal values | `null` | `null` | Forbidden |
| Unsupported native evidence | existing v0.4 unsupported values | `null` or a typed refusal when a provider-capable route was requested | normally `null`, otherwise object | Forbidden |

For the request branch, lifecycle `run_id`, observation revision, snapshot digest,
and logical root must equal the same fields inside the request. Snapshot completeness
and inventory validity must be true, and writer-race evidence must be false. For a
refusal, the observation may intentionally report an invalid snapshot or absent
exclusivity; such a refusal is diagnostic evidence and never create authority.
These joins are semantic-validator requirements, not merely prose: the Slice 1
lifecycle fixtures and tests mutate each outer identity and the branch action list
independently and require deterministic refusal.

`provider_create_permitted_after_authorization=true` is a native capability gate.
It says only that this exact request may become create-capable after the grant and
all current-state checks pass. It is not authorization and is never emitted false
inside a request; refusal and non-request branches carry no create-capable request.

## Request kinds and ordering

### `ordinary_action_set`

- Contains between 1 and 32 independently authorized native actions.
- Actions are sorted by ascending lexical `action_id`.
- This order is canonicalization only, not dependency or execution order.
- `initial_wave` is `null`.

### `initial_wave_admission`

- Contains exactly the six members of one prepared initial wave.
- Preserves the wave's semantic member order; action IDs are never re-sorted.
- Repeats the wave ID/digest, route contract, assignment/profile identities,
  member count, and ordered member-binding digests.
- Every repeated member binding digest must equal the corresponding ordered action.

Every request contains each complete public spend binding, not merely its digest.
That transitively binds stage, route, request bytes, model, service level, maximum
output, maximum commitment, profile, state revision, and versioned price book.
Provider payloads, prompts, protected subject data, credentials, and provider
responses are excluded.

## Canonical digests

All content digests use SHA-256 over UTF-8 canonical JSON with keys sorted,
no insignificant whitespace, and non-ASCII characters preserved.

- request digest: the complete request excluding
  `external_authority_request_sha256`;
- refusal digest: the complete refusal excluding `refusal_sha256`;
- grant digest: the complete grant excluding `grant_sha256`;
- binding digest: the complete binding object;
- authorization-document digest: the complete ordinary authorization document,
  including its authorization reference.

Changing order, a repeated identity, one binding field, an authorization reference,
or an authorization document changes the relevant enclosing digest.

## Aggregate grant semantics

The grant repeats the exact request identity and observation basis and contains an
ordered member entry for every requested action. Each entry binds:

- `action_id`;
- `binding_sha256`;
- the full per-action authorization document's SHA-256; and
- its bounded external authorization reference.

The validator also validates each complete supplied authorization document: its
closed field set and schema identity, exact action ID, exact binding object, digest,
and reference must all match the corresponding request and grant member. A document
cannot become acceptable merely by changing the grant to match its digest.

For an initial wave, the grant also repeats the complete wave context. Validation
is all-or-none: partial, extra, duplicate, reordered, stale, or mismatched members
refuse the whole invocation before authorization mutation or provider I/O.

The grant schema represents only the positive API decision `granted`. Delay or
temporary inability to reserve is represented by withholding the grant. A final API
denial uses the existing providerless-denial contract; it is not encoded as a
partial or negative grant. The SBE-native `external_authority_refusal` is likewise
not an API spend-policy decision.

For the v0.5 constrained continuation, this grant is the invocation-level aggregate
envelope. The older `astrowoof.initial_authoring_wave_authorization.v1` envelope is
not sufficient by itself because it is not bound to lifecycle observation v0.5.
The six existing per-action authorization documents remain required. Historical
0.4.x commands and artifacts remain readable but cannot authorize this new path.

## Native refusal

The closed initial refusal vocabulary is:

- `initial_wave_lineage_unjoinable`;
- `snapshot_invalid`;
- `native_state_inconsistent`;
- `provider_submission_ambiguous`;
- `provider_identity_conflict`;
- `unsupported_provider_capable_route`.

The refusal carries only closed, redacted evidence categories. It is always
`review_required=true` and `provider_create_permitted=false`. In particular,
`initial_wave_lineage_unjoinable` is not a generic contract error: it means native
history proves prior initial-wave/provider lineage but cannot prove one exact wave
that may safely be resumed.

Stale request or grant, changed revision, changed binding, unknown/duplicate member,
or provider evidence appearing after inspection are execution-time typed refusals,
not new lifecycle refusal reason codes. Slice 3 will freeze that result vocabulary;
the lifecycle refusal describes why SBE cannot publish an exact request at all.

## Single-writer and provider atomicity boundary

The constrained command must hold native single-writer control while it:

1. restores and validates the complete snapshot;
2. reconstructs and matches the current request;
3. validates the grant and all six member authorization documents;
4. applies native authorization; and
5. persists a durable pre-submit intent checkpoint.

It then releases the writer during slow provider I/O and reacquires it to persist
each provider identity. This does not create atomicity between local storage and the
provider API. A crash after durable intent but before a durable provider identity is
ambiguity/review unless the identity can be reconciled; it is never permission to
create again.

## Compatibility and rollout

- v0.4 remains a valid historical inspection contract.
- v0.4 does not expose enough authority evidence for the constrained continuation;
  an API must not infer that evidence from `run.json`, logs, snapshots, or IDs.
- The resource catalog remains on the implemented v0.4 contract during this design
  slice. It moves only when runtime v0.5 is implemented and qualified.
- A retained 0.4.13 workspace may be resumed only if the new reader can validate its
  complete snapshot and construct one exact request. Conflicting/unjoinable lineage
  produces the typed refusal and remains retained for review.
- Aster is not a migration fixture and will not be mutated during qualification.

## API review gate

Before Slice 2 or runtime work, please confirm:

1. the lifecycle branch matrix is sufficient for strict API selection;
2. the request contains everything needed for one transactional reservation
   decision without native-file access;
3. the positive-only aggregate grant plus existing negative authorization is the
   correct decision split;
4. the new grant superseding the older initial-wave aggregate envelope on the v0.5
   constrained path is acceptable;
5. the ordinary lexical and initial-wave semantic ordering rules are sufficient;
6. the lifecycle-refusal versus execution-refusal distinction is sufficiently
   machine-readable; and
7. v0.4 historical inspections should be treated as incapable of authorizing this
   new continuation rather than silently upgraded.
