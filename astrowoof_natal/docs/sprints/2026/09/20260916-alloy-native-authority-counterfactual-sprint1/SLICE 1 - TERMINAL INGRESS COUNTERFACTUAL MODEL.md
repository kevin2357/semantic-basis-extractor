# Slice 1 — Terminal Ingress Counterfactual Model

Status: complete; offline bounded Alloy analysis

## Artifact

`tools/native_authority_terminal_ingress_counterfactual_v1.als`

The model is content-free: atoms represent only public identity equality and a
closed command/result vocabulary. It deliberately excludes real result bytes, SHA
algorithms, Python control flow, subprocess stdout, provider payloads, log delivery,
and private workspaces.

Model SHA-256:

```text
ee6520d4ea8142993b0ebb80f941b2ae0cf7b1138583ca45d1e7a7a74498a48b
```

## Analyzer execution

Analyzer: Alloy 6.2.0 from the verified temporary `C:\tmp` distribution.

```text
C:\tmp\alloy-6.2.0\bin\alloy.exe exec --quiet --force --type json \
  --output C:\tmp\alloy-native-authority-model-a \
  <model path>
```

The Analyzer receipt is retained only in `C:\tmp`:

```text
receipt bytes: 9,868
receipt SHA-256: 72d30bfdd55af2469574ccd5e0b84ffce2139717c39136bd81a57c71fd164a2d
solver: SAT4J
```

## Historical permissive witnesses

Each `run` below is SAT in its exact small scope. That is the counterfactual result:
without the corresponding rule, the abstract control plane admits the historical
unsafe shape.

| Command | Exact scope | Witness found |
| --- | --- | --- |
| `LegacyAsterTerminalFallback` | 1 run/result/invocation/decision | terminal result + `GenericRetry` |
| `LegacyBrambleDuplicateCloseout` | 1 run/result/invocation/decision/custody, 2 settlements | two settlements bind the same terminal result and custody resource |
| `LegacyAsterPendingOrdinaryResume` | 1 run/result/invocation/decision/provider identity | pending provider identity + `OrdinaryResume` |

These are not reconstructions of the named runs. They are minimized structural
witnesses for the three separately documented historical defects.

## Corrected properties

`CorrectedAdapter` adds only three rules:

1. terminal result permits `Closeout` or `Refuse`, never `GenericRetry`;
2. a nonterminal result with pending provider identity permits `Reconcile` or
   `Refuse`, never `OrdinaryResume`; and
3. one result/custody pair has at most one settlement.

The three `check` commands found no counterexample through scope 3:

| Assertion | Result |
| --- | --- |
| `TerminalDominatesGenericFallback` | no counterexample |
| `TerminalSettlementIsExactOnce` | no counterexample |
| `PendingProviderIdentityBlocksOrdinaryResume` | no counterexample |

This is meaningful only within the stated abstraction and scope. It proves neither
that historical ordering was fully retained nor that a current Python adapter
implements these rules correctly.

## Non-vacuity checks

The corrected model still has intended behavior:

| Command | Result |
| --- | --- |
| `ValidTerminalCloseout` | SAT: terminal result selects closeout and one settlement |
| `ValidPendingReconciliation` | SAT: nonterminal pending state selects reconciliation |

Therefore the properties did not “pass” merely because the model disallowed every
decision.

## Counterfactual conclusion

Model A says the three Aster/Bramble-adjacent failures were model-friendly. A small
cross-package control-plane model would have made each unsafe transition visible as
a one-step counterexample and stated the missing rule before live execution:
validated native evidence must precede API fallback/command selection, and terminal
custody settlement is exact-once.

The model does not claim it would have located the source line, constructed the
missing adapter, or detected a runtime serialization defect. Those remain executable
and installed-wheel concerns.

## Gate B request

Model A is ready for review. If accepted, Slice 2 will create the separate exact
external-authority Model B; it will not modify Model A or production contracts.

