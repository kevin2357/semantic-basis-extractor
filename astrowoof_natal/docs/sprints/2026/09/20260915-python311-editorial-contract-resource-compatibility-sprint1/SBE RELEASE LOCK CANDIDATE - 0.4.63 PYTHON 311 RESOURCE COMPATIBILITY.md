# SBE release-lock candidate — 0.4.63 Python 3.11 resource compatibility

## Decision

The release-lock source is ready to commit. Tagging and publication are not
authorized. The commit containing this record becomes the proposed immutable
release target only after exact-source rebuild and installed qualification.

## Frozen pre-lock coordinates

- Version: `0.4.63`
- Artifact-source commit: `3e065e759ab8cb92b88cd9415b4e9d6254c114ad`
- Artifact-source epoch: `1789481170`
- Canonical filename:
  `astrowoof_natal_authoring-0.4.63-py3-none-any.whl`
- Expected bytes: `1,385,639`
- Expected SHA-256:
  `fe0fba0c0be87ec25257a9b9c8c5f6e0166f9544df99fc8f940b20109ea1e355`
- Expected member count: `310`

## Accepted evidence

- Live failure reproduced exactly on Python 3.11.15 and contrasted with
  Python 3.12.14.
- Live helper repair approved and focused tests green.
- Companion resource sweep corrected only four proven namespace-package
  failures and retained six real-runtime-compatible controls unchanged.
- Release-bound focused matrix green on both Python 3.11.15 and 3.12.14.
- Manifest-controlled full suite: 1,200 tests, 60 expected skips, zero failures.
- Two artifact-source wheels: byte-identical, 310 members, no forbidden members.
- Clean installed Python 3.11.15 and 3.12.14 dependency, smoke, editorial QA,
  and 15-test capture/diagnostics gates: passed.
- Provider/runtime external operations, spend, and authoritative mutation: zero.
- Alloy impact: none.

## Required exact-lock gate

After committing this record:

1. record the release-lock commit and its timestamp as the exact build epoch;
2. create two detached clean worktrees at that commit;
3. build independently and require the same canonical filename, size, SHA-256,
   member inventory, and package-data checks;
4. repeat clean installed qualification on Python 3.11.15 and 3.12.14; and
5. return the exact commit/wheel coordinates for API final pre-tag review.

Do not tag, publish, deploy, or run a live witness without later explicit owner
authorization.

