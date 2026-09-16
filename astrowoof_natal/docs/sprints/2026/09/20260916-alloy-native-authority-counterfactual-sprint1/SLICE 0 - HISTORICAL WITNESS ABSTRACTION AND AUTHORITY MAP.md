# Slice 0 — Historical Witness Abstraction and Authority Map

Status: complete; provider-free documentary analysis

## Purpose

This slice turns historical incidents into a deliberately small vocabulary for
counterfactual modeling. It does **not** recreate a retained workspace or claim that
all original event ordering is authoritative. Each row separates: (a) the
contract-level fact the model may represent, (b) the unsafe historical transition,
and (c) the safe result the later public contract requires.

## Authority rule for this model

Use sealed native results/receipts, public lifecycle/request/grant meaning, and
API-owned custody/authorization facts. Use logs only to explain a historical
chronology when the authoritative record did not preserve it. Do not encode raw log
messages, private `run.json` branches, provider dashboard observations, paths,
prompts, or payload bytes as model authority.

## Witness abstraction matrix

| Witness | Model | Public preconditions worth modeling | Historical unsafe transition | Corrected safety property | Valid alternative that must remain SAT |
| --- | --- | --- | --- | --- | --- |
| Aster native-terminal handoff | A | A valid sealed terminal native result is available for an invocation; API has not yet selected disposition. | Generic nonzero-exit retry wins before terminal result intake, re-entering a terminal run. | A valid terminal result for the invocation excludes generic retry and is ingested at most once. | Invalid/unavailable terminal evidence may leave ordinary process handling available; valid terminal closeout is possible. |
| Bramble closeout | A | Valid native completion and one matching API custody resource/observation exist. | The same observation is used for a second providerless-denial/closeout attempt. | One validated terminal observation settles/releases one matching custody resource at most once; no provider create is implied. | One exact terminal closeout can release the matching API resource. |
| Aster provider-pending loop | A | Durable provider identities are pending; lifecycle contract makes reconciliation route available. | API selects ordinary resume repeatedly instead of retrieval-only reconciliation. | Pending provider identities with the matching route select bounded reconciliation, not ordinary authoring resume. | A lifecycle state with true local executable work can select ordinary resume. |
| Retained Aster initial-wave reanimation | B | Prior initial-wave authority/provider lineage exists, but no exact reusable inventory can be proved. | Fresh initial-wave preparation creates a new six-action inventory. | Prior lineage without one exact reusable inventory produces typed refusal/review and zero create. | Fresh lineage with one exact prepared inventory can obtain matching authority and create once per member. |
| Diffie/Hellman retry handoff | B | A retry may be locally prepared and API authorization may exist; exact v2 request/grant/dispatch may be absent. | Generic retry posture persists or provider creation is attempted without the exact envelope. | Create requires an exact live request, matching grant, and unconsumed matching dispatch; missing join is stable refusal, not a synthetic resume. | A correctly joined ordinary retry dispatch can create its authorized member(s). |
| Ambiguous post-intent submission | B | Pre-submit intent is durable, but provider identity is absent. | A new create is treated as a safe retry. | Durable intent plus no identity is ambiguity/review and forbids new create. | Durable intent plus matching provider identity can proceed through retrieval/reconciliation, not duplicate create. |
| Pippin/Duchess review with mixed custody | B | Valid terminal-review result exists while unrelated-looking API retry rows can still be present. | Count-based inference relabels terminal review as continuation permission. | Terminal review is non-create-capable; only a distinct exact live authority request can open a continuation. | A separate exact, eligible request may be observable without changing the terminal result's own meaning. |

## Model boundary decisions

### Model A: terminal meaning and command choice

The three Danish-adjacent witnesses share an **adapter precedence** problem: API
must consume an SBE public result/inspection before choosing its own generic worker
fallback or custody operation. They do not share a root cause, so the model has
separate forbidden transitions rather than one omnibus `bad` state.

Minimal relations:

- `availableResult`, `validResult`, `ingestedResult`;
- `selectedCommand` in `{genericRetry, ordinaryResume, reconcile, closeout, refuse}`;
- `settles` relation between an observation/result and an API custody resource; and
- `pendingProviderIdentity`.

### Model B: exact continuation authority

The retained/retry/ambiguity witnesses share a true common invariant: no actor can
manufacture provider-create permission from partial evidence. A model needs only
identity equality, membership/order abstraction, liveness/consumption, prior lineage,
intent, provider identity, and a bounded create count. It does not need real UUIDs,
hash functions, or prompt contents.

Minimal relations:

- `requestBinds`, `grantBinds`, `dispatchBinds` to an abstract inventory;
- `priorLineage`, `exactReusableInventory`, `intentRecorded`, `providerIdentity`; and
- `createUses` from a create event to exactly one dispatch/request/grant triple.

## Formal-versus-empirical classification

| Claim | Classification | Why |
| --- | --- | --- |
| A terminal native result must outrank generic retry. | Formal design property. | It is a closed precedence relation over abstract states. |
| A custody resource is settled at most once per terminal observation. | Formal design property. | It is a bounded cardinality/identity constraint. |
| Reconciliation is selected for a particular real deployed inspection. | Mixed. | The selection rule is modelable; whether a Python adapter receives/validates a concrete inspection remains executable-test territory. |
| A request/grant/dispatch join is required before create. | Formal design property. | It is an exact relation and liveness/consumption rule. |
| A particular historical API/SBE process actually received a result before an exit code. | Historical chronology. | Original append-only authority did not retain every inter-invocation ordering fact; logs informed the investigation. |
| A wheel, JSONL adapter, Python resource reader, or R2 root emits the intended bytes. | Empirical integration property. | Alloy does not execute Python or inspect deployed artifacts. |

## Gate A conclusion

The seven witnesses reduce to two compact models without loss of their meaningful
distinctions. Model A has three independent historical counterexamples under a shared
“validated native fact before API fallback/command choice” rule. Model B has four
variants of a stricter shared “no invented continuation” rule.

Proceed to tooling approval and Model A only. Do not install an Analyzer or add an
`.als` file until the source/version/invocation are separately reviewed.

