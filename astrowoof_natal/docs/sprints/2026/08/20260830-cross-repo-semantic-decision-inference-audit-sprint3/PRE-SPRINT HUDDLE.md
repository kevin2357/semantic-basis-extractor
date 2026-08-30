# Pre-sprint huddle — stop deriving decisions from descriptive labels

## Why this sprint exists

Repeated integration failures have shared one structural cause: API code has
occasionally treated an SBE status, adjective, exit code, missing collection, or
artifact-presence signal as if it were a complete scheduling or authority
decision. The inferred meaning was plausible, but broader than the native fact
actually asserted.

Recent examples include:

- treating `sealed` as terminal, even though sealing establishes immutable,
  verifiable evidence and does not preclude a later sealed successor;
- treating every result that is not `release_until_due` as local continuation;
- treating provider absence or an empty dependency list as terminal failure;
- treating a nonzero command exit as the disposition instead of ingesting the
  sealed typed result published before exit; and
- treating a lifecycle/status name as permission to resume, reconcile, release
  authority, or publish without validating the explicit native predicates.

These are not merely naming problems. One inferred predicate can retain a worker
slot indefinitely, skip terminal-result ingestion, release authority too early,
retry paid work, or obscure an operator-review condition.

## Guiding rule

> A descriptive SBE label is never an API disposition unless a closed public
> contract explicitly defines it as that disposition.

SBE owns validated native execution truth. API owns product state, global spend
authority, reservations, leases, capacity, persistence, and public delivery.
SBE should publish explicit native facts and a supported native command; API
should validate those facts and map them to its own decisions. Neither side
should reconstruct the other's authority from convenient proxies.

## Important distinctions to preserve

### Evidence finality is not run finality

`sealed`, immutable, receipt-valid, and snapshot-bound describe evidence
integrity. They do not independently mean:

- native run terminal;
- delivery publishable;
- provider custody absent;
- local continuation absent;
- reservation releasable; or
- no successor result may exist.

A sealed result may truthfully describe a nonterminal, detached, refused, or
review-required checkpoint. A later state change may produce a new sealed
successor without mutating the predecessor.

### Native scheduling is not API-global admission

SBE may assert facts such as local work readiness, provider retrieval due,
provider ambiguity, native terminality, or a selected supported command. It
must not assert API slot availability, lease state, global spend admission, or
reservation settlement.

### Absence is not a positive assertion

An empty array, missing provider identity, absent result, zero exit code, or
missing dependency must not be promoted into a stronger semantic conclusion
unless the relevant closed contract defines that exact relationship.

### One word may legitimately appear in several phases

Status names often summarize the dominant native posture while custody,
authority, local work, review, delivery, and terminality remain independent
dimensions. Consumers must validate the complete required predicate rather
than assign one total meaning to the status string.

## Audit target

The audit should find every API boundary that consumes SBE evidence and changes:

- job, run, reading, or delivery state;
- queue eligibility, retry timing, lease, or worker capacity;
- native command selection;
- provider reconciliation or provider creation;
- reservation, consumer authority, or billing custody;
- operator-review disposition;
- terminalization, closeout, or publication; and
- replay, recovery, or retained-workspace handling.

For every decision, record the exact public SBE document/version and exact
validated fields that authorize it. Logic based on status names, `sealed`, exit
codes, result existence, truthiness, emptiness, or fallback negation is presumed
unsafe until justified by a closed contract.

## Expected output

The primary deliverable is a joint semantic decision registry, not an immediate
schema redesign. Each row should state:

1. the API decision;
2. the SBE-owned native facts required for it;
3. the API-owned facts additionally required;
4. the current implementation location;
5. the exact contract/version consumed;
6. any proxy or inference currently used;
7. contradiction and unknown-version behavior;
8. severity and reachable routes; and
9. installed SBE version/wheel compatibility identity; and
10. the recommended correction owner.

Every row must name the **positive permission** consumed by the decision. A fact
that work exists is not necessarily permission to execute it now. In particular:

- provider custody is not provider retrieval permission;
- provider retrieval due is not provider creation permission;
- local work existence is not local work eligibility now;
- native terminality is not API settlement completion; and
- sealed evidence is not permission to terminalize anything.

Each row must also state separate outcomes for absent evidence, contradictory
evidence, and an unknown contract version. Those cases must not collapse into
`False`, an empty collection, a default enum, or a generic fallback branch.

The audit should then distinguish:

- **API mapper defects:** SBE already publishes sufficient explicit evidence;
- **SBE contract gaps:** the necessary native fact is not publicly available;
- **joint join gaps:** both facts exist but no public identity/digest joins them;
- **documentation ambiguity:** contract is sufficient but wording encourages an
  invalid inference; and
- **historical compatibility gaps:** old artifacts cannot safely support the
  current decision.

## Result-selection precedence

When an SBE invocation returns an exact sealed result ID, that invocation-bound
result is the authoritative ingestion target. Its validated typed result outranks
the subprocess exit code.

Availability-based discovery of another result—whether described as latest,
current, or available—is permitted only for an explicitly documented
recovery/preflight case where the invocation did not return an exact result ID.
Discovery is not transition authority by itself; API must still validate and
join the discovered result, receipt, checkpoint, invocation provenance, and
installed compatibility identity under the relevant recovery contract.

This sprint must therefore audit exact-result ingestion and availability-based
fallback as separate decision paths.

Only proven SBE contract gaps should become schema proposals. API-owned decisions
must remain API-owned rather than being moved into an oversized SBE disposition
field.

## Candidate native fact vocabulary for audit comparison

This is an audit checklist, not a frozen schema proposal:

- native terminal and terminal cause;
- local work ready now;
- local continuation remains;
- provider custody remains;
- provider retrieval due and SBE-selected bounded subset;
- provider submission ambiguity;
- new provider creation permitted under native state;
- review required and closed reason/classification;
- delivery complete and delivery publishable;
- selected supported native command;
- evidence sealed/receipt-valid; and
- successor/predecessor identity.

The registry must treat “validated native terminal result” and “API job/run
terminalization” as separate decisions. API terminalization may still require
settlement, provider-custody disposition, reservation release, product-state
updates, or an explicit nonpublishable-delivery mapping.

The audit must first determine which of these already exist, under what names and
versions, and whether their joins are strict. Do not add duplicate booleans merely
to make the registry visually uniform.

## Safety posture

- Read source, schemas, fixtures, tests, and process documents only.
- No QA workspace restore, provider call, spend, deployment, database mutation,
  queue operation, or retained-run recovery is needed for the audit.
- Do not patch production routing while inventory is incomplete.
- Treat contradictory evidence as distinct from a truthful typed refusal.
- Preserve closed-world validation and fail closed for unknown versions.
