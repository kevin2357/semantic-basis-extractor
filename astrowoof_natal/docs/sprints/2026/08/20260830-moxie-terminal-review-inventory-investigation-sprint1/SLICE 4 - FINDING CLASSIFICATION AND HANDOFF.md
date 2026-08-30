# Slice 4 — Finding classification and handoff

## Primary classification

**SBE runtime defect: native provider-result fan-in/adoption ordering.**

The terminal-review projection, strict API join, local-work progress fence, and
existing public authority contracts behaved correctly. The defect is earlier:
completed retry-2 provider evidence existed durably in the spend ledger, but
ordinary authoring selected retry 3 from stale pass/attempt truth before it had
validated, parsed, and deterministically QA'd retry 2 into that truth.

The eight-row review result was therefore truthful but not API-adoptable. It was
the first public evidence of the eighth action, for which API had never received
a request, admission, or grant.

## Required native ordering

For an interactive pass with completed retained provider evidence, one native
single-writer progression must preserve this order:

1. Resolve the completed response artifact by the exact action/provider identity.
2. Validate response identity, action binding, route, pass, attempt, and expected
   response/output shape.
3. Parse/materialize the response through the existing authoring result path.
4. Run the existing deterministic metadata repair and pass-QA path.
5. Persist the provider metadata, response workspace, QA report, terminal
   attempt state, and ledger reporting/settlement facts as one coherent native
   checkpoint progression.
6. Mark the predecessor local-work operation consumed.
7. Only after steps 1–6, select the next native disposition:
   - accepted pass: no successor retry;
   - QA-rejected pass with remaining attempts: prepare exactly one successor and
     expose it through the normal post-consumption external-authority inspection;
   - invalid, unavailable, conflicting, or ambiguous evidence: preserve the
     existing typed review/custody route, prepare no successor, and do not claim
     the predecessor consumed.

“Adoption” is not a ledger-state rewrite or a blind pass-state flip. It is the
existing validation, parsing, materialization, deterministic QA, and durable
checkpoint path applied to already-retrieved provider evidence.

## Existing public contracts are sufficient

No new lifecycle, terminal-result, or authority schema is required:

- lifecycle v0.7 already advertises the completed-evidence local operation;
- the local-work progress contract already prevents semantic no-op/replay;
- external-authority v2 already carries the exact successor action inventory;
- terminal-review v0.2 correctly projects the complete native ledger; and
- API's strict action/binding/provider join correctly rejects unknown rows.

The runtime correction must derive any legitimate retry authority from the
successor inspection after predecessor consumption. It must not construct a
request directly from private state or weaken API's exact join.

## Failure and interruption posture

| Boundary | Required durable posture |
|---|---|
| Completed artifact unavailable or snapshot-invalid | Existing custody/review remains; no successor; predecessor operation unconsumed. |
| Identity/binding/route/pass/attempt mismatch | Typed review/refusal; no successor; no consumption. |
| Parse/materialization failure | Typed existing integrity/review outcome; no successor; no consumption. |
| Deterministic QA accepted | Attempt/pass accepted and predecessor operation consumed; no retry. |
| Deterministic QA rejected | Rejection is durable before one successor is prepared; successor remains providerless pending external authority. |
| Crash before coherent adoption checkpoint | Restore cannot infer adoption or prepare a successor from partial facts. |
| Crash after adoption but before successor preparation | Restore observes consumed/adopted predecessor and may deterministically select the same next step without provider creation. |
| Crash after successor preparation | Successor is recoverable only through its published exact authority request; generic create remains forbidden. |

## API handoff

API behavior remains unchanged:

- admit only an exact validated external-authority request;
- never manufacture an action from terminal-review evidence;
- never accept an unchecked subset of a native result;
- never deny a native-only providerless action retrospectively; and
- retain/release API capacity and custody only from supported typed evidence.

The separate API containment fix for a strict terminal-ingress refusal remains
valid but does not correct this native ordering defect.

## Implementation slice activation

After Voof-paws 5 approval, Slice 5 should implement the narrow exact-interactive
fan-in adoption correction and provider-free tests for:

1. valid accepted response → no successor;
2. valid QA-rejected response → one successor and exact authority request;
3. unavailable/invalid/identity-conflicting response → no successor and no
   predecessor consumption;
4. interruption before/after adoption and successor preparation;
5. replay → no duplicate successor and no provider create; and
6. terminal review never introduces an unadmitted successor.

Bounded and Batch applicability must be characterized before changing them. They
remain out of runtime scope unless they use the same exact adoption primitive and
can share it without weakening their route-specific evidence.

## Retained-run posture

Moxie remains suspended and untouched. This sprint does not authorize repair,
denial, reconciliation, provider access, result rewriting, or API mutation.
