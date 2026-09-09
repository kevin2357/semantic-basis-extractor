# Slice 1ε.0 — executable contract foundation

## Result

Complete. The approved editorial-review shape now has a package-owned,
provider-free executable foundation:

- eleven closed Draft 2020-12 JSON Schemas (fixture-bundle and qualification
  schemas were added by Slices 1ε.1–1ε.2 without changing native vocabulary);
- one machine-readable semantic contract manifest;
- strict UTF-8/single-value JSON parsing with duplicate-key, non-finite-number,
  and trailing-content rejection;
- canonical native JSON/digest and domain-separated ID primitives;
- a closed immutable validation-result type;
- a dependency-free closed-root/version validation stage;
- a staged semantic-validator registry that fails closed until each deeper
  stage is implemented; and
- bidirectional manifest/handler/test-target coverage checks.

No runtime packet builder or fixture payload was added in this slice. Slices
1ε.1–1ε.2 remain responsible for truthful positive histories and full semantic
enforcement/mutations.

## Packaged resources

| Resource | SHA-256 |
| --- | --- |
| `editorial-review-artifact.v1.schema.json` | `6800686250600126ee45f51cbd028d0538fc56d8960039b1af1233999d404e7d` |
| `editorial-review-capture-status.v1.schema.json` | `da1f203de04d550313fe9c28faf17ac2e41fc97696a49f70bd32b688260a6e8e` |
| `editorial-review-contract-fixture-bundle.v1.schema.json` | `0bae57d92721b59f6cfa0a8c58eee1fecbb3a13146cdc74f71709d823a2b6789` |
| `editorial-review-contract-qualification.v1.schema.json` | `142d3c3f3beb836781da197247e9304cefeab743b721f44a9ea3bad54c3929f3` |
| `editorial-review-decision.v1.schema.json` | `c1da324ef7c4afc7fce7494ac3ef2aa9f5c39ac3f6f2fce53b0f91867f00914e` |
| `editorial-review-finding.v1.schema.json` | `4b6923c92e73cb662a378efd8a0c34c48c3c2e826f2e83c8c93c5f1b23694f42` |
| `editorial-review-packet.v1.schema.json` | `21ae4ade39eaede07845debbe17c212479abd8e3ee0295e0536ef6e90b024a85` |
| `editorial-review-projection.v1.schema.json` | `1ee12dcf61694876be842f7b3e0d06cc26133e253f6070d59ab7cbaf96f9f4c5` |
| `editorial-review-transport.v1.schema.json` | `567c322d4ea114f5c56de705094e36afbc3d0b67e8977b4595b8fdb64d711a97` |
| `editorial-review-validation-result.v1.schema.json` | `b46c8a9c4cfbfc63b7c6e850d32ed1b0a153481b90be56cdea7ea08996343838` |
| `editorial-review-validation.v1.schema.json` | `3aaa4a6918c6649dec195f683ffddd4f484b28f1aebac683b308144cb69bc602` |

Semantic manifest:

- resource: `editorial-review-semantic-contract.v1.json`;
- SHA-256:
  `ff6e7d5548edf8ff94be191064070f0ebe6407987f0a68d94416df250e007a20`;
- compatibility identity:
  `astrowoof.editorial-review.native-contract.v1`.

The manifest reader independently recomputes every declared schema digest and
rejects unknown root/rule fields, unknown rule owners, duplicate resources, or
unsupported versions.

## Contract boundaries frozen here

- API annotations and `observed_at` remain outside native digest domains.
- Transport native content is one of the exact packet/projection/artifact/
  capture-status contracts, not an untyped open object.
- Only full deck/provider-response payload members are intentionally opaque;
  their wrappers remain closed and their released payload schemas are carried
  separately by identity.
- Artifact IDs use a packet-scoped derivation domain. Equal payload bytes in
  another packet are joined through `object_sha256`, not wrapper identity.
- Terminal selection explicitly distinguishes decision-owned from
  assembly-owned evidence.
- Terminal-owned validation is a discriminated owner form, never a synthetic
  decision.
- A valid editorial closeout is valid evidence; contradictory evidence remains
  an invalid typed classification.
- Registered but not-yet-implemented semantic stages raise rather than return a
  false valid result.

The API-owned preflight profile is recorded descriptively as canonical JSON
UTF-8, gzip level 9 with `mtime=0` and no filename/comment/extra fields, maximum
99 editorial events, and a proposed 9 MiB safe threshold below the verified
10 MiB external ceiling. API still owns live envelope bytes and final preflight.

## Verification

Focused foundation plus runner-manifest suite:

```text
Ran 27 tests in 0.567s
OK (skipped=1)
```

The one skip is the existing optional third-party `jsonschema` check because it
is not present in the selected bundled Python runtime. Dependency-free package
resource parsing, digest binding, closed-root/version checks, strict JSON,
public exports, rule coverage, and test-manifest coverage all passed.

`git diff --check` is clean for the implementation surface (aside from the
repository's existing line-ending notice on `__init__.py`).

No provider, network, R2, Better Stack, API, database, subprocess, retained QA
workspace, runtime integration, or release operation occurred.

## Next boundary

Slice 1ε.1 builds the separate accepted-delivery and editorial-closeout
positive fixtures and deterministic qualification. This is not yet the final
1ε voof-paws; that remains after Slice 1ε.2.
