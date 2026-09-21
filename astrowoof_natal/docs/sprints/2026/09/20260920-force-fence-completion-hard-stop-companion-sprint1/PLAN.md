# Plan — force-fence completion hard-stop companion

## Status

**Active — contract/model discovery only.** No runtime action, new release,
or API resource release is authorized before joint Gate A/B approval.

## Slice 0 — post-fence route and evidence inventory

- Map every active native route into one of three completion classes:
  cooperative SBE safe-stop proof, API-parent-owned exact child/process-group
  exit proof, API/platform-proven worker replacement, or unresolved
  escalation. An unsupported SBE route is not a capacity-releasing final
  outcome unless an exact parent or platform proof exists.
- Inventory each route's cooperative safe points, blocking external calls,
  command/process topology, and exact parent-owned exit observability. Treat
  `provider_reconciliation_cycle` as the first required route because it is
  the live peer-block witness; do not defer it behind ordinary-v2 coverage.
- Identify the durable identities required to bind an SBE proof to the exact
  API force fence, checkpoint/workspace, native run, and allocation.
- State which pre-existing cooperative artifacts can be reused and where a
  new closed handoff schema is needed.
- Prove which retained facts are non-scheduling custody, and provide API enough
  exact evidence to release the target's execution slot only after a final
  proof class is satisfied, without fabricating a native/provider fact.
- For platform replacement, inventory the old boot/invocation identities whose
  late result, receipt, stdout, or control artifact must be refused after the
  replacement. SBE does not attest process exit from a replacement; API owns
  that control-plane proof.

## Slice 1 — proposed producer/result contract

- Propose closed result kinds for safe completion and all non-completion
  outcomes.
- Forbid inferred exit, provider cancellation, terminalization, or capacity
  release in every SBE artifact.
- Require every non-success result to distinguish a final cooperative
  completion from a transient unresolved escalation. The latter must name the
  exact safe-stop or parent-owned exit observation still required; it may not
  invite API capacity release.
- Separate final non-success results from transient unresolved results whose
  child/parent status still needs exact safe-stop or exit evidence; no result
  may invite API capacity release while it leaves that fact unknown.
- Specify the SBE-visible identity/inventory evidence needed for API's bounded
  worker-replacement fallback, including refusal when a collateral active child
  cannot be safely classified.
- Give API the exact validation/replay/precedence requirements.
- Require late artifacts bound to a retired worker boot to be non-authoritative
  for completion, terminalization, or ordinary reactivation. The API/platform
  replacement receipt, not an SBE artifact, is the final proof class in that
  path.

**Gate A:** API review before schema/reader/runtime changes.

## Joint Slice 2 — model and adversarial fixtures

- Build a compact formal state model and deterministic fixtures for normal,
  late, stale, replayed, ordinary-result-precedence, parent-loss, blocked
  external-call, and unsupported cases. Model `child_alive`, active capacity,
  and retained provider custody as independent facts. Require post-outcome
  peer admission after every **final** outcome, and require continued exact
  escalation—not release—after every unresolved outcome.
- Include target-scoped / worker-scoped replacement, a no-new-child admission
  fence before the active-child inventory, collateral-child refusal or
  explicit recovery records, old-boot exclusion, late-artifact rejection, and
  post-replacement peer admission.

**Gate B:** joint model approval.

## Slice 3 — approved runtime support and qualification

- Implement only approved producer/reader paths.
- Qualify installed wheel with API's completion consumer and provider-free
  transcripts. Preserve all unsupported paths as unresolved.
