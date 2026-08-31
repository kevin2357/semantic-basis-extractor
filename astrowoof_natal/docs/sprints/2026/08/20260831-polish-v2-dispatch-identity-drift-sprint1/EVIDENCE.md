# Evidence — polish v2 dispatch identity drift

## Planning inputs

- `Background.md` supplied by the API agent.
- Frozen API/native/checkpoint/action/admission/grant coordinates contained in
  that document.
- The Render trace path originally declared in the background was inspected and
  found to contain only the early initial-wave window. It is superseded for
  Slice 0 by the owner-supplied full export identified below.
- Current SBE `main` source for:
  - `cli/external_authority_v2.py`;
  - `external_authority_v2_execution.py`;
  - `temporal_lifecycle.py`; and
  - relevant closure request/binding construction sites.

## Preliminary source facts before retained inspection

- The v2 CLI loads supplied inspection, request, grant, and authorization
  documents separately.
- Intent commit validates the workspace snapshot and native dispatchability
  under the lifecycle writer before applying authorization.
- Selected actions must be providerless, unconsumed `PREPARED` work and must not
  be submitting or ambiguous.
- The executor rebuilds the current temporal lifecycle at the supplied
  observation time, joins the request to it, and requires exact equality with
  the supplied inspection.
- Grant/member authorization validation occurs only after those native/current
  checks.
- At this preliminary stage no conclusion was drawn about which check produced
  the retained incident; the Slice 1 evidence below closes that gap.

## Slice 0 diagnostic evidence

- Corrected full SBE log export:
  `C:\Users\kevin\Downloads\sbe logs.txt`;
  - bytes: `845872`;
  - lines: `1200`;
  - SHA-256:
    `61813d879183d4637553f96875df6459335b2b24a21bd7098ee33df10808e087`.
- The trace proves `a838af…` is stable across repeated v1 request reads at
  revision 75, while the lifecycle-v0.5 embedded request digest changes on each
  later observation and the constrained v2 request remains `07300bd…`.
- The trace records the exact earlier failure:
  `ValueError: Local-work consumption history is not append-only`.
- The v2 refusal stack proves dispatch failed because the requested identities
  did not match the native persisted intent after intent revalidation had been
  deferred for `action_state_or_custody_mismatch`.
- Focused provider-free checks:
  - v2 request identity stable across observation time;
  - complete v2 request/grant/document join accepted;
  - partial, reordered, wrong-binding, and cross-version joins refused.
  Result: `3 passed`.

## Slice 1 retained evidence

- Access manifest SHA-256:
  `b05eef946d2093579b1fac1b631bc8abc716ae7d0a6a38bc0551e16fb680e896`.
- Exact remote operations: one `HEAD`, one `GET`, zero list/write/delete.
- Archive:
  - bytes: `4779709`;
  - SHA-256:
    `ec70409af469ea8fffb9217533a2173a8c206675a9949aa249f9ce4e1be92000`;
  - provider version/ETag: `052b105050b4067d818814ae581d8b01`.
- Strict API archive restoration:
  - inventory SHA-256:
    `dba64797a61449848bb378bba82e74491d5a0b6d2b02fd75bff81d790a37ca4c`;
  - members: `964`;
  - expanded member bytes: `19897082`;
  - generation: `11`;
  - predecessor archive SHA-256:
    `5b115ce782a508c95b6f9417e3241db40b46047af3f4754603f994ffe400808b`.
- Inner native snapshot: all `934` declared members exist with exact byte sizes
  and SHA-256 digests; no missing, extra, or mismatched member.
- Retained state projection:
  - state revision `75`;
  - polish action `paid_c90…`: `PREPARED`, provider null, consumption absent,
    authorization null;
  - persisted intent request/grant: `e35ca8…` / `e09fbc…`;
  - persisted intent action: `paid_707…`, intent `PROVIDER_PENDING`;
  - corresponding ledger action: `REPORTED`, provider identity durable.

## Current gate

Published as SBE `0.4.34`. The authorized remote budget
is exhausted. No external provider, spend, retained reconciliation/resume/repair,
or retained-run mutation occurred.

## Slice 3 provider-free evidence

- New focused witness:
  `tests/test_external_authority_v2_sequential_intent_slice3.py`.
- Production boundaries exercised:
  - `commit_external_authority_v2_dispatch_intent`;
  - `dispatch_external_authority_v2_intent`;
  - `inspect_temporal_lifecycle`;
  - v2 request, grant, and authorization-document builders/validators.
- Exact reproduced outcomes:
  - first action set: `detached_provider_pending` with its ordered scripted
    identities durable;
  - fresh successor commit: `action_state_or_custody_mismatch`;
  - fresh successor dispatch: `authorization_mismatch`;
  - successor provider creates: `0`.
- Focused command:
  `python -m unittest astrowoof_natal.tests.test_external_authority_v2_sequential_intent_slice3 astrowoof_natal.tests.test_external_authority_v2_intent_fence`
- Result: `18 passed`.

## Slice 4 source-boundary evidence

- `SpendController.settle_active()` is the native transition that records
  provider-reported terminal action truth.
- Worker-thread settlement uses `persist_state()` and does not publish a complete
  workspace snapshot; it is therefore not alone a valid retirement checkpoint.
- `checkpoint_spend_boundary()` calls coordinator-owned `save_state()` before
  publishing the next native result/authority pause. That state-plus-snapshot
  boundary is the first complete checkpoint suitable for exact retirement.
- Existing dispatch already treats provider evidence as intent-revalidation
  deferral and supports a history lookup before provider creation. Extending
  that lookup for one strict `provider_completed` record can return the existing
  closed v3 `exact_replay` result without a new public schema.
- Existing pre-provider-refusal history supplies a compatible append-only native
  history container, but completed retirement requires a distinct schema and
  stronger exact terminal join.

## Slice 5 implementation evidence

- Runtime source:
  - `external_authority_v2_execution.py`: strict retired-intent validator,
    all-or-none retirement, and exact history replay;
  - `closure.py`: writer-fenced coordinator checkpoint integration before local
    progress/successor selection.
- New provider-free fixture:
  `tests/test_external_authority_v2_intent_retirement_slice5.py`.
- Direct Slice 5 result: `5 passed`.
- Affected matrix result: `49 passed, 1 optional-schema skip` across retirement,
  sequential v2, v2 contracts/routes, intent-fence, Moxie adoption, and composed
  post-fan-in tests.
- The actual creative-retry test enters `closure.main()`, adopts retained
  completed response evidence, runs normal reporting, and proves retirement is
  durable before the subsequent local-progress decision.
- No public schema/version changed; exact replay validates through the existing
  v2/v3 result validators.

## Slice 6 installed-wheel evidence

- Candidate version: `0.4.34`.
- Reproducible wheel SHA-256:
  `20a64e366840e143f1f9cb6cd936a7dd15341dc2041562e8f33860eb4ed70b2d`.
- Packaged command: `astrowoof-v2-intent-retirement-qa`.
- Receipt schema:
  `astrowoof.external_authority_v2_intent_retirement_qualification.v1`.
- Two installed executions produced byte-identical files with SHA-256
  `a5aea64d753995050defa832842a83e905313181a76cc8d42cf0a7fb9b2e5abc`
  and canonical receipt identity
  `0b2c6b1d201f59a9ecfbfa37f608af282726cbba881d518457399f5ca8381f5e`.
- The installed Python semantic validator and packaged Draft 2020-12 schema
  both accepted the receipt.
- Installed environment: SBE `0.4.34`, SPC `0.11.1`, `pip check` clean.
- Installed gates passed:
  - generic release smoke;
  - external-authority-v2 qualification;
  - post-fan-in-retry qualification;
  - terminal-review qualification;
  - intent-retirement qualification twice.
- Source-focused qualification: 7 passed, 1 expected optional-schema skip.
- Final affected runtime/contract matrix: 49 passed, 3 expected optional-schema
  skips in the lean host interpreter.
- This is provider-free qualification: external provider/network calls `0`,
  real provider creates/retrievals `0`, spend `$0`, retained Delerium access `0`.

## Publication evidence

- Source commit: `c5ec8c20216971f22da768f827a3602f42f1d04a`.
- Tag: `astrowoof-natal-authoring-v0.4.34`.
- Release:
  `https://github.com/kevin2357/semantic-basis-extractor/releases/tag/astrowoof-natal-authoring-v0.4.34`.
- Public asset: `astrowoof_natal_authoring-0.4.34-py3-none-any.whl`.
- GitHub asset digest and downloaded verification SHA-256:
  `20a64e366840e143f1f9cb6cd936a7dd15341dc2041562e8f33860eb4ed70b2d`.
- Release is public, non-draft, and non-prerelease.
