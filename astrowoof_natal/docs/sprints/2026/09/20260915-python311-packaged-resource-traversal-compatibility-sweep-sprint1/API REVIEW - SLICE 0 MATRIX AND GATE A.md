# API review — Slice 0 matrix and Gate A

## Decision

Approved for implementation under the concrete-runtime matrix:

- correct exactly the four proven Python 3.11 namespace-package failures;
- retain `resource_access.py`, `adversarial_consumer.py`, and
  `adversarial_trace.py` unchanged as tested no-op controls; and
- preserve the predecessor live-helper correction as an unchanged control.

## Why this scope is correct

The static inventory was useful for discovery, but it is not the implementation
authority.  The real Python 3.11/3.12 probes establish the relevant distinction:
the four failing readers start at namespace-package `MultiplexedPath` values,
where Python 3.11 permits one child per `joinpath`; the six controls start at a
regular top-level package `pathlib` traversable and already support their
current call shapes.

Avoiding a generic `resource_access.py` rewrite is particularly appropriate:
it has high reach, works on the declared minimum runtime, and carries a
deliberate relative-path-string contract.  Changing it would add surface area
without a compatibility benefit.

## Implementation and qualification fences

For each of the four repairs, retain the stated real-resource byte/digest
checks and missing/malformed/closed-name controls on Python 3.11 and 3.12.
The external-authority and provider-economics fixture readers are public
contract/qualification surfaces, so their successful Python 3.11 execution is
required—not optional because they are fixtures.

The final source-tree qualification must also execute representative callers
for every no-op control on both runtimes.  The final inventory should report
zero *unsupported supported-path* variadic traversals, rather than claiming
that syntax alone disappeared everywhere.

## Release handoff

Once this sweep completes, return an exact reviewed commit and two-runtime
evidence to the predecessor live-defect sprint.  That predecessor alone should
build the wheel and conduct installed-wheel/API release qualification.  No API,
schema, lifecycle, custody, packet, transport, Better Stack, or Alloy change
is implicated.
