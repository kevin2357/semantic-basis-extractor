# Native Worker Change Playbook

```yaml
status: accepted
owner: semantic-basis-extractor
scope: safely planning, implementing, qualifying, releasing, and jointly integrating native-worker changes
last_reviewed: 2026-08-30
```

## Purpose

Use this playbook when changing semantic-basis extraction, bounded-Natal
extraction, authoring, paid-provider orchestration, lifecycle control, native
workspace persistence, delivery, or the public evidence consumed by AstroWoof API.
It is written for human maintainers and agents new to the repository who need a
safe starting process without reconstructing current invariants from sprint logs.

This guide is not transition authority. Installed, versioned contracts and validated
native artifacts define SBE behavior. Sprint records explain how a boundary was
designed and qualified. Release-specific records identify the exact immutable
implementation. If those sources disagree, stop and reconcile them explicitly.

The first half of this document concerns SBE-owned native-worker development. The
second half concerns joint SBE/API work and the boundary between native execution
truth and API orchestration authority.

## Read before planning

For any non-trivial native change, read these first:

1. [SBE Authoring Execution and Authority Model](SBE%20Authoring%20Execution%20and%20Authority%20Model.md)
2. [Runtime Contracts](Runtime%20Contracts.md)
3. [Semantic Closure Runner](Semantic%20Closure%20Runner.md)
4. [Authoring Lifecycle Consumer Handoff](Authoring%20Lifecycle%20Consumer%20Handoff.md)
5. [Provider Spend Enforcement](Provider%20Spend%20Enforcement.md)
6. [Spend Authorization Consumer Handoff](Spend%20Authorization%20Consumer%20Handoff.md)
7. [Provider Disclosure and Durable Workspace Contract](Provider%20Disclosure%20and%20Durable%20Workspace%20Contract.md)
8. [Maintainer Release Playbook](Maintainer%20Release%20Playbook.md)
9. [Adversarial Lifecycle Simulation Playbook](Adversarial%20Lifecycle%20Simulation%20Playbook.md)

Also read the current release notes, compatibility statement, API handoff, known
limitations, manifest, and packaged contract catalog. For a shared boundary, read
the applicable recent SBE sprint and the API's current pipeline change playbook,
state/evidence model, transition oracle, and worker invocation contract.

Read only the focused extraction references needed by the change. Exact-Natal
selection policy starts with
[Semantic Basis Extractor Pipeline and Scoring Metrics](../extractor/Semantic%20Basis%20Extractor%20Pipeline%20and%20Scoring%20Metrics.md).
Bounded-Natal work must also read the bounded sprint handoff and official SPC
bounded contracts rather than applying exact-chart assumptions by analogy.

# Part I — Changing the native worker

## Native guiding lights

- **Native evidence owns native truth.** `run.json`, the paid-action ledger,
  accepted-pass evidence, provider identities, transition journal, snapshots,
  immutable results, publication receipts, and delivery manifests each have
  documented roles. Logs, stderr, exit codes, filenames, and test fixtures do not
  replace those artifacts.
- **Run authority is frozen.** A run remains bound to its authoring/generation
  profile, route, model configuration, price book, ceilings, and compatibility
  identities. New defaults apply to new runs; they do not silently rewrite active
  or retained runs.
- **Accepted evidence is monotonic.** Resume may add evidence or advance state. It
  must not demote accepted passes, replace provider identity, discard reported
  usage, weaken provenance, or reinterpret an earlier terminal outcome.
- **Every paid submission starts with exact authority.** A new provider operation
  requires one durable prepared action and exact external authorization. Polling an
  existing provider identity is not a new commitment.
- **Ambiguity is a result, not a retry hint.** If submission may have occurred but
  no provider identity is durable, report ambiguous submission and fail closed.
  Deterministic local keys are not proof of provider idempotency.
- **One writer consumes authority.** Native run mutation and authorization
  consumption are single-writer operations. API leases are external declarations;
  SBE must still use its local locks and stale-observation checks.
- **Snapshots attest quiescent workspaces.** A ledger/state write during provider
  work is not automatically a resumable checkpoint. The coordinator publishes a
  complete snapshot only after the transition's mutations settle.
- **Publication is validated composition.** Journal range, immutable command
  result, snapshot/checkpoint basis, and later content-addressed receipt must
  validate together. This is an atomic publication protocol, not literal atomicity
  across several filesystem files.
- **Provider-visible data is minimized at the last boundary.** Protected subject
  parameters and provenance stay local unless a documented editorial requirement
  changes the allowlist and the provider-disclosure inventory.
- **Routes are explicit policies.** Exact Natal, bounded Natal, Responses, and
  Batch share infrastructure only where their contracts agree. Unsupported
  combinations are rejected rather than approximated.
- **Authoring fan-out is an editorial invariant.** Five isolated ten-card story
  contexts plus a separate summary/theme context prevent bulk short-form work from
  collapsing into templated prose. Concurrency may be reduced, but a transport or
  scheduler refactor must not merge those logical contexts into one model request.
  For a frozen route assignment, interactive and Batch use the same pass membership,
  ordering, instructions, writable schema, retry feedback, and assembly semantics;
  only provider submission and retrieval differ.
- **Artifacts are products, not incidental files.** Contract schemas, guidance,
  profiles, fixtures, reference data, event vocabularies, and package typing are
  part of the released runtime and must be qualified with the Python code.

## Classify the proposed change

Before editing, identify every affected category:

1. extraction admission, scoring, selection, or synthesis;
2. authoring/editorial policy or provider-visible request content;
3. provider submission, retrieval, Batch handling, or reconciliation;
4. spend preparation, authorization, consumption, accounting, or denial;
5. native lifecycle/status, closeout, or terminalization;
6. snapshot, journal, result, receipt, repair, or workspace restoration;
7. delivery, provenance, public projection, or consumer contract;
8. package/resource/typing/CLI surface; and
9. API-owned behavior that SBE must expose evidence for but must not implement.

Name the current authority for every changed fact. State whether the change can
submit provider work, alter spend commitment, mutate a retained workspace, change a
schema, invalidate old runs, or affect a downstream consumer. If any answer is
uncertain, investigate before selecting an implementation.

## Plan before implementing

For a change beyond a small isolated defect:

1. Create a dated sprint directory with `PLAN.md`, `LOG.md`, `EVIDENCE.md`, and a
   `results/` index.
2. Reproduce the issue provider-free when possible. Preserve the original run as
   forensic evidence; create a sanitized fixture rather than repairing history.
3. Inventory the legal, stale, duplicate, interrupted, malformed, terminal, and
   legacy paths.
4. Freeze closed vocabularies, schema versions, idempotency/replay tuples, ownership,
   requiredness, route/mechanism support, and refusal behavior before runtime code.
5. Split implementation from consumer surfaces, cross-platform qualification, and
   release work. Put explicit review gates between them.
6. State which tempting adjacent changes are deferred so a safety fix does not
   become an unbounded redesign.

Prefer the smallest policy seam that preserves future extensibility. Shared
mechanics may be factored into route-neutral functions, but exact-Natal and
bounded-Natal admission/selection policies should remain explicit. Do not generalize
away epistemic differences merely to reduce file count.

## Preserve extraction and evidence semantics

- Validate embedded input identity and contract metadata; filenames are discovery
  labels, not semantic authority.
- Preserve caller-owned opaque source identity through claims, synthesis,
  authoring state, delivery, and provenance.
- Keep selected-card evidence distinct from broader summary/whole-dog evidence.
- Preserve projected-term registry merge, completeness, and closure validation.
- Keep exact-Natal scoring and bounded-Natal editorial-only selection policies
  distinguishable. Do not invent structural confidence for bounded invariants.
- Admit only bounded invariants. Never reconstruct midpoint placements, exact
  houses/angles, strength, confidence, or suppressed temporal detail.
- Keep claim count/basis-size policy explicit and tested. Do not conflate the
  semantic claim budget with dollar spend ceilings.
- Treat provider-written prose as editorial output. Reattach immutable claim
  authority, registry content, evidence, and provenance deterministically.

## Preserve paid-provider safety

Every new paid action must bind at least:

- action and run identity;
- exact request digest;
- generation profile and profile digest;
- prepared native state revision;
- route, provider mechanism, and stage;
- model/service level and maximum output;
- commitment in integer micro-USD;
- versioned price book; and
- external authorization reference.

Authorization consumption is single-writer and exact-binding. A mismatched, stale,
duplicated, unknown, already provider-bound, consumed, reported, or ambiguous action
must fail closed.

Track these separately:

- committed cost before submission;
- provider-reported usage/cost when available;
- SBE estimates with their basis;
- usage unavailable or billing reconciliation pending; and
- append-only external reconciliation references.

Never represent unavailable Batch usage as reported `$0.00`. Do not create a new
commitment while polling known provider work. Keep authoring initial, creative retry,
polish, critic, and qualitative candidate as separate stages. Optional-stage
skipping is generation-profile policy; required-stage external denial must reach a
typed terminal non-delivery outcome rather than an infinite continuation loop.

SBE owns its immutable per-run ceiling and native accounting. It does not own
cross-run reservations, account quotas, entitlements, global circuit breakers,
capacity allocation, authoritative provider billing, or product publication policy.

## Preserve lifecycle and capacity semantics

Keep these concepts separate:

1. local execution capacity;
2. provider retrieval/provider-pending custody; and
3. consumer reservation, financial, or review authority.

A safe worker-release checkpoint does not release provider or consumer authority.
A terminal provider operation may need no more polling while unavailable usage or
integrity conflict still requires API authority. Delivery may be available while a
nonblocking critic remains provider-pending.

Lifecycle inspection must carry validated route family, provider mechanism,
operation binding, timing, checkpoint, action/stage, and custody classification.
Consumers must not infer native route from their requested product record.

`resume_not_before` is SBE's durable lower-bound recommendation. An early cycle
returns a typed nonmutating `not_due` result. Retrieval cycles must have explicit
per-call and per-cycle wall-clock bounds. When due work exceeds one cycle, persist
what was handled and schedule remaining work without a tight loop.

Providerless denial is allowed only after exact eligibility preflight proves no
provider identity, consumption, reported usage, or ambiguity. Batch denial validates
every member before mutation and applies all or none. Required external spend denial
terminalizes as budget exhaustion with a distinct cause; product cancellation or
policy refusal remains a distinct policy stop. Optional profile-driven skipping does
not terminalize the run.

Preserve two denial lists when a successful ordered batch causes a run transition:

- `denied_action_ids` is the complete ordered denial history for audit and
  diagnostics; and
- `required_action_ids` is the exact causal subset whose requiredness triggered
  terminalization.

Do not infer causality from the broader history or omit optional members merely
because they did not determine the run-level disposition.

## Preserve workspace and publication integrity

- Restore a resumable workspace at the stable logical absolute root recorded by the
  run. Path rebasing is unsupported unless a future contract explicitly adds it.
- Validate every authoritative snapshot member and reject missing, changed,
  additional, truncated, or relocated content.
- Exclude only narrow documented ephemeral/receipt namespaces. Never introduce a
  broad ignore-extra-files rule.
- Keep the snapshot-excluded `native-publication-receipts/` namespace in complete
  durable consumer capture.
- Validate a just-written full snapshot against actual workspace bytes before
  sealing its publication receipt.
- Bind receipts to result ID/hash, full snapshot hash, checkpoint-basis hash,
  journal-range hash, run/invocation IDs, and logical root.
- Use a bounded journal range as command correlation. Do not require every projected
  provider record to carry the command's invocation ID.
- Treat `--latest` as discovery only. Exact ingestion re-reads and validates the
  requested result ID.
- Keep inspection/export provider-free and workspace-read-only. Any explicit output
  path must resolve outside the run directory.

Failure between files is expected. Readers expose a result only when the complete
publication validates. Exact provenance-bound orphan reconstruction may project a
missing journal/result/receipt once; it must never bless arbitrary bytes or replace
an already conflicting publication.

## Evolve contracts deliberately

- Additive fields are safe within a version only when existing strict consumers can
  accept them. If a consumer validates exact top-level keys, use a new version.
- Meaning changes, new required fields, renamed values, or changed closed
  vocabularies require a new schema/contract version.
- Keep result outcomes, causes, requiredness, custody, cost disposition, and refusal
  reasons machine-distinguishable.
- Preserve historical-reader compatibility explicitly or reject old artifacts. Do
  not silently migrate legacy paid authority.
- Document which artifact is stable consumer contract and which fields are
  candidate-generation or observational conveniences.
- Events are redacted, bounded, failure-isolated observations. They never authorize
  state transitions or replace native artifacts.

## Treat labels as coordinates, not decisions

Descriptive words such as `sealed`, `terminal`, `review_required`, `pending`,
`complete`, `failed`, and `unsupported` are not standalone transition authority.
The same word may occur in an integrity contract, native editorial result, provider
operation, lifecycle scheduler, API product record, or diagnostic event with
different scope.

For every consumer decision, maintain a semantic decision registry that names:

- the exact schema/version and installed wheel identity;
- exact required fields and their closed values;
- the positive permission being consumed;
- every run/action/binding/provider/invocation/result/receipt/snapshot join;
- additional API-owned lease, reservation, settlement, or publication facts;
- distinct behavior for absent, contradictory, and unknown-version evidence; and
- the forbidden inference that a tempting label, null, empty list, presence check,
  exit code, or default branch would otherwise invite.

Keep these decisions in separate registry rows even when one transaction performs
several of them:

1. accept and persist a native terminal result;
2. terminalize an API job/run/reading;
3. release local capacity or a lease;
4. retain/release provider or consumer authority;
5. settle billing; and
6. publish delivery.

An exact invocation-returned result identity outranks exit code and generic
discovery. Availability discovery is permitted only in a named preflight/recovery
path when no invocation identity exists; the discovered exact result must still be
read and fully validated. Normal ingress must not contain a generic “latest sealed”
fallback.

Absence is not negative permission. A missing readiness value cannot become local
continuation; an empty provider inventory cannot prove terminality; no local
dependencies cannot disprove deterministic fan-in; and a failed outer product state
cannot imply that provider custody, settlement, or publication is complete.

## Test failure boundaries, not only outcomes

For lifecycle, provider-custody, authority, wrapper, or scheduler-facing changes,
use the adversarial simulator before relying on another paid QA cohort. Add the
affected transition to the semantic oracle, prove its event admissibility, and test
stutter, cycle, contradiction, and starvation behavior where applicable. A shared
boundary must also run through the API's real translator and persistence services;
an SBE-only receipt cannot claim API lease or fairness behavior. Follow
[Adversarial Lifecycle Simulation Playbook](Adversarial%20Lifecycle%20Simulation%20Playbook.md).

Inject interruption before and after:

- prepared-action and authorization-request persistence;
- single-writer authorization consumption;
- provider submission and provider-ID persistence;
- provider terminal evidence and usage persistence;
- ledger-to-journal projection;
- native mutable-state/public-state writes;
- final/QA artifact mutation;
- complete snapshot write and post-write validation;
- immutable result write;
- publication-receipt write; and
- cleanup/closeout transition.

After each interruption, prove exact replay or an explicit fail-closed state. Replay
must not duplicate provider work, commitments, journal transitions, terminalization,
or delivery. Exercise stale observations and concurrent writers separately from
ordinary replay.

## Native qualification ladder

Advance only after the preceding layer passes:

1. focused unit/schema/truth-table tests;
2. provider-free route/stage/failure matrix;
3. complete repository suite;
4. two fixed-epoch byte-identical wheel builds;
5. wheel inventory, resource, schema, fixture, entry-point, and `py.typed` checks;
6. installed Windows Python 3.11 `pip check`, lifecycle smoke, and release smoke;
7. installed Linux Python 3.11 equivalent in a clean container;
8. exact upstream wheel/version/hash compatibility checks; and
9. controlled paid QA only when authoring/provider behavior materially requires it
   and Kevin separately authorizes the exact ceilings/cohort.

Use fake provider identities and scripted transports for deterministic qualification.
Patch provider/network entry points to fail if a provider-free test unexpectedly
attempts network access. Record provider-operation count and spend even when both are
zero.

At every slice gate, update the full plan, log, evidence ledger, results index, and a
compact slice result. Link all of them for review. A defect found during a gate is a
successful QA result: add a regression test, rerun the affected layers, and never
waive the invariant because the release is nearly ready.

## Release the installed product, not the checkout

Follow [Maintainer Release Playbook](Maintainer%20Release%20Playbook.md). In
particular:

1. Obtain explicit release authorization after implementation/consumer review.
2. Create an artifact-source commit containing the exact package version and source.
3. Build twice from that commit with its fixed `SOURCE_DATE_EPOCH`.
4. Run source and installed Windows/Linux gates against the exact intended upstream
   wheels.
5. Record wheel bytes, entries, resource count, cache count, SHA-256, source commit,
   compatibility, tests, provider count, spend, and limitations.
6. Create a later release-lock commit containing the final manifest/checksum/handoff.
7. Create an annotated component-scoped tag targeting that release-lock commit.
8. Publish the exact qualified wheel and checksum.
9. Download the published assets independently and reverify their hashes.
10. Record publication evidence in a later ordinary commit without moving the tag.
11. Remove only the exact verified temporary qualification tree and confirm a clean
    repository boundary.

The artifact-source commit, release-lock/tag commit, and post-publication evidence
commit are intentionally different identities. Never claim that a post-publication
documentation commit is the immutable release tag.

## When a native run behaves unexpectedly

1. Stop ordinary retry or resubmission.
2. Preserve the exact workspace, logical root, snapshot, journal, result/receipt
   namespace, provider IDs, ledger, authorizations, and API authority references.
3. Inspect native lifecycle and publication through supported read-only interfaces.
4. Identify whether the discrepancy is authoritative mutation, incomplete
   publication, provider ambiguity, stale consumer observation, or API persistence.
5. Compare the sequence with current contracts and provider guarantees.
6. Create a sanitized provider-free regression fixture before another paid test.
7. Repair only through a narrow typed, idempotent, provenance-bound path with exact
   preconditions. There is no generic rehash, force-resume, or bless-workspace mode.

Historical evidence is not something to make aesthetically consistent with current
schemas. If it cannot be consumed safely, retain it for review or start a separately
authorized new run.

# Part II — Joint SBE/API development

## Joint guiding lights

- **Authority is fact-scoped.** SBE owns native execution truth. The API owns jobs,
  runs as product records, leases, capacity, reservations, PostgreSQL/public state,
  global spend policy, billing reconciliation, and publication policy. Durable
  object storage preserves complete immutable captures.
- **Terminal first.** The API validates and transactionally ingests exact native
  terminal evidence before generic subprocess-exit fallback.
- **Producer and consumer share a contract, not an implementation.** SBE emits and
  validates native evidence. The API validates, persists, and maps it without
  parsing private SBE internals or forking native orchestration.
- **Local capacity release is not authority release.** Joint tests must distinguish
  worker slot, provider custody, and financial/review authority.
- **Failures at the seam are first-class.** A crash after SBE publication but before
  API commit, or after API commit but before lease release, belongs in the model and
  fixtures rather than being treated as an unlikely deployment detail.
- **Claims stop at repository ownership.** SBE may prove its artifact and API
  validator parity; only API evidence can prove PostgreSQL/R2 transactionality,
  capacity release, queue fairness, or public reader state.

## Freeze the crossing before concurrent implementation

For a shared change, agree in writing on:

- schema/version and strict unknown-field behavior;
- run, invocation, result, journal-range, snapshot, and receipt identities;
- route family, provider mechanism, operation, action, and stage vocabularies;
- terminal/waiting/refusal/ambiguity semantics;
- replay/idempotency tuple and conflicting-second-operation behavior;
- provider custody and consumer-authority classifications;
- missing-usage/cost disposition;
- legacy-run compatibility or refusal;
- ownership of every mutation and external side effect; and
- the exact evidence each repository may claim after qualification.

Do not let both sides independently invent fields for the same fact. Do not add a
safety-critical field to an unvalidated nested payload merely to avoid versioning a
strict public schema.

## Use explicit cross-repository review gates

A productive joint sprint normally pauses at:

1. **Reproduction gate:** SBE/API agree on the observed sequence, authoritative
   facts, missing evidence, and irreducible crash windows.
2. **Contract gate:** ownership, schemas, outcomes, replay, route/cost semantics,
   and refusal behavior are frozen before runtime implementation.
3. **Producer gate:** SBE implementation and failure injection prove native
   persistence/replay without claiming API behavior.
4. **Consumer-fixture gate:** packaged sanitized SBE fixtures and public readers are
   accepted by the API before operational integration.
5. **Cross-platform gate:** the same candidate wheel passes installed Windows/Linux
   qualification and the real API validator.
6. **Operational gate:** the API proves its worker/PostgreSQL/R2/lease/capacity
   transaction from the immutable SBE artifact.
7. **Closeout gate:** both sides review compatibility, limitations, release order,
   and exact claims before the SBE version bump/tag.

Record reviewer questions and responses in the sprint. If the answer depends on
later implementation, defer it explicitly and answer it in a final response rather
than guessing early.

## Coordinate implementation without coupling repositories

- SBE should expose stepwise, typed prepare/read/reconcile/deny/closeout operations
  where the API needs an authorization or scheduling seam.
- The API should call those public surfaces rather than mutate `run.json`, fabricate
  snapshots, infer state from stderr, or import private helpers.
- SBE must not write AstroWoof PostgreSQL or decide API reservations/capacity.
- The API must not construct provider requests, reimplement SBE retry policy, or
  reinterpret native accepted evidence.
- Both repositories should validate the same packaged fixture rather than maintain
  large similar-looking JSON oracles with independent semantics.
- Sanitized fixtures may use durable fake provider IDs; never commit credentials,
  real protected subject data, provider request bodies containing protected fields,
  or private paid-run artifacts.

Concurrent work is appropriate after the contract gate. Keep the consumer on a
candidate fixture/public interface until the immutable wheel exists. Avoid pinning a
temporary source checkout as if it were the release artifact.

## Joint release and adoption order

Use this sequence unless a documented exception is reviewed:

1. freeze the joint contract and ownership;
2. implement SBE producer/reader and native failure recovery;
3. publish packaged candidate fixtures for API validation;
4. implement and review API validation/transaction mapping;
5. qualify both sides against the same candidate;
6. obtain final API consumer and Kevin review;
7. publish the immutable SBE wheel/checksum/tag;
8. pin the exact SBE wheel URL and SHA-256 in the API;
9. build a worker image whose digest, SBE wheel, upstream wheels, and generation
   profile are mutually compatible;
10. update the API and every relevant worker role to the exact same compatibility
    identities and selected profile configuration;
11. deploy and attest each live runtime independently, including its image digest,
    installed wheels, compatibility identities, and selected configuration;
12. register a fresh immutable generation-profile ID for that exact combination;
13. prove a newly created run binds the fresh profile ID and manifest rather than
    an older still-valid configuration;
14. run API-owned provider-free operational qualification; and
15. authorize a bounded paid cohort only if the change needs live confirmation.

Treat artifact publication, image deployment, runtime configuration selection,
generation-profile registration, and new-run profile binding as separate evidence
gates. A correctly pinned wheel and digest-pinned image do not prove that a live
worker selected the intended profile.

Do not hold an SBE release hostage to an API-owned operational claim when both sides
have explicitly accepted that SBE's artifact boundary is complete. Conversely, do
not describe an API transaction or deployed worker behavior as qualified merely
because the SBE wheel and API fixture validator pass.

## Joint qualification scenarios

At minimum, exercise applicable combinations of:

- exact Natal Responses;
- exact Natal Batch;
- bounded-Natal Responses;
- explicit bounded-Batch refusal;
- delivery complete, review terminal, provider terminal failure, provider pending,
  ambiguous submission, budget exhaustion, policy stop, and malformed evidence;
- exact replay, stale observation, duplicate invocation, and conflicting second
  operation;
- crash after native publication but before API ingestion;
- API transaction rollback followed by exact re-read;
- worker loss after API commit but before lease/capacity cleanup;
- unavailable usage with provider polling complete but consumer authority retained;
- peer isolation, FIFO/capacity behavior, and no cross-run release; and
- complete R2 capture/restoration including publication receipts.

Provider-free qualification must prove zero provider operations, zero new
commitments, and no durable synthetic residue. Paid qualification requires separate
approval, frozen aggregate and per-stage ceilings, supported reconciliation only,
and a final audit of provider operations, native commitments/reported usage, API
reservations, cleanup, and spend.

When lifecycle semantics, wrapper translation, capacity disposition, or scheduling
changes, also require the installed adversarial catalog/joint campaign appropriate
to the ownership boundary. Promote a newly discovered incident to a minimized,
sanitized deterministic fixture rather than relying only on a retained workspace or
random seed.

For mapper changes, mutate one independent fact while holding the tempting proxy
constant. Include sealed/nonterminal, review with and without custody, terminal but
nonpublishable, provider identity due/not-due, missing readiness, exact invocation
identity versus discovered latest, exit 0 with typed refusal, and exit 2 with an
invocation-bound result. Unknown, absent, and contradictory evidence must be three
separate cases.

## Finish a joint change

Before calling the work complete:

- update the authoritative SBE contracts and current release handoff;
- update API contracts, transition oracle, runbook, and worker compatibility pins;
- record exact source commits, schemas, fixture hashes, wheel/hash, image digest,
  test counts, platform versions, provider count, spend, and known limitations;
- record the selected compatibility identities and configuration for every relevant
  API/worker runtime, the fresh immutable generation-profile ID, and evidence that
  a newly created run bound that exact profile;
- state separately which SBE-native and API-operational claims passed;
- preserve any pending API or product follow-up rather than implying it disappeared;
- leave both repositories free of qualification trees and unrelated edits; and
- provide one final cross-repository adoption checklist a new maintainer can follow
  without reading the sprint conversation.

## Related procedures

- [Adversarial Lifecycle Simulation Playbook](Adversarial%20Lifecycle%20Simulation%20Playbook.md)
- [Maintainer Release Playbook](Maintainer%20Release%20Playbook.md)
- [Runtime Contracts](Runtime%20Contracts.md)
- [Authoring Lifecycle Consumer Handoff](Authoring%20Lifecycle%20Consumer%20Handoff.md)
- [Provider Reconciliation Route Parity Handoff](Provider%20Reconciliation%20Route%20Parity%20Handoff.md)
- [Provider Spend Enforcement](Provider%20Spend%20Enforcement.md)
- [Spend Authorization Consumer Handoff](Spend%20Authorization%20Consumer%20Handoff.md)
- [Provider Disclosure and Durable Workspace Contract](Provider%20Disclosure%20and%20Durable%20Workspace%20Contract.md)
- [Packaged Runtime Smoke Test](Packaged%20Runtime%20Smoke%20Test.md)
- [SBE 0.4.5 API Consumer Handoff](../../releases/0.4.5/API%20CONSUMER%20HANDOFF.md)
- [Native Transition Sprint Final API Response](../sprints/2026/08/20260817-native-terminal-transition-journal-sprint1/FINAL%20API%20RESPONSE.md)
