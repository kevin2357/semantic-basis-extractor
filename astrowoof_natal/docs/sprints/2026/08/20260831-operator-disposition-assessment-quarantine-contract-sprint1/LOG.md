# Sprint log

## 2026-08-31 — Slice 0 complete

- Read the API plan review in full and incorporated all seven refinements.
- Inventoried lifecycle v0.5, temporal v0.6, local-work v0.7, retry-lineage
  v0.8, external-authority, exact native-result, result-availability, and
  operator-retirement public readers.
- Froze native-only posture semantics; no API lease, capacity, reservation, or
  release fact is asserted.
- Added the missing `native_local_work_ready` class rather than misclassifying
  concrete ordinary work as quiescent or inconsistent.
- Chose an always-present empty list as the sole no-next-action representation;
  removed the ambiguous `none` action token.
- Froze exact digest-bound assessment identity and an opaque, non-path logical
  workspace identifier.
- Froze reader-bound terminal classification: explicit exact result reads are
  normal authority; availability is bounded recovery discovery only.
- No code, schema, fixture, provider, retained workspace, deployment, version,
  tag, or release change was made.

Current gate: paused at Voof-paws 1 before Slice 1 schema implementation.

## 2026-08-31 — Slice 1 complete

- Incorporated API's two Slice 0 documentation corrections into `Background.md`.
- Added the closed v1 JSON Schema and strict Python semantic validator.
- Froze eight class/posture/action/reason combinations and native-evidence
  precedence.
- Froze opaque logical-root identity and assessment-wide canonical digest.
- Added eight positive fixtures plus strict mutation coverage.
- Focused tests after API corrections: 12 passed, 1 optional `jsonschema` check skipped on the lean
  host interpreter.
- `git diff --check`: clean for the sprint contract/schema/test changes.

Current gate: paused at Voof-paws 2 before Slice 2 reader/projection work.

## 2026-08-31 — Slice 2 complete

- Closed lifecycle versions to released v0.5–v0.8.
- Closed the evidence-category vocabulary.
- Enforced completed-evidence/provider-identity and complete bounded-reference
  count relationships.
- Added the snapshot-validating root-level reader and exports.
- Added exact result/receipt/current-checkpoint terminal joining.
- Added a fail-closed v0.5 historical fallback without inventing local-work
  evidence.

## 2026-08-31 — Slice 3 complete

- Exercised exact/bounded × interactive/Batch provider custody.
- Proved completed and ambiguity precedence in mixed inventories.
- Proved unsupported legacy bounded Batch remains prohibited.
- Focused disposition suite: 21 passed, 1 optional schema check skipped.
- Affected lifecycle/retry-lineage regression set: 31 passed.
- `git diff --check`: clean.

Current gate: paused at Voof-paws 3 before packaging/installed qualification.

## 2026-08-31 — Voof-paws 3 correction complete

- Changed `read_operator_disposition_assessment()` so availability-based
  terminal-result discovery defaults disabled.
- Preserved explicit opt-in recovery discovery and its exact-result reader join.
- Added a regression that spies on the availability reader and proves an
  ordinary/default assessment never calls it.
- Focused disposition suite: 22 passed, 1 optional schema check skipped.

Current gate: Slices 2–3 approved; Slice 4 packaging is in progress.

## 2026-08-31 — Slice 4 source packaging complete

- Added the read-only `astrowoof-operator-disposition-assessment` CLI.
- Its ordinary surface exposes no recovery, authority, provider, or mutation
  input and refuses output inside the native workspace.
- Added a packaged sanitized eight-class fixture reader/validator.
- Added a closed qualification receipt/schema and
  `astrowoof-operator-disposition-qa` entry point.
- Qualification invokes the real CLI twice in fresh Python processes and proves
  replay, nonmutation, privacy, provider-free operation, and default-disabled
  availability discovery.
- Focused source suite: 26 passed, 1 optional schema check skipped.
- Froze the fresh candidate version as `0.4.37` before wheel qualification.

Current gate: installed-wheel Slice 4 qualification.

## 2026-08-31 — Slice 4 and lean candidate gate complete

- Ran the final `0.4.37` wheel qualification from an installed environment.
- `pip check`: no broken requirements with SPC `0.11.1`.
- Installed qualification receipt: `09294f61c5582ef207960048f0b50c5b1a4d3f9b79a97f508fd9e8198074c94f`.
- Built two controlled wheels with byte-identical SHA-256
  `032a2ab0d9367e4dad68c1a9814b75bbf7e108a00fde44c2fdc1602875ec0a7c`.
- Focused plus affected reader/lifecycle/retirement suite: 84 passed, 5
  expected optional-schema skips.
- `git diff --check`: clean (line-ending notices only).
- Full runtime suite deliberately not run under the package-only lean gate.
- Provider calls/retrievals/network/spend: zero. Retained QA/R2 access: zero.

Current gate: API review and explicit owner approval before commit/tag/publish.

## 2026-08-31 — final release approval

- API final review: approved without conditions.
- Owner approval: commit, tag, and publish `0.4.37`.
- Release execution begun from the reviewed source and deterministic candidate.

## 2026-08-31 — `0.4.37` published and verified

- Release source commit: `bb94fe1c5b9f63e9dd2b60ca07d886dbcca2c5a5`.
- Immutable tag: `astrowoof-natal-authoring-v0.4.37`.
- Published GitHub Release wheel and checksum assets.
- Downloaded the published wheel and independently reproduced SHA-256
  `032a2ab0d9367e4dad68c1a9814b75bbf7e108a00fde44c2fdc1602875ec0a7c`.
- Reinstalled the downloaded artifact; `pip check` reported no broken
  requirements.
- Published-wheel operator-disposition qualification passed with receipt
  `09294f61c5582ef207960048f0b50c5b1a4d3f9b79a97f508fd9e8198074c94f`.

Sprint status: complete.
