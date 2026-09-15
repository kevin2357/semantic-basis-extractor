# Slice 2 — Provider-free executable contracts

## Result

Complete and paused at Voof-paws C. SBE now packages closed executable readers
for the API supervision envelope and suspension request, plus the SBE native
result, receipt, command-result transport, and a full joined fixture bundle.
No coordinator safe point, CLI argument, control-file polling, process control,
provider operation, API mutation, R2 access, or release behavior was added.

## Public implementation

- `native_suspension_contracts.py` contains the closed readers, exact join
  validators, request replay classifier, and canonical digest helper.
- `native-cooperative-suspension-contracts.v1.schema.json` packages the full
  schema family and fixture-bundle shape.
- `native-suspension-fixtures.v1.json` packages one complete positive
  C1-to-C2 dispatch case, including envelope, request, result, receipt, and
  command-result documents.
- `contract-catalog.json` names all six additive public contract versions.

## Serialization correction

The prose statement that a result itself binds a final receipt digest could not
be implemented without circular hashing: the receipt must also bind the result
digest. The executable contract follows the existing native-publication shape:

```text
result (independently hashed)
  -> receipt binds result ID + digest
  -> command-result binds result and receipt IDs + digests
```

The joined bundle reader enforces the B2 one-to-one cardinality globally. The
result does not embed or preclaim the later receipt digest. Gate B prose was
updated accordingly before runtime implementation.

## Executable invariants

The focused tests cover:

- closed field sets, versions, enums, UTC ordering, and canonical hashes;
- absolute, digest-bound, disjoint executable/control roots;
- complete envelope/request identity joins and expiry;
- exact replay versus invocation-wide conflict even with a changed key;
- C1 equality or exact contiguous C2 successor, rejecting non-successors;
- all six closed suspension outcomes and deferred continuation shape;
- action ordering, unique IDs, and provider custody requiring durable provider
  identity;
- prior ordinary-result evidence suppressing suspension publication;
- recomputed-digest receipt and command-result join mutations; and
- global request/result/receipt uniqueness in the full fixture bundle,
  including rejection of a fully re-sealed second semantic result for the
  same exact request.

Focused source result: **11 tests passed, 1 expected optional `jsonschema`
skip**. The neighboring release-contract module also passed, for **25 tests
passed total with the same one skip**.

## Alloy traceability

Every B2 relation now has an executable counterpart in
`test_native_suspension_contracts_slice2.py`. The model remains a design check;
the Python readers and schema are the public executable boundary.

## Remaining boundary

This slice validates document bytes and joins supplied directly by a caller. It
does not yet open an envelope/control path, inspect filesystem links, atomically
read a request, observe an actual coordinator safe point, publish via the native
writer, or select an API resource disposition. Those remain Slice 3/4 work and
are still gated.

This is Voof-paws C. Runtime integration must not start before reciprocal API
review of the exact schemas, readers, packaged fixture, and serialization
correction.
