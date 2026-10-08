# API Agent Gate B Review

## Disposition

**Changes requested before Gate B acceptance.** The Slice 1 split is otherwise
sound: it keeps ordinary v2 lexical behavior closed, carries the six-member
semantic initial-wave projection through request/grant/no-grant, and proves
binding-descriptor tamper fails before authority export.

## Required correction: join the inspection's native route family

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

Please add:

1. an explicit `native_route.route_family == "bounded_natal"` requirement in
   the initial-wave v2 validation path; and
2. a focused test that changes the inspected route family (or its equivalent
   sealed route projection) while retaining a bounded initial-wave projection,
   and proves request/grant/no-grant refusal before native mutation or provider
   I/O.

## Confirmed strengths

- Semantic member order is preserved separately from ordinary lexical order.
- The six-member projection and per-member binding digests join the inspected
  inventory.
- Projection and member-document tampering refuse.
- Descriptor tampering suppresses authority export before grant construction.
- No v1 document is accepted as a v2 document, and no execution intent exists
  in this slice.

Once the native-route-family join/refusal is present, API will approve Gate B
and SBE can proceed to the durable intent/execution adapter.
