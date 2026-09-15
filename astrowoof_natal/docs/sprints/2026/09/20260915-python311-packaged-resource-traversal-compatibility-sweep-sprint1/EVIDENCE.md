# Evidence — Python 3.11 packaged-resource traversal sweep

## Source evidence

- Predecessor Slice 0 used official Python 3.11.15 and 3.12.14 containers with
  the repository mounted read-only.
- Python 3.11 concrete signature: `joinpath(self, child)`.
- Python 3.12 concrete signature: `joinpath(self, *descendants)`.
- Chained traversal returned byte-identical resource content on both runtimes.
- Missing resources remained `FileNotFoundError`; malformed JSON remained
  `ValueError`.

## Release-blocking witness

After the narrow live helper repair:

- focused foundation suite passed on both runtimes: 13 tests, 1 optional skip;
- broader editorial-contract suite passed on Python 3.12.14: 29 tests, 1 skip;
- broader editorial-contract suite on Python 3.11.15: 29 tests, 8 errors,
  1 skip; and
- every error terminated at `editorial_review_fixtures.py:628` with
  `TypeError: MultiplexedPath.joinpath() takes 2 positional arguments but 4
  were given`.

## Control Room ruling

API issue `kevin2357/astrowoof-api#23` requires:

1. classification of all remaining explicit and starred multi-component calls;
2. priority assessment for generic `resource_access.py` with caller coverage;
3. byte-identity proof on Python 3.11 and 3.12 for every justified correction;
4. missing/malformed failure preservation;
5. installed-wheel provider-free qualification on the declared minimum; and
6. explicit documentation of any unsupported historical-only path.

No additional live logs, Better Stack data, R2 objects, or retained workspaces
are required for the initial provider-free sweep.

## Slice 0 concrete-runtime correction

The post-hot-fix AST inventory contains nine explicit multi-argument calls and
one starred-component call. Real accessor execution on both official runtimes
showed:

- four namespace-package calls fail only on Python 3.11: editorial fixture
  reader, external-authority fixture reader, and two provider-economics
  readers;
- the generic accessor succeeds on Python 3.11 and 3.12 because it starts from
  the regular top-level package;
- all five adversarial explicit/starred calls likewise succeed on both
  runtimes; and
- independently selected resource bytes/digests are recorded in the Slice 0
  matrix.

This corrects the inherited “eleven remaining” count and prevents unnecessary
changes based solely on syntax rather than concrete traversable behavior.
