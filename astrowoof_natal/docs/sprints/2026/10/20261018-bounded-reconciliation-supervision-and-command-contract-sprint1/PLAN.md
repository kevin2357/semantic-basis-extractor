# Plan — bounded reconciliation supervision and command contract

**Status:** API and SBE approve the narrowed contract and frozen fixture
definitions; **Gate A is closed**. The next deliverable is provider-free
construction of complete shared fixture bytes, not an installed-wheel pass.
See the [inventory](SLICE%200A%20-%20NATIVE%20AND%20API%20BOUNDARY%20INVENTORY.md)
and [contract proposal and matrix](SLICE%200B%20-%20NATIVE%20COMMAND%20AND%20SUPERVISION%20PROPOSAL.md).
This is the SBE companion to API sprint 129. Gate A precedes implementation.

**Alpha scope refinement:** the [narrowed Gate A proposal and matrix](SLICE%200C%20-%20ALPHA%20SAME-CALL%20HANDOFF%20AND%20CONTAINMENT.md)
supersede 0B's invocation-scoped durable-binding/reconstruction mechanism and
related Candidate A/B research. Exact same-call handoff remains required;
ambiguous lost output/crashes remain held for investigation rather than being
automatically reconstructed. The older documents remain historical design
context, not additional release requirements.
The follow-on [Slice 0D](SLICE%200D%20-%20ALPHA%20COMMAND%20OUTCOMES%20AND%20CONTAINMENT%20REVIEW.md)
proposes the concrete command/companion, outcome table, clock topology and
durable containment tests; the subsequent joint review closes the contract gate.
API's Slice 0D review identifies a specific untyped early integrity refusal and
the need for a genuinely usable cross-host clock policy. SBE's response in API
sprint 129 proposes a narrowly bound typed companion, tightens the table, and
originally proposed a stricter clock proof. The owner and API/SBE subsequently
agreed the alpha policy: retain operator-origin deadlines under an explicit
reasonable-clock assumption, unknown skew and no guaranteed hard cutoff;
use the branch-specific typed refusal companion. See API sprint 129's
`SBE AGENT - GATE A ALPHA SHARED HANDOFF AND FIXTURES.md`. Shared executable
fixture definitions are frozen by API review and SBE sign-off in API sprint
129's `SBE AGENT - GATE A SHARED FIXTURE DEFINITIONS AND SIGNOFF.md`.
Genuine fixture generation and later implementation/qualification remain.

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

## Gate A — joint review before implementation (approved)

API reviews the proposal against its actual worker, lease/fence, child-process,
ingestion, economics and checkpoint contracts; documents its matching handoff;
and identifies changes or missing evidence. SBE incorporates and re-reviews
material corrections. Both sides agree on the executable contract and test
matrix; the owner resolves consequential product or operational choices.
API's Gate A alpha handoff review and SBE's matching sign-off approve the
contract and frozen fixture definitions. This does not imply complete
executable fixtures, a release candidate or provider work.

Review must specifically settle observation-time freshness versus the existing
launch-time timestamp, checkpoint ancestry after local continuation, exact
same-call terminal publication selection versus the existing latest reader,
and the API-side cross-version routing and direct-child/checkpoint proofs.
Review the narrowed 0C contract and matching API handoff, including exact
same-call receipt selection, no-output containment, the real clock topology,
outcome-by-outcome checkpoint/exit mapping, and the supported operator path.
Agree the executable schemas and test matrix before implementation. Existing
review and research files retain their historical findings, but durable
attempt-keyed recovery, Candidate A/B and automatic recovery from lost stdout
are not Gate A or alpha release requirements. No latest-result substitution,
custody loss or duplicated paid work is permitted under the narrower scope.

## Slice 0E — provider-free shared executable fixture construction

Build complete, reproducible synthetic shared workspace, authority, stream and
negative fixture bytes according to the frozen API-sprint definitions. Use
existing native validators and real source artifact shapes; no real provider
I/O. Derive result/receipt IDs and digests from genuine synthetic evidence,
not illustrative placeholders. Verify source fixture construction and share
exact paths/hashes with API. Fixture generation cannot assume the new command
is already implemented. If actual native shapes conflict with the frozen
contract, pause for joint revision; do not silently loosen it.

## Later work — sequencing after the fixture slice

After approval, detail separate SBE implementation/provider-free unit and
exact-route regression slices; create and qualify the immutable bounded
successor profile and reproducible SHA-pinned candidate; obtain API review;
then jointly exercise the real installed command and API persistence/checkpoint
paths against those exact bytes. API's separately owned work includes its
route-aware adapter and economics investigation. Package release, no-reset QA
rollout and a fresh paid canary each have separate review/owner gates; check
old-run custody and existing-run routing before any operational transition.
