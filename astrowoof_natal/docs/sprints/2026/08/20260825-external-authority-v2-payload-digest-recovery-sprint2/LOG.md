# Log

## 2026-08-25 — Sprint opened

- API supplied the first fresh-cohort evidence of two ordinary v2 commands sealed
  as `pre_provider_refusal / request_payload_digest_mismatch` with zero provider
  I/O.
- Confirmed the repository is on `main` after SBE 0.4.23 publication.
- Initial source tracing identified a concrete representation mismatch: ordinary
  exact authoring binds the complete payload but persists a redacted request plus
  the exact workspace prompt separately; the v2 resolver currently hashes the
  redacted JSON directly.
- Created a focused recovery plan. No runtime source, provider operation, retained
  QA workspace, version, tag, or release was changed.

Next action: owner/API plan review, then Slice 0 provider-free reproduction.

## 2026-08-25 — Plan approved; Slice 0 begins

- Owner and API approved the plan with three clarifications: bounded applicability
  must be assessed rather than assumed; historical reconstruction receives stricter
  exact-structure/encoding/uniqueness tests than new direct persistence; and the
  old refusal receipt/action history must remain immutable while recovery derives
  a fresh truthful native posture rather than pretending the refusal never occurred.
- Updated the plan accordingly and began the provider-free production-path
  characterization.

## 2026-08-25 — Slice 0 characterization complete

- Added a provider-free regression through the production exact authoring adapter.
  It proves the complete payload binding, lossy redacted request artifact, current
  resolver refusal, and exact match when the original three-block segment structure
  is available.
- Found that the prompt text file flattens three content blocks and omits the two
  cache-breakpoint annotations. The two persisted files are therefore insufficient
  for the originally proposed literal field reattachment.
- Assessed bounded applicability: bounded initial and later ordinary interactive
  paths persist their complete request bodies and do not share this defect. No
  bounded runtime expansion is recommended.
- Characterized 0.4.23 refusal handling: immutable refusal history is retained, but
  unentered actions become history-bearing operational `PREPARED` work. Recorded
  the API clarification as a contract decision rather than silently changing it.
- Focused test passed: 1. External provider/network/spend and retained-QA activity
  remained zero.

Next action: API review chooses the exact historical compatibility rule and confirms
whether history-bearing `PREPARED` remains valid current posture.

## 2026-08-25 — Slice 0 approved; compatibility decisions frozen

- API selected snapshot-bound deterministic rebuild for historical exact work and
  rejected literal two-file reattachment.
- API accepted the current history-bearing operational `PREPARED` posture, provided
  immutable refusal/grant history remains and every later attempt begins with fresh
  inspection/request/grant authority.
- New work must persist a direct private payload through a binding-owned,
  snapshot-declared content reference; recursive discovery is prohibited.
- Bounded runtime remains out of scope because its complete direct-payload evidence
  already satisfies the stronger rule.

## 2026-08-25 — Slice 1 complete

- New ordinary requests now persist one private complete-payload artifact before
  authorization and attach its exact path, file digest, canonical request digest,
  representation, and schema identity to the native ledger action.
- The v2 resolver validates that sole action-owned reference against the complete
  snapshot and binding. It no longer recursively searches for plausible payloads;
  an unreferenced duplicate is ignored.
- Historical exact 0.4.23 creative retries use a deliberately closed compatibility
  adapter. It validates runtime/run/resource/profile/provider/route/attempt/source/
  feedback identities, rebuilds through the production request builder, and then
  matches the persisted flattened prompt, exact redaction shape, and binding digest.
- Historical bounded work and unsupported historical shapes remain fail-closed;
  bounded direct-payload persistence remains unchanged except for receiving the
  same exact action-owned reference.
- Focused payload and surrounding v2/spend suites passed: 47 tests.

## 2026-08-25 — Slice 2 complete; API recovery review gate

- Added a production-shaped provider-free sequence using the real lossy 0.4.23
  artifacts and real resolver. The first invocation produces the incident's exact
  `request_payload_digest_mismatch` with `not_attempted`, replays exactly, leaves
  history-bearing `PREPARED` native work, and cannot reuse its old authority.
- A later inspection emits a distinct request; a fresh grant authorizes the exact
  historical deterministic rebuild and produces exactly one scripted provider
  create. Exact replay produces no second create, and the original refusal history
  remains byte-semantically unchanged within the append-only history.
- The compatibility adapter now additionally requires its retained source archive
  to resolve beneath the restored logical workspace; an external same-hash archive
  fails closed.
- Combined payload, CLI, refusal/replay, intent-fence, route, and spend suite passed:
  57 tests. Provider/network/spend and retained-QA activity remained zero.

Next action: API reviews the Slice 2 recovery evidence before installed-wheel and
consumer-handoff work.

## 2026-08-25 — Slice 3 complete; release review gate

- Added the public `astrowoof-payload-recovery-qa` installed-wheel command, closed
  Python validator/reader exports, and packaged Draft 2020-12 receipt schema.
- The command accepts no provider credential, production input, run directory,
  payload, request, grant, or authorization. It constructs a sanitized temporary
  historical workspace and exercises the real refusal/fresh-authority/rebuild/
  create/replay path.
- Added the API recovery handoff and retained-run procedure. Protected request
  bytes remain private and never enter its receipt or public artifacts.
- Focused candidate suite passed: 59 tests.
- Candidate 0.4.24 wheel installed into an isolated environment; the new
  qualification and generic installed release smoke both passed.
- Two deterministic candidate builds under the frozen build epoch were identical:
  `eae1206e54e83e4f874de0595a8d2c616fc11a3980ba91f228d34e3186a27404`.
- Provider/network/spend and retained-QA activity remained zero.

Next action: final owner/API release review before source commit, final source-bound
rebuild, tag, or publication.

## 2026-08-25 — SBE 0.4.24 published and verified

- Committed and pushed implementation/source identity `00351b0`.
- Full committed-source suite passed: 730 tests with 37 expected skips.
- Rebuilt twice with the frozen epoch; both wheels matched SHA-256
  `eae1206e54e83e4f874de0595a8d2c616fc11a3980ba91f228d34e3186a27404`.
- Reinstalled the final wheel and reran generic smoke and payload-recovery QA;
  both passed.
- Published immutable tag `astrowoof-natal-authoring-v0.4.24` and wheel/checksum
  assets. GitHub's asset digest and an independent download both match.
- No provider, spend, or retained-QA activity occurred.
