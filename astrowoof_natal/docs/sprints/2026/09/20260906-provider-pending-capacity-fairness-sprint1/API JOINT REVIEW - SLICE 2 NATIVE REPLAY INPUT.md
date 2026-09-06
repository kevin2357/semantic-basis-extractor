# API joint review — Slice 2 native replay input

## Decision

Approved as the native half of the joint provider-free replay. API will consume
only the final meanings documented here; it will not infer a capacity yield
from trace output or manufacture `release_until_due` from elapsed time.

## Frozen API interpretation

- `release_until_due` remains an exact final handoff. API may defer to the
  supplied due boundary and release the independent API-run allocation.
- `continue_local_cycle / provider_reconciliation_due` remains immediately
  actionable native work. In particular, a four-member bounded retrieval with
  the exact two-member immediately-due suffix is **not** a cooperative yield.
- `continue_local_cycle / local_work_ready` is likewise a prompt local-native
  continuation, not an API-created provider wait.
- API owns its allocation, `available_at`, eligible set, next claim, and
  lateness receipt. SBE owns neither allocation nor cross-run selection.

## API Slice 1 status

The API production-boundary cells now establish:

1. exact `release_until_due` releases A, admits B, then permits A's lawful due
   reclaim;
2. `continue_local_cycle / provider_reconciliation_cycle` retains A and
   excludes ready B while the one-slot allocation remains full;
3. the direct queue boundary proves the configured 15-second ordinary defer
   and no-claim interval deterministically; and
4. the post-`8c389b3` retry-ceiling terminal cleanup releases A and admits B,
   explicitly separately from healthy provider-pending behavior.

The remaining API work is the Sprint 58 terminal-precedence negative control,
the healthy `d451a88 -> 8c389b3` source comparison, and the ordered joint
receipt. No fairness runtime policy has been selected or requested.

## API Slice 1 completion update

The remaining controls are complete and committed on API `main` at
`514f6b8` (following provider-free checkpoints `79120a7` and `10db03d`).

- Sprint 58 is rejected as a demonstrated healthy provider-pending regression:
  its release-pair source surface does not touch queue/capacity/defer behavior;
  focused installed terminal-preflight controls pass.
- `8c389b3` is a positive control only for retry-ceiling terminal cleanup. Its
  source diff deliberately leaves healthy `release_until_due` and
  `continue_local_cycle` handling unchanged; its after-cell releases a peer
  only when A has already become terminal.
- The real worker and direct queue/capacity cells reproduce the remaining
  current seam: a truthful `continue_local_cycle` retains A's allocation,
  defers A 15 seconds, and restricts a full one-slot eligible set to A, leaving
  ready B without a claim before or at that ordinary boundary.

API therefore requests the planned joint Slice 2 causal/policy review. The
question is not whether to falsify native quiescence; it is whether an existing
final, durable API/SBE command boundary lawfully permits a bounded peer turn,
or whether a versioned cooperative-yield contract is actually required.

## Response to SBE API Slice 1 review

SBE's requested separately characterized local-work-ready cell is complete in
API commit `2a7e0d7`, with `5 passed` for the focused fairness module.

The result is deliberately parallel but not conflated with due retrieval:
completed evidence with zero provider-local dependencies and positive
`ordinary_resume` local work retains A's allocation, records the ordinary
defer, and selects A again over ready B. The cell performs zero provider
create/retrieval operations. API evidence wording now correctly says all five
cells pass.

API therefore accepts the Slice 1 approval and is ready for the joint Slice 2
causal/policy classification. No runtime policy or SBE public-contract change
is approved by this response.
