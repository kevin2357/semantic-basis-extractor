# Slice 4 — Bounded Interactive Concurrent Submission

Status: complete; awaiting Kevin review before commit.

## Outcome

Fresh bounded-Natal interactive authoring now uses the same reviewed initial-wave
coordinator as exact Natal while retaining bounded-specific packet, schema,
provider-minimization, hydration, validation, and provenance authority.

SBE prepares all six bounded pass actions at one state revision. One exact API wave
envelope and six ordered member authorizations must validate before any authority
is applied or provider request begins. Six create-only Responses calls then overlap;
each returned ID receives an immediate serialized ledger, journal, marker, timing,
pass-state, and event checkpoint. The run detaches after create fan-out and leaves
retrieval to the established bounded short-cycle reconciliation path.

Batch remains unchanged. Optional stages and creative retries remain pass/stage
local and do not join the initial wave.

## Bounded authority preserved

- The create-only request body is byte-semantically equal to the established
  bounded interactive body for the same frozen pass request.
- Interactive and Batch continue to differ only by transport envelope/background
  fields; pass membership, prompt, schema, retry feedback, and immutable bounded
  authority do not drift.
- Every request traverses `assert_provider_minimized`; protected birth time,
  location, coordinate, and provenance evidence remain excluded.
- Provider output remains editorial-only. SBE deterministically reattaches claim
  authority, evidence provenance, subject view, and projected-term registry.
- Durable provider IDs are reconciliation-only on recovery. An identity-less
  interrupted submission fails closed.

## Correctness regressions landed with this slice

### Final-QA precedence

`FINAL_QA_REQUIRES_REVIEW` and `FINAL_QA_FAILED` now outrank generic pass-derived
`AUTHORING_COMPLETE` status during persistence. The regression validates native
state, public state, snapshot-backed lifecycle inspection, immutable native result,
and publication receipt evidence. Optional stages cannot reopen after this review
boundary.

### Equivalent Mean/True Node admission

Selected Mean Node and True Node claims with the same claim kind, projected terms,
operators, canonical object, sign, and projected mode are rejected before paid
authoring with typed code `bounded_equivalent_node_claims`. SBE does not merge or
rewrite upstream provenance. A nearby fixture with genuinely different projected
semantics remains valid, proving the guard is semantic rather than name-based.

SPC remains authoritative for upstream projection policy.

## Public invocation seam

`astrowoof-run-bounded-natal` accepts:

```text
--initial-wave-authorization WAVE.json
--spend-authorization MEMBER-1.json ... MEMBER-6.json
```

The command exits with the existing nonterminal code and public lifecycle state;
no new public state name is introduced.

## Verification

- Focused new behavior: 4 tests passed in 2.698 seconds.
- Bounded authoring/provider/lifecycle suite: 54 tests passed in 93.257 seconds
  before the final expanded publication/parity assertions; those assertions passed
  in focused reruns.
- Combined bounded authoring/provider/lifecycle, provider-pending capacity, and
  lifecycle inspection/contracts/closeout suite: 119 tests passed in 118.177
  seconds.
- Compile and `git diff --check`: pass.
- Provider operations: zero.
- Paid spend: `$0`.
