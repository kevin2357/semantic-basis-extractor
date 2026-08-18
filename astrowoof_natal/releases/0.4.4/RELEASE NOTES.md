# AstroWoof Natal Authoring 0.4.4

Status: release candidate for immutable annotated tag
`astrowoof-natal-authoring-v0.4.4`.

This patch extends bounded, fresh-worker provider reconciliation across every
currently supported Natal route and provider mechanism. Exact Natal Responses,
exact Natal Batch, and bounded-Natal Responses now share one strict public
scheduling/custody boundary without pretending their provider mechanics are
identical.

## Added

- lifecycle inspection v0.3 with validated native route, mechanism, and operation
  identity;
- reconciliation-cycle result v0.2 with closed provider-custody and financial-
  authority dispositions;
- retrieval-only exact Batch reconciliation with atomic terminal-file/member
  preflight and one paid action per Batch round;
- bounded-Natal Responses reconciliation across initial authoring, creative retry,
  polish, critic, and candidate stages enabled by the frozen profile;
- route-neutral public Python and CLI reconciliation interfaces;
- fresh-worker replay from durable completed evidence without duplicate provider
  retrieval or submission;
- redacted reconciliation observations and a packaged route-parity transition
  oracle for API adoption; and
- explicit fail-closed rejection of bounded Batch.

Missing Batch usage is never represented as reported zero cost. Provider retrieval
custody may end while API-owned financial or review authority remains retained.
SBE does not own API reservations, queue slots, billing, or dollar exposure.

Provider operations and provider spend during implementation and qualification:
zero / `$0`.

## Qualification

- complete repository suite: 356 passed;
- concurrent exact-Responses, exact-Batch, and bounded-Responses cohort passed;
- API transition-oracle compatibility baseline: 18 passed;
- exact 0.4.4 wheel installed smoke passed on Linux CPython 3.11;
- Windows installed-runtime qualification passed on CPython 3.12.13;
- two fixed-epoch release builds were byte-identical;
- wheel SHA-256:
  `ee98db9512a5d0bb7082ef1e4b92ab5923bac9bbb88014f2a35fbfceeee2e6bd`;
- wheel bytes/entries/resources/cache entries: 751150 / 91 / 50 / 0;
- exact AGF 0.8.1 and SPC 0.11.0 compatibility remains pinned; and
- artifact source commit:
  `8ca7bf98a2d48f059eb218834e756482dba439a3`.

Tagging, publication, and authenticated-download verification are pending the
release-record commit.

