# 0.4.72 publication and download verification

Published 2026-10-18 20:21:53 UTC:
https://github.com/kevin2357/semantic-basis-extractor/releases/tag/astrowoof-natal-authoring-v0.4.72

| Item | Identity |
| --- | --- |
| GitHub release ID | `416688160` |
| Annotated tag object | `a52f4a0fc74a600086440e824e0b6ecc74beaaea` |
| Peeled release-lock commit | `9bd4b32bb6be928c097fdbab9d32047b84d2bf61` |
| Wheel asset ID | `654399639` |
| Wheel size | `1,442,607` bytes |
| Wheel SHA-256 | `298273523a05c7a72cdd5404ca1727ef3f03c5c922785a7c5ba4da6f2990c364` |
| `SHA256SUMS.txt` asset ID | `654399638` |
| `SHA256SUMS.txt` SHA-256 | `bc429723b4036cfdfa3b86869189803d992ec0c87db0b3c5e6c5c604b37f5e43` |

The uploaded wheel is the original retained candidate approved by API, not a
substitute. Two independent canonical-LF archives of the release-lock commit,
using `SOURCE_DATE_EPOCH=1791479232`, reproduced its exact filename, size,
330-member inventory and whole-wheel SHA. The inspected archive contained no
duplicate names, Python bytecode, packaged test directories or CRLF text.

The original wheel and SPC 0.11.1 were installed in a fresh isolated venv;
`pip check`, `astrowoof-release-smoke --require-installed`, the public external
authority v2 CLI help, and the provider-free `astrowoof-adversarial-qa` passed.
Imports resolved to `site-packages`; the installed version was `0.4.72`.
The adversarial receipt reports 22 route cells, zero external network calls,
zero real provider creates and zero provider spend. Receipts are retained under
`C:\tmp\sbe-0472-release-lock-9bd4b32b\`.

GitHub's reported wheel digest matches the qualified wheel. Both assets were
downloaded into a fresh directory; the recomputed wheel and checksum-file
digests match GitHub, and the downloaded checksum line names and hashes the
wheel exactly. The remote peeled tag was rechecked at the lock commit.

API's Gate D review approves the exact published bytes for package release;
it does not authorize QA or production rollout, profile activation, paid work,
or live alert qualification. See the API sprint 128 package release review and
crash-custody design for the remaining coverage and operator-signal limits.
