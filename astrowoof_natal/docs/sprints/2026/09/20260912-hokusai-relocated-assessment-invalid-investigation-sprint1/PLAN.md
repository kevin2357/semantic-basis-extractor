# Plan — Hokusai relocated-assessment refusal investigation

## Status

**Slice 0 investigation active; all implementation is gated.** This sprint is paired with API Sprint 94.

## Slice 0 — SBE reader causal classification

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

If Slice 0 proves a genuine defect or observability ambiguity, propose the narrowest compatible correction. It must preserve strict snapshot/root/digest authority and return no fictional assessment. Include provider-free fixtures and an installed-wheel API consumer gate. Do not implement yet.

## Slice 2 — Conditional implementation/release qualification (not authorized)

Only after joint approval: implement exactly the approved change, run focused and installed-wheel qualification, and provide a release handoff. A new QA exercise requires separate API/owner authorization.
