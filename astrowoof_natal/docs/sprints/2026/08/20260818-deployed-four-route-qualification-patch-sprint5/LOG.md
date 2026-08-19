# Deployed Four-Route Qualification Patch Sprint 5 Log

## 2026-08-18 — 0.4.9 published and independently verified

- Immutable annotated tag `astrowoof-natal-authoring-v0.4.9` points to commit
  `f920b71fc48545e8f16f878306366dcaec23f906`; tag object is
  `d5d68f1d6cbe797883d1c26a90e1b8a1bfbf35f2`.
- GitHub release 372739029 was published at `2026-08-19T00:58:50Z` (UTC).
- Independently downloaded wheel: 836,513 bytes, SHA-256
  `3b900cc3216dd07e164af1a18a4a607c17e3fa1190711893808ba6527042f83d`.
- Wheel asset 520184930 and checksum asset 520184932 are durable release assets.
- Post-publication records land after the immutable tag and do not move it.

## 2026-08-18 — Exact 0.4.9 artifact qualified and authorized

- Kevin explicitly authorized the fresh immutable 0.4.9 release.
- Full source suite: 474 total, 454 passed, 20 expected skips.
- Versioned artifact source commit:
  `220aae69badb54ed657f2370167691db0e5be5cf`.
- Two fixed-epoch builds were byte-identical: 836,513 bytes, SHA-256
  `3b900cc3216dd07e164af1a18a4a607c17e3fa1190711893808ba6527042f83d`.
- Exact Windows and network-isolated Linux wheels passed `pip check`, lifecycle
  smoke, release smoke, and `astrowoof-deployed-qa`.
- Exact 0.4.9 receipt digest:
  `104e81d5fc9e6014264c7887e5e1dac626286d29fe732cbb4b07c719497face5`.
- Provider operations/spend: 0 / USD 0.

## 2026-08-18 — V2 API review accepted

- API approved the corrected real-mechanism exact and bounded Batch cells.
- Confirmed the public command is sufficient for API Slice 4's deployed-QA gate
  and remains qualification-only/non-authoritative.
- API recommends fresh immutable 0.4.9. Version bump, final artifact gates, tag,
  and publication remain pending Kevin's explicit authorization.

## 2026-08-18 — Batch mechanism correction complete

- API approved the command/receipt/interactive shape but rejected the initial
  qualification-local Batch round simulation as insufficient deployed evidence.
- Replaced it with the native exact `author_pending_passes_batch` path using six
  generated qualification workspaces and a pending scripted transport.
- Replaced the bounded simulation with the native bounded Batch preparation and
  authoring-cycle path using six minimized qualification pass packets and the
  equivalent pending scripted transport.
- Each native route now persists exactly one round, one provider Batch ID, and six
  distinct ordered custom IDs; a fresh reader reconstructs those facts from
  native `run.json`.
- Focused suite: 24 passed. Installed Windows and network-isolated Linux command:
  pass with unchanged receipt digest. Provider operations/spend: zero.

## 2026-08-18 — Implementation checkpoint

- Added qualification-only public API, validator, schema reader, and console
  command with no credential, network, authority, or production-run inputs.
- Added a closed content-addressed receipt covering all four route cells, bounded
  final-QA precedence, and duplicate-claim pre-provider refusal.
- Registered the schema in the packaged contract catalog and lifecycle smoke.
- Focused source/API gate passed; strict schema validation passed.
- Installed Windows and network-isolated Linux command invocations passed from a
  built wheel and emitted the same receipt digest.
- Candidate retains immutable published version 0.4.8 and is not publishable.
  Proposed fresh patch version is 0.4.9 after API/Kevin review.
- Provider operations and spend: zero.
