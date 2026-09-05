# Log

## Intake

- Companion to API Sprint 78.
- No implementation, artifact retrieval, provider operation, retained-run
  mutation, release, or commit has occurred.

## Slice 0 — Source and trace characterization

- Reviewed the complete four-part SBE worker trace export under
  `C:\tmp\astrowoof-sbe-polish-authority-20260904`.
- Hype and Frisbee follow the same deterministic sequence:
  1. all ordinary passes are accepted and the run reaches
     `AUTHORING_COMPLETE`;
  2. final assembly produces `FINAL_QA_WARN` with zero validation errors and
     only lint findings;
  3. `finalize_subjects()` intentionally enters `polish_subject()`;
  4. the spend controller durably prepares the first polish action and raises
     the ordinary authorization pause;
  5. the outer status becomes `AWAITING_SPEND_AUTHORIZATION`;
  6. lifecycle nevertheless selects `retain_for_review / none` and publishes no
     external-authority request; and
  7. semantic closure returns `review_required` without provider I/O.
- Source topology explains the trace without a retained-workspace read:
  - `finalize_subjects()` treats `FINAL_QA_WARN` as the input to enabled polish;
  - `polish_subject()` creates a `SUBMITTED` attempt before the spend boundary
    prepares its paid action;
  - `finalization_conclusion()` also classifies every `FINAL_QA_WARN` subject as
    `review_required`; and
  - lifecycle gives that conclusion precedence over the prepared-action
    external-authority branch.
- Added a provider-free public-inspection characterization proving both sides:
  - prepared polish is currently hidden behind `retain_for_review`, with no v2
    request; and
  - the same warning without elected polish remains a non-dispatching review
    closeout.
- No R2 access is needed for the causal gate. Logs and public/source behavior
  establish the contradiction directly.
- No production implementation has been changed. Pause for reciprocal review.

## Verification

```text
python -m unittest \
  astrowoof_natal.tests.test_polish_authority_handoff_slice0 \
  astrowoof_natal.tests.test_terminal_dominance_slice1 -v

Ran 5 tests in 0.042s — OK
git diff --check — clean for Slice 0 files
```

## Slice 1 — Exact provisional-polish identity join

- Incorporated `API SLICE 0 REVIEW.md`.
- The provisional exception is now closed and subject-local. It requires:
  - the subject state is `FINAL_QA_WARN`;
  - that same subject's current/last polish attempt is `SUBMITTED`;
  - the attempt carries one exact `paid_action_id`;
  - exactly one ledger action has that identity;
  - the action is `PREPARED` with no authorization, provider, or consumption;
  - its binding is `stage=polish`, exact
    `<subject>:polish:<attempt-number>` route, and interactive service; and
  - the run is not the bounded route.
- `polish_subject()` now persists the action ID from the typed authorization
  pause onto the already-durable current attempt before re-raising. This closes
  the provenance join that production previously omitted.
- A genuinely sealed `terminal_transition` remains dominant even if stale bytes
  appear to contain a matching prepared polish action.
- Provider-free tests cover:
  - the exact positive join and one ordinary-v2 request/action identity;
  - no elected polish;
  - wrong subject route;
  - wrong attempt action ID;
  - reported/stale action;
  - unrelated stage;
  - Batch service; and
  - a committed terminal transition.
- No generic resume, API behavior, provider I/O, R2 access, or retained QA was
  changed or exercised.

## Slice 1 verification

```text
Focused provisional-polish + terminal-dominance matrix: 9 passed
Lifecycle inspection + existing polish pause regression: 8 passed
```

## Slice 2 — Public qualification and neighboring-stage audit

- Added the provider-free public command
  `astrowoof-polish-authority-handoff-qa` and its closed packaged schema.
- The receipt proves:
  - exact subject/attempt/action/binding evidence selects external authority;
  - the derived request is `astrowoof.external_authority_request.v2` with the
    one exact action ID;
  - warning-without-polish remains non-dispatching;
  - mismatched subject, mismatched action, stale action, unrelated qualitative
    stage, Batch service, and sealed terminal evidence produce no request; and
  - provider/network/spend counts remain zero.
- The neighboring-stage audit ran the established mixed-custody and terminal-
  dominance matrices beside the new qualification. They preserve:
  - provider-bound optional work selecting reconciliation;
  - providerless authorized polish remaining nonterminal;
  - call-entry ambiguity outranking review;
  - final delivery refusing later local successor work; and
  - no-custody final-QA review remaining legitimate.
- No runtime exception was extended to critic/candidate. Their appearances in
  the negative matrix prove unrelated qualitative actions cannot unlock polish
  provisionality.

## Slice 2 verification

```text
Public qualification + identity matrix + terminal/custody neighbors: 21 passed
Source public qualification receipt: pass
External network/provider create/spend: 0 / 0 / 0
git diff --check: clean
```

## Slice 2 schema-parity correction

- Incorporated `API SLICE 2 REVIEW.md`.
- The packaged JSON Schema now freezes the same exact six negative-case names
  and four check names as the Python validator.
- Added direct schema-only mutations proving an alternate case inventory and an
  alternate check name are rejected even when a consumer does not invoke the
  Python validator.
- Corrected the new test module's source-tree import bootstrap so focused tests
  cannot accidentally import an older installed SBE package.
- Focused public/schema/terminal matrix: **13 passed**.

## Slice 3 — Release-bound regression gate

- Incorporated `API SLICE 3 REVIEW.md` and froze the fresh candidate version as
  `0.4.49` before expensive release testing.
- Updated the version-bound providerless-denial fixture and recomputed its
  receipt digest before the broad suite.
- Expanded focused matrix: **37 passed**.
- Packaged schema/public subset: **13 passed**.
- Broad/full suite: **1,052 passed, 3 expected skips** in 921.962 seconds.
- The broad run was green on its first release-bound execution; no late runtime,
  schema, validator, package-data, or harness correction followed it.
- No provider, R2, retained-QA, or spend activity occurred.
- Proceeding to committed-source reproducibility and installed-wheel
  qualification; immutable tagging remains a separate approval boundary.

## Slice 3 — Artifact-source build and installed qualification

- Committed the tested artifact source as
  `4fd7f9f7c8249c727bf15f276825b2b6fef8bb1e`.
- Exported that commit cleanly and built twice with
  `SOURCE_DATE_EPOCH=1788571152`.
- Both wheels are exactly 1,213,701 bytes with SHA-256
  `a99c93787514abaf86c1096b2565872ee90be577b635a04858e4672b50e339fa`.
- A third same-epoch build used for installation reproduced that exact digest.
- Installed the candidate into a fresh Python 3.12 environment with the local
  qualified `semantic-projection-core==0.11.1` wheel and the declared
  `jsonschema` dependency.
- `pip check` reported no broken requirements; the package imported from the
  isolated environment's `site-packages` at version `0.4.49`.
- The installed public `astrowoof-polish-authority-handoff-qa` command passed.
  Its stdout validated against both the installed packaged schema and Python
  validator. Receipt SHA-256:
  `eef7e5123b9895793fe81a1db35c5fa41f89841fcb936b48687a9b6e58812d79`.
- Receipt activity is provider-free: external network calls 0, provider creates
  0, provider spend USD 0.
- A Windows tool-session ACL prevented reopening the first generated wheel from
  a later process. The qualification therefore rebuilt and installed within one
  invocation; its digest exactly matched both independently built candidates.
  This was an environment file-access issue, not package drift.
