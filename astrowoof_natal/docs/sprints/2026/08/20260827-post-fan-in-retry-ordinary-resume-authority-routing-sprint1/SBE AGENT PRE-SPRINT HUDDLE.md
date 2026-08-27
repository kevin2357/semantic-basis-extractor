# SBE Agent Pre-Sprint Huddle

Date: 2026-08-27
Status: analysis for planning; no runtime or retained-run action authorized

## Understanding

The incident is not adequately described as “OpenAI completed but polling was
slow.” Both retry provider identities are durable at the API boundary, while SBE
0.4.26 repeatedly advertises one `ordinary_resume` local operation and the invoked
semantic-closure command refuses inside an initial-wave aggregate-authorization
guard. Strudel then cycles through quiescent local continuation while retaining the
only SBE capacity allocation, starving Princess.

The intended boundaries are different:

- an initial six-member interactive wave uses its exact snapshot-bound v1 request,
  aggregate grant, and six member authorization documents;
- an ordinary post-fan-in retry provider operation is reconciled by provider ID;
- completed retrieved evidence may expose one local fan-in/retry-evaluation
  operation through lifecycle v0.7;
- the next ordinary prepared retry uses the v2 ordinary-action authority path; and
- generic resume must not manufacture or reuse either form of authority.

The current exact closure code has two suspicious broad predicates:

1. ordinary `--spend-authorization` documents are rejected whenever
   `initial_authoring_wave` is still a dictionary; and
2. `exact_initial_wave_mode` is true whenever that historical wave dictionary
   exists, without first proving the wave is still an active initial admission.

A completed initial wave remains useful lineage and must not be deleted merely to
escape these guards. The correction should classify the current operation from
validated wave/action/provider facts rather than from artifact presence alone.

This is a strong hypothesis, not yet the complete diagnosis. The retained QA
evidence also reports zero provider-local dependencies while provider IDs exist at
the API boundary. Slice 0 must determine whether native SBE state contains those IDs
and how provider reconciliation status, local-work inventory, and command arguments
combine to select the broken path.

## Safety and ownership

- Keep Strudel and Princess suspended and untouched during contract work.
- Make no OpenAI request, retrieval, retry, denial, terminalization, or repair.
- Use a sanitized provider-free workspace and scripted transport.
- SBE owns native classification, command eligibility, initial-wave lineage,
  provider custody, local-work inventory, and native mutation.
- API owns leases, capacity, queue scheduling, reservations, global spend policy,
  persisted provider-operation projection, and retained-cohort operational action.
- No fix may invent a grant, infer API authority, discard immutable refusal/provider
  history, or weaken the initial-wave create fence.

## Planning conclusions

This should be treated as a focused lifecycle/authority-routing patch with a real
contract matrix, not as a one-line deletion of the guard. Exact and bounded routes
must be assessed because they have parallel initial-wave fences, but code should be
changed only where the same operation classification applies.

The existing public vocabulary may be sufficient:

- provider reconciliation remains `provider_reconciliation_cycle`;
- local fan-in remains `ordinary_resume` with a concrete v0.7 operation;
- next ordinary authority remains `await_external_authority`;
- incompatible or ambiguous evidence remains typed review/refusal.

Prefer hardening the current lifecycle versions in place if the issue is an invalid
combination they already intended to reject. Introduce a new version only if the API
needs a genuinely new public operation identity or field to select safely.

## Questions Slice 0 must answer

1. Which exact native action states and provider fields exist at the failing
   checkpoint?
2. Is the retry provider identity durable in SBE, only in API persistence, or both?
3. Has retrieval occurred natively, or is dashboard completion merely external
   knowledge?
4. Why does lifecycle v0.7 construct
   `provider_result_fan_in_and_retry_evaluation` rather than provider reconciliation
   or external authority?
5. Which CLI documents/options does API pass on the failing invocation?
6. Does the first refusal mutate state/snapshot/result publication, or is the later
   quiescent loop caused entirely by wrapper mapping?
7. Does bounded interactive share the same invalid predicate or only a similar
   guard?
8. Can current v0.7 fields express the corrected decision without a contract bump?

## Deferred work

- No retained-cohort recovery or resumption.
- No provider call/retrieval.
- No API queue/capacity redesign.
- No Batch topology change.
- No retry-policy, prompt, scoring, QA, accounting, or cost-estimation change.
- No generic “ignore initial wave” compatibility mode.
