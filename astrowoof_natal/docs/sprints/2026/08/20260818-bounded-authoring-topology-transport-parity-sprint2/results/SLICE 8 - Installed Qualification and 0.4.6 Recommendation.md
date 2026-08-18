# Slice 8 — Installed Qualification and 0.4.6 Recommendation

Status: complete; awaiting explicit release authorization

## Recommendation

Recommend `astrowoof-natal-authoring` 0.4.6 as the next fresh immutable pinnable
release. Do not alter or replace published 0.4.5.

The current qualification wheel still identifies itself as 0.4.5 and therefore is
not publishable. It proves the post-0.4.5 source boundary. Release authorization
must trigger a 0.4.6 version bump, exact-source commit, two reproducible final
builds, repeated installed gates, immutable tag, and publication.

## Candidate evidence

| Evidence | Result |
|---|---|
| Source commit | `58f6779` |
| Fixed epoch | `1787040000` |
| Independent builds | 2, byte-identical |
| Qualification wheel SHA-256 | `bf864e2376ba36f3a8a292b3092c095ee52fac2ce8fcf081521f6ad3a3350ff2` |
| Wheel bytes / entries / resources | 800,957 / 106 / 61 |
| `py.typed` | present |
| Tests or bytecode | absent |
| Provider operations / spend | 0 / USD 0 |

## Gates

- Full repository: 423 passed in 428.695 seconds; 10 expected environment skips.
- Strict contract/release environment: 48 passed without skips.
- Windows CPython 3.12 installed: `pip check`, lifecycle smoke, release smoke,
  resource CLI, and all four fake-provider route modes passed.
- Linux CPython 3.11 installed: the same gates and all four fake-provider route
  modes passed.
- SPC 0.11.0 wheel SHA-256 reverified as
  `82290df44fe5697e87df2e27eb0aa4bab3b7954c66ce988efda0962964e1366d`.

## Frozen consumer resources

- Oracle v2:
  `c355a3c47b69fcbc78622df97b89572172133253f34d0342ae18e609e1e4d97d`.
- Bounded traces v1:
  `02d8aba73028c144c97e8c806cd0f8b3505fe4ca3410284d4bc8e2d4c33f0268`.

These identities are repeated in the 0.4.6 API handoff and candidate manifest, as
required by API consumer approval.
