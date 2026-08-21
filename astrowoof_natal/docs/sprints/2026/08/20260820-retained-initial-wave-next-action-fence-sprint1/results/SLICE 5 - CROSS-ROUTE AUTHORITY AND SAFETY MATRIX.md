# Slice 5 — Cross-Route Authority and Safety Matrix

Status: implemented and provider-free qualified; awaiting review.

## Rule

The new aggregate external-authority grant is a create fence for an interactive
six-member initial wave. It does not replace the established authorization
contract for independently prepared actions or the one-action Batch-round model.
Lifecycle inspection v0.5 publishes the complete current request or a closed
native refusal, so a consumer never needs `run.json`, packets, logs, or provider
identities to decide which supported authority boundary applies.

## Route matrix

| Route/stage | Native authority unit | Supported continuation | Fail-closed condition |
|---|---|---|---|
| exact interactive initial wave | six ordered actions, one exact aggregate grant | snapshot-validated external request + grant + six complete authorization documents | generic resume after wave preparation; stale/mixed grant; unjoinable lineage |
| bounded interactive initial wave | six ordered actions, one exact aggregate grant | same public request/grant contract, bound to bounded route/wave identity | legacy envelope, generic resume after preparation, or consumed authority without durable create outcomes |
| exact Batch initial/retry round | one paid Batch-round action; six logical members are audit evidence | established ordinary spend-authorization boundary | no implicit interactive-wave reinterpretation |
| bounded Batch initial/retry round | one paid Batch-round action; six logical members are audit evidence | established ordinary spend-authorization boundary | legacy bounded topology or member-as-reservation reinterpretation |
| exact/bounded pass-local creative retry | one independently prepared action | established ordinary action authorization | no authorization, provider evidence conflict, or ambiguous submission |
| polish | one independently prepared optional action | established ordinary action authorization | optional policy skip stays a skip; required denial terminalizes under existing policy |
| qualitative critic | one independently prepared optional action | established ordinary action authorization | delivery may remain publishable while critic custody/authority remains separately visible |
| qualitative candidate | one independently prepared optional action | established ordinary action authorization | zero-dollar configuration does not bypass native preparation/validation rules |

The lifecycle `ordinary_action_set` projection is the closed, ordered public
selection and binding surface for ordinary actions. Authorization is still applied
through the route's existing complete per-action authorization documents; the new
aggregate grant is required only for the interactive initial-wave create boundary.

## Lifecycle compatibility

- Inspection v0.5 adds `external_authority_request` and
  `external_authority_refusal`; it adds no public run-status names.
- v0.4 remains readable but cannot authorize the new constrained continuation.
- Exact historical initial evidence without one provable wave is
  `initial_wave_lineage_unjoinable`.
- Bounded legacy one-pass work is not accidentally classified by the exact
  historical-lineage recognizer.
- Provider reconciliation, providerless denial, optional-stage skip, and terminal
  delivery semantics are unchanged.

## Safety evidence

- Exact and bounded interactive initial waves require the exact current snapshot,
  request digest, route/wave identity, six action bindings, and all six complete
  authorization documents before create permission exists.
- Bounded authorization, all six `SUBMITTING` transitions, and one capability-bound
  constrained submission intent are committed under native single-writer ownership;
  provider I/O remains outside that lock. Each returned identity or ambiguity is
  persisted after reacquiring the lifecycle writer.
- Generic bounded resume refuses `AWAITING_SPEND_AUTHORIZATION`, `AUTHORIZED`, and
  `SUBMITTING` waves. Prepared request files are never provider-outcome evidence.
- A bounded crash after provider return retains durable identities/ambiguity for
  reconciliation without granting generic create permission. A crash immediately
  after the intent checkpoint cannot be resumed into provider I/O without the
  in-memory capability held by the constrained invocation.
- The public request reader validates the complete exact/bounded wave join across
  wave, bundle, ledger bindings, request bytes, and pass attempts.
- Existing bounded reconciliation and optional-stage tests continue to exercise
  ordinary authorization rather than being relabeled as a fresh initial wave.
