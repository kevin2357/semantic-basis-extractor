# Log — terminal-dominance handoff

- 2026-09-04: Sprint created from the fresh Rascal/Madeleine QA cohort. The
  supplied facts come from API’s authoritative PostgreSQL readback plus
  filtered SBE worker traces. No source implementation, provider access, R2
  access, API/QA mutation, workspace retrieval, deployment, or release has
  occurred in this sprint.

- 2026-09-04: Slice 0 source mapping completed, provider-free and read-only.
  `inspect_lifecycle()` already treats successful delivery and final-QA review
  statuses as terminal, and explicitly says optional evidence must not reopen
  them. Three production entry paths nevertheless call
  `run_qualitative_review()` immediately after `finalize_subjects()` accepts
  delivery: the Batch reconciliation coordinator, the interactive
  reconciliation coordinator, and direct authoring. Both reconciliation
  coordinators also publish a `local_continuation` record after finalization,
  even if the resulting native inspection is terminal. This matches Rascal's
  post-delivery critic selection and Madeleine's terminal-result/local-progress
  contradiction. No runtime code changed; the next gate is contract/review
  before a shared terminal-dominance implementation.

- 2026-09-04: Slice 1 implemented provider-free. Finalization now persists
  before later optional-stage selection in direct authoring and both exact
  reconciliation coordinators. A complete subject-finalization conclusion
  suppresses new qualitative work; a concluded run with separately created
  local successor work is retained for typed review rather than resumed. Batch
  cycle results no longer advertise local continuation when their coordinator
  reaches such a conclusion. Focused contract/lifecycle tests: 32 passing.

- 2026-09-04: Slice 2 completed provider-free. New production-shaped tests
  exercise the direct public CLI plus exact interactive and exact Batch
  reconciliation coordinators. Each commits a delivery conclusion while a
  qualitative critic is configured, proves the critic cannot run, and proves
  no successor action, external-authority request, grant, or synthetic local
  continuation is published. The focused matrix (including retained-custody
  and local-successor contradiction controls) passed: 35 tests. No external
  access or mutation occurred.

- 2026-09-04: Slice 3 pre-release installed-candidate qualification completed.
  A locally built wheel was installed into an isolated qualified environment;
  it imported from `site-packages`, passed dependency checking, exposed the
  packaged detailed terminal-review v2 schema, and completed the
  provider-free terminal-review/reconciliation continuity command with zero
  create/POST activity. Its detailed receipt discloses the exact immutable
  result, receipt, checkpoint, and snapshot join.
  The currently labeled candidate version is already released, so no tag was
  prepared; release review must choose a fresh patch version and repeat the
  final immutable-wheel qualification.

- 2026-09-04: API pre-release gate selected fresh version `0.4.46`. The
  committed release candidate was rebuilt twice with `SOURCE_DATE_EPOCH=0`;
  the final wheels are byte-identical at SHA-256
  `c6155ed71428865faa49eaeaf3442f5f64bb670e2317b1ec6dfd0bda54dcbb14`.
  The final wheel was force-installed into the isolated environment, passed
  `pip check`, exposed only the packaged v2 terminal-review schema, and passed
  both public terminal-review qualification forms. Its detailed receipt hash
  is `9f0f1c7788e591fe869cdb75451b18f13d54dc8be7d276ca690aed9d14755545`.
  This remains provider-free: one scripted GET and zero POST/create, external
  network, or spend. Tag/publication awaits explicit owner approval.

- 2026-09-04: Owner explicitly approved the full release process. A mistakenly
  named source-only tag `v0.4.46` had briefly been pushed without a GitHub
  release or wheel asset; it was removed locally and remotely under that
  authorization. The established release coordinate is
  `astrowoof-natal-authoring-v0.4.46`, with the exact qualified wheel and
  checksum assets still to be published and independently downloaded.

- 2026-09-04: SBE `0.4.46` published under annotated tag
  `astrowoof-natal-authoring-v0.4.46`. The tag object is `5468258` and resolves
  to release-coordinate commit `b95c4f1`. GitHub release `382856483` carries
  the exact qualified wheel and `SHA256SUMS.txt`; GitHub reports wheel asset
  digest `c6155ed71428865faa49eaeaf3442f5f64bb670e2317b1ec6dfd0bda54dcbb14`.
  A fresh authenticated download reproduced that digest and matched the
  downloaded checksum manifest. This post-publication evidence does not move
  the immutable tag.
