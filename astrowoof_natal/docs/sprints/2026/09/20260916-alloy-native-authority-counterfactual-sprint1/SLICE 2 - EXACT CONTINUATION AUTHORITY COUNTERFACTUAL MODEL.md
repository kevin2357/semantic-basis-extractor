# Slice 2 — Exact Continuation Authority Counterfactual Model

Status: complete; offline bounded Alloy analysis

## Artifact and abstraction

`tools/native_authority_continuation_counterfactual_v1.als`

Each `Inventory` atom represents an equality-bearing complete ordered public
action/binding projection. Equality means “the same exact inventory”; inequality
means the join is not proven. This deliberately models neither UUID syntax nor
cryptographic hashing/order algorithms. It tests the authority relation that those
production mechanisms enforce.

Model SHA-256:

```text
5ca081d5a2e65fda87d88471255d8e6ca4eb220cd388a5482b1bee9ae66f96f3
```

## Analyzer execution

Analyzer: verified temporary Alloy 6.2.0 under `C:\tmp`; SAT4J solver; offline
execution only.

Receipt:

```text
C:\tmp\alloy-native-authority-model-b\receipt.json
bytes: 14,990
SHA-256: 84846173a2713e726a62c04073b82437520a5e6c60e13a27275c3458ec5e198b
```

## Historical permissive witnesses

Each `run` was SAT in its exact small scope. These are minimized counterfactual
traces, not attempts to replay retained runs.

| Command | Unsafe shape admitted before corrected boundary |
| --- | --- |
| `LegacyRetainedInitialWaveReanimation` | prior initial-wave lineage, no exact reusable initial inventory, then fresh initial-wave create |
| `LegacyRetryWithoutExactDispatch` | API-side grant exists but retry create has no matching dispatch |
| `LegacyAmbiguousIntentRecreates` | durable intent lacks provider identity, then same-inventory create occurs |
| `LegacyReviewReopensAuthority` | terminal-review state coexists with provider create |

## Corrected boundary

`CorrectedBoundary` contains five narrow constraints:

1. every provider create uses exactly one dispatch;
2. every dispatch supports at most one provider create;
3. unjoinable prior initial-wave lineage forbids a fresh initial-wave create;
4. intent without provider identity forbids another create for that inventory; and
5. terminal review forbids provider create.

The five bounded `check` commands found no counterexample through scope 4:

| Assertion | Result |
| --- | --- |
| `RetainedUnjoinableInitialWaveCannotCreate` | no counterexample |
| `ProviderCreateNeedsExactDispatch` | no counterexample |
| `DispatchCannotCreateTwice` | no counterexample |
| `AmbiguousIntentCannotCreateAgain` | no counterexample |
| `TerminalReviewCannotCreate` | no counterexample |

## Non-vacuity

The corrected model remains satisfiable for the intended ordinary cases:

| Command | Result |
| --- | --- |
| `ValidInitialAdmission` | SAT: new initial-wave inventory with exact request/grant/dispatch/create and no prior initial lineage |
| `ValidAuthorizedRetry` | SAT: prior initial lineage plus a separate retry inventory and exact dispatch/create |
| `ValidAmbiguityRetention` | SAT: durable intent with no provider identity and no same-inventory create |

## Counterfactual conclusion

For the tight no-invented-continuation family, Alloy would plausibly have been a
high-leverage early design aid. The retained Aster reanimation, the missing v2
dispatch envelope, ambiguity reopening, and review-as-authority mistakes reduce to
small, distinct SAT counterexamples. The corrected rules are likewise compact and
do not block valid initial admission or valid exact retry dispatch.

That does not prove the release-era code already or always implemented those rules:
public schemas, Python adapters, CLI serialization, installed wheels, and live
custody persistence remain separately verified by executable tests. The model says
which relationship must exist; it does not prove a concrete adapter carried it.

## Gate C request

Models A and B now answer the core counterfactual. Review whether an optional Model
C (public-evidence adapter refinement) adds enough new insight to justify its extra
abstraction. The recommended default is to stop after these two models and close
with a concise practical-use conclusion.

