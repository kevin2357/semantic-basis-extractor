# Slice 7 — Release and Consumer Handoff

## Result

Slice 7 and publication are complete. The final wheel is reproducible, freshly
installed, smoke-tested, checksummed, documented for an API worker, tagged,
published, and independently downloaded and verified from the private GitHub
release.

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

## Publication

- Annotated tag: `astrowoof-natal-authoring-v0.1.0`
- Tag commit: `8fdad164b151c87f77dfc416f6efb754cf00fd7b`
- Release ID: `365479789`
- Published: `2026-08-05T11:33:40Z`
- Release URL:
  `https://github.com/kevin2357/semantic-basis-extractor/releases/tag/astrowoof-natal-authoring-v0.1.0`
- Wheel asset ID: `502545315`
- Checksum asset ID: `502545321`
- Draft: no
- Prerelease: no

Both assets were downloaded after publication through the authenticated private
release API. The downloaded wheel's size and digest matched the final manifest,
and the downloaded checksum named the same digest. The annotated tag remains
fixed at the reviewed release commit; this post-publication record lives on
`main` and does not move the tag.
