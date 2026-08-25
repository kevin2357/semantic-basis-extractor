# Sprint Log

## 2026-08-24 — Sprint created

Created from the fresh QA temporal-lifecycle finding. The worker was suspended
after confirming the v2 request was valid but no paired execution command
existed. No implementation, provider work, retained-run mutation, or release
occurred in this sprint.

## 2026-08-24 — Detailed plan prepared

Expanded the sprint plan with the request-reference/grant/execution ownership
model, route/stage applicability audit, exact writer-versus-provider-I/O fence,
replay taxonomy, quiescent awaiting-grant semantics, holistic 4+2 qualification,
installed-wheel gate, and explicit API/owner review paws. No Slice 0 work began.

## 2026-08-24 — Plan approved; Slice 1 decisions recorded

- API and owner approved beginning Slice 0.
- Froze authorization documents as the sole complete-binding carrier. The compact
  v2 grant carries immutable document references/digests; SBE rederives binding
  digests and joins them to current inspection.
- Froze grant + selected inventory + all authorization consumption + submission
  intent as one complete native checkpoint publication unit.
- Removed any implication that no-grant quiescence asserts API-global consumer
  authority, reservation, lease, admission, or capacity facts.

## 2026-08-24 — Slice 0 contract and lineage audit

- Reproduced a real snapshot-valid v0.6 `ordinary_action_set` request through the
  public temporal lifecycle and v2 request builders.
- Proved the released provider-capable external-authority CLI remains the v1
  six-member initial-wave command and cannot execute the ordinary v2 request.
- Added the route/stage applicability matrix and kept optional Batch routes
  explicitly deferred/fail-closed.
- Froze complete authorization documents as the binding source, the atomic native
  checkpoint unit, refusal precedence, and native-only quiescent facts for review.
- No provider, retained-workspace, network, credential, or spend operation occurred.

## 2026-08-24 — Slice 1 closed v2 grant and passive result

- Added strict grant and passive-result schemas, Python builders/validators/readers,
  catalog entries, public exports, and a sanitized packaged contract fixture.
- Made lexical `action_id` order normative in v2 request validation, not incidental
  builder behavior.
- Kept complete bindings solely in ordered ordinary authorization documents; grant
  members carry only binding/document digests and authorization references.
- Required one homogeneous provider mechanism per ordinary action set.
- Added a strictly non-dispatching no-grant result with four false side-effect flags
  and no API-global authority/capacity claims.
- Added focused mutation, cross-version, schema, replay, privacy, and read-only
  coverage. No native executor or provider path was added in this slice.

### Slice 1 API clarification

- Added explicit `request_schema_version` to the v2 grant and froze it to
  `astrowoof.external_authority_request.v2` in schema, semantic validation,
  fixtures, and mutation coverage.

## 2026-08-24 — Slice 2 native intent fence

- Added writer-fenced revalidation of the restored snapshot, current v0.6 basis,
  request, aggregate grant, complete authorization documents, native inventory,
  action state, provider evidence, and consumption.
- Published authorization consumption and `SUBMITTING` intent for the complete
  lexical inventory as one candidate native checkpoint before provider I/O.
- Added the strict packaged `astrowoof.external_authority_intent_result.v2`
  contract binding request/grant, revisions, inventory, and post-snapshot digest.
- Proved failure before persistence is nonmutating and interruption between state
  and snapshot leaves a fail-closed snapshot-invalid workspace containing the
  complete unit rather than a valid partial checkpoint.
- Proved provider evidence/ambiguity precedence, stale/binding refusal, and
  no-second-checkpoint replay behavior.
- No provider I/O, retained-QA access, network, credential, or spend operation
  occurred. Paused for API review before Slice 3 provider dispatch.

## 2026-08-24 — Slice 3 provider dispatch and replay fence

- Added persisted-intent-selected ordinary provider dispatch outside the native
  writer; callers cannot supply or narrow the action subset.
- Added a durable per-member `CALL_ENTERED` fence, immediate returned-identity
  checkpoint, and cursor advancement before the next create is permitted.
- Added conservative ambiguity for entered-call exceptions, process interruption,
  competing dispatchers, missing/invalid identities, and duplicate identities.
- Added exact zero-I/O replay after the complete provider identity inventory is
  durable and safe continuation only for members proven unentered by the cursor.
- Added the strict packaged provider-dispatch result schema/validator and public
  exports.
- Proved lifecycle transitions to the existing reconciliation-only command after
  identities become due; no provider-result ingestion path was added.
- Added failure-isolated redacted events and sink-failure coverage.
- Focused result: 50 tests passed. No OpenAI/network/credential/spend/retained-run
  operation occurred. Paused for API review before Slice 4.

## 2026-08-24 — Slice 4 route and holistic lifecycle qualification

- Qualified exact and bounded interactive v2 execution for creative retry, polish,
  qualitative critic, and qualitative candidate actions.
- Added same-workspace exact/bounded traces from six initial scripted creates
  through real SBE-selected 4+2 reconciliation into v2 request/grant/intent,
  ordinary dispatch, durable identity, and due reconciliation selection.
- Moved adapter eligibility into the writer-fenced preflight so unsupported Batch
  or route/stage cells refuse before authorization, consumption, intent, or I/O.
- Froze v2 ordinary Batch as deferred/fail-closed for the first release while
  preserving the existing exact/bounded initial-wave Batch mechanisms.
- Re-ran the existing deployed four-route and provider-pending qualifications.
- Focused result: 59 tests passed. No OpenAI/network/credential/spend/retained-run
  operation occurred. Paused for API review before Slice 5 packaging.

## 2026-08-24 — Slice 5 source packaging

- Added the supported v2 CLI with passive no-grant and constrained OpenAI
  create-only modes.
- Added strict snapshot-bound prepared-payload resolution by exact request digest;
  missing, changed, or duplicate payload matches refuse before provider work.
- Added a closed joined command-result contract and safe exact command replay.
- Added the provider-free installed-wheel qualification command and closed receipt,
  covering exact/bounded 4+2 bridges and all four ordinary Response stages.
- Published the API consumer handoff with prominent deliberate ordinary-Batch v2
  deferral guidance.
- Built two byte-identical nonpublishable candidate wheels, installed the candidate
  into an isolated environment, and passed `pip check`, generic installed smoke,
  and the provider-free v2 qualification command.
- The installed receipt proves exact/bounded 4+2 bridges, all four ordinary
  interactive Response stages, next reconciliation selection, and explicit
  ordinary-Batch refusal.
- The full suite exercised all 655 tests. Its only failure was a pre-existing
  frozen-artifact test hashing Windows CRLF checkout bytes against a canonical-LF
  manifest. The test now canonicalizes line endings and its focused regression
  passes; no runtime or frozen artifact changed.
- No version bump, tag, publication, real provider operation, credential use,
  spend, or retained-run access has occurred. Final API/owner release review is
  the next gate.

## 2026-08-24 — Final review cleanup and release authorization

- API and owner approved the v2 contract, fence, dispatch/replay model, passive
  waiting behavior, deliberate ordinary-Batch deferral, qualification, and handoff.
- Removed duplicate command-result constants/builders/validators/readers and the
  duplicate lexical-order predicate without changing behavior.
- Bumped the fresh release version to `0.4.20`; immutable `0.4.19` remains intact.
- Fast focused source gate: 33 tests passed with 2 expected optional-schema skips.
- Release/tag/publication authorized subject to the fresh committed-source wheel,
  installed qualification, and artifact checks.
