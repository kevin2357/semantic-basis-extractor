# Terminal Review Closeout Handoff Sprint 1 Plan

## Status

Slices 0–5 complete and API-approved; Slice 6 broad regression, deterministic
build, installed qualification, and release preparation are complete. Final API
and owner review is required before tag/publication. The
controlled read-only retained-checkpoint inspection is complete, with no
provider operation, deployment,
version bump, tag, or publication is authorized by this plan.

## Objective

Make a terminal editorial `review_required` decision cross the supported native
handoff before the authoring command exposes its nonzero process outcome.

The published evidence must let an API consumer distinguish, without reading
private `run.json` or logs:

- completed and reported paid actions;
- provider-submitted actions whose identities are durable but whose results remain
  unreconciled;
- authorized actions for which provider creation was never entered; and
- any ambiguous or contradictory action that requires retention for review.

The correction must preserve provider safety, exact replay, snapshot integrity,
native/API ownership, and the existing separation between editorial review and the
companion investigation into whether the particular QA review decision was valid.

## Problem statement

SBE 0.4.27 contains an established native publication protocol and the ordinary
exact-Natal CLI visibly calls `publish_native_execution_result()` before
`SystemExit(2)` for review statuses. The fresh Pippin/Duchess traces nevertheless
showed a bare worker failure with no terminal native publication. The last valid
native result remained `provider_pending`.

This yields two questions that must not be collapsed:

1. **Execution-path defect:** which real resume/fan-in/finalization path reaches
   review-required without the intended result/snapshot/receipt publication?
2. **Consumer-evidence sufficiency:** once publication occurs, does the sealed
   public result expose enough exact action disposition and custody evidence for
   the API to retain submitted work and act only on authority proved unused?

Slice 0 answers the first from provider-free production-shaped evidence. Slice 1
freezes the answer to the second before runtime changes proceed.

## Ownership boundary

### SBE owns

- native run status and state revision;
- native paid-action identity, binding, state, provider identity, consumption,
  ambiguity, and reconciliation evidence;
- editorial terminal/review disposition;
- complete workspace snapshot validation;
- journal/result/snapshot/receipt publication and replay;
- the supported run-level reconciliation and providerless-denial operations; and
- proof that a command performed no new provider creation.

### API owns

- API job/run status and failure classification;
- worker lease and capacity release;
- API reservation and global spend authority;
- PostgreSQL/R2 ingestion and transactionality;
- whether and when to invoke supported denial/reconciliation operations;
- public product status and operator policy; and
- deletion or continued retention of worker scratch.

SBE must not claim that API reservations were released. API must not synthesize a
native terminal result or infer provider absence from a process exit.

## Frozen safety rules

1. Native result publication precedes the terminal nonzero exit.
2. A process exit, log event, or API action row is not native terminal authority.
3. A durable provider identity is retrieval-only custody; it never authorizes a
   replacement create.
4. Identity-less call-entry remains ambiguous and fail-closed.
5. A providerless authorized action remains separately identifiable; publication
   alone does not silently deny it or release API authority.
6. Editorial `review_required` may coexist with unresolved provider custody. The
   result must represent both truths rather than flattening one into the other.
7. Reconciliation after editorial review may settle already-submitted work but
   must not reopen editorial authoring or submit new work.
8. The publication protocol is a validated multi-file protocol, not a claim of
   literal filesystem-wide atomicity.
9. Events and `✨🐶` logs explain execution but remain non-authoritative.
10. The retained Pippin and Duchess workspaces are evidence only and remain
    untouched throughout source implementation and provider-free qualification.

## Applicability matrix to resolve

| Route | Mechanism | Required posture |
| --- | --- | --- |
| Exact Natal | interactive Responses | Release-blocking incident path; full support and qualification |
| Exact Natal | Batch | Characterize; parity-support if it shares the safe terminal finalizer, otherwise explicit fail-closed/deferred record |
| Bounded Natal | interactive Responses | Characterize shared terminal path; parity-support if no route-specific weakening is required |
| Bounded Natal | Batch | Characterize only unless the existing bounded Batch mechanism composes safely without broadening scope |

No route may silently claim terminal publication coverage merely because a helper
function is shared.

## Contract questions for the Slice 1 gate

1. Can `astrowoof.native_execution_result.v0.1` express the required mixed action
   dispositions strictly, or is a fresh closed version required?
2. Should exact action disposition be embedded in the execution result or provided
   as a content-addressed, snapshot-bound public projection referenced by it?
3. Which closed custody values distinguish reported, provider-pending,
   providerless-authorized, ambiguous, denied, and terminally failed work?
4. What exact digest binds the complete terminal action inventory and its order?
5. Does editorial `review_required` remain a terminal execution outcome while
   provider reconciliation remains a permitted custody-only follow-up?
6. What result/closeout fields prove `new_provider_create_permitted=false` without
   implying that no historical provider work exists?
7. Which existing providerless-denial result remains the only release evidence for
   an unused authorized action?

## Slice 0 API review decisions

- The incident is presently classified as an API ordinary-resume ingestion gap,
  not as a proven generic SBE publication-order defect.
- API must ingest the exact result produced by the invocation it launched; a
  naively discovered latest result is not sufficient command correlation.
- Slice 1 will use a fresh closed result version with an ordered per-action custody
  projection rather than widening v0.1.
- Editorial terminality and custody finality are separate public facts. The new
  result must carry an explicit custody-finality disposition and the exact
  reconciliation-only inventory when custody remains.
- The result must state `new_provider_create_permitted=false`; this does not imply
  that historical provider work is absent.
- Publication alone never releases a providerless reservation. Existing supported
  providerless-denial evidence remains required.
- A controlled read-only inspection of retained Pippin/Duchess checkpoint evidence
  is authorized solely to determine whether their exact invocations published a
  sealed result. It may read only result-index/result/receipt/snapshot/journal
  metadata, must hash what it accesses, and must not resume, reconcile, repair,
  delete, write, or invoke a provider.
- The retained active archives contain complete, hash-valid native result histories
  but no `review_required` result. Their latest sealed results are
  `ordinary_authoring / provider_pending`. Therefore the incident includes a real
  live-route publication gap in addition to the API ingestion gap; the generic
  provider-free reproduction alone did not cover the exact production branch.

## Slice 0 — Reproduce the real terminal handoff gap

**Status:** complete. The generic SBE publication-order hypothesis was not
reproduced. See `SLICE 0 - PUBLIC ROUTE REPRODUCTION AND CAUSAL FINDINGS.md` for
the corrected cross-boundary finding and proven v0.1 evidence gap.

### Work

- Build a provider-free, production-shaped exact-interactive workspace through
  supported runtime code, not by testing publication helpers in isolation.
- Drive the public ordinary-resume/dispatch path through:
  initial accepted passes, completed fan-in, retry preparation, and the exact
  review-required transition implicated by the incident.
- Model the mixed action inventory where possible: reported work, one durable
  provider identity, and one authorized/providerless action.
- Capture before/after:
  state revision, snapshot digest, lifecycle inspection, local-work operation,
  result index, native journal range, receipt inventory, exit code, typed events,
  and provider transport counts.
- Locate the exact branch that bypasses or loses publication. Determine whether
  the cause is early exit, stale in-memory state, exception conversion,
  local-work checkpoint interaction, publication refusal, or wrapper behavior.
- Use the retained read-only finding as a regression requirement, not as permission
  to execute or repair the retained runs.
- Compare exact route behavior with bounded and Batch entry points only enough to
  fill the applicability matrix.
- Add a focused regression that fails against the current implementation through
  the real public command/runtime boundary.

### Gate

- The defect is reproduced without network/provider calls.
- The missing publication is attributable to a concrete control-flow boundary.
- No retained QA bytes are read or mutated.
- The result records what current v0.1 public evidence can and cannot prove.

### Voof-paws 1

Pause for owner and API review of the causal finding before freezing a public
contract.

## Slice 1 — Freeze terminal-review and mixed-custody contract

**Status:** complete and API-approved after consumer-join corrections.

### Work

- Write a contract proposal defining editorial terminality separately from action
  custody and financial settlement.
- Bind the result to the exact invocation that produced it so consumers never
  substitute a merely latest result.
- Choose one closed representation for ordered terminal action dispositions.
- Bind every action projection to native run ID, action ID, full public binding or
  binding digest, stage/route, provider mechanism, native action state, provider
  identity/evidence class, consumption/reporting class, and whether existing
  providerless denial is applicable.
- Define a canonical terminal action-inventory digest and strict joins to the
  execution result, checkpoint basis, journal range, snapshot, and receipt.
- Preserve null/unknown distinctly from zero/absent.
- Specify that a providerless-authorized action is not release evidence until the
  existing supported denial result says so.
- Define allowed custody-only reconciliation after editorial review and forbid
  new provider creation or editorial reopening.
- Carry an explicit custody-finality disposition plus an ordered
  reconciliation-only inventory where durable provider custody remains.
- Version any changed public artifact honestly; do not widen a closed schema in
  place.
- Add strict Python semantic validation independent of optional `jsonschema`, plus
  mutation tests for run/action/binding/provider/inventory/digest contradictions.

### Gate

- One exact request/result/receipt interpretation is machine-readable without
  private workspace parsing.
- API can map each action to retain, reconcile, or separately deny without SBE
  claiming API resource release.
- Historical artifact versions remain readable but fail closed where they cannot
  prove the new handoff.

### Voof-paws 2

Pause for API schema/authority review before runtime mutation.

**Gate result:** approved for exact-interactive Slice 2 only. Batch and bounded
runtime paths remain out of scope.

## Slice 2 — Centralize publication-before-exit

**Status:** complete for exact interactive only; Batch and bounded routes remain
unchanged. See `SLICE 2 - EXACT INTERACTIVE PUBLICATION BEFORE EXIT.md`.

### Work

- Implement one supported terminal finalization boundary used by the real ordinary
  authoring routes.
- Under native single-writer control, re-read state, validate snapshot/checkpoint,
  derive the terminal outcome and mixed custody projection, append the bounded
  journal transition, publish result, publish/validate the complete snapshot, and
  seal the immutable receipt.
- Return the sealed public identity to the caller before translating review into
  process exit 2.
- Emit a closed command-result envelope containing the exact native invocation,
  result, and receipt identities/digests before exit 2; latest-result discovery is
  never invocation correlation.
- Ensure logging/event sink failure cannot prevent or alter publication.
- Ensure stdout/result output cannot precede or masquerade as a valid receipt.
- Wire exact interactive production resume first, then only matrix cells proven
  safe in Slice 0/1. Slice 2 is explicitly exact interactive only; Batch and
  bounded routes remain unchanged pending later matrix evidence.
- Make repeated finalization exact replay or compatible already-published behavior;
  never mint a second semantic terminal transition.

### Gate

- The real public command publishes a validated review-required result and receipt
  before exit 2.
- Result, snapshot, journal, and receipt joins validate from a fresh reader.
- Zero provider creates occur during terminalization.

## Slice 3 — Preserve custody-only follow-up and unused-action handling

**Status:** complete for exact interactive and paused at Voof-paws 3. See
`SLICE 3 - REVIEW CUSTODY SETTLEMENT WITHOUT AUTHORING REOPEN.md`.

### Work

- Prove that submitted provider work remains visible and reconciliation-only after
  editorial review.
- Permit the supported reconciliation cycle to retrieve only durable provider IDs,
  checkpoint returned evidence, and publish a successor native result without
  reopening authoring or changing the editorial review decision.
- Prove that authorized-but-never-submitted work remains providerless and is acted
  on only through the existing exact single/batch denial contract.
- Verify providerless denial cannot touch submitted, consumed, reported, or
  ambiguous actions.
- Make closeout expose the correct typed disposition when editorial review is
  terminal but custody remains, and after custody is fully resolved.
- Preserve API-owned reservation/billing decisions outside SBE.

### Gate

- Mixed custody never collapses into `provider_local_dependency_count=0` when SBE
  has durable unresolved provider identity.
- Reconciliation performs GET-only observation and no POST/create/retry.
- Providerless authority release remains backed by the existing denial artifact,
  not inferred from terminal review.

### Voof-paws 3

Pause for API review of the runtime result and custody mapping.

**Gate result:** approved; Slice 4 completed and was subsequently API-approved.

## Slice 4 — Interruption, replay, concurrency, and privacy matrix

**Status:** complete for the exact-interactive terminal-review boundary. See
`SLICE 4 - INTERRUPTION REPLAY AND IMMUTABLE REVIEW LINEAGE.md`.

### Work

- Inject failures at minimum:
  after native terminal state persistence; after journal append; after immutable
  result write; after snapshot write; after snapshot validation; after receipt
  publication; and after publication immediately before exit 2.
- Prove supported repair completes only the exact recognizable publication write
  set and never submits provider work.
- Race two resumers/finalizers and prove native single-writer exclusion plus one
  semantic terminal result.
- Replay the exact terminal command and custody-only reconciliation.
- Mutate action inventory, provider identity, binding, result, journal, snapshot,
  and receipt independently and prove fail-closed behavior.
- Capture typed publication start/complete/refusal diagnostics with bounded safe
  fields; make event sinks failure-isolated.
- Use protected payload/subject sentinels and prove absence from public fixtures,
  events, logs, and command diagnostics.

### Gate

- No crash cut or concurrency schedule yields duplicate create, duplicate terminal
  transition, partially valid publication, or cross-run effect.
- Exact replay is deterministic and idempotent.

## Slice 5 — Packaged fixtures and installed-wheel qualification

**Status:** complete; paused at Voof-paws 4 for API fixture/consumer review. See
`SLICE 5 - INSTALLED TERMINAL REVIEW QUALIFICATION AND API HANDOFF.md`.

### Work

- Publish sanitized, closed fixtures for:
  review-required with all actions reported; mixed reported/provider-pending/
  providerless-authorized custody; ambiguous submission; malformed inventory;
  pre-receipt interruption; exact replay; and post-review custody reconciliation.
- Add a provider-free installed-wheel qualification command/API that exercises the
  actual public ordinary-resume, native-result reader, reconciliation, denial
  compatibility, closeout, and replay boundaries in fresh processes/workspaces.
- Emit one concise closed receipt with fixture and artifact hashes, route matrix,
  provider GET/POST counts, publication identities, and privacy assertions.
- Explicitly prove exit 2 occurs only after the terminal receipt validates.
- Add consumer handoff examples showing API ingest-first ordering and the distinct
  handling of submitted versus unused authority.

### Gate

- Source and isolated installed-wheel qualification pass.
- Published fixtures validate with packaged readers only.
- External network calls, provider creates, spend, and retained-QA access are zero.

### Voof-paws 4

Pause for API fixture/consumer review before release qualification.

## Slice 6 — Broad regression and release preparation

**Status:** complete; Voof-paws 5 final API and owner release approval received.

### Work

- Run focused terminal publication, lifecycle, reconciliation, providerless denial,
  closeout, adversarial simulation, and route-parity suites.
- Run the broad source suite once after focused stability is established.
- Build deterministic candidate wheels from committed source and verify byte
  identity.
- Run generic installed smoke plus the new terminal-review qualification against
  the isolated wheel.
- Record exact source commit, wheel hash, dependency identities, fixture/receipt
  hashes, tests/skips, and zero-provider/zero-spend evidence.
- Update release notes, compatibility, known limitations, contract catalog, and API
  handoff. Keep the companion editorial-validity investigation explicitly separate.

### Gate

- No implementation or consumer blocker remains.
- API consumes the exact candidate wheel/fixture identities in its companion test.
- Owner and API release review are explicit before version/tag/publication work.

### Voof-paws 5

Final API and owner review. Tag/publication requires separate explicit approval.

## Test strategy

### Focused tests first

- public ordinary-resume review transition;
- publication-before-exit ordering;
- strict result/action-inventory validation;
- mixed custody and providerless distinction;
- post-review reconciliation and closeout;
- crash cuts and replay;
- route applicability; and
- installed command/reader behavior.

### Provider transport assertions

Every fixture records exact method/count/identity expectations:

- terminal finalization: POST 0, GET 0;
- post-review reconciliation: POST 0, GET only the SBE-selected durable IDs;
- replay: POST 0 and no duplicate GET for already reconciled work;
- malformed/contradictory evidence: POST 0, GET 0.

### Broad gate discipline

Run the expensive full suite only after focused source and installed-wheel gates are
stable. Line-ending-only warnings are not product failures, but `git diff --check`
must be clean before every commit/release gate.

## Deliverables

- causal Slice 0 reproduction/finding document;
- terminal-review mixed-custody contract proposal;
- strict schemas/readers/builders and contract catalog updates if required;
- centralized publication-before-exit runtime integration;
- provider-free fixture set and installed-wheel qualification receipt;
- API consumer handoff and compatibility notes;
- sprint `LOG.md` and `EVIDENCE.md`; and
- release recommendation only after all review gates pass.

## Explicit exclusions

- deciding whether Pippin/Duchess editorial review was correct;
- mutating or resuming either retained QA workspace;
- inventing API reservations, leases, or billing outcomes;
- resubmitting provider work;
- redesigning authoring retry policy;
- broad Batch/bounded work not justified by the applicability assessment; and
- tag, publication, deployment, or paid QA before later explicit approval.
