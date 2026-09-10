# Log

- 2026-09-10: Sprint opened with API-provided immutable coordinates and local Render-log export. No native or retained-QA mutation has occurred.
- 2026-09-10: Initial SBE review split Slice 0 into terminal-review,
  fresh-delivery, and retry/delivery-validation handoffs. The investigation will
  locate any omission among native publication, command serialization,
  subprocess parsing, and cycle-result translation before requesting retained
  checkpoint access.
- 2026-09-10: Slice 0 local source/log discovery completed. Both exact native
  publications are proven. Gutenberg lost its review handoff across detached
  provider-reconciliation exit semantics; Hypatia attempted publication before
  same-cycle accepted-delivery authority, then completed through a later
  delivery-validation retry with no lawful invocation identity to rediscover.
  Retained checkpoint access is not needed. Slice 1 will reproduce the two
  seams provider-free while preserving strict no-latest-result behavior.
- 2026-09-10: Slice 1 SBE producer correction implemented. Detached
  reconciliation now emits the existing exact terminal review/delivery command
  contract directly from the same invocation's returned sealed result and
  receipt. Nonterminal publications emit no terminal handoff. Focused
  source-tree qualification passed 20 tests with 4 skips. API retains ownership
  of detached exit-3 consumption and accepted-delivery publication ordering.
- 2026-09-10: API review requested a real detached CLI/stdout-JSONL regression.
  It exposed that reconciliation's review publication was still native v0.1,
  which cannot supply the custody-final terminal-review command. The producer
  now selects native terminal-review v0.2 for an exact `review_required` cycle.
  CLI qualification proves one exact review command plus the ordinary cycle
  result at exit 3, while provider-pending exit 3 emits no terminal command.
  Focused qualification now passes 24 tests with 4 skips.
- 2026-09-10: API re-review approved Slice 1 for package qualification.
  Following the Maintainer Release Playbook, selected the broad/full gate
  because reconciliation, custody-final terminal publication, and API wrapper
  translation are affected. Candidate identity `0.4.59` was confirmed unused
  locally and on origin and frozen before release-bound testing. The editorial
  contracts and optional Alloy model are unchanged: this correction transports
  an existing exact terminal identity and does not alter packet chronology,
  ownership, selection, projections, or capture semantics.
- 2026-09-10: The supported broad/full coordinator passed from candidate
  `0e61a4a53a00d6f808da9c0f42220b4e445f76c6`: 1,167 tests passed, 60
  skipped, in 977.011 seconds. Test-inventory SHA-256 was
  `c5c2fcbe8cd3e8a474d4422ce193382c6f3f7da5916c23c9e93e4b7b875bcd3e`.
  No manifest change was required because all new cases were added to existing
  classified test modules. Package reproducibility and installed-wheel gates
  are next; tag and publication remain unauthorized.
- 2026-09-10: Exact-lock package qualification passed. Two clean archive builds
  of `e5127caea466b12340472eee48b2563abfd68650` at
  `SOURCE_DATE_EPOCH=1789062636` produced byte-identical 1,376,264-byte wheels
  with 307 members and SHA-256
  `9211b7a7fd2e1a10a42cfe6bf47cafd749fa2076767b2dd7500621a93d9cbe92`.
  Clean installed import, dependency, release-smoke, and adversarial gates all
  passed. The immutable candidate is ready for API installed-wheel review;
  no tag, push, or publication occurred.
- 2026-09-10: API correctly blocked review after its independent build differed
  by one byte from the qualified wheel. Both original SBE qualification wheels
  remain intact and reproduce the recorded digest. A byte-for-byte handoff copy
  was retained at
  `C:\tmp\astrowoof_natal_authoring-0.4.59-e5127ca-qualified-py3-none-any.whl`,
  and the exact Python/pip/setuptools/wheel toolchain was added to the release
  qualification. API should test this retained artifact rather than a substitute
  rebuild.
- 2026-09-10: Owner authorized commit, push, tag, and publication. Main was
  pushed, annotated tag `astrowoof-natal-authoring-v0.4.59` was created at and
  remotely verified to peel to release lock
  `e5127caea466b12340472eee48b2563abfd68650`, and the exact qualified wheel plus
  `SHA256SUMS.txt` were published. A fresh separate download reproduced the
  1,376,264-byte wheel and SHA-256 `9211b7a7…d9cbe92`; GitHub's reported digest
  and the downloaded checksum line agree. Release `0.4.59` is complete.
