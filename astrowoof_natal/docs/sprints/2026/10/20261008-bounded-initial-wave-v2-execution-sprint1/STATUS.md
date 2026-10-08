# Status

**Canonical replacement candidate is built and qualified for renewed API
intake.** The
bounded branch of `astrowoof-external-authority-v2` commits and dispatches in
one process, so its raw capability never crosses the API/SBE boundary. It
emits a typed bounded result distinct from ordinary v2.

The earlier local `0.4.71` wheel was Gate C-only and is superseded. The first
unpublished `0.4.72` candidate (`dadd3969…99cb29b`) is also superseded after
the broad suite exposed an exact-route lifecycle regression. The replacement
uses the same unreleased distribution version from source `986e05ea`, with
`SOURCE_DATE_EPOCH=1791479232`, two clean canonical-LF archives, SHA-256
`298273523a05c7a72cdd5404ca1727ef3f03c5c922785a7c5ba4da6f2990c364`, and
1,442,607 bytes. Its two archive builds are byte-identical and contain no CRLF
packaged text members. The retained wheel is
`C:\tmp\sbe-0.4.72-regression-candidate\canonical-wheel-a\astrowoof_natal_authoring-0.4.72-py3-none-any.whl`.
The manifest-driven broad rerun from `986e05ea` passed: 1,267 tests, 62
expected skips, zero failures/errors, one worker, and 1,345.694 wall seconds.
Its receipt is `C:\tmp\sbe-0472-canonical-broad-suite-receipt.json`.
No release, provider call, deployment, or activation occurred.

The final two Gate C corrections are included: `checkpoint_published` is now
per invocation (false on exact replay), and the command envelope has a public
validator plus packaged closed JSON schema. Focused tests include altered
envelope refusal.

The new process-local capability is deliberately not written into the
workspace: a later process may reconcile durable identities but cannot turn a
persisted intent into a new provider create. Provider-free tests cover exact
intent replay, six-member fake dispatch, descriptor tamper, pre-intent
injected failure, and duplicate authorization refusal. Slice 3 minted the
immutable bounded `stable_facts.v3` / prompt-release `v3` pair bound to the
new `0.4.72` package descriptor; neither supersedes the historical `v1` or
`v2` records. The remaining gate is API's exact installed-wheel
admission/resume/replay against this replacement wheel; no release, provider
action, deployment, or activation is authorized.
