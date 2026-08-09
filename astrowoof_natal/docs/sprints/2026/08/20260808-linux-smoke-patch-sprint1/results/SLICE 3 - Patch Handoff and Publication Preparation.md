# Slice 3 - Patch Handoff and Publication Preparation

Status: complete; published and independently verified.

Prepared the complete 0.2.1 release-record bundle: candidate manifest,
checksum, hash-pinned API-worker requirement, release notes, compatibility
delta, and worker handoff. All coordinates agree on wheel size 624,157 bytes
and SHA-256
`0d273c2d0e98d54abadd28ff1a36f670bd4bbd7e7441bac263f6dbafe75bfc08`.

The handoff directs the API worker to replace only SBE's wheel/version/hash,
retain the existing qualified dependency pins, ingest public state into
API-owned persistence, and run the installed smoke in the final Linux image.
It links directly to the detailed spend-authorization, spend-enforcement, and
packaged contract catalog sources.

The records explicitly reuse 0.2.0 production qualification and state that
0.2.1 changes only fake-provider portability and release-smoke failure
handling. No production contract, paid-provider route, or API ownership moved.

## Publication evidence

The reviewed records were committed as
`9e9db5f7378d459db1e5418f1607edc7f4c060bf`. Annotated tag object
`7998c299824b13240215b9a501a1a3aeb309464f` peels to that exact commit locally
and remotely. The immutable tag is `astrowoof-natal-authoring-v0.2.1`.

GitHub release 367357028 was published at `2026-08-09T02:17:11Z` as a
non-draft, non-prerelease release. Its assets are:

- wheel asset 506995740, 624,157 bytes, SHA-256
  `0d273c2d0e98d54abadd28ff1a36f670bd4bbd7e7441bac263f6dbafe75bfc08`;
- checksum asset 506995739, 115 bytes, SHA-256
  `e46fa25e4e187b3fa39172c01010b4100ccdf661c0fc6b6cdecaf7b642700c7a`.

Both assets were authenticated-download retrieved into a fresh directory. The
downloaded wheel matches the reviewed candidate digest and size, and the
downloaded checksum independently validates that wheel. The tag was not moved
after publication.

Release URL:
<https://github.com/kevin2357/semantic-basis-extractor/releases/tag/astrowoof-natal-authoring-v0.2.1>
