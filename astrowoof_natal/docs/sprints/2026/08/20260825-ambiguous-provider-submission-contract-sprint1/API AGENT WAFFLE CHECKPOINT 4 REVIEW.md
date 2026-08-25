# API Agent Waffle Checkpoint 4 Review

Date: 2026-08-25  
Reviewer: AstroWoof API agent  
Scope: final release-candidate review for `astrowoof-natal-authoring` 0.4.23

## Verdict

**Conditional approval for the 0.4.23 tag and publication.** The condition is
a small documentation correction described below; it does not require another
runtime, contract, fixture, or qualification pass.

The release candidate closes the actual defect exposed by the frozen QA cohort:
the old durable `CALL_ENTERED` boundary preceded deterministic request
materialization, so a provably pre-provider failure was conservatively but
incorrectly sealed as submission ambiguity. The new v3 dispatch / v2 command
result pair makes the relevant distinctions public, closed, and consumable:

- `pre_provider_refusal` / `not_attempted` proves that this invocation did not
  make provider I/O possible;
- `ambiguous_submission` / `create_entered_unknown` preserves review custody
  without authorizing another create;
- `detached_provider_pending` / `provider_identity_durable` preserves only
  retrieval/reconciliation custody; and
- exact replay does not create new provider work or a new API transition.

That is the correct shape for API admission, reservation release, scheduling,
and operator handling. In particular, the contract does **not** ask the API to
infer a provider-submission conclusion from logs, missing IDs, exit status, or
private workspace state.

## Evidence reviewed

- Candidate source: `9f3e3874aee74099b7c1a43b5094fe55c8426fb3`.
- Release evidence record: `2e0c3405a86b61dead6ad850b80b7a72cdb36940`.
- Candidate wheel: 0.4.23,
  `adf16ecc785c2eeb98bcc1b4ed77d49bba0f208a1943c58e74320b2eed5135de`.
- Reproducible double build, exact SPC 0.11.1 dependency, installed-wheel
  fixture/export qualification, generic installed smoke, and the documented
  broad suite result of 719 passed / 3 expected skips.
- Provider-free fixture matrix covers pre-fence refusal, post-fence ambiguity,
  durable provider pending, exact replay, and malformed evidence.
- API reviewer reran the focused consumer/runtime/CLI gate locally:
  18 tests passed with 1 optional `jsonschema` skip in the lean runtime. The
  candidate qualification environment separately recorded the same contract
  checks with the optional Draft 2020-12 validation active.

No retained QA workspace, provider credential, network call, or spend was used
for this review.

## Final release condition: make the normative handoff final-state accurate

`releases/0.4.23/API CONSUMER HANDOFF.md` identifies
`AMBIGUOUS PROVIDER SUBMISSION API CONSUMER HANDOFF.md` as the normative detailed
handoff. That sprint document still says `Scenic Waypoint 3 candidate; API
fixture review pending` and finishes with the old Waypoint 1 questions.

Before tagging, update that document so a downstream API consumer cannot
reasonably read the released contract as still pending. It should instead state
that Waypoint 3 API fixture review completed and Waypoint 4 is qualified pending
owner/API publication authorization; the historical questions may be moved to a
clearly labelled decision-history section or removed. Update any linked status
line if necessary.

After that documentation-only correction, this reviewer approves tagging and
publishing immutable 0.4.23. API adoption remains a separate pinned-release
change: validate the packaged v3/v2 pair and fixtures, then implement the
published capacity/custody decision table without reconstructing SBE custody.
