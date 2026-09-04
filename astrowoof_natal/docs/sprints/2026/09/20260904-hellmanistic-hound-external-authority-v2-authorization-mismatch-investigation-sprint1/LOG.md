# Log — Hound external-authority v2 authorization mismatch

- 2026-09-04: Companion sprint opened with API-provided current QA coordinates
  and an unfiltered, read-only SBE log export. No implementation, provider work,
  retained-run access, or commit occurred.
- 2026-09-04: Slice 0 was sharpened to prove the exact dispatch predicate and
  the predecessor-intent retirement path. The supplied trace already suggests
  that the first polish authority passed its fence and provider creation, while
  a reported predecessor retained `PROVIDER_PENDING` intent state before a
  successor authority attempt. This remains a source/log hypothesis pending
  public-boundary reproduction.
- 2026-09-04: Slice 0/1 completed. The trace proves the fresh successor
  request/grant reached `external_authority.fence_validated`; the first native
  conflict is `action_state_or_custody_mismatch` against Hound's retained old
  intent. Released `0.4.44` reconciliation publishes completed response facts
  without requesting intent retirement. The public v2 CLI then catches that
  conflict but calls dispatch with the fresh identities, producing a generic
  `authorization_mismatch` before provider I/O. A provider-free public-CLI
  regression reproduces this sequence with zero payload resolution/create.
  No retained QA state was accessed or mutated.
- 2026-09-04: Implemented the narrow repair candidate. The coordinator-owned
  post-adoption reconciliation checkpoint requests strict retirement of an
  exactly completed ordinary-v2 intent; incomplete, pending, or ambiguous
  inventory cannot retire. The v2 CLI now turns a legacy stale-intent conflict
  into a closed v4 command-result/v5 dispatch-result refusal instead of calling
  dispatch with different identities. Focused v2/retirement/mixed-custody
  suite: 16 passed, provider-free. Awaiting API review of the public result
  shape before qualification or release preparation.
- 2026-09-04: Incorporated API's classification narrowing. The public v4/v5
  refusal is gated by the exact nonmutating completed-intent retirement proof,
  not the broad `action_state_or_custody_mismatch` error family. A live
  submitting/non-`PREPARED` negative regression confirms unrelated action-state
  failures preserve their original exception and cannot be mislabeled as an
  unresolved completed intent. Focused suite: 17 passed; diff check clean.
- 2026-09-04: Slice 3 installed-wheel qualification completed for frozen
  `0.4.45`. Controlled duplicate builds matched at
  `bcee274df15e877ca54efecbada15bed8565a604493689fdc9790e6178aeb42b`.
  The isolated installed candidate passed public intent-retirement qualification,
  installed CLI/module regression, and packaged v4/v5 schema-reader checks with
  no provider, R2, or retained-QA access. SPC `0.11.1` and its declared
  `jsonschema` dependency installed in the isolated runtime; `pip check`
  reported no broken requirements. Final tag/publication remains pending
  explicit approval.
- 2026-09-04: API technically approved the `0.4.45` candidate for
  tag/publication. Deployment sequencing is explicit: the API must implement
  and qualify exact v4/v5 refusal intake before the QA fleet relies on the
  patch; unknown results remain fail-closed in the interim.
