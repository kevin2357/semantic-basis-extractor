# AstroWoof Natal Authoring Linux Smoke Patch Sprint

```yaml
status: planned
planned: 2026-08-08
owner: semantic-basis-extractor
target_distribution: astrowoof-natal-authoring
proposed_target_version: 0.2.1
proposed_target_tag: astrowoof-natal-authoring-v0.2.1
predecessor_release: astrowoof-natal-authoring-v0.2.0
execution_authorized: false
paid_provider_work_authorized: false
publication_authorized: false
```

## Outcome

Produce a narrowly scoped patch release that makes SBE's deterministic fake
provider and installed release smoke portable across Windows and Linux. The
patch must preserve the original QA failure when a smoke run misses delivery,
emit a structured failed-smoke report, and never mask that result by attempting
completed-run cleanup on a nonterminal run.

This plan creates planning records only. It does not authorize implementation,
version changes, wheel construction, tagging, pushing a release tag, or
publication. Execution begins only after explicit approval.

## Triggering evidence

The API worker's hash-locked offline Python 3.11 Linux image successfully
installed the exact qualified AGF 0.6.0, SPC 0.10.0, SBE 0.2.0, and
pyswisseph wheels. `pip check`, AGF projection/doctors, and SPC installed smoke
passed. No OpenAI request was made and spend was USD 0.

SBE's installed smoke reached `FINAL_QA_REQUIRES_REVIEW` because three fake
cards normalized to the same twelve-word passage:

```text
insight a d e reveals one memorable behavior through an independent cadence
```

The fake body uses a hexadecimal uniqueness token, while the production linter
retains alphabetic sequences and drops digits. Distinct hashes can therefore
collapse to the same normalized word sequence. Fake generation also includes
a tree-global ordinal whose assignment depends on platform-sensitive path
enumeration. Windows happened to avoid the collision; Linux exposed it.

After recording the failed delivery check, the smoke unconditionally invoked
completed-run cleanup. Cleanup correctly rejected the nonterminal state with a
`ValueError`, masking the structured smoke report and its original lint cause.

The retained diagnostic image is
`astrowoof-domain-worker:diagnostic`, image digest
`sha256:54389124c29b972797622c92c36e86ef9631e57ad9e619d4c9df92eb0fd37c93`.
External acceptance evidence remains outside this repository under
`.acceptance/` and `C:\tmp\astrowoof-domain-worker-acceptance`; it is input
evidence, not sprint output to commit wholesale.

## Scope boundary

### In scope

- `FakeAuthoringProvider` and its deterministic fake field generator;
- installed release-smoke failure control flow and cleanup gating;
- focused fake-provider and smoke regressions;
- the complete deterministic repository test suite;
- reproducible patch-wheel construction and inspection;
- exact-wheel installed smoke on Windows and Linux;
- 0.2.1 patch-release coordinates, notes, checksums, and consumer handoff; and
- publication only after a separate explicit gate approval.

### Out of scope

- extraction, selection, scoring, synthesis, registry closure, or evidence;
- OpenAI Responses or Batch requests, routing, retries, polish, or critic;
- spend authorization, disclosure, snapshots, production acceptance/lint
  rules, assembly, provenance, or delivery semantics;
- AGF, SPC, pyswisseph, API, or product-policy changes;
- live provider tests or any paid operation; and
- replaying the seven-slice 0.2.0 qualification campaign.

`FakeAuthoringProvider` is packaged runtime code and is selectable through the
fake provider route, so the patch is not literally test-files-only. It is,
however, isolated from every paid/production provider path. If implementation
requires a change outside the listed fake-provider, smoke, tests, version, or
release-record surfaces, stop and request a plan revision.

## Proposed implementation

### Platform-independent fake output

- Remove dependence on a tree-global traversal ordinal.
- Bind fake content to stable logical inputs: pass ID, POSIX-relative workspace
  path, field path, and a file-local occurrence index only where needed.
- Encode the digest as a contiguous alphabetic token that survives
  `editorial_lint.words()` unchanged, for example a deterministic `a`-through-
  `p` mapping of hexadecimal nibbles.
- Assert uniqueness after the production linter's actual normalization, not
  merely before normalization.
- Preserve the deliberate first-attempt duplicate injection used to test retry
  rejection.

### Structured smoke failure

- Treat delivery completion as a prerequisite for delivery-artifact and
  cleanup checks.
- If the run misses `DELIVERY_COMPLETE`, preserve the observed run/subject
  state and original QA/lint evidence in the returned report.
- Skip `cleanup_completed_run` for nonterminal or review states.
- Always render the smoke JSON report and exit through the documented failed
  smoke status rather than an uncaught cleanup traceback.
- Keep completed-run cleanup coverage unchanged for successful smoke runs.

## Slices

### Slice 0 - Reproduction and patch boundary

- Confirm the clean source baseline and immutable 0.2.0 tag target.
- Reduce the retained Linux evidence to the exact normalized collision, final
  state, cleanup traceback, installed coordinates, and zero-spend fact.
- Reproduce the normalization collapse directly in focused tests without
  Docker or provider access.
- Confirm the proposed diff can remain within the declared scope boundary.

Gate: approve the reproduction, exact patch surface, and 0.2.1 coordinates.

### Slice 1 - Deterministic fake and smoke correction

- Implement stable fake identity material and normalization-safe alphabetic
  uniqueness.
- Gate cleanup and downstream delivery checks on successful completion.
- Add regressions for reordered path enumeration, different workspace roots,
  normalization uniqueness, structured non-delivery failure, and successful
  cleanup.
- Run focused tests, the complete deterministic repository suite, and
  `git diff --check`.

Gate: review and approve the narrow source/test diff. Any production-path diff
returns to planning.

### Slice 2 - Exact patch artifact qualification

- Update only approved patch-release coordinates and documentation.
- Build the wheel twice with a recorded `SOURCE_DATE_EPOCH`; require identical
  bytes and SHA-256.
- Inspect the complete wheel allowlist and confirm no diagnostic workspaces,
  caches, secrets, or acceptance artifacts entered the wheel.
- Clean-install the exact wheel outside the checkout and pass the Windows
  installed smoke.
- Replace only the SBE wheel/hash in the cached Linux acceptance image and pass
  the Linux installed smoke, preserving a compact machine-readable report.
- Run `pip check`; retain the existing qualified AGF/SPC/pyswisseph identities.

Gate: both installed smokes, artifact identity, wheel audit, and full suite are
approved. No live OpenAI qualification is required.

### Slice 3 - Patch handoff and publication

- Prepare 0.2.1 release manifest, checksum, hash-pinned requirement, patch
  notes, compatibility delta, and API-worker handoff.
- State explicitly that 0.2.0 production evidence is reused and that 0.2.1
  changes only fake-provider/smoke qualification behavior.
- After separate explicit approval, commit the reviewed records, create the
  annotated tag, push, and publish the wheel plus checksum.
- Authenticated-download both assets into a fresh directory and independently
  verify size, digest, checksum, tag target, and release metadata.
- Record post-publication evidence without moving the immutable tag.

Gate: pinnable 0.2.1 artifact is published and independently verified.

## Required tests

The minimum proportional test set is:

1. focused fake-provider normalization and ordering tests;
2. focused smoke success and structured-failure tests;
3. the complete deterministic repository suite;
4. two byte-identical wheel builds and wheel-member audit;
5. clean installed-wheel smoke on Windows;
6. clean installed-wheel smoke on Linux in the existing acceptance harness;
7. `pip check` in the Linux worker image; and
8. post-publication authenticated asset verification, if publication is
   separately approved.

Explicitly not required: OpenAI calls, Batch detach/resume, spend-policy live
testing, provider disclosure replay, full editorial live qualification, or the
seven-slice 0.2.0 release campaign.

## Controls

- Follow `docs/sprints/README.md`; pause at every slice gate before commit or
  progression.
- Preserve the immutable 0.2.0 tag and published assets.
- Make no paid provider call; fake and smoke paths must remain offline.
- Do not weaken or special-case the production linter to make fake output pass.
- Do not suppress the original QA failure when smoke orchestration fails.
- Test the installed wheel without checkout imports.
- Keep Docker layers, wheels, virtual environments, and raw acceptance output
  outside Git; commit only compact evidence and release records.
- Do not modify the API agent's existing uncommitted roadmap or acceptance
  harness work.

## Exit criteria

- fake output is byte-stable across supported Windows/Linux path behavior and
  unique under production word normalization;
- deliberate fake rejection still causes one rejected attempt and an accepted
  retry;
- failed smoke produces valid JSON, preserves the original failure, skips
  cleanup, and exits nonzero without an uncaught traceback;
- successful smoke reaches delivery and completes cleanup;
- focused tests and the complete deterministic suite pass;
- final wheel builds are byte-identical and pass the allowlist audit;
- the exact installed wheel passes smoke on Windows and Linux;
- Linux `pip check` and the qualified upstream wheel identities remain valid;
- release/handoff coordinates agree; and
- no live provider work or production workflow change occurred.

## Planned result records

Each completed slice will add `results/SLICE N - <name>.md` and compact JSON
where useful. `LOG.md` will record approvals, commands, commits, artifact
identities, cross-platform results, surprises, and any explicit plan revision.
