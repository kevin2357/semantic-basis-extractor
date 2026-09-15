# Slice 1 — Narrow helper correction and qualification boundary

## Outcome

The approved live-helper correction is implemented and passes focused tests on
Python 3.11.15 and 3.12.14. Broader Python 3.11 editorial-contract
qualification is blocked by one of the explicitly excluded latent call sites.
No broader source correction was made.

## Narrow implementation

Only `editorial_review_contracts._resource_bytes()` changed in production. It
now traverses `CONTRACT_PREFIX` and `name` in separate single-component
`joinpath()` calls.

The existing, already manifested
`test_editorial_review_contract_foundation.py` gained assertions that:

- the helper returns the exact packaged semantic-contract bytes;
- those bytes retain SHA-256
  `306fcf0e55c56f5fe48b18eaced64dbb3338ab783a5722a801f7759af96e52e5`;
- a missing resource remains `FileNotFoundError`; and
- the test's own resource lookup is Python 3.11 compatible.

No new test module was created, so `test_suite_manifest.json` required no
change. The module is already registered there.

## Focused qualification

The foundation module passed on both runtimes:

- Python 3.12.14: 13 tests run, 1 optional test skipped, success;
- Python 3.11.15: 13 tests run, 1 optional test skipped, success.

## Broader qualification finding

The three-module `test_editorial_review_contract*.py` suite produced:

- Python 3.12.14: 29 tests run, 1 optional test skipped, success;
- Python 3.11.15: 29 tests run, 8 errors, 1 optional test skipped.

All eight Python 3.11 errors converge on the separately inventoried call at
`editorial_review_fixtures.py:628`:

```text
TypeError: MultiplexedPath.joinpath() takes 2 positional arguments but 4 were given
```

That packaged-fixture reader is not the live runtime helper approved for Slice
1. Changing it now would violate the API scope ruling that all eleven latent
sites receive a separate tested compatibility sweep.

## Decision required

Keep the narrow live fix intact, but do not advance to candidate-wheel Gate B
qualification until the separate compatibility sweep resolves at least the
packaged editorial-fixture reader that blocks Python 3.11 qualification.

The recommended next step is a sibling compatibility-sweep sprint covering all
eleven inventoried sites with caller-specific real-resource tests, beginning
with `resource_access.py` and `editorial_review_fixtures.py`. This sprint should
remain the release-driving live-defect record and consume the sweep only after
its independent review.

