# AstroWoof Natal Authoring 0.2.0

This release evolves the pinnable authoring runtime for UUID upstream identity,
durable paid-provider authorization, minimized provider disclosure, and safe
workspace restoration.

## Included

- opaque source identity across extraction, synthesis, authoring, and delivery;
- a frozen per-run/per-stage micro-USD ledger distinct from the fifty-claim
  semantic budget;
- exact prepare/authorize/execute bindings, single-writer consumption,
  committed-versus-reported accounting, and append-only reconciliation refs;
- machine-distinct awaiting authorization, hard exhaustion, optional skip, and
  ambiguous provider submission outcomes;
- no new commitment when polling recorded OpenAI work;
- minimized provider-visible subject fields across Batch, retry, polish,
  critic, and qualitative candidate routes;
- stable-logical-absolute workspace and complete-snapshot resume enforcement;
- separate selected-card and whole-dog evidence provenance; and
- installed AGF 0.6/SPC 0.10 UUID contract smoke coverage.

The OpenAI provider does not offer an atomic create-and-durably-record boundary
to SBE. A failure after provider acceptance but before provider-ID persistence
is therefore classified ambiguous and requires reconciliation, not blind retry.

## Qualification

All 144 repository tests pass. Two final builds are byte-identical, and the
exact clean-installed wheel passes deterministic release smoke. The approved
Ella live gate safely stopped at `BUDGET_EXHAUSTED`: initial reported estimated
spend was USD 0.263381 and the unsubmitted retry commitment exceeded its
approved USD 1.00 stage ceiling. This bounded exhaustion was explicitly
accepted as satisfying the live gate.

Tagging and publication remain pending explicit Slice 7 authorization.
