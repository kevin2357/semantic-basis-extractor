# Evidence Index — Alloy Counterfactual Native-Authority Sprint

## Evidence posture

All entries below are historical documentation and provider-free test/contract
evidence. They are not instructions to reopen, repair, replay, or mutate any old
run. Live logs were useful for chronology in the original investigations, but sealed
native results, receipts, API persistence, and published contracts remain the
authority for any modelled transition claim.

## Primary historical witnesses

| Witness | Date range | Model | Historical issue | Primary record |
| --- | --- | --- | --- | --- |
| Aster terminal reanimation | Aug 16–17 | A | Valid native terminal state lost to generic nonzero-exit retry | `C:/dev/github/astrowoof-api/docs/sprints/2026/08/20260817-native-terminal-transition-ingestion-sprint26/BACKGROUND.md` |
| Bramble stale closeout | Aug 15–21 | A | Completion/custody settlement attempted more than once from stale observation | `C:/dev/github/astrowoof-api/docs/sprints/2026/08/20260815-admission-capacity-discovery-sprint18/EVIDENCE.md` |
| Aster pending loop | Aug 19 | A | Ordinary resume selected instead of retrieval-only reconciliation | `C:/dev/github/astrowoof-api/docs/sprints/2026/08/20260819-provider-pending-reconciliation-contract-repair-sprint32/Background.md` |
| Retained Aster initial-wave reanimation | Aug 20 | B | Historical lineage treated as fresh six-action creation | `astrowoof_natal/docs/sprints/2026/08/20260820-retained-initial-wave-next-action-fence-sprint1/BACKGROUND AND CONTRACT ASSESSMENT.md` |
| Diffie/Hellman retry handoff | Aug 30 | B | API authorization existed but exact v2 command envelope was absent | `astrowoof_natal/docs/sprints/2026/08/20260830-retry-external-authority-v2-dispatch-handoff-sprint1/BACKGROUND.md` |
| Pippin/Duchess review/mixed custody | Aug 28 | B | Terminal review must not be mistaken for permission to reopen retries | `astrowoof_natal/docs/sprints/2026/08/20260828-review-required-with-pending-retries-investigation-sprint1/BACKGROUND.md` |

## Existing counterexample mapping

The API’s later historical-counterexample corpus already classifies the key
boundaries: native terminal ingestion, Bramble closeout, initial-wave authority,
external-authority precedence, and post-fan-in local-work/authority routing. This
sprint may reuse its **semantic categories** but must not claim that its executable
fixtures are Alloy results.

`C:/dev/github/astrowoof-api/docs/sprints/2026/08/20260825-executable-lifecycle-adversarial-simulation-sprint52/results/SLICE 7 - HISTORICAL COUNTEREXAMPLE CORPUS.md`

## Existing Alloy material

The repository currently has Alloy models for editorial packet collection and
cooperative suspension. They establish local modeling style and receipt conventions,
but do not model the historical native lifecycle/authority state space. New models
must therefore be additive and clearly labelled counterfactual.

- `astrowoof_natal/docs/sprints/2026/09/20260907-editorial-review-packet-collection-contract-sprint1/tools/editorial_review_contract_v3.als`
- `astrowoof_natal/docs/sprints/2026/09/20260915-native-cooperative-suspension-hard-stop-handoff-sprint1/tools/native_cooperative_suspension_v1.als`

## Tooling observation

At sprint creation, no local Alloy command or Analyzer JAR was found on this host.
Do not download or install one until the plan’s tooling gate is explicitly approved.

