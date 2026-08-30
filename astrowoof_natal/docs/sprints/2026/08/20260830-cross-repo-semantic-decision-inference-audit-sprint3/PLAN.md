# Plan — cross-repository semantic decision inference audit

## Goal

Systematically identify every place where AstroWoof API derives scheduling,
authority, custody, terminality, or delivery meaning from an SBE proxy rather
than the exact closed public evidence. Produce a reviewed decision registry,
reachable-risk matrix, and bounded correction backlog. Propose SBE contract work
only where the audit proves that explicit native evidence is missing.

## Status

Slices 0–2 are complete. No runtime changes, API changes, schema changes,
provider activity, or release are claimed. The completed semantic decision
registry is paused at the joint review gate before adversarial classification.

## Scope boundary

This sprint goes through the complete API code audit and joint classification of
findings. It does not automatically implement every correction. Small test-only
or documentation corrections may be proposed, but production mapper or SBE
contract changes require a follow-up implementation plan after the audit freeze.

## Slice 0 — freeze vocabulary, versions, and authoritative boundaries

Inventory the public SBE surfaces currently available to API, including where
applicable:

- lifecycle inspection v0.5/v0.7/v0.8;
- temporal lifecycle v0.6 and checkpoint-basis decisions;
- native transition results, journals, snapshots, receipts, and result
  availability;
- external-authority request/grant and constrained-dispatch results;
- provider reconciliation results and custody evidence;
- terminal-review, denial, retirement, and closeout evidence;
- accounting observations where they influence settlement but not scheduling;
- installed qualification receipts and consumer handoffs.

For each field likely to drive API behavior, record its narrow normative meaning
and explicitly list meanings it does not carry. Start with `sealed`, terminal,
review, local continuation, provider custody, due/not-due, publishable, and
release-eligible.

Deliverables:

- SBE public-fact catalog by schema version;
- vocabulary collision/ambiguity list;
- identity and digest join map;
- list of historical versions that must fail closed; and
- initial semantic decision registry template.

The template must include columns for the consumed positive permission,
installed SBE version/wheel identity, and distinct absent/contradictory/unknown-
version outcomes. It must contain separate rows for native terminal-result
acceptance and API job/run terminalization.

Gate: API reviews the catalog before its code is judged against it. This prevents
the audit from encoding a mistaken SBE interpretation as the standard.

## Slice 1 — enumerate API decision sinks

Search API source and tests for every point that changes or returns:

- claimability, lease, capacity, retry count, or wake time;
- local resume, provider reconciliation, constrained dispatch, or no-op command;
- admission, reservation, consumer authority, settlement, or release;
- job/run/reading status;
- review, blocked, failed, cancelled, or terminal state;
- delivery completion or publication;
- result ingestion, replay, successor adoption, or recovery.

Build a call-site inventory with file/function/test references. Include direct
comparisons and indirect helper predicates. Search especially for:

- status/string comparisons;
- `sealed`, `terminal`, `complete`, `pending`, `review`, and `failed`;
- subprocess exit-code branching;
- result/artifact presence checks;
- `if not ...`, empty-list, null, and fallback-default logic;
- conversions from SBE result models into API enums;
- catch-all validation-error handling; and
- branches that skip result ingestion before scheduling.

Inventory subprocess precedence explicitly: an exact invocation-returned sealed
result ID and its typed validated result outrank the process exit code. Inventory
availability discovery separately as a recovery/preflight path, never as an
implicit substitute for an invocation-returned identity.

Gate: every decision sink has an owner and an intended authoritative input. No
risk conclusion is required yet.

## Slice 2 — trace evidence source to decision sink

For every Slice 1 sink, trace the full path from:

```text
installed SBE command/read surface
  → returned/located artifact
  → schema and semantic validation
  → identity/digest join
  → API persistence
  → mapper/projection
  → queue/authority/product decision
```

Record whether the implementation:

- validates the exact supported version;
- validates semantics without optional dependencies;
- joins run/action/binding/provider/result/snapshot identities;
- validates predecessor/successor continuity when a named recovery path adopts
  a successor, rather than equating recency or sealing with authority;
- prefers the exact invocation-returned result ID whenever one exists;
- uses availability-based discovery only under a named recovery/preflight
  contract when the invocation did not return an exact result ID;
- distinguishes absent, unknown, unavailable, false, and zero;
- preserves contradictory evidence separately from typed refusal;
- performs terminal-result ingestion before follow-on scheduling; and
- keeps SBE native conclusions separate from API-global state.

For every sink, record the precise positive permission consumed—not merely the
fact, state, or inventory that made the branch seem plausible. Also record the
installed SBE distribution version and wheel/compatibility identity whose public
contract is being interpreted.

Deliverable: a completed semantic decision registry with evidence citations and
an explicit “forbidden inference” column.

Voof-paws: joint review before assigning defects. This is the main factual audit
checkpoint.

## Slice 3 — adversarial inference review

For each decision family, mutate one semantically independent dimension while
holding the tempting proxy constant. At minimum reason through or add
provider-free mapper fixtures for:

- sealed + nonterminal;
- exact invocation result + conflicting availability-discovered result;
- no returned result ID + valid recovery availability discovery;
- sealed predecessor + later sealed successor;
- review-required + retained provider custody;
- no local dependencies + local fan-in ready;
- provider identity present + retrieval not due;
- provider evidence complete + local work ready;
- terminal + nonpublishable delivery;
- provider terminal + usage unavailable;
- exit 0 + typed non-dispatching refusal;
- exit 2 + sealed result available;
- empty action inventory + nonterminal local operation;
- status unchanged + checkpoint basis advanced; and
- status changed + authoritative basis unchanged or contradictory.

For each mutation, exercise absent evidence, contradictory evidence, and an
unknown contract version as separate typed outcomes. None may reach the ordinary
false/empty/default branch.

Tests should exercise API mappers/validators using public SBE fixtures or
packaged readers. API must not reconstruct private SBE workspaces or native
composition rules.

Deliverables:

- inference mutation matrix;
- missing-test inventory;
- confirmed false-positive/false-negative decisions; and
- minimized fixtures suitable for follow-up regression work.

## Slice 4 — classify and prioritize findings

Classify every finding as:

1. API mapper defect;
2. SBE public-contract gap;
3. cross-artifact join gap;
4. documentation/naming ambiguity;
5. historical compatibility limitation; or
6. safe, contract-backed inference.

Assign severity based on potential impact:

- duplicate or unauthorized provider work;
- premature reservation/custody release;
- lost terminal/review evidence;
- infinite retry or retained-capacity loop;
- incorrect delivery/publication;
- billing settlement corruption; or
- diagnostics-only confusion.

For every proposed SBE addition, prove that the native fact is not already
available. Prefer a strict validator or join correction over a new schema field
when sufficient evidence already exists.

Voof-paws: API and SBE freeze the classification and correction ownership.

## Slice 5 — correction backlog and implementation handoffs

Produce bounded follow-up plans rather than mixing unrelated fixes into one
release:

- immediate API mapper/test patches where existing evidence is sufficient;
- SBE contract proposals only for demonstrated native-evidence gaps;
- joint fixture/qualification additions for seam behavior;
- documentation wording corrections; and
- explicit unsupported/historical fail-closed rules.

The SBE proposal should favor orthogonal facts over a monolithic API-disposition
field. The API proposal should use a closed mapping table whose every decision
names required SBE facts and required API-owned facts.

Final deliverables:

- reviewed semantic decision registry;
- prioritized defect and test backlog;
- API implementation handoff;
- any SBE contract proposal/handoff;
- process/runbook updates; and
- recommendation on whether a release is required in either repository.

The final registry must keep native terminal-result consumption separate from
API job/run terminalization and document any intervening settlement, custody,
reservation, and delivery decisions.

Final gate: owner and both repository agents approve the audit record before any
cross-repository implementation sprint begins.

## Acceptance criteria

- Every API scheduling/authority/terminal/delivery decision consuming SBE
  evidence appears in the registry.
- Every row names exact contract versions, fields, validators, joins, and API
  facts, plus installed SBE version/wheel identity.
- Every row names the positive permission being consumed.
- Every row defines distinct absent, contradictory, and unknown-version
  outcomes.
- No row relies on a bare status name, `sealed`, exit code, artifact presence,
  emptiness, or negated fallback without a cited closed contract.
- Unknown versions and contradictory evidence fail closed.
- Evidence integrity, native terminality, delivery, custody, local work, and API
  resource state remain separate dimensions.
- Exact invocation-returned result identity outranks exit code and generic
  availability discovery; discovery is used only by a documented fallback.
- Provider-free mutation cases cover the recurring inference patterns.
- Findings are assigned to the correct repository and do not move API-global
  authority into SBE.
- No provider work, retained-QA mutation, deployment, or spend occurs.

## Explicit non-goals

- Renaming every historical status.
- Replacing explicit facts with one universal disposition enum.
- Making SBE decide API leases, slots, reservations, or product state.
- Making API reproduce native state-machine logic.
- Relaxing closed-world validation for compatibility.
- Treating all existing inference as defective before tracing its contract.
- Shipping production changes before the audit and ownership freeze.
