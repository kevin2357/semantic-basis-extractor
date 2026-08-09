# API Agent Responses

Status: release-candidate answers; publication remains separately gated.

## 1. Defect classification

**Answer:** Yes, qualified. SBE 0.2.1 had two proven defects at the polish retry
authorization boundary: the locally mutated subject record was assigned into
operator state only after polish returned, and workspace snapshot publication
could overlap mutations. Provider/spend persistence correctly preserved the
reported first action and prepared second action, but it published state from a
different moment than the final files. The retained run proves the resulting
mixed checkpoint; deterministic tests prove both general mechanisms. The
available evidence does not identify which external worker lifetimes overlapped
in the transient race.

**Confidence:** high.

**Evidence:** Slice 0 forensic hashes and reproductions; Slice 1 quiescent
checkpoint tests; retained run revision 60.

**Residual uncertainty:** exact external process interleaving during the
original transient race.

**Consumer consequence:** treat the 0.2.1 workspace as an incomplete native
transition, not user corruption and not a resumable checkpoint without repair.

## 2. Authoritative snapshot contents

**Answer:** Yes. Before exposing attempt 2 as awaiting authorization, the
checkpoint must include the updated final deck and QA reports, state-owned
subject and both polish-attempt records, attempt-1 Response/usage evidence,
attempt-2 request, spend ledger, authorization request, operator state, public
state, provenance, and every other authoritative workspace member. The
coordinator publishes the snapshot only after the stage unwinds and those
mutations quiesce.

**Confidence:** high.

**Evidence:** Slice 1 architecture and tests; Slice 4 repaired checkpoint at
revision 61; workspace contract documentation.

**Residual uncertainty:** none for the supported boundary.

**Consumer consequence:** copy worker scratch only after SBE exits and the
coordinator snapshot validates; never snapshot from a nested spend callback.

## 3. Existing-run recovery

**Answer:** Yes, through the new constrained command. SBE 0.2.1 previously
supported only restoration of the exact recorded snapshot and provided no
native way to bless the observed transition. Version 0.2.2 adds
`astrowoof-repair-polish-checkpoint`, dry-run by default. It requires the stable
logical path, exact three-member mismatch, byte equality with retained attempt
1, consistent Response and reported spend, exact attempt-2 request and external
authorization binding, an entirely unused prepared action, a separate
byte-identical backup, an API lease reference, and SBE's local lock. It refuses
all additional, missing, altered, conflicting, authorized, consumed, or
submitted variants.

Apply retains all existing files, accepted passes, provider IDs, usage, spend
actions, and reconciliation evidence. It changes operator/public/authorization-
request state, reconstructs the missing subject plus partial attempt 1 and
pending attempt 2, and publishes a new snapshot. The repaired copy reached
revision 61 and validated. The canonical retained run was not changed. Action 2
remains for the API owner to authorize and execute through the normal seam.

**Confidence:** high.

**Evidence:** eight repair qualification tests; Slice 4 dry-run, apply,
monotonic digests, native validation, and exact-wheel Linux dry run.

**Residual uncertainty:** the canonical copy itself has not been repaired;
that remains a separately authorized operational action.

**Consumer consequence:** inspect first, back up, apply only under the API
lease, persist the external report/evidence, then re-enter normal authorization
orchestration. Do not manually edit or rehash the workspace.

## 4. Corrective deliverables

### 4.1 Exact regression

**Answer:** Yes. **Confidence:** high. **Evidence:** Slice 0 reproduces lost
subject publication and mixed-generation inventory. **Residual uncertainty:**
none. **Consumer consequence:** retain these tests when upgrading orchestration.

### 4.2 Corrected snapshot ordering

**Answer:** Yes. **Confidence:** high. **Evidence:** persistence-only callbacks,
state-owned subjects, coordinator checkpoint unwind, and snapshot tests.
**Residual uncertainty:** none for tested exits. **Consumer consequence:** use
only coordinator-validated exit snapshots.

### 4.3 Interrupted provider reconciliation

**Answer:** Yes, within the provider's actual guarantees. Matching durable
Response markers resume with GET only; conflicts become ambiguity; absence of a
durable provider identity after submission remains blocked. **Confidence:**
high for SBE behavior, medium for provider-side creation atomicity. **Evidence:**
Slice 2 failure injection. **Residual uncertainty:** the provider does not offer
a documented transaction joining creation and SBE persistence. **Consumer
consequence:** never infer exactly-once behavior from deterministic keys.

### 4.4 0.2.1 repair procedure

**Answer:** Yes. **Confidence:** high. **Evidence:** Slice 3 refusal matrix and
Slice 4 repaired-copy validation. **Residual uncertainty:** canonical run not
mutated. **Consumer consequence:** use the installed constrained command only
for an eligible dry-run result.

### 4.5 Documentation and release guidance

**Answer:** Yes. **Confidence:** high. **Evidence:** durable workspace, spend,
runner, critic consumer contract, 0.2.2 recovery advisory, and API integration
documents. **Residual uncertainty:** publication coordinates remain pending.
**Consumer consequence:** pin only after immutable publication is authorized.

## 5. Production restart guarantee

**Answer:** Qualified yes. After a coordinator-valid checkpoint, the API may
destroy scratch, restore the complete directory at its recorded logical
absolute path, and resume known provider work or the next authorization
boundary without duplicate SBE submission. This requires one API-owned run
lease, complete snapshot copying, exact profile/provider configuration, and
normal authorization consumption. `AMBIGUOUS_PROVIDER_SUBMISSION` is a required
reconciliation state, not an automatic-resume guarantee. The provider/local
creation atomicity gap remains when acceptance occurred but no ID became
durable.

**Confidence:** high for SBE/restored-checkpoint behavior; medium across the
irreducible provider creation gap.

**Evidence:** Slice 2 GET-only tests, Slice 4 offline restored resume with zero
transport calls, Windows/Linux installed smoke, and exact-wheel Linux repair
dry run.

**Residual uncertainty:** undocumented provider idempotency/retention behavior.

**Consumer consequence:** API owns lease, storage, restoration path, retries,
and reconciliation policy; it must never resubmit an ambiguous action merely
because budget remains.

## 6. Stable critic artifact

**Answer:** Yes. `critic-findings.json` is stable beginning with v0.1 in 0.2.2.
**Confidence:** high. **Authority:** packaged JSON Schema and contract catalog;
this is normative, not merely current implementation. **Compatibility:**
unversioned artifacts are unsupported consumer formats. **Change:** source,
schema, catalog, fixture, docs, and release changes were made. **Consumer
consequence:** API Slice 5 may consume v0.1 immediately after pinning 0.2.2.

## 7. Explicit schema version

**Answer:** Yes: `astrowoof.qualitative_critic_findings.v0.1`.
**Confidence:** high. **Authority:** top-level artifact field and packaged
schema/catalog. **Compatibility:** unsupported or absent versions fail closed
before candidate resume and must be rejected by API ingestion. **Change:** yes.
**Consumer consequence:** dispatch on the artifact field, never SBE release
number alone.

## 8. Closed vocabularies

**Answer:** The exact `scope`, `priority`, `repairability`, and ten
`quality_dimension` values documented in the consumer contract are closed for
v0.1. `required_context` and `selection_reason` are closed as well.
**Confidence:** high. **Authority:** packaged schema plus source constants.
**Compatibility:** new values require a new schema version. **Change:** these
sets were promoted from implementation behavior to normative contract.
**Consumer consequence:** API may use checked enums and reject unknown values.

## 9. Guaranteed finding fields

**Answer:** All fields named in the question are guaranteed on every
`critic.findings` item: paths/context, diagnosis/objective, and normalized
selection fields. `eligible_findings`, selected paths/count, and limits are
versioned denormalized projections; `critic.findings` is authoritative.
**Confidence:** high. **Authority:** packaged schema and consumer contract.
**Compatibility:** field removal or semantic change requires a new version.
**Change:** explicit validation and schema were added. **Consumer consequence:**
API may index bounded fields while retaining the complete private artifact.

## 10. Authoritative critic provenance

**Answer:** v0.1 directly contains run-relative descriptors and SHA-256 for the
criticized deck and raw response, Response ID/model/reasoning/service, run and
operator schema, state revision, profile identity/digest, runtime release, and
resource-set identity. `run.json` remains overall operator/spend authority but
is not required to infer critic byte identity.
**Confidence:** high. **Authority:** packaged schema, source constructor, and
consumer contract. **Compatibility:** legacy unversioned artifacts lack this
direct chain. **Change:** provenance was added. **Consumer consequence:** verify
hashes during ingestion and retain run/artifact joins.

## 11. Private artifact versus PostgreSQL index

**Answer:** Yes. Store diagnosis, rewrite objective, strengths, risks, and paths
only in immutable private JSON/object storage; index bounded enums, confidence,
counts, selection status, schema version, artifact hash, and object reference.
**Confidence:** high. **Authority:** normative consumer contract; API remains
storage/privacy authority. **Compatibility:** no SBE database contract is
implied. **Change:** documentation only for storage ownership. **Consumer
consequence:** the proposed API Slice 5 split may proceed against v0.1.

## 12. Canonical critic fixtures

**Answer:** Existing Kevin and Ella files are unversioned historical evidence,
not canonical v0.1 fixtures. The release packages a small sanitized canonical
fixture at `resources/fixtures/critic/critic-findings.v0.1.json`.
**Confidence:** high. **Authority:** packaged resource set and contract tests.
**Compatibility:** do not ingest old fixtures as v0.1 by inference. **Change:**
one canonical fixture was added; real-subject fixtures were not republished.
**Consumer consequence:** use the packaged fixture for API parser/index tests.

## Final ownership reminder

SBE owns per-run state, action binding, local spend ceilings, provider evidence,
checkpoint integrity, critic artifact construction, QA, and delivery. The API
owns transactional cross-run reservations, quotas, circuit breakers,
entitlements, queues, exclusive leases, durable storage, HTTP status authority,
account billing reconciliation, and product policy.
