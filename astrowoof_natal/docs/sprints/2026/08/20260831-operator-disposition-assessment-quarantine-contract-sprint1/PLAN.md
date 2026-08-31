# Plan — Operator disposition assessment and generic quarantine contract

## Status

Slices 0–3 are complete and API-approved. The v1 schema, strict Python validator, deterministic
builder, snapshot-validating read-only reader, root exports, and cross-route
matrix are implemented. Availability-based terminal-result discovery now
defaults disabled and is available only through an explicit reader opt-in.
Provider activity, retained-workspace access,
deployment, version bump, tag, and release have not begun. Paused at
Slices 0–4 and the lean `0.4.37` candidate gate are complete. Installed-wheel
qualification, affected regression coverage, dependency verification, and
deterministic rebuild evidence are recorded. API and owner approved commit,
tag, and publication; release execution is in progress.

## Objective

Publish a supported, closed, snapshot-validating SBE assessment of whether one
exact native checkpoint requires an ordinary local authoring worker to remain
scheduled. API may join that native evidence to its own quarantine/resource
decision under its own authority. The assessment preserves and names all
remaining native/provider/spend custody; it grants no mutation, recovery,
cancellation, denial, reconciliation, terminalization, provider authority, or
API resource disposition.

Public contract:

`astrowoof.operator_disposition_assessment.v1`

## Non-goals

- No retained QA access or run mutation.
- No provider GET/POST, spend, denial, cancellation, or repair.
- No SBE command that performs API quarantine.
- No API lease, slot, reservation, billing, or queue assertion.
- No automatic unquarantine or restart behavior.
- No inference from status labels, empty collections, logs, or “latest” result.
- No redesign of lifecycle v0.5–v0.8 or temporal lifecycle.
- No widening into operator retirement; retirement remains a separate native
  terminal transition with stricter preconditions.

## Authority split

### SBE owns

- exact native run/route/checkpoint identity;
- snapshot validity and compatibility identity;
- native provider/local/authority custody facts;
- custody classification and supported native next actions;
- whether the native evidence is contradictory or unsupported; and
- the local-quarantine posture as a bounded native assessment.

### API owns

- operator authorization and audit identity;
- job fencing and prevention of ordinary worker claims;
- lease/capacity release;
- reservation, spend, billing, queue, and deployment state;
- persistence/admission of the exact assessment; and
- any later named action or fresh assessment required to leave quarantine.

`quarantine_posture=permitted` means only that the native evidence does not
require API to keep an ordinary local worker slot occupied. It never transfers,
forgets, resolves, or releases provider/native/spend custody.

## Contract shape to freeze

The assessment should contain only closed, privacy-bounded fields:

- `schema_version`
- `assessment_sha256`
- `native_run_id`
- `route_family` and route contract/version
- opaque `logical_workspace_root_id` (never an absolute/R2/host path)
- installed SBE version and compatibility identity
- native state revision
- snapshot/checkpoint basis digest and snapshot digest
- exact lifecycle inspection schema/version and digest
- `native_custody_class`
- bounded provider/local/authority counts and assertions
- safe provider-operation references where necessary for diagnosis
- `quarantine_posture`
- ordered `supported_next_actions`
- closed `reason_code`
- optional bounded evidence-category list

No prompt, provider payload, subject/card/deck content, credentials, request
body, authorization document, or private workspace path beyond the already
public logical root is permitted.

## Closed vocabularies

### Native custody class

- `provider_free_quiescent`
- `provider_pending_known_identity`
- `completed_unadopted`
- `native_local_work_ready`
- `providerless_authority`
- `submission_ambiguous`
- `sealed_terminal`
- `unsupported_or_inconsistent`

### Local quarantine posture

- `permitted`
- `prohibited`
- `native_prior_action_required`

### Supported next-action vocabulary

Freeze in Slice 1 from existing public commands only. Candidate values:

- `provider_reconciliation_cycle`
- `ordinary_resume`
- `external_authority_v1`
- `external_authority_v2`
- `providerless_denial`
- `terminal_result_ingress`
- `operator_retirement_assessment`
- `operator_review`
- `fresh_disposition_assessment`

The assessment names supported operations; it does not authorize or invoke
them. API must not reconstruct action/member subsets from the assessment.
No supported native next action is represented only as the empty ordered list.
There is no `none` action token, and absence of the field is invalid.

## Classification precedence to freeze

The initial proposed precedence is:

1. **Invalid snapshot, unknown contract, failed identity join, contradictory
   evidence** → `unsupported_or_inconsistent`; fail closed.
2. **Entered provider call without one durable coherent identity, or explicit
   ambiguous state** → `submission_ambiguous`.
3. **Durable completed provider evidence not yet adopted into native truth** →
   `completed_unadopted`.
4. **Durable known provider identity still pending/due** →
   `provider_pending_known_identity`.
5. **Concrete deterministic local work is eligible now** →
   `native_local_work_ready`.
6. **Providerless prepared/authorized/denial-required authority remains** →
   `providerless_authority`.
7. **Exact sealed terminal result/receipt/checkpoint join with no contradictory
   live custody** → `sealed_terminal`.
8. **No provider, ambiguity, authority, local executable work, or unresolved
   native transition remains** → `provider_free_quiescent`.
9. Any unclassified mixture → `unsupported_or_inconsistent`.

Mixed inventories must not be flattened. A dominant class may select the safe
posture, while bounded assertions/counts preserve subordinate custody. In
particular, provider custody outranks providerless authority and terminal-looking
status; ambiguity outranks all forward work.

## Slices

### Slice 0 — public inventory and classification table

Inventory and map the supported fields/readers from:

- lifecycle v0.5, temporal v0.6, local-work v0.7, retry-lineage v0.8;
- provider custody/reconciliation timing;
- external-authority v1/v2 request/refusal state;
- native result availability and exact result/receipt readers;
- operator-retirement assessment; and
- installed compatibility/provenance identity.

Produce a source-to-contract table for all eight custody classes, including
positive proof, disqualifiers, precedence, quarantine posture, supported next
actions, and unknown/contradictory behavior. Explicitly decide:

- whether pending/ambiguous/completed-unadopted classes permit local API
  capacity release while custody remains retained;
- when `native_prior_action_required` applies;
- whether sealed terminal requires exact invocation-returned result identity or
  may use the existing narrowly supported availability reader; and
- which lifecycle version is the minimum sufficient evidence for each class.

**Voof-paws 1:** API reviews the classification and native-only posture meaning
before schema freeze.

### Slice 1 — v1 schema and semantic contract freeze

Define the JSON Schema plus a strict Python semantic validator. The Python
validator must independently enforce the closed shape and primitive constraints
when `jsonschema` is absent.

Freeze:

- canonical JSON/digest rules;
- exact snapshot/checkpoint/lifecycle joins;
- run, route, revision, compatibility, and logical-root joins;
- class-specific required/forbidden assertions;
- bounded provider identity inventory and overflow behavior;
- class/posture/next-action compatibility;
- deterministic ordering; and
- privacy exclusions.

Add one positive fixture per custody class and mutation tests for every identity,
digest, count, assertion, class/posture pairing, unknown version, extra key, and
privacy sentinel.

**Voof-paws 2:** API freezes its admission/persistence mapping against the exact
schema before the reader is wired.

### Slice 2 — snapshot-validating reader and projection

Implement root-level public APIs, tentatively:

- `build_operator_disposition_assessment(...)`
- `read_operator_disposition_assessment(run_dir, ...)`
- `validate_operator_disposition_assessment(value)`
- `read_operator_disposition_assessment_schema()`

The reader must:

1. resolve the exact workspace root without recursive discovery;
2. load and validate the supported public lifecycle/checkpoint evidence;
3. validate the current exact snapshot before projection;
4. join native result/receipt evidence only through supported readers;
5. classify by the frozen precedence table;
6. emit no mutation and perform no provider I/O; and
7. return byte-identical output for byte-identical native evidence.

Do not add a persisted assessment inside the native workspace unless a later
contract decision proves that necessary. The default is a read-only returned
artifact that API persists outside the workspace.

### Slice 3 — provider-free cross-route matrix

Exercise production-shaped fixtures for:

- exact and bounded interactive initial work;
- ordinary creative retry;
- polish, critic, and candidate;
- Batch custody where supported and explicit unsupported classification where
  not supported;
- pending known response identity;
- completed evidence before native adoption;
- ambiguous call entry / missing identity;
- providerless prepared and authorized evidence;
- sealed terminal with and without contradictory live custody;
- provider-free quiescent state;
- retry-lineage conflict and unknown-version evidence; and
- mixed inventories where precedence matters.

For every cell prove zero provider calls, zero workspace mutation, exact replay,
snapshot binding, and closed next-action output. A failing diagnostic/event sink
must not change the returned assessment.

**Voof-paws 3:** consumer review of the fixture matrix and API mapping.

### Slice 4 — packaged CLI and installed-wheel qualification

Add a provider-free, read-only CLI suitable for worker/operator use, for example:

```text
astrowoof-operator-disposition-assessment --run-dir <restored-root>
```

The CLI accepts no provider credentials, authority/grant documents, mutation
flag, recovery input, or production command payload. It writes the assessment
only to stdout or an explicitly named path outside the native workspace.

Package:

- schema;
- sanitized fixtures;
- root-level readers/builders/validators;
- CLI entry point;
- closed qualification receipt and validator; and
- API consumer handoff.

Installed qualification must use a clean wheel, fresh process, real public
reader/CLI, fixture workspaces, privacy sentinel, and byte-identical replay.

### Slice 5 — lean release preparation

If no runtime semantics changed, use the additive/package-only lean gate:

- focused contract/semantic/mutation matrix;
- affected lifecycle/native-result/retirement-reader tests;
- installed-wheel disposition qualification;
- package resource/export/CLI smoke;
- `pip check`;
- deterministic wheel rebuild from committed source;
- `git diff --check`; and
- explicit record that the full runtime suite was not run.

Freeze the fresh version before building or running release-derived fixtures.
Tag/publication require separate explicit owner approval.

If any production lifecycle, reconciliation, provider, native-mutation, or
scheduling behavior changes, stop using this lean gate and replan the release
qualification proportionately.

## Failure and replay rules

- Invalid or contradictory evidence never becomes a false negative/empty list;
  it yields `unsupported_or_inconsistent` or a typed validation refusal.
- Same checkpoint and same public evidence produce an exact byte-identical
  assessment.
- A changed revision/snapshot/checkpoint/lifecycle/result identity requires a
  fresh assessment; the old one is stale and cannot authorize API action.
- Assessment discovery is not transition authority.
- Quarantine does not consume native work.
- Unquarantine requires a named later operation plus a fresh assessment.

## Test and safety posture

- Provider calls: prohibited.
- Retained QA/R2 access: not required and not authorized by this plan.
- Workspace writes: prohibited for assessment paths and qualification.
- Logs/events: diagnostic only and privacy-bounded.
- Existing untracked release/workspace artifacts: preserve and ignore.

## Expected outcome

This should remain short relative to recent lifecycle sprints because it adds a
read-only projection over already-supported public evidence. The likely release
is a genuine fasty-patchy additive wheel. The classification table and strict
cross-evidence joins—not code volume—are the substantive work.
