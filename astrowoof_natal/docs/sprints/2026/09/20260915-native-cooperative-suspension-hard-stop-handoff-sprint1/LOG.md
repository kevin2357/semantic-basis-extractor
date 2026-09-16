# Log

## 2026-09-15 — Sprint creation

- Reviewed API Sprint 92 Slice 0 topology, Gate A response, and Slice 1 durable
  force-fence proposal.
- Confirmed cooperative native suspension is feasible only with a pre-launch
  invocation identity and bounded control channel.
- Closed the old `0.4.60` sprint around its actual relocated read-only
  assessment delivery and moved all prospective hard-stop work here.
- Froze the initial ownership rule: API owns fencing and process supervision;
  SBE owns truthful native safe-point and custody evidence; later resource
  release requires an explicit join.
- Added mandatory joint review before any runtime mutation or process-control
  work.

## 2026-09-15 — Slice 0 safe-point inventory

- Mapped direct authoring, ordinary-v2 dispatch, interactive reconciliation,
  initial-wave fan-out, optional qualitative stages, bounded, Batch, and
  terminal publication paths.
- Confirmed SBE has no current suspension request/control channel or signal
  handler. Existing invocation IDs are diagnostic or publication identities,
  not API pre-launch supervision authority.
- Identified exact interactive ordinary-v2 dispatch and response reconciliation
  as the cleanest first cooperative implementation cells.
- Recorded the unavoidable POST-entry-to-provider-ID ambiguity and the need for
  aggregate cancellation semantics before initial-wave fan-out can claim
  cooperative suspension.
- Paused at Voof-paws A before freezing Gate B fields or implementing runtime
  behavior.

## 2026-09-15 — Voof-paws A approved

- API approved exact interactive ordinary-v2 dispatch and response
  reconciliation as the complete v1 cooperative route scope.
- Deferred initial-wave fan-out pending a separate aggregate partial-wave
  cancellation protocol; legacy direct, bounded, and Batch remain unsupported.
- Selected a distinct API-created pre-launch supervision invocation ID and an
  atomic request-isolated control-file channel outside the executable workspace.
- Required the envelope to bind the canonical absolute control root and
  relocated copies to reject the capability before request parsing.
- Froze resource handling: exact envelope-bound child exit may reclaim only
  worker-execution capacity. Run allocation and all native/external custody stay
  held.
- Authorized Slice 1 contract work only. Gate B still blocks runtime mutation,
  signaling, process control, and release behavior.

## 2026-09-15 — Slice 1 Gate B proposal

- Drafted the closed four-document v1 contract: API pre-launch supervision
  envelope and suspension request; SBE native suspension result and receipt.
- Froze an atomic request-isolated control-file channel whose canonical absolute
  root is envelope-bound and rejected by relocated workspaces before parsing.
- Enumerated exact ordinary-v2 dispatch and response-reconciliation safe points,
  provider/local-work outcomes, and the unavoidable provider-entry ambiguity.
- Preserved exact ordinary terminal/delivery result precedence over a later stop
  observation and prohibited latest-result discovery as command authority.
- Defined append-only request/result/process-observation/resolution evidence and
  exact replay behavior across restart and stale channels.
- Recorded the resource join: exact child exit may reclaim worker execution
  only; run allocation and provider/spend/workspace/native custody remain held.
- Added the provider-free identity, channel, lifecycle-race, crash, publication,
  replay, and unrelated-run qualification matrix.
- Paused at joint Gate B. No schemas, readers, runtime hooks, signaling, process
  control, provider work, or capacity release were implemented.

## 2026-09-15 — Gate B API review incorporated

- Recast the force-fence admission checkpoint as an immutable predecessor
  anchor rather than an observation-time equality requirement.
- Required SBE to bind both admission checkpoint C1 and an exact same-lineage
  safe-point checkpoint C2, accepting only equality or a validated contiguous
  successor and rejecting forks/non-successors.
- Froze dedicated ordered CLI arguments for the immutable envelope file and
  canonical control root, including wrong-location and substitution failures.
- Added closed `suspension_deferred` continuation modes so API never infers
  process exit or release.
- Clarified that malformed/conflicting/unsupported control input prohibits new
  native/provider work even when a typed refusal cannot safely be published.
- API is aligned and ready to review the canonical Alloy spike. Runtime
  implementation remains blocked.

## 2026-09-15 — Alloy spike added

- Added a post-Gate-B, pre-implementation Alloy spike for the joined API/SBE
  protocol.
- SBE will own one canonical model; API will review and bind evidence to its
  exact commit and digest rather than maintaining a drifting duplicate.
- Scoped the model to identities, ordering, append-only evidence, authority,
  custody, precedence, replay, and cross-run isolation.
- Explicitly excluded filesystem, subprocess, provider-timing, hashing, schema,
  packaging, and deployment claims from the model's proof boundary.
- Added a separate Voof-paws B2 before contract implementation.

## 2026-09-15 — Slice 1A Alloy campaign

- Restored the pinned official Alloy Analyzer CLI `6.2.0`; the downloaded
  distribution matched the prior recorded SHA-256 exactly.
- Built one content-free shared API/SBE protocol model with exact identity,
  checkpoint lineage, timing, replay, resolution, custody, and cross-run joins.
- Corrected an initial vacuity bug where optional model relations accidentally
  made every scenario impossible, then required satisfiable full-contract
  worlds before interpreting assertion results.
- Obtained four satisfiable valid scenarios, nine `UNSAT` assertion checks, and
  five satisfiable deliberately weakened bad-world witnesses.
- Tightened Gate B prose based on counterexamples: one canonical result per
  request; ordinary-result precedence at native `observed_at`; and acyclic,
  non-branching same-fence resolution successors.
- Recorded the exact model digest, stable receipt, rule-to-fixture map, finite
  scope, and proof limits.
- Paused at Voof-paws B2. No schema, reader, runtime, process-control, provider,
  API, R2, or release action occurred.

## 2026-09-15 — Gate B2 corrections

- Read API's B2 hold and agreed with both identified relational gaps.
- Made request conflict invocation-wide: a distinct later request refuses even
  when its idempotency key differs, while the first canonical result remains
  unchanged.
- Split safe-point observation from suspension-result publication and made a
  prior ordinary result suppress suspension result/receipt/transport creation
  entirely.
- Added compact one-result-to-one-receipt-to-one-command-result relations with
  exact same-invocation binding.
- Reran the complete campaign: four valid scenarios `SAT`, ten protected checks
  `UNSAT`, and seven deliberately weakened bad-world witnesses `SAT`, including
  duplicate-receipt and cross-invocation transport mutations.
- Returned to Voof-paws B2; Slice 2 remains blocked pending re-review.

## 2026-09-15 — Gate B2 approved and Slice 2 contracts

- Incorporated API's Gate B2 approval and preserved the runtime-integration
  fence.
- Added closed provider-free readers for supervision, request, result, receipt,
  command-result, and complete fixture-bundle documents.
- Packaged the full schema family, one complete C1-to-C2 positive fixture, and
  six new public catalog entries.
- Resolved a prose-only circular-hash dependency: result seals independently,
  receipt binds result, and command envelope binds both final digests.
- Covered all six outcomes, exact replay/new-key conflict, stale and mismatched
  identities, C1/C2 lineage, relocated root identities, prior ordinary-result
  suppression, transport mutations, and bundle-wide cardinality provider-free.
- Focused result: 10 tests passed with one expected optional-schema skip; 24
  passed total when paired with the neighboring release-contract module.
- Paused at Voof-paws C before any coordinator, CLI, control-file, process,
  provider, API, R2, or release behavior.

## 2026-09-15 — Voof-paws C cardinality correction

- Read API's executable-contract review and reproduced the bundle-level gap:
  transport IDs were unique, but a second coherently re-sealed result could
  still target the same exact request.
- Made the bundle reader reject a repeated `(request_id, request_sha256)`
  identity before admitting another result/receipt/command triple.
- Added a provider-free mutation that changes the semantic conclusion and
  recomputes every downstream digest and identity; the bundle now refuses it.
- Exact replay continues to return the already published identities rather
  than append another fixture result.
- Runtime integration remains blocked at Voof-paws C pending re-review.

## 2026-09-15 — Voof-paws C approved and Slice 3 safe-point integration

- Incorporated API's executable-contract re-review and opened only the
  previously approved exact-interactive ordinary-v2 cells.
- Added the immutable envelope/control-root argument pair to the public v2
  dispatch and reconciliation commands. Missing pairs, relocated roots,
  unexpected control members, stale requests, and identity mismatches refuse
  before the request can affect provider work.
- Serialized request observation under the existing native writer locks at
  dispatch intent, provider-call entry, provider identity/ambiguity, and
  reconciliation retrieval/response-publication boundaries.
- Checkpointed the observation record before publishing a separate immutable
  suspension result/index, receipt, retained snapshot/basis, and exact command
  result. Suspension artifacts remain excluded from the executable snapshot,
  like the existing native publication receipts, avoiding circular identity.
- Made interrupted publication restart-safe: a restart after observation but
  before result publication reconstructs the same canonical result, while
  exact replay returns it and a second request for the invocation conflicts.
- Required ordinary terminal/delivery dominance to pass the existing native
  result reader, including result, journal, receipt, retained evidence, and
  workspace validation; a forged result-index entry cannot suppress the stop.
- Preserved provider-entry ambiguity as `provider_boundary_ambiguous`; did not
  synthesize provider identity, retry work, signal/kill a process, or release
  API/provider/spend/workspace/native custody.
- Kept bounded interactive, exact Batch, and bounded Batch reconciliation
  explicitly unsupported when a suspension observer is supplied.
- Verification: Slice 3 module 11 passed; combined contract/v2/reconciliation
  matrix 112 passed with 2 expected optional skips. No provider, network, API,
  R2, process-control, packaging, release, or deployment activity occurred.
- Paused at Voof-paws D before installed/package or API supervision work.

## 2026-09-16 — Voof-paws D approved; Slice 4 dependency split

- API approved Slice 3 without correction: exact interactive ordinary-v2
  scope, writer-lock observation, checkpointed handoff, and strict separation
  from API fencing/process/release authority all remain intact.
- Read the API companion branch after its durable force-fence Slice 3A. Its
  API-owned authority fence is complete, but the real subprocess adapter does
  not yet create/pass the supervision envelope and control root or consume the
  suspension result; that work is intentionally deferred to API Slice 3B.
- Identified a release-pair dependency cycle in the original Slice 4 wording:
  SBE awaited the real API adapter while API awaited an exact packaged SBE
  candidate.
- Split Slice 4 into 4A SBE packaged-candidate qualification, intervening API
  Slice 3B real-adapter integration, and 4B joined release-pair qualification.
- Opened Slice 4A only. No API implementation, provider/R2/process action,
  resource release, tag, publication, or deployment is authorized.

## 2026-09-16 — Slice 4A source/package qualification surface

- Added a public installed qualification command,
  `astrowoof-native-suspension-qa`, and a closed packaged receipt schema.
- The qualification creates a disposable exact-interactive ordinary-v2
  workspace, launches the public v2 CLI as a real child process, consumes its
  exact output file, validates the immutable result/receipt/retained evidence,
  and repeats the command to prove replay identity.
- Added unrelated-workspace refusal and packaged schema/fixture readability
  checks. The qualification records zero provider create/retrieve, spend,
  network, live process termination, and API resource release.
- Exported the public contract readers/validators and qualification reader from
  the package root so API Slice 3B need not import private runtime helpers.
- Bumped the prospective candidate version to `0.4.65` before package testing.
- Source evidence: 3 qualification tests passed with 1 expected optional-schema
  skip; combined suspension/v2/reconciliation matrix 115 passed with 3 expected
  skips.
- Next: commit the exact candidate source, build/install a controlled wheel,
  and run the public qualification from site-packages. No tag/publication or API
  integration is authorized yet.

## 2026-09-16 — Slice 4A installed candidate complete

- Built prospective SBE `0.4.65` from source commit `5f5d9aa6` with
  `SOURCE_DATE_EPOCH=1789531794`.
- Candidate wheel: 1,407,338 bytes; SHA-256
  `6c5db7b3134805f74343b841ea50ace128c313ab8ac292196fdf483fa6b1ce6b`.
- Downloaded the immutable SPC `0.11.1` release wheel; its known SHA-256
  `dc345cd3253de333a5428e4fc7e24816447a065215ef288ba76527960a7da612`
  matched prior release evidence.
- Rejected an initial system-site venv as clean evidence when `pip check`
  exposed the host runtime's missing `jsonschema` dependency.
- Created a fresh venv, installed pinned SPC plus declared dependencies and the
  candidate wheel, and obtained a clean `pip check`.
- Proved SBE `0.4.65` imported from the fresh venv's `site-packages`; the
  installed qualification/schema console commands passed. Root public Python
  validation and packaged JSON Schema validation both accepted the receipt.
- Qualification SHA-256:
  `0282608bd9c0df8c3a4761b3f39a48df9bbdf9ead43c15cbe8cc3b4f16d134dd`.
  All safety counters were zero.
- Slice 4A is complete. Paused for API Slice 3B real-adapter integration before
  joined Slice 4B. No tag, publication, deployment, live API/R2/provider work,
  signal, process termination, or resource release occurred.

## 2026-09-16 — API Slice 3B ordering discovery reopens Slice 4A

- API correctly refused to synthesize a force fence before child launch. The
  original envelope required a fact that can lawfully arise only after an
  operator fences an already-running lease.
- Superseded prospective `0.4.65` wheel
  `6c5db7b3134805f74343b841ea50ace128c313ab8ac292196fdf483fa6b1ce6b`.
  It was never tagged or published and is not eligible for adapter intake.
- Corrected the unpublished v1 contract family in place: the launch envelope
  binds a pre-launch supervision capability; the later request binds that
  capability plus the independently admitted immutable force fence; result,
  receipt, and command result bind both.
- Regenerated the packaged fixture from the corrected closed documents.
- Focused executable contract/runtime/qualification matrix: 26 passed, 2
  expected optional-schema skips. No provider, API, R2, spend, process-kill,
  deployment, or release operation occurred.
- Slice 4A remains open pending a fresh prospective `0.4.66` candidate and
  installed qualification.

## 2026-09-16 — Corrected Alloy launch-order campaign

- Extended the shared model with explicit supervision capability and launch
  events, exact fence-to-capability binding, and strict
  capability-before-launch-before-fence-before-request ordering.
- Added a dedicated ordinary-result-dominance world for the interval after
  fence admission and before native observation.
- The first run found a cross-run resolution counterexample: a mismatched
  request's typed refusal could still be selected across its unrelated fence
  in the abstract resolution relation. Tightened selected-suspension resolution
  to require the exact capability/fence join.
- Final bounded Alloy 6.2.0 campaign: five inhabited scenarios SAT, twelve
  full-contract checks UNSAT, and nine deliberately weakened bad-world
  witnesses SAT. Model SHA-256:
  `f8c0a9afc7c258541d7d30b8596f6f73415c05c08074ba7ce003119f069d4064`.
- No candidate wheel was rebuilt. Renewed API review remains required before
  corrected Slice 4A packaging.
