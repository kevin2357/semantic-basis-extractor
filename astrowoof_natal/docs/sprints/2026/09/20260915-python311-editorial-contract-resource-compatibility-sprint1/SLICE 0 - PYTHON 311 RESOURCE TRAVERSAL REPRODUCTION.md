# Slice 0 — Python 3.11 resource-traversal reproduction

## Decision

The live defect is reproduced and the compatibility hypothesis is confirmed.
Production implementation remains paused for Gate A review.

## Method

The repository was mounted read-only into official `python:3.11.15-slim` and
`python:3.12.14-slim` containers. The provider-free probe is retained as
`slice0_resource_probe.py`. It imports the real source package and uses the real
packaged editorial semantic-contract resource.

No provider, network application, R2, Better Stack, API, queue, lifecycle, or
workspace operation was performed. Network access was used only to fetch the
two official Python container images.

## Exact reproduction

Python 3.11.15 reports:

```text
joinpath_signature (self, child)
original_outcome TypeError
```

Python 3.12.14 reports:

```text
joinpath_signature (self, *descendants)
original bytes 11604 sha256 306fcf0e55c56f5fe48b18eaced64dbb3338ab783a5722a801f7759af96e52e5
original_identical True
```

This reproduces the live `TypeError` at the exact two-descendant call shape and
explains why Python 3.12 qualification did not expose it.

## Byte-preserving correction proof

On both runtimes, chained single-component traversal and direct `/` traversal
selected identical bytes:

```text
bytes 11604
sha256 306fcf0e55c56f5fe48b18eaced64dbb3338ab783a5722a801f7759af96e52e5
chained_identical True
```

The proposed traversal correction therefore does not select a different
contract or alter its bytes.

## Failure preservation

On both runtimes:

```text
missing_outcome FileNotFoundError
malformed_outcome ValueError
```

Chained traversal does not make a missing resource successful, and existing
strict JSON parsing continues to reject malformed content.

## Related call-site inventory

AST inventory found ten calls with more than one explicit positional argument,
plus one starred call whose runtime arity can exceed one. All are incompatible
with Python 3.11 when exercised with the concrete filesystem `Traversable`.

| Module | Lines | Classification |
| --- | --- | --- |
| `editorial_review_contracts.py` | 221 | Live production defect; Slice 1 target. |
| `editorial_review_fixtures.py` | 628 | Editorial packaged-fixture reader; latent Python 3.11 qualification defect. |
| `resource_access.py` | 16 | Generic package resource accessor; latent Python 3.11 defect when called. |
| `adversarial_consumer.py` | 64, 65, 70 | Adversarial packaged-fixture/qualification readers; line 70 uses starred components. |
| `adversarial_trace.py` | 577, 781 | Adversarial schema and fixture readers. |
| `external_authority_v2.py` | 276 | External-authority packaged-fixture reader. |
| `provider_economics.py` | 570, 578 | Provider-economics packaged-fixture/corpus readers. |

The current live correction should remain narrow. The additional sites deserve
a separately reviewed compatibility sweep or individually justified changes;
they do not justify silently broadening this production fix.

## Gate A request

Approve Slice 1 to replace only
`editorial_review_contracts._resource_bytes()` with chained
single-component traversal and add Python 3.11-focused byte/failure regression
coverage. Decide separately whether the ten latent calls belong in this release
or a follow-up compatibility sprint.

