# Slice 5: Closeout and Release Recommendation

## Outcome

All sprint exit criteria pass. New required providerless denials terminalize
atomically; exact retained 0.4.1 evidence has a supported fail-closed recovery
path; private/public state, runner behavior, inspection, quiescence, closeout,
events, CLI, packaged contracts, and installed smoke agree.

The complete response to the originating API handoff is
[`API RESPONSE.md`](../API%20RESPONSE.md).

## Final qualification

```text
focused consumer/lifecycle suite: 79 passed
complete repository suite: 310 passed in 134.137s
py_compile: passed
git diff --check: passed
Windows Python 3.11 installed-wheel smoke: passed
Linux Python 3.11 installed-wheel smoke: passed, network disabled
wheel required-member inspection: passed
provider operations: 0
paid spend: $0
API key used: no
```

Two isolated builds used the source commit timestamp as `SOURCE_DATE_EPOCH` and
produced byte-identical wheels:

```text
filename: astrowoof_natal_authoring-0.4.1-py3-none-any.whl
build A SHA-256: a344dfedf3b71beef52006ed7f19037d5c001cadc583f9d88026c05d4067f296
build B SHA-256: a344dfedf3b71beef52006ed7f19037d5c001cadc583f9d88026c05d4067f296
```

That filename/hash is a temporary qualification artifact, not a release. Both
build trees, Windows venv, and cross-platform smoke workspaces were removed after
compact evidence was retained. No `.tmp`, `.qualification`, wheel, or venv belongs
in the sprint commit or future tag.

## Compatibility

The next release remains a patch over SBE 0.4.1 and retains the existing upstream
compatibility boundary: semantic-projection-core 0.11.0 and the bounded AGF 0.8.1
input lineage already pinned by SBE 0.4.x. Requests remain v0.1. Current successful
single and batch denial results are v0.2; v0.1 results remain readable historical
evidence. Existing single and atomic batch operations remain supported.

## Recommendation

Prepare a pinnable SBE `0.4.2` patch from the eventual committed sprint-closeout
source. Build twice from that exact commit, record the final artifact hash and
source commit distinctly, rerun the installed Windows/Linux lifecycle smoke, then
tag and publish only after explicit authorization.

No release, version bump, immutable artifact, tag, or publication occurred in this
slice.
