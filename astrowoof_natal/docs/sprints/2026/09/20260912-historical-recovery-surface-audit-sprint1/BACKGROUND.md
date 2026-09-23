# Historical Recovery Surface Audit — SBE Background

## Control Room source

This companion sprint supports [AstroWoof API Control Room issue #5: Audit and simplify historical recovery surfaces](https://github.com/kevin2357/astrowoof-api/issues/5).

Early QA recovery work accumulated native workspace, journal, authority, and retained-artifact compatibility bridges. The purpose is to distinguish durable native operator support and deliberate versioned migrations from logic that existed only to rescue one historical run shape.

## Objective

Build the native half of a cross-repo inventory. Preserve useful generic operator behavior and explicit supported migrations; identify candidates that can become clean, typed, fail-closed unsupported-history outcomes instead of permanent production rescue branches.

## Guardrails

- Audit and contract mapping only; no runtime implementation, release, provider work, workspace mutation, or retained-run action is authorized by this scaffold.
- Do not infer a removal merely from age. Record exact version/artifact applicability, current API callers, evidence authority, and test coverage.
- Keep operator capabilities generic and run-ID independent.
- Preserve historical proof in docs and fixtures rather than leaving bespoke production paths alive.

## Required inventory record

Every native surface recorded by this audit must identify:

- its source location and originating incident/sprint or released-contract
  provenance;
- the exact accepted `run.json`, workspace-snapshot, journal, result, receipt,
  or contract-schema version(s), including whether the acceptance is runtime
  production behavior or fixture-only compatibility;
- public CLI, Python export/reader, package-resource, API caller, and ordinary
  worker reachability;
- authority boundaries and the typed failure posture for an unsupported
  historical artifact; and
- targeted/current test coverage, including any fixture whose retained bytes
  must survive a later production-code removal.

Age, an incident label, an empty QA table, or a run-ID-specific fixture is not
by itself a removal decision.

## API companion

`C:\dev\github\astrowoof-api\docs\sprints\2026\09\20260912-historical-recovery-surface-audit-sprint95`

The API companion has completed its incident-driven reconnaissance and current
API surface inventory. Its primary records are:

- `Early Pipeline Update Sprint Candidates.md`
- `API Recovery Surface Inventory.md`

The API work is intentionally API-only. This SBE sprint should independently
inventory native readers, workspace/journal compatibility, command/result
contracts, and versioned retained-artifact support. Do not infer a cross-repo
removal decision from the API classification alone.

## Incident-era starting map

The following API sprints mention the early retained QA witnesses Aster and/or
Bramble. `Pipeline fix?` means the API sprint changed pipeline behavior in
direct response to the named incident, even if it preserved the historical run
rather than repairing it in place. This is a discovery aid for finding SBE
companions from the same era, not a claim that every matching SBE change is
legacy-only.

| API sprint | Aster | Bramble | Pipeline fix? | Incident role |
|---|---|---|---:|---|
| 18 — Admission/capacity discovery | yes | yes | N | Capacity evidence and policy discovery. |
| 19 — Provider-pending scheduling | yes | yes | N | General provider-pending scheduling capability. |
| 20 — State-transition control | yes | yes | N | General state model and operator-surface design. |
| 22 — Paid unattended qualification | yes | yes | N | Fresh cohort qualification. |
| 24 — Final pre-alpha updates | yes | yes | N | General retry-policy and terminal-failure-visibility design. |
| 26 — Native terminal-transition ingestion | yes | — | Y | Aster exposed native terminal-result ingestion gap. |
| 27 — SBE 0.4.5 lifecycle-inspection compatibility | yes | yes | Y | Aster exposed lifecycle-inspection reader mismatch. |
| 29 — SBE 0.4.9 compatibility requalification | yes | yes | N | Release-pair requalification. |
| 32 — Provider-pending reconciliation contract repair | yes | yes | Y | Aster provider responses were not reconciled. |
| 33 — Retained initial-wave recovery fence | yes | — | Y | Aster recovery attempted an unsafe new initial wave. |
| 35 — API/SBE executable contract qualification | yes | — | Y | Aster exposed missing released-wheel command qualification. |
| 37 — Legacy provider-pending bridge | yes | — | Y | Exact Aster pre-v1/v0.5 retained-workspace bridge. |
| 38 — Stuck-run terminal retirement | yes | — | Y | Exact quiescent `720f8b3c…` allocation-holder retirement. |

## Current API findings relevant to native review

API's strongest possible historical-only candidates are the retained
validator/lifecycle-evidence replay recoveries and the Sprint 37 legacy
provider-pending and temporal-lifecycle bridges. They remain only provisional:
SBE must determine whether any supported native artifact/journal/result reader
still requires those compatibility paths. API's terminal ingress,
provider-pending branch selection, initial-wave fence, external-authority
admission, and native operator retirement currently appear generic and durable.
