# API review — initial plan and Gate A

## Decision

Approved for Slice 0's provider-free reproduction and correction-fence work.
This is approval to test the Python 3.11 compatibility hypothesis, not advance
approval to modify production code, version, package, release, or deployment.

## Why the current framing is sound

The two independent delivery witnesses agree on the exact safe boundary:

- both completed root normalization, exact-result reading, eligibility, source
  proof, pre-assembly collection, guarded packet assembly, and validation;
- both then failed in `typed_status_construction` at
  `editorial_review_contracts.py::_resource_bytes:221` with the same
  `TypeError` fingerprint; and
- production is CPython 3.11.15 while the recent installed-wheel qualification
  used CPython 3.12.14, despite the declared `>=3.11` package floor.

That is sufficient to make the multi-descendant `Traversable.joinpath(...)`
call the right first reproduction target.  It does *not* authorize changing
roots, native identity handling, exact result readers, evidence collection,
packet assembly, validation, API observer selection, or Better Stack
transport.

## Slice 0 review points

The proposed contrast is exactly right:

1. exercise the real packaged-resource traversal on CPython 3.11, rather than
   a permissive mock;
2. contrast it with CPython 3.12;
3. prove chained single-component traversal resolves the same resource and
   returns byte-identical bytes; and
4. inventory every other multi-descendant `Traversable.joinpath(...)` use
   before deciding whether any further, separately justified source change is
   needed.

Please retain the specified error-preservation check: malformed or missing
resources must remain failures.  The correction must not turn an absent or
invalid resource into a successful capture.

## Contract and ownership ruling

The expected chained traversal is an implementation compatibility repair only.
Provided Slice 0 establishes byte identity and no different resource selection,
there is no API contract, schema, lifecycle, authority, custody, packet,
transport, or Alloy-model change.  API remains the terminal observer and
transport owner; SBE owns the packaged-resource access compatibility repair.

Proceed through Slice 0 and return with the actual Python 3.11 reproduction,
3.12 contrast, resource-byte evidence, and classified call-site inventory for
Gate A before implementing Slice 1.
