# Slice 3 — Cooperative Safe-Point Integration

## Result

The approved cooperative-suspension contract is now integrated into the two
exact-interactive ordinary-v2 runtime cells: external-authority dispatch and
provider-response reconciliation. It remains provider-free in qualification
and does not give SBE OS process-control or API resource-release authority.

## Runtime boundary

The public commands accept one exact argument pair:

- `--supervision-envelope <immutable-envelope-path>`
- `--suspension-control-root <canonical-request-isolated-root>`

Either both are absent or both are present. The observer validates the
envelope and fixed request path, canonical logical workspace/control-root
joins, freshness, digests, invocation/run/command identity, and closed control
directory before using request content.

Observation occurs only while the existing native writer lock is held:

| Command cell | Safe point | Provider boundary |
| --- | --- | --- |
| v2 dispatch | after durable dispatch-intent checkpoint | provider not entered |
| v2 dispatch | immediately before provider POST | provider not entered |
| v2 dispatch | after durable provider-ID checkpoint | known provider custody |
| v2 dispatch | after durable ambiguous-return checkpoint | ambiguous provider entry |
| reconciliation | before any provider GET | known provider custody, no new create |
| reconciliation | after durable response checkpoint | completed, unadopted evidence |

The admission checkpoint may equal the observed checkpoint or be its supplied
immediate predecessor. Forked/non-successor identities refuse.

## Publication and precedence

SBE first persists and snapshots the observation record. It then publishes a
content-addressed result, request-to-result index, receipt, retained snapshot
and checkpoint basis, and exact command-result envelope. The command exits 0
only through that exact output document.

An interruption after the observation checkpoint is repairable without a
second result. Exact replay returns the same result/receipt/command identities;
a distinct request for the same supervision invocation refuses. An ordinary
terminal/delivery result suppresses suspension only when the existing public
native-result reader validates its result, journal range, receipt, retained
evidence, and workspace binding.

Provider-call ambiguity remains explicit as `provider_boundary_ambiguous`.
No missing provider identity is invented, no provider work is retried, and no
API lease/allocation, provider, spend, workspace, or native custody is released.

## Explicit exclusions

- initial-wave fan-out;
- legacy/direct authoring;
- bounded interactive reconciliation;
- exact or bounded Batch reconciliation;
- signal handling, OS process killing, PID ownership, or API force-fence logic;
- installed-wheel/API subprocess qualification, packaging, release, and deploy.

Unsupported reconciliation routes reject an attached suspension observer
rather than silently ignoring it.

## Provider-free evidence

- `test_native_suspension_runtime_slice3`: **11 passed**.
- contract plus neighboring v2/reconciliation regression matrix: **112 passed,
  2 expected skips**.
- Covered public CLI output, pre-POST zero-create suspension, pre-GET zero-GET
  suspension, request arrival during GET, durable response evidence, prior
  ordinary-result precedence, forged-result non-dominance, absent/malformed
  control state, conflicting requests, interrupted publication repair, exact
  replay, and unsupported bounded routing.

No provider/network/spend, live API/R2, process-control, packaging, release, or
deployment activity occurred.

## Review gate

Paused at Voof-paws D. Slice 4 cross-package supervision qualification remains
blocked pending runtime review.
