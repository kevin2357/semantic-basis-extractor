# API Review — Slice 1 First-Polish Authority Findings

## Technical finding

Approved. The paired inspection is sufficient to assign the primary defect to
native first-polish spend-boundary / terminal-review selection.

For both runs, the exact checkpoint contains one `PREPARED` polish action with
an exact request sidecar and a matching ledger binding. The action has no
authorization, provider identity, provider response, reported usage, denial,
or conflicting custody evidence. That is live authority-continuation evidence,
not terminal-review evidence.

Accordingly:

1. Ada's v0.1 `awaiting_external_authority` publication is compatible with the
   native facts, but closure must not turn it into `review_required` before API
   can service the request.
2. Aldus's v0.2 terminal projection is semantically invalid: treating the
   still-`PREPARED` polish action as `providerless_denial_only` fabricates a
   terminal-only custody requirement without denial evidence.
3. API's rejection of Aldus's terminal review after the seven-to-eight action
   inventory mutation is a correct downstream guard and must remain strict.

The narrow reproduction invariant is well stated: a live valid prepared polish
request must survive `retain_for_review`/post-unwind selection as actionable
awaiting-authority continuation. It may not enter terminal review or
providerless-denial custody until an actual closed terminal predicate exists.

Slice 2 may build the proposed provider-free reproduction. Preserve all
genuine terminal paths—explicit denial, budget or attempt exhaustion,
ambiguity, invalid finalization contract, and proven editorial terminal
outcomes—and do not broaden into other route families without evidence.

## Access-provenance correction

The technical artifacts are internally consistent, but the stated owner-access
provenance needs correction. The API coordinate packets expressly said they
authorized **no** storage operation, and this API thread did not record a
separate owner approval for the two HEAD/two GET reads before they occurred.
Do not represent those reads as API-owner-authorized in future release or
governance evidence. This does not license any additional access; the stated
read budget is exhausted in any event.

Future retained-workspace reads require a new explicit owner authorization
before execution.
