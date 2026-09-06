# Evidence — Muffin Local-Resume Quiescent-Loop Investigation Sprint 1

Status: closed before Slice 0; API-owned defect identified

## Reviewed evidence

- API-provided `BACKGROUND.md` for Muffin and Biscotti.
- SBE 0.4.25 lifecycle v0.7 selection and consumption implementation.
- SBE 0.4.25 provider-pending lifecycle v2 qualification implementation.
- API Sprint 50 v0.7 adoption plan/log and worker scheduling branch.

## Initial finding

The existing qualification directly changes completed retry native state before
calling the public consumption commit. The runtime regression mocks the authoring
continuation with the same expected mutation. Neither proves that real reconciled
creative-retry response evidence is consumed by the production ordinary-resume
path.

This finding is a hypothesis about the retained incident until Slice 0 reproduces
the full production path provider-free. No retained workspace was inspected.

## Safety totals

- Muffin access/mutation: 0
- Biscotti access/mutation: 0
- provider creates/retrievals: 0
- external network calls: 0
- spend: USD 0
- production deployment/configuration changes: 0

## Accepted diagnosis

The API worker correctly obtained SBE's typed lifecycle inspection, then reduced
it to the boolean inverse of `release_until_due`. That reduction incorrectly maps
the closed non-local dispositions `retain_for_review` and
`unsupported_retain_capacity` to local continuation.

This is sufficient to explain the observed repeated `local_resume -> quiescent ->
deferred` loop and retained capacity without positing an SBE v0.7 contract defect.

## Resulting ownership

- SBE source/schema/runtime changes: 0
- SBE release required: no
- API typed-result translation correction: required
- API starvation regression: required
- API expired-lease reaper/reset-precondition correction: separate and required
- retained Muffin/Biscotti access or mutation by SBE: 0
