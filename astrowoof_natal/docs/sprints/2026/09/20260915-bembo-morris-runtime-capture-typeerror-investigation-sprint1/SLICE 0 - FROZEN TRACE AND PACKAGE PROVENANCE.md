# Slice 0 — frozen trace and package provenance

## Result

The two witnesses are frozen at one common boundary, but the normalized
`type_error` does not identify an inner expression. The evidence excludes an
incorrect call-time root string, missing diagnostics, packet transport, and
Better Stack delivery as causes.

## Trace identity

| Export | Bytes | Records | First/last UTC | SHA-256 |
| --- | ---: | ---: | --- | --- |
| `sbe-worker-01-0220Z-to-0230Z.json` | 638,490 | 230 | 02:27:50.447Z / 02:29:59.838Z | `230ebd8c50e4161b0485ed7be2f285d34da30f8a1a8bc24ba20940801874d0e0` |
| `sbe-worker-02-0230Z-to-0240Z.json` | 1,780,950 | 868 | 02:30:00.045Z / 02:39:54.337Z | `41aa024ed3570c58aff8491cb9c088c4701b41907ee1a27debf3859e032a597e` |

Files 03–06 are zero bytes and each has SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
The two nonempty files contain complete concatenated Render JSON records and
remain below the 1,000-record export cap.

Bembo joins API run `c77f8bfe-6c8b-4612-8dcd-de76d7d5822b`, native run
`a1523be35ee0d47fa5e471fc6dc8b4bd6ee5b3d8959ba591b7b720cf4977d3e0`,
and exact delivery result `nres_a83f5a0c2946e06876d7e79c`. Morris joins API
run `f679b5af-8dcb-4db5-a79b-72c67fac4f6f`, native run
`b374742b24ec55c5f04dec878e663cdc4bf8d86d4e476542fdde5ff224651220`,
and exact review result `nres_3f628ce39fa7673b7c141a25`.

For each join, exact authority selection precedes capture entry. Capture then
fails as `type_error`; the wrapper returns `unavailable` with zero artifacts;
the completed event preserves that class; and no envelope, request-preflight,
HTTP, or artifact event occurs. Bembo's call-time root digest is
`8d924a9bf4d41931be78dd844686ff0353c0cd6dd90144e6ffa84c5097b19e41`;
Morris's is
`ec1ae981f99ac42c29d411dc84bf36d4badcdfeab0dcc57c706f4fc885ead689`.
Each equals SBE's independently emitted logical-root digest for that run. This
proves the passed root string, not the shape of members beneath the root.

## Installed provenance

- SBE release: `0.4.61`
- tag: `astrowoof-natal-authoring-v0.4.61`
- peeled release commit: `477cfa2491f33377f1a873772c5e465c588f0741`
- wheel: `astrowoof_natal_authoring-0.4.61-py3-none-any.whl`
- wheel size: 1,383,877 bytes
- wheel SHA-256:
  `8dd151fced3fc7823ef914c7642798a977eca93d19b1136bf34da55b589ef723`
- deployed API source revision:
  `3731930afe963b0722a5bf23df664d77c6dab1e7`
- deployed SBE-worker image digest:
  `sha256:525fa40802cffd757351a93343355709c44c2baeede01ba94a5df0f6cce9a5b2`

The API virtual environment reports installed distribution `0.4.61`. Its
installed `editorial_review_runtime.py` is byte-different only because it has
CRLF line endings: after CRLF-to-LF normalization it exactly equals the source
module, with normalized SHA-256
`44bc9c15bbe8bf435e526092e75c7f1d913427d73b65c70eafb5a66b39f7ef50`.
The checked-out module has no diff from the 0.4.61 tag.

## Boundary ruling

The wrong-root and release-pair-skew hypotheses are not supported. The first
exception is within the installed public capture call, before API assembly of
an envelope. Source inspection leaves two ways for a `TypeError` to escape:
evidence collection before the packet builder's guarded assembly region, or a
second `TypeError` while constructing typed unsupported status after a guarded
assembly failure.

