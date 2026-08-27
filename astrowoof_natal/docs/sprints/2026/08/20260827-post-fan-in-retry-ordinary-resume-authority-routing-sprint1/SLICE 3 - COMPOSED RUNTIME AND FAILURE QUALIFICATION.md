# Slice 3 — Composed Runtime and Failure Qualification

Date: 2026-08-27
Status: complete; awaiting API runtime/failure-boundary review

## Exact-interactive composed proof

A provider-free production-shaped run now traverses the supported boundaries in
order:

1. A creative-retry provider identity is pending but not due.
2. Lifecycle v0.7 selects `provider_reconciliation_cycle` with
   `eligible_now=false`.
3. A not-due reconciliation invocation performs zero retrievals and leaves
   `run.json` and the workspace snapshot byte-identical.
4. At the exact due instant, the real reconciliation engine retrieves only the
   SBE-selected provider identity from a scripted transport.
5. The durable response identity and completed evidence are preserved and the
   reconciliation result is `progressed_local`—meaning provider retrieval made
   native local work ready, not that semantic acceptance was invented.
6. Lifecycle v0.7 selects one
   `provider_result_fan_in_and_retry_evaluation` operation.
7. The public semantic-closure resume boundary reaches ordinary authoring despite
   retained `DETACHED` initial-wave lineage.
8. Local fan-in reports the retrieved action, cumulatively consumes the exact
   operation key, and exposes the later prepared retry as
   `await_external_authority`.
9. Temporal inspection and the public v2 builders produce an exact one-action
   ordinary request and grant/document join.
10. The supported v2 intent and dispatch APIs create one scripted provider
    operation and detach into provider-pending custody.
11. Exact dispatch replay returns `exact_replay` and creates no second operation.

No later retry authorization is needed to retrieve or fan in the earlier response.
No initial-wave v1 authority is accepted for the later ordinary action.

## Bounded and stage parity

The wider qualification retains:

- exact and bounded response-route 4+2 provider reconciliation;
- bounded/exact local fan-in selection;
- ordinary v2 response dispatch for creative retry, polish, qualitative critic,
  and qualitative candidate;
- provider custody before local work and new authority;
- explicit ordinary-v2 Batch refusal before intent/provider I/O; and
- active initial-wave, unknown-state, ambiguity, stale/binding, and replay fences.

The runtime source correction is shared only at the closed state-classification
helper. Bounded's previously correct active-wave behavior remains unchanged.

## Failure and replay evidence

- not due: zero retrieval and byte-identical authoritative workspace;
- active initial admission: aggregate-grant refusal remains intact;
- unknown/malformed wave state: `unsupported_contract`, nonmutating;
- provider ambiguity/identity evidence: review/reconciliation precedence retained;
- ordinary local no-op: existing consuming-operation validator refuses;
- v2 stale/binding/partial intent: existing intent-fence suite retained;
- successful v2 replay: `exact_replay`, zero duplicate create; and
- Batch ordinary v2: explicitly unsupported before provider I/O.

## Test evidence

Focused composed and route/failure suite:

```text
44 tests passed
```

The prior wider initial-wave/external-authority/bounded suite also remains green:

```text
77 tests passed
```

## Safety totals

- External provider/network calls: 0
- Real provider creates/retrievals: 0
- Scripted local retrievals in the exact composed proof: 1
- Scripted local creates in the exact composed proof: 1
- Duplicate scripted creates on replay: 0
- Retained QA workspaces accessed or mutated: 0
- Spend: USD 0

## Gate

API review is required before Slice 4 adversarial/joint fairness work. This evidence
does not authorize retained-cohort recovery or paid QA.

