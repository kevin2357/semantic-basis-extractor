# Slice 9 - Installed Cross-Repository Acceptance and Handoff

Status: complete, installed Linux acceptance passed, and API consumer review
accepted. Release is recommended but remains separately authorized.

## Outcome

SBE now has a reproducible 0.4.0 review candidate, installed command boundary,
packaged typed interface, bounded consumer contracts, sanitized delivery example,
and explicit AGF/SPC pins. No tag, publication, provider operation, or spend
occurred.

The public command is `astrowoof-run-bounded-natal`. It creates or resumes a
snapshotted bounded workspace, exposes machine-readable public state, exits `3` at
authorization/budget/ambiguity boundaries, and uses SBE's shared lifecycle and
spend machinery. OpenAI Responses are resumable by durable provider ID. Batch is
rejected because a real bounded Batch adapter has not been implemented.

The final provider schema is deliberately editorial-only. OpenAI can return prose
and claim/summary correlation IDs, but SBE—not the provider—reattaches semantic
authority, evidence scopes, selected terms, subject view, and registry bytes. It
rejects missing, duplicate, and unknown identities before final validation.

## Evidence

- 274 repository tests passed in 149.848 seconds.
- Two builds using `SOURCE_DATE_EPOCH=1786665600` were byte-identical.
- Candidate: `astrowoof_natal_authoring-0.4.0-py3-none-any.whl`, 711,052 bytes,
  SHA-256 `4fb7a114ae4866475778d36b677d170499a5558e0f1a854aeb88616b9c6c8c84`.
- Wheel inventory: 78 entries, 38 packaged resources, no cache/bytecode entries,
  and `py.typed` present.
- Exact upstream pins are AGF 0.8.1
  (`860c48793318c82c986b32664cd0f3fe97c4b1e02fb1e489561bc395c8b5a3ed`)
  and SPC 0.11.0
  (`82290df44fe5697e87df2e27eb0aa4bab3b7954c66ce988efda0962964e1366d`).
- The final candidate passed installed Linux `pip check`, lifecycle/release smoke,
  full four-context fake delivery, complete and valid workspace inventory,
  quiescence inspection, and closed closeout in the qualified AGF/SPC image.
- The installed bounded run reached `DELIVERY_COMPLETE` with no provider or local
  continuation and no unresolved provider actions.
- Windows final-candidate bounded E2E is likewise pending because the temporary
  SPC environment lacked `jsonschema` and dependency-install authorization was
  unavailable.
- Provider operations: zero. Provider spend: `$0`.

## Review boundary

The API agent accepted all nine consumer-contract points and recommended release
after hygiene reconciliation. Artifact source is commit `946f6fd`; later release
records do not change the wheel bytes, and the immutable tag target will identify
the final evidence lock. No tag or publication occurred during this sprint gate.
