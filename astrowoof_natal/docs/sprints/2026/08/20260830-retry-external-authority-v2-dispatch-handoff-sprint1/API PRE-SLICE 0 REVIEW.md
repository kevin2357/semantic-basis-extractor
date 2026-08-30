# API pre-Slice 0 review

## Disposition

Approved as an evidence-led Slice 0 plan, with the refinements below. The plan
correctly treats Hellman's `external_authority_v2_dispatch_required` outcome as
a successful no-provider-I/O fence, not as the native defect by itself. It also
correctly avoids flattening Diffie's strict lifecycle-consumption failure and
Hellman's safe capacity-holding loop into one presumed cause.

## Required evidence discipline

1. Keep evidence provenance explicit in the timeline matrix. Native checkpoint
   members can establish SBE action/custody/selection facts; API rows establish
   API authorization, job, lease, reservation, and receipt facts. A later API
   `reported`/settlement observation must never be represented as a fact inside
   an earlier native checkpoint unless that exact checkpoint member proves it.

2. The R2 portion is properly narrow, but remains an explicit secondary gate.
   Slice 0A may define and hash the needed coordinate packet. Do not make the
   exact retained-object HEAD/GET calls until an owner-provided packet and
   authorization for those two objects is present. No prefix/listing discovery,
   provider access, or retained mutation is approved.

## Production-boundary reproduction

The 0F sequence is the right campaign, particularly the mixed-custody case:
one provider-bound retry plus one providerless successor. Please make the
division concrete in the fixture/assessment:

- SBE fixture/runtime produces only its public lifecycle request, refusal,
  constrained-dispatch, reconciliation, result, and receipt artifacts.
- The API-shaped participant may model API admission/grant/document handoff,
  but cannot read private SBE state, choose action members, or turn an API
  authorization row into an implicit grant.
- The test must separately count retrieval and creation. A dashboard-visible
  completed Response is not a retrieval receipt.

This will make a resulting fix clearly assignable to SBE, API, or the explicit
public join—and keeps a passing fixture from hiding a private-state shortcut.

## Contract questions to answer before proposing a new schema

1. At the first stable providerless retry checkpoint, does SBE already publish
   a valid one-action v2 request? If yes, identify why API did not consume it.
2. If it does not, determine whether the earlier retained provider result has
   precedence and requires reconciliation/fan-in before any request may exist.
3. Establish whether Hellman's providerless action had only API admission or a
   compatible current-basis SBE request/grant/document set.
4. State the precise API-visible outcome a generic refusal must cause: release
   until due, wait for a public request, typed review/refusal, or another
   supported action. It must not map to a capacity-holding no-op retry loop.

## API consumer commitment

Once Slice 0 identifies the public artifact and lifecycle predecessor, the API
companion sprint will consume only that released contract and add its own strict
validation and capacity/lease mapping. It will not infer intent from the
`ordinary_resume` label or reconstruct native workspace state.

## Gate

SBE may begin Slice 0's source/public-contract work and the provider-free
reproducer. Retained-workspace access remains gated as above; no runtime,
provider, retained-run, deployment, or release action is authorized by this
review.
