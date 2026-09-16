# Slice 3 — Public-Evidence Adapter Counterfactual Model

Status: complete; offline bounded Alloy analysis

## Purpose and abstraction

`tools/native_authority_adapter_counterfactual_v1.als`

Model C is deliberately narrower than an implementation model. It treats the
adapter as a translator between public evidence and a native action, with no JSON,
stdout, exception, package, or hidden-workspace state. A `PublicResult` can be
valid terminal, valid nonterminal, or invalid; a `PublicAuthorityRequest` and an
`ExactGrant` form the only dispatch-capable pair. A generic authorization is a
different thing and cannot become a synthetic request.

Model SHA-256:

```text
9d4add3c5c2d3387866ebef1b73360b21e0d9f96ed548ef858361d668843e7f0
```

## Analyzer execution

Analyzer: verified temporary Alloy 6.2.0 under `C:\\tmp`; SAT4J solver; offline
execution only.

Receipt:

```text
C:\tmp\alloy-native-authority-model-c\receipt.json
bytes: 14,230
SHA-256: cdfcad51f71af7e71e02c33423dfc9b511b7f514d2a82a5c480cc06d4b0719bd
```

## Permissive counterfactual witnesses

Each historical-shaped permissive command was SAT in the exact small scope. These
are minimized relation witnesses, not retained-run replays.

| Command | Unsafe adapter behavior |
| --- | --- |
| `LegacyTerminalFallsToGenericRetry` | valid terminal result is consumed by generic retry fallback |
| `LegacyGenericAuthorizationSynthesizesDispatch` | generic authorization, with no public request, produces exact dispatch |
| `LegacyExactRequestFallsToGenericRetry` | exact public request/grant exists but adapter chooses generic retry |
| `LegacyTerminalReopensAsDispatch` | valid terminal result is reopened as a dispatch-capable path |

## Corrected boundary and non-vacuity

The corrected relation requires terminal evidence to persist or refuse, requires
exact request/grant pairing for dispatch, forbids generic-only authorization from
standing in for a request, and forbids exact-pair generic retry. Four `check`
commands found no counterexample through scope 3:

| Assertion | Result |
| --- | --- |
| `TerminalDoesNotUseFallbackOrDispatch` | no counterexample |
| `ExactDispatchUsesExactPublishedPair` | no counterexample |
| `GenericAuthorizationCannotStandInForRequest` | no counterexample |
| `ExactPairDoesNotUseGenericRetry` | no counterexample |

The model remains non-vacuous: valid terminal persistence, valid dispatch from an
exact request/grant pair, and safe refusal of generic-only authorization were all
SAT.

## Counterfactual conclusion

Model C supports the modest counterfactual: had this exact adapter boundary been
modeled before the authority-era changes, it would likely have surfaced the
terminal-fallback, missing exact-v2, and synthetic-authority classes as concise
counterexamples during design. It does **not** say that Alloy could have detected
concrete Python serialization bugs, installed-wheel skew, persistence races, or
live custody errors by itself.

It also does not justify a fourth model. Models A and B identify the substantive
state/authority rules; Model C merely proves that an adapter must preserve them
rather than select a generic fallback. Keep these three models as small design and
review aids when a proposal changes terminal precedence, custody, or creation
authority. Continue relying on contract fixtures, installed-wheel gates, and
runtime evidence for implementation truth.
