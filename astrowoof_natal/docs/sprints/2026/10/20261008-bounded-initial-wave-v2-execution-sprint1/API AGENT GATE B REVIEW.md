# API Agent Gate B Review

## Disposition

**Approved after revision `4f814e4e`.** The Slice 1 split keeps ordinary v2
lexical behavior closed, carries the six-member semantic initial-wave
projection through request/grant/no-grant, and proves binding-descriptor tamper
fails before authority export.

## Resolved correction: join the inspection's native route family

The frozen Gate A contract requires that the initial-wave branch bind the
native route as well as its `initial_wave.route_contract`. The current
`_validate_initial_wave_request()` proves the latter equals
`astrowoof.bounded_natal.authoring_run.v2`, but it does not explicitly require
that the inspected checkpoint's `native_route.route_family` is
`bounded_natal`.

That leaves a theoretical cross-route shape in which an inspection from one
route is paired with an otherwise syntactically valid bounded initial-wave
projection. The public grant echoes the inspection route family, so that
mismatch needs rejection *before* grant/no-grant construction rather than
merely being representable in a signed payload.

Revision `4f814e4e` adds the required
`native_route.route_family == "bounded_natal"` condition in the shared
initial-wave validation helper. Its focused test re-seals a cross-route
inspection while retaining the bounded projection and proves refusal during
request construction, before grant/no-grant construction, native mutation, or
provider I/O. This satisfies the requested route-family join fence.

## Confirmed strengths

- Semantic member order is preserved separately from ordinary lexical order.
- The six-member projection and per-member binding digests join the inspected
  inventory.
- Projection and member-document tampering refuse.
- Descriptor tampering suppresses authority export before grant construction.
- No v1 document is accepted as a v2 document, and no execution intent exists
  in this slice.

Gate B is accepted. SBE may proceed to the durable intent/execution adapter.
The Slice 2 proof must retain the current distinction: a valid new v2
initial-wave grant may create exactly one bounded intent, while the old v1
authorized QA witness remains ineligible for transformation or replay.
