# Slice 2 - Exact Patch Artifact Qualification

Status: complete; gate approval pending.

## Artifact identity

The only release-coordinate change is the project version from `0.2.0` to
`0.2.1`. Two isolated wheel builds used `SOURCE_DATE_EPOCH=1786240889`, the
UTC commit timestamp of the approved Slice 1 commit `7379ea4`. They are
byte-identical:

- filename: `astrowoof_natal_authoring-0.2.1-py3-none-any.whl`;
- size: 624,157 bytes;
- SHA-256: `0d273c2d0e98d54abadd28ff1a36f670bd4bbd7e7441bac263f6dbafe75bfc08`;
- members: 40; and
- wheel audit failures: 0.

The complete member audit found no caches, sprint or diagnostic records,
provider payloads, credentials, acceptance workspaces, or other disallowed
content.

## Installed qualification

A clean Windows virtual environment installed the exact wheel outside the
checkout. The installed-runtime smoke imported from `site-packages`, reached
`DELIVERY_COMPLETE`, retained the deliberate rejected first attempt and
accepted retry, delivered 50 cards and four summaries, verified all manifest
hashes, passed final QA, and completed cleanup.

The API agent's retained Docker context was copied under `C:\tmp`; the retained
context itself was not edited. Only the SBE 0.2.0 wheel and locked hash in that
copy were replaced with the candidate wheel and hash. Docker built the image
with `--network=none` from the same pinned Python 3.11 Linux base and qualified
wheelhouse. The build installed exact AGF 0.6.0, SPC 0.10.0, SBE 0.2.1, and
pyswisseph 2.10.3.2; the existing AGF doctors and SPC installed smoke passed.

Running `astrowoof-release-smoke --require-installed` as the image's non-root
worker user passed and reached `DELIVERY_COMPLETE`. Windows and Linux agree on
all semantic/delivery counts, QA statuses, retry behavior, delivery members,
and the 19-resource aggregate digest
`439c8771fe7944ddb1b5b83465b7d2f76f252340624f1b85c85f9278fba55404`.
Platform-local temporary fixture-file hashes and reclaimed byte counts differ,
as expected; neither is an authored resource or cross-platform contract.

Linux `pip check` reported no broken requirements. The candidate image is
`astrowoof-domain-worker:sbe-0.2.1-smoke`, Linux/amd64 image digest
`sha256:b3420fe8c4ff3183e5ebbdced1a678a2e0c278f3791189586488e7792a264dc0`.
No network or OpenAI operation occurred and provider spend remained USD 0.

The full deterministic suite was already run against the identical Slice 1
source before artifact construction: 148 tests passed. Slice 2 introduced no
runtime behavior beyond the approved version coordinate, so no seven-slice
0.2.0 replay or live provider qualification is required.

Next action: review and approve the exact artifact identity, wheel audit, and
cross-platform installed-smoke evidence before committing Slice 2 or preparing
the Slice 3 handoff/publication records.
