# API review — Slice 4 and Voof-paws 5

## Decision

Approved. The primary classification is correct: **SBE runtime defect in
exact-interactive provider-result fan-in/adoption ordering**.

The terminal-review result was complete and truthful. API's strict join was
correct to reject the native-only successor. Neither public contract needs a
scope expansion, and the API must retain its existing rules: exact v2 admission
only, no action manufacture from terminal evidence, no retrospective denial,
and no subset acceptance.

## Implementation conditions

Proceed with Slice 5 under the specified single-writer ordering. In addition to
the planned provider-free matrix, make the interruption boundary explicit in
tests:

- no durable successor may exist without a corresponding successor inspection
  that can yield its exact public external-authority request after restore;
- a crash before coherent adoption cannot produce either predecessor
  consumption or successor preparation by inference; and
- a crash after adoption but before successor preparation cannot replay provider
  creation or produce more than the one deterministic successor.

Keep Batch and bounded routes characterization-only unless they demonstrably
share the same exact adoption primitive and preserve their route-specific public
evidence.

Voof-paws 5 is satisfied. Slice 5 implementation is approved; pause before
packaging/release so API can review the concrete tests and public behavior.
