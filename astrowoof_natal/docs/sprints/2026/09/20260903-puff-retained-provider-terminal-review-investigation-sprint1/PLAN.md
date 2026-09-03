# Pastiche editorial advisory and Puff retained-provider investigation — Sprint 1

## Objective

Explain two contemporaneous QA failures without conflating them:

1. why Pastiche's pass-6 theme-group findings were logged as advisory but still
   rejected attempts 2 and 3; and
2. why Puff's completed/accepted polish reconciliation left an unconsumed local
   operation and provider custody when the v0.2 review result was sealed.

Produce strict, public-evidence-backed conclusions and implement two separated
corrections after review: exact optional-stage completed-evidence adoption, and
a product-approved dormant posture for all theme-group QA evaluation.

## Scope and safety

- No provider access, retained-run mutation, deployment, or new paid work.
- Source/test/document changes may begin only after the pre-implementation
  review gate. Release remains separately gated.
- Begin with source and the supplied Render trace. Read retained
  workspaces/checkpoints only after exact coordinates and a bounded access gate
  are recorded.
- Treat API state as authoritative for custody; SBE may interpret native workspace/lifecycle semantics.
- Do not infer that the two runs share a cause merely because they were adjacent
  in one worker export.
- Preserve theme-group data fields for compatibility, but remove their runtime
  QA significance under the recorded dormant-feature product decision.
- Keep theme-group policy removal and Puff's adoption repair separate in code,
  tests, evidence, and rollback reasoning even if they share one release.

## Slices and review gates

### Slice 0 — Freeze the two timelines

Status: complete; review/checkpoint-coordinate gate reached.

- Record exact run/action/provider/result/receipt identities exposed by the
  worker trace.
- Build concise transition tables for Pastiche and Puff from the `✨🐶` trace,
  preserving timestamps, revisions, snapshots, selected branches, provider-I/O
  boundaries, local-work decisions, publications, and exits.
- Separate confirmed log facts from API-provided facts and hypotheses.
- Locate the exact source call sites corresponding to each decisive trace line.

Gate: agree that the two reproductions are accurately characterized before any
retained-workspace access or implementation proposal.

Status: complete and API-approved.

### Slice 1 — Pastiche advisory/rejection boundary

- Trace the pass-acceptance subprocess result through `run_pass_acceptance` and
  `author_one_pass`.
- Determine whether the acceptance artifact contained only advisory findings or
  another hard failure not represented by the concise log.
- Add a provider-free characterization using a production-shaped pass-6 report:
  advisory-only theme-group findings must either accept the attempt or produce a
  distinct, contractually justified disposition; they must not be both
  “advisory” and the sole rejection cause.
- Check attempts 1–3 and terminal publication/replay, not only the last attempt.

Gate: classify as expected behavior, log-label defect, or runtime policy defect.

Status: complete. Retained evidence proves valid hard
`theme_group_assignment` failures; no runtime policy defect.

### Slice 2 — Puff post-polish progress join

- Join the trace's polish action, provider identity, acceptance result,
  reconciliation publication, v0.7 local-work operation/key, consumed-key
  history, v2 intent, and terminal-review v0.2 result.
- If logs/public artifacts cannot prove the missing join, request exact
  checkpoint coordinates and perform only the separately approved bounded
  read-only inspection.
- Compare the live path with the released optional-stage progress-ordering and
  intent-retirement invariants; determine whether the stage consumer was not
  reached, reached without durable consumption, or correctly refused because a
  native prerequisite remained unresolved.
- Add a provider-free production-boundary reproducer for the exact proven path.

Gate: freeze the causal invariant before changing runtime behavior.

Status: complete and API-approved through the checkpoint finding. The
provider-free production-boundary reproduction is also complete: polish has one
intentional expected-failure regression, while critic and candidate have
passing re-entry topology characterizations. Runtime implementation has not
begun.

### Slice 3 — Ownership and contract classification

For each branch independently classify:

- expected native review;
- native runtime defect;
- public contract/observability gap;
- API intake/scheduling mismatch; or
- insufficient historical evidence.

Specify precedence and safety consequences, including whether provider custody,
local work, or terminal review is authoritative at each checkpoint. Any proposed
result/lifecycle change must remain closed and machine-readable rather than
requiring API inference from logs.

Gate: API review before implementation if either finding changes a public
contract or cross-repository disposition.

Status: complete for the evidence-supported boundary. Pastiche is expected hard
editorial rejection. Puff is an SBE native runtime defect; existing public/API
custody semantics correctly contain it and require no API contract change.
Voof-paws implementation review is now open.

### Slice 4 — Make theme-group QA dormant

Status: complete; owner-approved dormant-feature implementation.

- Remove theme-group assignment, coverage, and balance evaluators from the
  runtime acceptance/finalization path rather than merely changing severity.
- Stop emitting theme-group QA findings/advisories and stop logging their
  results.
- Preserve theme-group fields and registry structures as inert compatibility
  data; do not alter the pass-6 prompt in this patch.
- Remove tests whose only contract is active theme-group evaluation. Replace
  them with focused regressions proving the evaluator is not invoked and no
  theme-group value can affect pass acceptance, retry count, finalization,
  terminal result, or exit status.
- Prove non-theme hard gates remain unchanged.

Gate: confirm the dormant boundary and reactivation rule before implementation.

### Slice 5 — Exact optional-stage completed-evidence adoption

Status: complete; API pre-packaging re-review approved.

- Implement only evidence-supported corrections.
- Before any optional-stage provider submission path, join exact completed
  reconciliation evidence to the exact stored in-progress polish, qualitative
  critic, or qualitative candidate consumer state.
- Preserve provider-create fences, exact replay, immutable publications,
  append-only consumed-operation history, and provider-custody precedence.
- Turn the Slice 2 polish expected failure into an ordinary passing regression;
  add exact/mismatch/replay coverage for every optional stage proven in scope.
- Cover Puff's completed-polish adoption/progress path through the real public
  boundary with scripted provider transports only.
- Prove no duplicate create/retrieval and no no-progress loop.

Gate: review runtime behavior and route matrix before packaging.

### Slice 6 — Packaging and handoff

Status: complete through packaging/installed-wheel qualification; awaiting
separate API/owner final release approval for candidate `0.4.41`.

- Publish sanitized consumer fixtures for any new/changed public result.
- If no public result/schema changes, state that explicitly; do not create a new
  API contract merely to describe an internal adoption repair or dormant QA
  policy.
- Run focused source and installed-wheel qualifications proportionate to the
  change, with explicit provider/R2/spend counts.
- Qualify both corrections independently and together so a rollback can
  distinguish editorial-policy behavior from custody/adoption behavior.
- Prepare a fresh immutable version only after API/owner release review.

## Completion criteria

Produce two source-backed causal records that distinguish confirmed facts from
inference; remove dormant theme-group QA from runtime decisions; correctly
adopt exact completed optional-stage evidence without provider re-entry; and
make no recommendation to mutate either retained QA run without a separately
authorized recovery decision.
