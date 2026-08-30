# Post-release — SBE 0.4.31 publication evidence

## Immutable identities

- Distribution: `astrowoof-natal-authoring==0.4.31`
- Artifact source commit: `3709f18d1b8c15c6030173868e175110a7894c51`
- Release/evidence-lock commit: `a1dde7714479b9ea150d8d7a534e58d1f1553d55`
- Annotated tag: `astrowoof-natal-authoring-v0.4.31`
- Wheel: `astrowoof_natal_authoring-0.4.31-py3-none-any.whl`
- Size: 1,111,586 bytes
- SHA-256: `6bb587c9cd5cd0ef8bf767a677450fbaf7fcd9bf3be655ef68584e279a03f0d9`
- SPC compatibility: `semantic-projection-core==0.11.1`

The artifact source and release-lock commits are intentionally distinct. The
wheel was built and qualified from the artifact source commit; the annotated tag
points to the records-only release lock that binds its final hash and evidence.

## Publication verification

GitHub release:

`https://github.com/kevin2357/semantic-basis-extractor/releases/tag/astrowoof-natal-authoring-v0.4.31`

The published asset was downloaded into a fresh verification directory. Its size
and SHA-256 exactly match the locally qualified committed-source wheel. GitHub's
asset digest reports the same SHA-256, and the annotated tag resolves to the
release/evidence-lock commit above.

## Safety

Publication and verification performed no provider call, spend, deployment,
worker resume, retained-QA read/write, recovery, or native-run mutation.
