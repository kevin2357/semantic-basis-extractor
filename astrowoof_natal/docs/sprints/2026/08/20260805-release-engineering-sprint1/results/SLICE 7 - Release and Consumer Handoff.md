# Slice 7 — Release and Consumer Handoff

## Result

Slice 7 is complete through the pre-tag boundary. The final wheel is
reproducible, freshly installed, smoke-tested, checksummed, and documented for
an API worker. The sprint is `ready_for_tag_approval`.

## Final artifact

- Filename: `astrowoof_natal_authoring-0.1.0-py3-none-any.whl`
- Bytes: 612,752
- SHA-256:
  `58f8d93066cce040ebfc07bc89ffb11254895f0768965aa305296a722aa39dfe`
- Wheel entries: 39
- Bytecode/cache entries: 0
- Python/ABI/platform: `py3-none-any`
- Local ignored artifact: `dist/astrowoof_natal_authoring-0.1.0-py3-none-any.whl`

Two independent builds used `SOURCE_DATE_EPOCH=1785928100`. Their bytes and
hashes matched exactly. This proves reproducibility for the recorded source and
build environment rather than merely comparing filenames or metadata.

## Installed verification

The final wheel was installed without dependencies into a fresh virtual
environment. All three console scripts resolved from site-packages. The
packaged smoke then verified:

- installed runtime isolation;
- four projected fixture hashes;
- initial checkpoint and separate-process resume;
- forced pass rejection followed by accepted retry;
- six accepted passes;
- 50 cards and four summaries;
- final validation and lint;
- five delivery members and matching manifest hashes;
- 19 resources with aggregate SHA-256
  `67be96ba08fbd89ab379d1ebf247ef011d595bd4446c4534edd5072a503dcdf2`;
- 20 reconstructable cleanup targets and 4,627,864 reclaimed bytes; and
- retention of durable final/operator artifacts.

The exact report is `slice7-final-installed-smoke.json`.

## Consumer handoff

`astrowoof_natal/releases/0.1.0/` now contains the machine release manifest,
checksum, hash-pinned requirement, compatibility declaration, API-worker
guide, and release notes.

The API integration treats the CLI and versioned JSON artifacts as the public
boundary. It does not couple the service to package-internal Python modules.
The API reads `public-run.json` for polling, holds an exclusive run lease before
invoking initial/resume commands, and promotes only `DELIVERY_COMPLETE`
artifacts.

## Remaining release action

After this Slice 7 change set is committed and explicitly approved:

1. create annotated tag `astrowoof-natal-authoring-v0.1.0`;
2. push the commit and tag when requested;
3. create the GitHub release; and
4. attach the exact wheel from `dist/` plus `SHA256SUMS.txt`.

The tag is intentionally not created as part of this pre-approval slice.
