# Retry external-authority v2 dispatch handoff — evidence index

## Planning evidence

- `BACKGROUND.md` — SBE incident summary, containment, identities, and open
  contract questions.
- `PRE-SPRINT HUDDLE.md` — initial interpretation, competing seam concerns, and
  investigation posture.
- `PLAN.md` — bounded evidence protocol, provisional slices, tests, and review
  gates.
- API Sprint 58 `BACKGROUND.md`, `PLAN.md`, `EVIDENCE.md`, and `LOG.md` — paired
  consumer facts and SBE-first sequencing.

## Known facts before Slice 0

- SBE 0.4.30's generic provider-dispatch refusal prevented provider I/O for the
  providerless Hellman retry.
- Hellman repeatedly returned to API retry-wait while retaining the active slot.
- Diffie instead failed strict ordinary-resume lifecycle consumption.
- API reports its retry authorization was persisted, but that alone does not
  prove that a current SBE v2 request/grant envelope existed.
- Dashboard-visible provider completion is diagnostic, not authoritative native
  evidence.
- QA SBE worker is reported suspended; no retained-run recovery is authorized.

## Current evidence limitations

- Exact retained checkpoint coordinates, object hashes, and snapshot members have
  not yet been frozen or inspected.
- Exact request/grant/document joins for the providerless retry are not yet proven.
- The precise native state of provider-bound retry completion/fan-in at each
  failing invocation is not yet known.
- No provider-free production-boundary reproducer has yet been added.

## Slice 0 source and provider-free evidence

- `SLICE 0 - SOURCE BOUNDARY AND PRELIMINARY CAUSAL ASSESSMENT.md` — source map,
  proven released behavior, falsified Diffie shortcut, and provisional ownership
  assessment.
- `test_retry_external_authority_v2_handoff_slice0.py` — mixed-custody v0.5/v0.7
  characterization, real generic CLI refusal with byte-identical nonmutation, and
  packaged complete-handoff qualification.
- Focused suite with existing composed-runtime and duplicate-submission tests:
  19 passed in 44.654 seconds.
- `SLICE 0 - REQUEST FOR RETAINED CHECKPOINT COORDINATES.md` — exact closed packet
  needed before bounded R2 inspection.

The earlier statement that no provider-free reproducer existed is historical
pre-Slice-0 status. A provider-free source/runtime characterization now exists;
retained-run reproduction and exact joins remain pending.

## Current gate

Historical pre-inspection gate above is superseded.

## Slice 0 retained evidence

- `API ACTIVE CHECKPOINT COORDINATE PACKET.json` and `.sha256` — exact authorized
  Diffie/Hellman object identities; packet hash
  `7071e19780a1bfa88f9789764a1d79e63b2a7ef3160881b3a830f1030fba26a5`.
- `SLICE 0 - READ-ONLY R2 ACCESS RECEIPT.json` — two HEADs, two GETs, zero lists,
  zero writes, zero provider operations, exact archive/inventory/snapshot hashes.
- `SLICE 0 - SANITIZED RETAINED TIMELINES.json` — machine-readable native/API
  chronology with provenance boundaries.
- `SLICE 0 - DIFFIE AND HELLMAN SANITIZED TIMELINES.md` — causal assessment and
  consumer implications.
- Hellman sealed result `nres_1087eba75d3c29aba23193d5`, SHA-256
  `1087eba75d3c29aba23193d525c3d1d58e30936b896ddf3de9172980490b338e`.
- Hellman receipt `nreceipt_f367d82b9a92c868399d9d17`, SHA-256
  `f367d82b9a92c868399d9d17624e371f69f5d719239bbf02b448da44abd7c2ce`.
- Hellman journal range 82–85, SHA-256
  `0154ba74e7ab574350ce14198849a0cd1442780f278e531a796f120e8aeb62ac`.

## Slice 0 conclusion

- Hellman: SBE sealed review-required before the later loop. The first proven seam
  is API terminal-result ingestion/routing, not missing v2 dispatch capability.
- Diffie: active checkpoint is coherent provider-pending/not-due and predates the
  later strict-consumer error. Exact rejected evidence was not present in the
  retained object.
- No SBE runtime/schema correction is presently justified.

## Current gate

Slice 0 complete; paused at Voof-paws 1 for owner/API review.

## Voof-paws 1 and Diffie bounded follow-up

- `API VOOF-PAWS 1 REVIEW.md` independently corroborates that API has no native
  receipt row for Hellman's sealed result and approves the API-first correction.
- `SLICE 0 - DIFFIE BOUNDED FOLLOW-UP.md` records the retained-evidence limit and
  the source-compatible strict-consumer seam.
- `test_completed_retry_beside_pending_retry_has_local_work_but_no_dependency`
  proves provider-free that completed local fan-in may coexist with pending
  provider custody, yielding v0.5 `ordinary_resume` with zero local dependencies
  while v0.7/v0.8 exposes an explicit local-work operation.
- The exact historical Diffie lifecycle document remains unavailable. The test is
  not represented as retained-run reproduction.
- Focused Slice 0 test module: 10 passed in 23.939 seconds; `git diff --check`
  clean.
- Owner-exported SBE-worker log: generation 8 accepted at `08:55:01.340Z`;
  attempt 7 claimed at `08:56:45.629Z`; embedded reconciliation inspection
  rejected at `08:56:52.347Z`; no successor checkpoint accepted.
- Owner-exported HTTP API-service log contains only deployment/health evidence and
  no SBE-worker validator inputs.
- No second R2 access, provider operation, retained mutation, or worker resume
  occurred.

## Current gate

Investigation complete. No SBE runtime/schema release is indicated. API review is
requested for terminal-result-first ingestion and newest-lifecycle consumption.

## API Slice 2 terminal-result preflight

- API Sprint 58 `SLICE 2 - TERMINAL PREFLIGHT CONTRACT NOTE.md` demonstrates that
  normal no-result availability and invalid discovery evidence are not safely
  distinguishable through the current convenience reader.
- `SBE RESPONSE TO API SLICE 2 - TERMINAL RESULT AVAILABILITY.md` freezes the
  proposed additive discovery-only schema, reader/CLI behavior, and test matrix.
- This is a narrow public-reader patch; no provider, lifecycle-selection, native
  transition, or authority behavior changes.

## Current gate

Paused for API contract review before implementing the availability surface.

## Slice 1 implementation evidence

- `API REVIEW - DIFFIE CEILING AND RESULT AVAILABILITY.md` approves the contract
  and records Diffie's final historical-evidence ceiling.
- `SLICE 1 - TERMINAL RESULT AVAILABILITY IMPLEMENTATION.md` records the exact
  public surface, binding, tests, and installed-wheel evidence.
- Focused source tests: 5 passed, 1 optional schema skip.
- Availability plus native-transition regressions: 49 passed, 1 optional schema
  skip.
- Non-release installed wheel SHA-256:
  `edb3303678492beec76272c70656dd7ee6b965af959913c3b59cf30b72aa944a`.
- Installed package entry point and schema present; installed CLI proved
  `none_available` and `available` without provider access.
- `git diff --check` clean apart from informational line-ending notices.

## Current gate

Slice 1 complete; paused for API consumer review. A fresh immutable version is
required before any release.

## Slice 1 API acceptance and release identity

- `API REVIEW - SLICE 1 TERMINAL RESULT AVAILABILITY.md` approves the additive
  discovery contract for API adoption.
- Fresh candidate identity: `0.4.31`.
- Candidate identity was frozen before broad/full qualification; `0.4.30`
  references above remain historical incident and non-release qualification
  evidence.

## Current gate

Release qualification is active against the final `0.4.31` version identity.

## Lean `0.4.31` release-candidate evidence

- Focused pre-release gate: 36 passed, one optional-schema skip.
- Full suite, run once: 905 cases; 857 passed, 47 expected skips, one deterministic
  packaged-receipt version mismatch.
- Corrected affected focused gate: 30 passed, two optional-schema skips.
- Byte-identical committed-source wheel builds:
  `6bb587c9cd5cd0ef8bf767a677450fbaf7fcd9bf3be655ef68584e279a03f0d9`.
- Artifact source commit:
  `3709f18d1b8c15c6030173868e175110a7894c51`.
- Installed SBE/SPC identity: `0.4.31` / `0.11.1`.
- Installed terminal-review receipt:
  `2f3ebfbcb6223c810e6c713ac446a04c2e0e4663a057faa8cb84540523d563be`.
- Installed release-smoke resource set:
  `c5dcbbf70c3378ec16cd69b77c9d8fe4cbcac04d67bbf247853dad3a0a10cb3d`.
- Installed availability CLI: `none_available` and `available` passed.
- External provider calls, spend, retained-QA reads/writes, worker resume, and
  deployment: zero.

## Current gate

Final owner/API release approval received. The full-suite exception remains
explicit and is not represented as a green full-suite run. The forthcoming
records-only release lock and tag are distinct from the artifact source commit.
