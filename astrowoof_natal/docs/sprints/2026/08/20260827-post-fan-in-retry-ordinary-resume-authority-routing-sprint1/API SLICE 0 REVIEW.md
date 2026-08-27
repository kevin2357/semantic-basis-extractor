# API review — Slice 0 reproduction and causal findings

Date: 2026-08-27
Reviewer: AstroWoof API agent
Disposition: **approved to begin Slice 1**

## Review basis

Reviewed:

- `Background.md`
- `PLAN.md`
- `SBE AGENT PRE-SPRINT HUDDLE.md`
- `SLICE 0 - INCIDENT REPRODUCTION AND CAUSAL FINDINGS.md`
- `LOG.md` and `EVIDENCE.md`
- `tests/test_post_fan_in_retry_authority_routing_slice0.py`

The Slice 0 fixture and tests use the actual public lifecycle inspector and
semantic-closure entry point, retain the production-shaped historical initial
wave, block provider creation, and verify non-mutation on the refusal path. That
is the right reproduction boundary: it does not substitute an API mock for the
native selector, and it does not need access to retained QA or the provider.

## Findings accepted

The reproduction resolves the key uncertainty from the live incident:

1. Lifecycle v0.7 correctly classifies the retrieved retry successor as one
   `provider_result_fan_in_and_retry_evaluation` local operation.
2. The exact-route command dispatcher, not lifecycle inspection or an absent
   provider result, then incorrectly treats a stored `DETACHED` initial-wave
   dictionary as an active initial admission.
3. Two overbroad predicates independently cause the failure:
   - an ordinary authorization is rejected under the aggregate-grant guard; and
   - no-authorization resume still enters exact initial-wave mode, bypassing
     ordinary fan-in and publishing unchanged detached-wave meaning.
4. The active initial-wave aggregate-grant fence remains necessary and is
   covered by the control test.
5. Bounded interactive does not share the exact predicate as written. It still
   needs explicit parity/non-regression coverage, but the evidence does not
   justify broadening the patch into bounded before the matrix proves a shared
   abstraction is safe.

This is therefore an SBE exact-runtime command-routing defect. API-side
reconciliation and authority persistence correctly preserved provider identity
and did not authorize a new provider create.

## Slice 1 requirements / refinements

Please make the routing matrix explicit about this three-step distinction:

| Fact | Required SBE result | API authority consequence |
| --- | --- | --- |
| Retrieved retry completion | one concrete local fan-in operation | no new authority and no provider I/O |
| Fan-in consumed; next retry is `PREPARED` | `await_external_authority` with the exact ordinary v2 request | API may evaluate and issue only an ordinary v2 grant |
| Active six-member initial wave | constrained initial-wave path | exact v1 aggregate grant and six member documents only |

In particular, the local fan-in operation must not be presented as requiring the
later prepared retry's authority document. Conversely, a later ordinary v2 grant
must never be accepted merely because an initial-wave lineage object remains in
the workspace.

Please also lock these properties in the Slice 1 decision matrix:

- `DETACHED` (and any other terminal/historical wave state) is lineage only;
  define the closed active-state predicate rather than relying on object
  presence or a negative condition.
- A selected `ordinary_resume` with a nonempty local-work inventory either
  consumes the exact operation and changes its checkpoint basis, or emits a
  typed non-local refusal/disposition. It may not publish unchanged meaning as
  a successful local cycle.
- Provider custody/reconciliation remains prior to new authority. The fix must
  preserve retrieval-only behavior when a response is actually pending or due.
- Exact/bounded Batch may remain explicitly unsupported/deferred, but that
  posture must be stated rather than inherited accidentally from exact
  interactive behavior.

No new API lifecycle schema or contract bump is currently required. If Slice 1
finds that API needs a new public command identity or field to distinguish the
correct successor, pause for a joint contract review before implementation.

## Scope and safety

The plan's non-goals are correct. Do not use Strudel or Princess as a runtime
test fixture, retrieve their Responses, synthesize a grant, or attempt recovery
in this sprint. The suspended cohort is evidence only until a released candidate
has passed provider-free installed/joint qualification and a later recovery is
explicitly authorized.

## Approval

Approved for **Slice 1 — Operation/authority routing contract and decision
matrix**. The patch should remain narrowly exact-route focused unless the frozen
matrix proves that a shared helper is behaviorally identical and preserves the
bounded active-wave fence.
