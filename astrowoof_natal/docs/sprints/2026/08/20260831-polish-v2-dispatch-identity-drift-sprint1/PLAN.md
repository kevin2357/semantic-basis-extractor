# Plan — polish v2 dispatch identity drift

## Status

Slices 0–6 complete and published as SBE `0.4.34`. The authorized generation-11
`HEAD` and `GET` are complete; no
external provider activity, remote write, retained worker execution, or
retained-run mutation occurred.

## Objective

Explain why the first post-authoring polish v2 dispatch produced several
request-digest observations and refused with
`action_state_or_custody_mismatch` / `authorization_mismatch` despite a coherent
API action, admission, request, and grant chain. Freeze the native/API invariant,
reproduce the general seam provider-free, and make only the narrow correction
supported by evidence.

## Non-goals

- Recovering, resuming, denying, or retiring Delerium.
- Selecting one trace hash as authoritative because it appears latest.
- Calling OpenAI or creating/retrieving provider work.
- Reinterpreting API reservation, lease, slot, or global capacity facts.
- Weakening exact v2 request/grant/inspection/action joins.
- Permitting generic resume to create polish work.
- Expanding Batch, bounded, or initial-wave behavior without evidence that the
  same defect and correction apply.
- Completing or releasing the separately planned general checkpoint-inspector
  product during this incident investigation.

## Relationship to checkpoint-inspector tooling

The planned general inspector lives in
`20260830-native-checkpoint-read-only-inspector-tooling-sprint1`. This sprint
will treat its existing one-off readers as characterization input and will feed
new requirements back to that plan. The current investigation may extract a
small read-only helper only when all of the following are true:

- it uses existing strict native validators;
- it accepts an already-restored local workspace, not credentials or remote
  coordinates;
- it performs no extraction, writer acquisition, execution, publication, or
  provider work;
- its output is incident-local until the general schema is reviewed; and
- extraction does not delay the causal investigation or imply a supported
  installed public surface.

## Invariants to preserve

1. One materialized request digest identifies one exact closed request object.
2. Repeated inspection of one immutable checkpoint basis and action inventory
   reproduces the same v2 authority request identity.
3. A changed checkpoint basis or ordered inventory produces a new request and
   invalidates the prior grant; it does not mutate the prior request.
4. Provider-capable execution remains constrained to an exact validated
   inspection/request/grant/authorization-document join under the native writer.
5. Provider identity, submission ambiguity, and consumed authorization outrank
   new provider creation.
6. A pre-provider refusal performs zero provider I/O and cannot become an
   implicit generic retry loop.
7. The API action state `authorized` does not prove the native action is
   dispatchable; native `PREPARED`, providerless, unconsumed evidence must be
   validated independently.
8. Logs explain branch selection but never override persisted evidence.

## Slice 0 — evidence freeze and production-boundary characterization

Deliverables:

- Hash and inventory the supplied background and Render trace export without
  copying protected payloads into sprint artifacts.
- Extract a sanitized ordered timeline for the creative-retry reconciliation,
  finalization, polish preparation, inspection, API grant, and v2 refusal.
- Map each observed hash to the exact code field and producer that logged it;
  classify unknown labels rather than assuming all are request identities.
- Trace the current production call path from API-provided files through
  `astrowoof-external-authority-v2`, writer reinspection, dispatchability checks,
  grant validation, intent persistence, and dispatch.
- Characterize whether current source can produce multiple request identities
  at one state revision solely through time, path normalization, inventory
  ordering, or changed checkpoint facts.
- Build a minimal provider-free characterization fixture from public contracts
  if source evidence alone can reproduce the refusal; do not yet alter runtime.
- Produce a validator-reuse/gap note for the general checkpoint-inspector
  sprint, including the exact request/inspection/action/grant joins needed by
  this incident.

Gate:

- Publish a source/trace identity map and list the exact retained fields still
  needed.
- Pause at **Oauf-paws 1** before protected checkpoint access or contract
  conclusions.

## Slice 1 — bounded read-only checkpoint inspection

Prerequisites:

- Revalidate the exact coordinate packet and storage identities in
  `Background.md`.
- Confirm the four R2 variables are present without printing their values.
- Record the approved object UUID, expected archive SHA-256, bytes, inventory
  SHA-256, ETag/provider version, and access budget before access.

Access:

- Perform exactly one `HEAD` and one `GET` for generation 11.
- Verify content length, ETag/provider identity where stable, archive digest,
  archive safety, inventory digest, compatibility identity, logical root, native
  run ID, and checkpoint generation before reading native evidence.
- Do not list the bucket or access another object implicitly.
- Retrieve generation 10 only after documenting a concrete differential question
  that generation 11 cannot answer; if used, apply the same one-`HEAD`/one-`GET`
  budget and validations.

Inspection targets:

- native polish action state, binding, authorization, consumption, provider, and
  request-payload reference;
- external-authority v2 intent, if any;
- stored lifecycle/temporal inspections and authority requests, if any;
- state revision and snapshot basis that produced the prepared polish action;
- creative-retry pass/action lineage and the post-reconciliation ambiguity fact;
- journal/result/receipt boundaries around finalization and polish preparation;
- exact canonical objects corresponding to `07300…`, `c5ac68…`, and `a838af…`,
  when present.

Outputs:

- Access manifest and receipt containing only hashes, sizes, object identities,
  and validation results.
- Sanitized retained-state projection with exact provenance pointers.
- Explicit evidence ceiling for any missing request/grant/inspection bytes.
- A tooling delta describing which incident-local parsing should later become
  general inspector behavior and which fields must remain private.

Gate:

- Pause at **Oauf-paws 2** for API review of the native/API join before causal
  classification.

## Slice 2 — causal and identity matrix

Construct a field-level matrix across:

- generation 11 native truth and the frozen generation-10 predecessor identity;
  retrieve generation 10 only if generation 11 cannot classify the defect;
- each persisted or reconstructed lifecycle inspection;
- each external-authority request object/digest;
- API admission/request/grant/member authorization evidence;
- native polish action binding/state/custody;
- v2 intent or absence;
- command/event/log observations.

The matrix must distinguish:

- immutable object identity from observation identity;
- checkpoint-basis change from time-only reinspection;
- API authorization state from native dispatchability;
- request digest from payload/binding/grant/inspection digests;
- creative-retry lineage ambiguity from polish action authority;
- proven cause, contributing condition, adjacent defect, and unknown fact.

Decision outcomes:

- **SBE runtime defect:** current native ordering or persistence can produce the
  contradictory state through supported commands.
- **API invocation/join defect:** native public evidence is coherent but files or
  identities supplied to the v2 command are from incompatible observations.
- **cross-repository contract gap:** each side is locally valid but no public
  artifact prevents the incompatible join.
- **diagnostic-only confusion:** runtime is correct and trace labels conflate
  unrelated digests.
- **historical evidence ceiling:** no stable causal selection is possible.

Gate:

- Pause at **Oauf-paws 3** before designing a contract or runtime correction.

Frozen retirement invariant:

- The singleton intent denotes only current live v2 dispatch authority.
- It may be retired only under the writer after the complete intent inventory
  exactly joins terminal ledger, authorization, consumption, provider,
  reconciliation, reported-usage, and retained-response evidence.
- Retirement archives the complete predecessor identity/evidence and frees the
  live slot in the same writer-fenced checkpoint that first makes the complete
  terminal reconciliation/reporting evidence durable. It is not delayed until
  a successor asks for the slot.
- Pending, submitting, partial, ambiguous, conflicting, or missing evidence
  retains/refuses/reviews and can never be cleared to admit a successor.
- Exact replay of a retired request/grant is answered from immutable retirement
  history and can never create provider work.
- Successor-time repair may recognize and retire a historically stranded but
  completely terminal intent as a compatibility path. It is not the normal
  steady-state lifecycle and must satisfy the same exact terminal join.

## Slice 3 — provider-free production-path reproduction

Using sanitized synthetic identities, exercise the real public boundaries:

1. complete and reconcile a creative retry;
2. consume completed evidence and finalize authoring;
3. prepare exactly one polish action;
4. inspect and export the exact v2 request;
5. build a matching grant and authorization document outside the workspace;
6. reopen in a fresh runtime and invoke the real v2 command with a scripted
   provider transport;
7. assert either one lawful create/detach or the exact reproduced typed refusal;
8. replay and prove no duplicate provider creation.

Perturbations must include:

- same basis/time and same basis/later time;
- stale inspection with current request;
- current inspection with stale request/grant;
- changed action binding with recomputed outer digests;
- native action `PREPARED`, `AUTHORIZED`, `SUBMITTING`, consumed, provider-bound,
  and ambiguous states;
- duplicate or absent native intent;
- post-reconciliation creative-retry ambiguity present/absent;
- event/log sink failure and privacy sentinels.

The fixture must use the installed/public command where practical and must never
perform external provider/network activity.

Gate:

- Pause at **Oauf-paws 4** with a minimal counterexample and proposed invariant.

## Slice 4 — contract freeze and joint handoff

Freeze, with API review:

- the authoritative request identity and its exact observation/basis join;
- native dispatchability requirements and refusal precedence;
- whether repeated inspection may lawfully yield a new request and under what
  changed facts;
- API command-file identity requirements;
- exact typed no-I/O disposition for stale/mismatched authority;
- whether the creative-retry ambiguity is causal and in scope;
- compatibility behavior for SBE 0.4.33 retained workspaces.

Prefer existing closed schemas and typed outcomes if they already express the
truth. Introduce a new public version only if the required fact cannot be
represented without widening a closed artifact.

Gate:

- **Oauf-paws 5:** explicit API/owner approval before runtime mutation.

Decision recorded:

- Normal retirement is internal native history plus the existing public
  `exact_replay` outcome; no API contract version change is required.
- The real integration point is the writer-fenced coordinator quiescent
  checkpoint after complete reconciliation/reporting truth becomes durable.
- Successor admission is not the steady-state retirement trigger.
- The proposed closed record, replay precedence, compatibility posture, and
  failure matrix are frozen in
  `SLICE 4 - RETIRED INTENT CONTRACT AND RUNTIME INTEGRATION DESIGN.md`.

## Slice 5 — narrow correction

Only if SBE or shared contract work is required:

- Correct ordering/persistence/identity construction at the earliest safe
  boundary.
- Revalidate the exact current action/request/grant under the writer before any
  mutation or provider I/O.
- Seal pre-provider refusal or review evidence before command exit.
- Preserve exact replay, ambiguity, provider-custody precedence, and generic
  resume refusal.
- Add focused regressions for the minimal counterexample and all adjacent safety
  states.

If the defect is API-only, close this slice as `not_applicable` and provide the
fixture/contract handoff without modifying SBE runtime.

Gate:

- **Oauf-paws 6:** API review of implementation and consumer fixtures.

Result:

- Implemented exact-interactive coordinator-checkpoint retirement, strict
  internal history, exact replay, and the provider-free safety matrix.
- Did not add historical compatibility repair, public schemas, initial-wave or
  Batch behavior, or bounded-route integration.
- Handoff: `SLICE 5 - INTENT RETIREMENT IMPLEMENTATION AND HANDOFF.md`.

## Conditional Slice 6 — installed qualification and release decision

Only if SBE code or packaged public artifacts change:

- Publish closed, privacy-bounded fixtures and a provider-free installed-wheel
  receipt.
- Prove exact request/grant success, stale/mismatch refusal, native-state
  precedence, replay, zero duplicate create, and zero external network/spend.
- Run a risk-proportionate focused/broad gate agreed before testing.
- Freeze the fresh version before any release suite to avoid release-derived
  fixture churn.
- Obtain separate final owner/API approval before commit/tag/publication.

If no SBE release is needed, close with an investigation handoff and no version
change.

Result:

- Frozen candidate version `0.4.34` before release qualification.
- Added the packaged `astrowoof-v2-intent-retirement-qa` command, closed receipt
  schema, Python reader/validator, and installed-resource tests.
- Proved durable coordinator-checkpoint retirement, exact inert replay, exactly
  one fresh-successor create, incomplete evidence retention, and contradictory
  identity refusal without external network or spend.
- Built two byte-identical candidate wheels and passed installed smoke plus the
  affected installed qualification set.
- Paused for the separate final release gate; no commit, tag, or publication is
  authorized by this result alone.

## Test strategy

- Source and trace characterization before protected access.
- Exact-object, hash-verified, read-only retained inspection.
- Provider-free tests through real public entrypoints.
- Fresh-runtime restore between lifecycle phases.
- Rehashed semantic mutations, not only broken outer hashes.
- Explicit provider-call counter fixed at zero for investigation/refusal paths.
- Privacy sentinels across stdout, stderr, events, fixtures, and receipts.
- Deterministic repeatability for any packaged qualification.

## Review points

1. Oauf-paws 1 — source/trace map and protected-access need.
2. Oauf-paws 2 — retained native/API join.
3. Oauf-paws 3 — causal classification.
4. Oauf-paws 4 — reproduction and invariant.
5. Oauf-paws 5 — contract freeze before mutation.
6. Oauf-paws 6 — implementation/consumer handoff.
7. Final release review, only if an SBE artifact changes.
