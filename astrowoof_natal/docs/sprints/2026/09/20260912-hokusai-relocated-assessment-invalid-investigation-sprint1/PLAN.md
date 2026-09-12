# Plan — Hokusai relocated-assessment refusal investigation

## Status

**Slice 0 approved and complete. No SBE implementation is indicated.** This
sprint is paired with API Sprint 94, which owns the correction proposal and
keeps all live execution separately gated.

## Slice 0 — SBE reader causal classification

**Status: approved and complete.** Provider-free paired controls identify
original-root binding as the exact compatible failure phase. API's job-bound
checkpoint/authoring-row join confirms the live authority used the API-run root
while native state preserved the allocation-root identity. No R2 read is
materially needed. See `SLICE 0 - RELOCATED ROOT IDENTITY CLASSIFICATION.md`
and `API REVIEW - SLICE 0 ROOT IDENTITY CLASSIFICATION.md`.

- Source-map the public `read_relocated_operator_disposition_assessment`, `validate_relocated_assessment_pair`, relocation authority construction, and exact snapshot validation paths in released `0.4.60`.
- Distinguish the exact checkpoint returned by API restoration for SBE job
  `3c1dc0cd-3169-4542-8f9b-40305d8dcf3b` from any run-wide "latest active"
  checkpoint. Freeze its checkpoint ID, generation, contract, compatibility
  identity, logical restore path, archive digest, and inventory digest before
  treating the catalogued `/work/deterministic-domain` path as assessment input.
- Build a provider-free Hokusai-shaped fixture: waiting provider custody, stable original logical root, copied physical root, exact authority fields, and no provider/mutation capability.
- Include paired root controls: one exact SBE-job authority whose original-root
  digest matches `run.json.workspace_contract.logical_root`, and one
  deterministic-domain/SBE-workspace mismatch proving the closed refusal phase.
- Exercise each closed reader/validator boundary and establish which one is compatible with the observed API generic rejection.
- Classify the reader in execution order without retaining raw paths or exception
  prose: authority/freshness, native identity, original-root binding,
  restored-root binding, snapshot manifest identity, snapshot inventory,
  terminal-result selection, inner assessment, post-read revalidation, and
  authority/wrapper pair intake.
- Compare API's documented deterministic-domain checkpoint restore path with native durable workspace-contract semantics using source/fixture facts only.
- Decide whether API validation/intake, SBE reader behavior, release-pair mismatch, or insufficient current evidence owns the next action.

**Exit:** exact reproduction or a bounded evidence gap; an explicit ruling on
whether the supplied checkpoint packet names the exact SBE-job checkpoint; list
of safe non-sensitive diagnostic classifications if needed; joint review before
any implementation or R2 request.

## Slice 1 — Conditional correction proposal (not authorized)

**Not opened on SBE.** Slice 0 proves an API identity-source defect, not an SBE
reader defect or observability ambiguity. API may propose the narrowest durable
native-root identity correction while preserving SBE's strict
snapshot/root/digest authority. Do not change SBE runtime behavior.

## Slice 2 — Conditional implementation/release qualification (not authorized)

Only after joint approval: implement exactly the approved change, run focused and installed-wheel qualification, and provide a release handoff. A new QA exercise requires separate API/owner authorization.
