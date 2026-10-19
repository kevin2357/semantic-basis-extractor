# Plan — bounded reconciliation supervision and command contract

**Status:** Slices 0A and 0B are complete; the native proposal is **awaiting
joint Gate A review**, not approved. See the [inventory](SLICE%200A%20-%20NATIVE%20AND%20API%20BOUNDARY%20INVENTORY.md)
and [contract proposal and matrix](SLICE%200B%20-%20NATIVE%20COMMAND%20AND%20SUPERVISION%20PROPOSAL.md).
This is the SBE companion to API sprint 129. Gate A precedes implementation.

## Objective and boundaries

Make the bounded interactive reconciliation path and API worker agree on an
honest, executable, versioned command and supervision contract, while
preserving native/API custody, immutable routing and exact-route behavior.
Prove the actual installed-command-to-API path with fake providers before
release qualification. Do not silently translate bounded v2 to v1 or weaken
supervision to make the command run.

This plan does not authorize provider calls, retained QA workspace access,
recovery or disposal of the prior run, release, deployment, profile activation,
or a paid canary. Existing provider identities, evidence and reservations are
preserved; their disposition and existing-run worker-context routing are
separate operational decisions. Synthetic fixtures and fake providers only
are in scope for the investigative and implementation test slices.

## Slice 0A — native and consumer boundary inventory

Investigate and record a source- and test-referenced current-state map, using
the released `0.4.72` wheel and its exact SHA where installed behavior matters:

1. Trace API's real bounded command builder, launch, stdout/stderr/event reader,
   exit handling, result validation and receipt/transition/checkpoint ingestion
   against the installed bounded CLI and native `bounded_natal` v2 route.
   Distinguish demonstrated mismatches from untested assumptions, and preserve
   the exact-route command as a regression control.
2. Inventory native reconciliation from selection and pre-GET observation through
   GET, response evidence, local durable checkpoint, continuation and possible
   terminal publication. Identify which operations may follow a successful GET;
   do not assume the entire continuation is GET-only or can create paid work
   without existing authority. Map state mutations, provider IDs, native result
   and receipt identity, and the API checkpoint publication boundary.
3. Inspect existing exact-route supervision, bounded explicit refusals, lease/
   force-fence and direct-child evidence interfaces. Identify which shared
   hooks are truly reusable versus unproven for bounded state, and distinguish
   local persistence from API's durable remote checkpoint.
4. Inventory relevant tests and design an executable synthetic bounded v2
   fixture with six identifiable operations, pending and completed responses,
   controllable GET barriers, durable state and terminal/nonterminal branches.
   Include privacy and malformed/mixed-route controls; no real provider I/O.
5. Keep `sealed_publication_join_mismatch` a separately traced question: record
   the evidence needed to locate it and its owner, without attributing it to
   the CLI mismatch absent proof.

**Deliverable:** an inventory/evidence document that explicitly names proven
behavior, gaps, relevant source/tests and any decisions required for 0B. A
provider-free reproduction may be used where needed; no implementation change.

## Slice 0B — SBE native contract proposal and qualification matrix

SBE drafts the native proposal for API review, rather than presupposing API's
adapter or claiming guarantees the implementation cannot provide. Specify and
justify at least:

1. The actual installed executable and closed argument contract, including
   profile/route/observed-time inputs, event and result channels, output format,
   exit/refusal semantics, privacy and backward compatibility. Decide whether
   to reuse an existing typed command envelope or add a versioned successor;
   specify which producer emits it and how it is distinguished from events.
2. Native v2 inspection, exact invocation/result/receipt identities,
   predecessor and successor bindings, terminal and nonterminal outcomes,
   result/receipt joins, and malformed/wrong-route/profile rejection. Describe
   both what SBE emits and what API must independently validate and persist.
3. Cooperative suspension observation before a GET and after a response is
   durably checkpointed, with a concrete account of the interval while GET is
   in flight. State that a fence cannot retroactively cancel an already-started
   GET or prove a remote checkpoint; specify when SBE may stop, what evidence it
   emits, and what API must prove about direct-child exit and no further writes.
   Separate an unresponsive child/forced stop from cooperative acknowledgement.
4. Failure and restart behavior before, during and after GET, response handling,
   native publication, API ingestion and API checkpoint publication. Distinguish
   repeatable retrieval of an already identified operation from a new paid
   create; require fail-closed handling of unproven custody and no duplicate
   create. Explicitly cover any later authorized continuation rather than
   assuming successful retrieval completes the run.
5. A matrix for pending/completed/failed responses, fence timing, child exit,
   replay, tamper, stale/missing evidence, terminal delivery/review, economics
   and receipt joins, and exact-route controls. State which tests are native,
   which require API's real worker/ingestion/checkpoint path, and what synthetic
   or local storage cannot prove. Include the six-member/multiple-result case.
6. A successor bounded profile/release-context strategy: immutable IDs,
   package descriptor, prompt allowlist/catalog and digest impacts, versioned
   worker routing and historical-run compatibility. Identify separately whether
   exact profile successors are needed; do not mutate old identities or infer
   that older work can resume under a newer worker.

**Deliverable:** a proposed native contract and test matrix, with open design
questions and explicit non-guarantees, for API's review and API-side handoff.
API owns its lease, worker, durable custody, economics, checkpoint and rollout
semantics; SBE does not claim to attest them from native state alone.

## Gate A — joint review before implementation

API reviews the proposal against its actual worker, lease/fence, child-process,
ingestion, economics and checkpoint contracts; documents its matching handoff;
and identifies changes or missing evidence. SBE incorporates and re-reviews
material corrections. Both sides agree on the executable contract and test
matrix; the owner resolves consequential product or operational choices.
Until then, no implementation, release candidate or provider work is implied.

Review must specifically settle observation-time freshness versus the existing
launch-time timestamp, checkpoint ancestry after local continuation, exact
same-call terminal publication selection versus the existing latest reader,
and the API-side cross-version routing and direct-child/checkpoint proofs.

## Later work — sequencing only, not yet authorized by Gate A

After approval, detail separate SBE implementation/provider-free unit and
exact-route regression slices; create and qualify the immutable bounded
successor profile and reproducible SHA-pinned candidate; obtain API review;
then jointly exercise the real installed command and API persistence/checkpoint
paths against those exact bytes. API's separately owned work includes its
route-aware adapter and economics investigation. Package release, no-reset QA
rollout and a fresh paid canary each have separate review/owner gates; check
old-run custody and existing-run routing before any operational transition.
