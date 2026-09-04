# Providence terminal-review settlement-boundary investigation plan

## Status

Slices 0–2 are complete and Voof-paws 3 passed. The separately authorized generation-12 checkpoint
read strictly certifies Providence's exact sealed v0.2 result, canonical v0.1
receipt, complete eight-action custody inventory, checkpoint basis, snapshot,
and journal range. The result correctly derives
`providerless_denial_required` for exactly one providerless prepared polish
action; reconciliation inventory is empty and provider creation is forbidden.
This confirms an API settlement-intake gap, not an SBE vocabulary, custody, or
publication defect. A new packaged provider-free eight-action qualification now
proves exact denial, refusal, replay, immutable precursor, and final-custody
successor semantics. The additive qualification was released immutably as SBE
`0.4.48` from exact release-lock commit `49f9e2e`. Voof-paws 4 and owner
authorization passed; tag, assets, and fresh-download verification are
complete. Runtime work and live Providence settlement remain unapproved and
belong to the API companion sprint.

## Goal

Determine whether Providence's sealed terminal-review result is internally
valid SBE v0.2 evidence and whether its unsupported settlement boundary belongs
to SBE or API. Preserve the exact distinction among:

- native terminal-review publication;
- unresolved providerless denial settlement;
- API job/run terminalization; and
- API-owned capacity, lease, and resource release.

No status word, subprocess exit code, log message, or result-index presence is
transition authority by itself. Decisions must follow a validated sealed result,
receipt, action inventory, and exact invocation/result join.

## Safety and scope

This sprint begins provider-free and read-only with respect to retained QA, R2,
and API state. It authorizes no storage listing, writes, provider calls,
reconciliation, denial, resume, repair, recovery, deployment, or release.

An exact retained-checkpoint read is optional, not presumed. Before such access:

1. API supplies one exact immutable object coordinate with object key,
   version/ETag, byte size, archive SHA-256, inventory SHA-256, and logical
   workspace identity.
2. The owner explicitly authorizes one `HEAD` and one conditional `GET` for that
   object.
3. Extraction remains bounded to snapshot/journal metadata and the named sealed
   result, receipt, result index, and paid-action ledger records.
4. Every accessed object and extracted member is hashed; prompts and generated
   content are neither read nor copied into sprint artifacts.

If public logs and API-owned evidence answer the contract question completely,
the retained checkpoint will not be downloaded.

## Pre-Slice 0 findings

The released `0.4.47` worker trace already establishes the following:

- native run `d7017c0c...0612f` reached revision 79 with eight paid actions;
- the six initial actions and one creative-retry action were `REPORTED`;
- polish action `paid_f5a73dc0325db8a8aedafe05` remained `PREPARED`, with no
  provider operation identity;
- provider custody count was zero and no v2 dispatch intent was present;
- SBE published sealed result `nres_0f3d3b6a3cc256db4b7a9c1b` and receipt
  `nreceipt_2b0e8df6e0278a32ff245d61`;
- the invocation-bound public command result reported
  `custody_finality=providerless_denial_required`, `outcome=review_required`,
  `new_provider_create_permitted=false`, and exit code 2; and
- API accepted checkpoint generation 12, then rejected the result solely when
  mapping it to an API disposition.

SBE's closed v0.2 validator recognizes five custody finalities and rederives
each from the complete ordered action dispositions. A `PREPARED` action without
a provider identity is `providerless_denial_only`; with no provider or ambiguity
custody remaining, the only valid aggregate finality is
`providerless_denial_required`.

API's strict transition-ingestion validator also recognizes and rederives this
finality. Its terminal-disposition mapper currently implements only `final` and
the narrow `provider_reconciliation_required` case. API Sprint 67 previously
classified `providerless_denial_required` as a typed nonterminal refusal pending
a supported denial-settlement boundary. Providence is therefore the first known
live reachability proof for that already-documented gap.

These are strong leading findings, not permission to mutate Providence or to
invent the missing denial transition.

## Slice 0 — frozen trace, source, and provenance reconstruction

### Work

- Extract the minimal Providence timeline from the four unfiltered worker-log
  windows, with Denver and UTC timestamps.
- Record exact provenance for every causal statement: log file and line, source
  predicate, public schema/validator, or API consumer branch.
- Map the invocation, result, receipt, checkpoint generation, action inventory,
  provider identities, local-work consumption, and command-result envelope.
- Confirm the exact API execution order: public result validation, finality
  derivation, disposition selection, mutation/persistence boundary, and error.
- Establish which required fields remain unavailable without a retained
  checkpoint or API-owned artifact export.

### Required outputs

- A frozen causal timeline.
- A source/contract map for SBE result construction and API disposition.
- A provenance table distinguishing observed, source-derived, and still-unknown
  facts.
- A decision on whether protected checkpoint access is necessary.

### Negative claims to preserve

- `terminal_closed` does not itself prove API terminalization authority.
- Exit code 2 does not invalidate a sealed typed result.
- The absence of provider custody does not make a prepared action terminally
  accounted.
- The prepared polish action does not authorize provider creation.
- API must not infer or fabricate providerless denial from the finality label.

**Voof-paws 1 — passed:** API approved the causal reconstruction and fixture
design. API confirmed it has no persisted exact result/receipt export, so the
retained checkpoint is required for exact Providence certification. Protected
access remains gated on an API-produced immutable coordinate packet and separate
owner authorization.

## Slice 1 — exact result reconstruction and normative classification

### Work

- Obtain the complete sealed v0.2 result and receipt from an already-supported
  API-owned artifact/export when available; otherwise use the separately
  authorized exact checkpoint read.
- Validate with the released SBE Python readers and validators, including:
  invocation/result/receipt identity; run and checkpoint bindings; action order;
  binding digests; action states; provider identities; custody dispositions;
  reconciliation and providerless-denial inventories; finality; journal range;
  snapshot/checkpoint basis; and content digests.
- Derive the aggregate finality from action rows independently and compare it
  with the sealed field.
- Identify the exact cause code and explain why the prepared polish action was
  retained for denial rather than dispatched or silently discarded.
- Compare the full result with API's current ingestion and disposition matrix.

### Decision matrix

| Evidence | Classification | Next owner |
| --- | --- | --- |
| Valid result; providerless-denial actions; no provider custody | Missing supported denial settlement | API implementation/qualification |
| Valid result with retained provider custody | Existing reconciliation disposition | API routing regression if mishandled |
| Valid result with provider and providerless custody | Explicit mixed settlement required | Joint contract review; no inferred ordering |
| Valid ambiguity custody | Stable review boundary | API review intake; no provider retry |
| Result/action/finality/receipt contradiction | Native/publication defect | SBE reproducer and correction |
| Exact result unavailable | Historical evidence limit | Record ceiling; do not infer validity |

**Voof-paws 2 — ready:** exact artifact certification confirms the API-owned
settlement gap. Freeze the owning side and exact settlement semantics before
building the provider-free qualification or changing runtime code.

## Slice 2 — provider-free settlement-boundary qualification

This slice is warranted even if the defect is API-only because the newly
reachable public shape needs a durable cross-repo consumer fixture.

### Fixture

Construct a production-shaped exact-interactive workspace with:

- six `REPORTED` initial actions;
- one `REPORTED` creative-retry action;
- one `PREPARED` providerless polish action;
- zero provider identities or custody for the polish action;
- zero ambiguity and no active v2 dispatch intent; and
- a sealed v0.2 terminal-review result and receipt whose complete action
  inventory rederives `providerless_denial_required`.

### Assertions

- The result, receipt, command envelope, checkpoint, and ordered action inventory
  pass all public SBE validators and exact joins.
- The denial inventory contains exactly the prepared polish action; the
  reconciliation inventory is empty.
- New provider creation, retrieval, and transport calls are all zero.
- A consumer cannot treat the result as final closeout before denial settlement.
- A supported exact providerless-denial invocation consumes only the named
  action and publishes a traceable successor.
- Reinspection after denial reaches the appropriate final native conclusion.
- Exact replay is inert and cannot deny twice, publish a divergent successor,
  or perform provider I/O.
- Wrong action, binding, result, receipt, checkpoint, inventory, finality,
  predecessor, or replay identity fails closed before mutation.

The fixture proves native/public semantics. It must not invent API database,
lease, reservation, or resource-release facts.

**Voof-paws 3 — passed:** API accepted the packaged fixture and froze its exact
intake, denial, successor-ingestion, capacity, and replay behavior. API also
approved installed-wheel qualification while retaining the rule that native
closeout facts do not authorize API cleanup.

## Slice 3 — installed-wheel and release preparation

### Work

- Freeze fresh unreleased candidate `0.4.48` before release-bound testing and
  refresh its version-bound packaged fixture digest.
- Use the focused patch gate because the diff is additive qualification
  surface only and every changed consumer is enumerable.
- Exercise the affected terminal-result, negative-authorization, lifecycle,
  replay, schema, and release-identity matrix from source.
- Build twice from one committed source identity with one recorded
  `SOURCE_DATE_EPOCH`; require byte-identical wheel bytes and inventories.
- Inspect the wheel for the CLI, module, v1/v2 schemas, packaged fixture, and
  absence of stale/generated/private members.
- Install the exact wheel into an isolated environment with SPC `0.11.1`, run
  `pip check`, verify imports resolve from `site-packages`, and exercise v1,
  v2, schema, reader, and fixture paths from outside the checkout.
- Record a release-lock commit and repeat the deterministic builds and
  installed qualification from that exact identity.

### Boundary

No tag, GitHub release, deployment, API mutation, live Providence settlement,
provider operation, or retained-QA access occurs without the later explicit
release authorization.

**Voof-paws 4 — passed:** API approved the exact candidate and the owner
authorized immutable tag/publication. The published wheel and checksum were
downloaded afresh and verified against the qualified candidate.

## Slice 3 — implementation only on the owning side

### Expected API-only path

If Slices 0–2 confirm the leading hypothesis, SBE runtime and public schemas do
not change. API should:

1. validate and persist the exact sealed review result and receipt;
2. retain the workspace and audit identity without terminal cleanup;
3. release or retain API-owned capacity only according to explicit API policy;
4. perform zero provider I/O and prohibit new provider creation;
5. invoke the supported providerless-denial boundary using the exact ordered
   denial inventory and current checkpoint binding;
6. ingest the traceable successor and reinspect before terminal closeout; and
7. make exact replay idempotent across interruption between native denial and
   API finalization.

SBE may add a packaged qualification fixture/reader only if the current public
package lacks a consumer-stable way to exercise the already-existing contract.
That additive packaging change alone requires its own risk-proportionate release
decision.

### SBE correction path

Only if strict reconstruction exposes contradictory native evidence will SBE
implement a correction. It must be the smallest provider-free fix to result
construction, custody derivation, sealing, or publication, followed by focused
and installed-wheel qualification. No release is presumed.

## Completion criteria

- Every Providence causal claim has a provenance pointer.
- The exact result is either strictly validated or explicitly unavailable.
- The settlement owner and no-I/O semantics are unambiguous.
- Providerless denial cannot be confused with final closeout, provider
  reconciliation, ambiguity, or fresh authority.
- The implementation sprint has a fixture-backed consumer contract and no need
  to reconstruct private native state.
