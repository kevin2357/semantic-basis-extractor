# AstroWoof Natal Authoring Next-Release Sprint

```yaml
status: planned
started: null
owner: semantic-basis-extractor
target_distribution: astrowoof-natal-authoring
target_version: pending_slice_0_approval
target_tag: pending_slice_0_approval
predecessor_release: astrowoof-natal-authoring-v0.1.0
execution_authorized: false
live_provider_work_authorized: false
publication_authorized: false
```

## Outcome

Produce the next pinnable Semantic Basis Extractor and Semantic Closure wheel
from the already implemented source-identity, provider-spend, minimized
provider-disclosure, and durable-workspace contracts. Qualify the exact
installed artifact against the supported AGF 0.6 / SPC 0.10 input boundary,
then prepare an immutable API-consumer handoff.

This plan does not authorize sprint execution, billable provider work, version
changes, tagging, pushing a release tag, or publication. Work begins only after
explicit approval to start the sprint. Each slice pauses at its gate before a
commit or progression to the next slice.

## Release candidate scope

The candidate includes:

- opaque caller-owned source identities throughout extraction and authoring;
- Semantic Closure run schema `astrowoof.semantic_closure_run.v0.9`;
- durable per-run provider-spend ledger and prepare/authorize/execute seam;
- exact authorization binding, single-writer consumption, ambiguity handling,
  append-only reconciliation references, and profile-driven optional stages;
- minimized provider-visible subject identity;
- stable-logical-absolute-path resume with complete hashed snapshots;
- selected-card versus broader summary/whole-dog evidence provenance;
- projected-term registry merge, preservation, and closure validation; and
- installed-wheel deterministic and controlled-live qualification.

The candidate does not add unknown-time claim suppression, variable semantic
basis sizes, Quick/Complete product modes, hierarchy redesign, or new critic
product policy. Cross-run reservations, account quotas, global circuit
breakers, entitlements, and authoritative billing reconciliation remain owned
by the AstroWoof API.

## Proposed slices

### Slice 0 — Baseline and release-coordinate freeze

- Confirm a clean, reviewed source baseline and record its commit.
- Review current package metadata, contract catalog, release playbook, and API
  handoff documents against the implemented runtime.
- Select the release version and tag under semantic-versioning policy; update
  this plan before changing package metadata.
- Record the exact intended AGF, SPC, Python, provider-model, and price-book
  compatibility tuple without inferring undeclared upstream facts.
- Inventory release-affecting changes since v0.1.0.

Gate: approve release coordinates, exact compatibility tuple, and the final
slice sequence. No artifact build or runtime modification before this gate.

### Slice 1 — Contract and integration qualification

- Exercise exact AGF 0.6 / SPC 0.10 projected input with opaque UUID-style
  source identity.
- Prove identity propagation through selected claims, syntheses, authoring
  packets/state, delivery provenance, and consumer-visible manifests.
- Prove projected-term registry merge and closure remain fully validated.
- Prove selected-card evidence and broader summary/whole-dog evidence remain
  separately identified.
- Audit operator/public states for machine-distinguishable waiting, warning,
  review, authorization, budget exhaustion, ambiguous submission, and delivery
  outcomes while accepted evidence remains monotonic.

Gate: focused contract report, full relevant tests, clean diff, and approval.

### Slice 2 — Spend, disclosure, and snapshot safety qualification

- Test every paid route: initial interactive and Batch authoring, creative
  retry, polish, qualitative critic, and qualitative candidate.
- Failure-inject prepare, authorization persistence, single-writer
  consumption, provider submission, provider-ID persistence, settlement, and
  reconciliation boundaries.
- Confirm polling known provider work creates no new commitment.
- Verify actual provider idempotency claims remain no stronger than published
  guarantees.
- Verify protected birth/location fields are absent from all provider payloads
  and Batch files while retained in protected local provenance.
- Verify exact-path restore succeeds and missing, changed, additional,
  truncated, or relocated snapshots fail closed before provider work.

Gate: safety matrix and deterministic regression report approved. No live call.

### Slice 3 — Reproducible candidate artifact

- Update package/release coordinates approved in Slice 0.
- Build the wheel twice with a recorded reproducible-build environment.
- Compare bytes and SHA-256; inspect the complete wheel member allowlist.
- Confirm no sprint workspaces, provider payloads, secrets, protected subject
  values, caches, or generated run artifacts leaked into the wheel.
- Record package resources and aggregate resource identity.

Gate: byte-identical candidate artifact and package audit approved.

### Slice 4 — Clean installed deterministic smoke

- Install the exact candidate wheel into a fresh environment outside the
  checkout and outside the repository working directory.
- Run extraction, six-pass fake authoring, forced rejection/retry, separate-
  process resume, assembly, registry validation, final QA, delivery, snapshot
  validation, and cleanup.
- Exercise the API-facing prepare/authorize/execute contract without paid
  submission, including fail-closed legacy state and public status views.
- Verify the smoke input and output carry the approved AGF/SPC/identity tuple.

Gate: installed smoke report, artifact hashes, full suite, and approval.

### Slice 5 — Controlled live release candidate

- Obtain explicit live-provider authorization and an approved, non-illustrative
  per-run spend policy before preparing any paid action.
- Run one bounded installed-wheel subject through the intended production
  authoring route.
- Exercise detach/resume, authorization, provider polling, accounting, final
  QA, provenance, snapshot, and delivery behavior without bypassing gates.
- Compare result class, editorial quality, token usage, committed/reported
  spend, and provider disclosure with the approved baseline.
- Stop safely on budget exhaustion, ambiguity, review, or any unrecognized
  state; do not repair by weakening contracts during the run.

Gate: live QA report and explicit approval of any corrective change. A changed
candidate returns to the relevant deterministic and build slices.

### Slice 6 — Final artifact and consumer handoff

- Build the final wheel reproducibly from the approved commit.
- Clean-install it and rerun the complete deterministic release smoke.
- Produce release manifest, checksums, compatibility statement, release notes,
  API-worker installation/invocation handoff, and contract catalog.
- Confirm API ownership of cross-run/account policy and SBE ownership of
  per-run enforcement and reconciliation references.
- Verify all documentation names the same version, tag, artifact, hashes,
  schemas, price book, and compatibility tuple.

Gate: final artifact and handoff review. Tagging/publication remain unauthorized.

### Slice 7 — Tag and publication

- Only after explicit approval, commit final release records and create the
  annotated AstroWoof-scoped tag at the reviewed commit.
- Push the commit and tag, publish the non-draft release, and upload the wheel
  plus checksum assets.
- Download published assets through the real authenticated consumer path and
  independently verify sizes, hashes, tag target, and release metadata.
- Record publication evidence without moving the immutable tag.

Gate: published assets and authenticated download verification pass.

## Controls

- Follow `docs/sprints/README.md`: each slice produces an independently
  reviewable result and pauses for approval before commit/progression.
- Never treat the fifty-claim semantic budget as dollar spend.
- Dollar allocations in design examples are not defaults or authorization.
- No OpenAI submission without an exact durable authorization for that action.
- No retry of an ambiguous provider creation request based solely on a
  deterministic key.
- No live API call before the exact candidate passes installed deterministic
  qualification and the user explicitly approves the live run and budget.
- Preserve accepted evidence monotonically; never recreate accepted passes to
  make a resume test convenient.
- Test installed behavior without checkout imports or repository resources.
- Build from a clean source baseline and use an explicit wheel allowlist.
- Keep large runs and raw provider artifacts outside Git; preserve compact
  hashes and reports under `results/`.
- Do not change upstream/API ownership boundaries inside release engineering.
- Do not tag, publish, or alter an existing immutable release without explicit
  approval.

## Exit criteria

- the approved exact AGF 0.6 / SPC 0.10 / SBE tuple passes end to end;
- UUID-style source identity survives claims, synthesis, authoring, delivery,
  and installed smoke;
- registry merge/closure and both evidence scopes are verified;
- all public/operator outcomes and monotonic acceptance are verified;
- every paid route passes spend-boundary and failure-injection tests;
- provider disclosure and durable snapshot contracts pass their negative
  matrices;
- two final builds are byte-identical and the wheel allowlist is clean;
- a clean installed deterministic smoke passes outside the checkout;
- one explicitly authorized installed-wheel live run passes, unless the user
  explicitly waives live qualification with that exception documented;
- release and API handoff artifacts agree on all coordinates and ownership;
- the complete relevant test suite and `git diff --check` pass;
- the annotated tag is created only after final approval; and
- published assets are downloaded and independently verified.

## Planned result records

Each completed slice will add `results/SLICE N - <name>.md` plus compact JSON
evidence where useful. `LOG.md` will record commands, decisions, surprises,
approvals, commits, artifact identities, and any plan revision chronologically.
