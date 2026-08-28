# SBE 0.4.28 API Consumer Handoff

## Terminal result ingestion

For exact-interactive exit 2, ingest the emitted
`astrowoof.terminal_review_command_result.v0.1` first. Validate it against the
exact referenced `astrowoof.native_execution_result.v0.2` and canonical
`astrowoof.native_publication_receipt.v0.1` before interpreting the process exit.
Do not substitute a latest-discovered result.

Join every ordered action projection to API's immutable per-action record using
native run ID, action ID, complete binding digest, route, stage, provider mechanism,
and provider identity where present.

## Custody mapping

- `terminally_accounted`: ingest the terminal native evidence; no SBE provider
  custody remains for that action.
- `provider_reconciliation_only`: retain API custody/financial authority and
  invoke only SBE's run-level reconciliation command when SBE selects it as due.
- `providerless_denial_only`: retain API authority until the existing supported
  denial result proves the exact action was denied.
- ambiguity or contradiction: retain for review; never create replacement provider
  work.

`review_required` is the immutable editorial outcome. Reconciliation and denial
publish traceable successor evidence; they do not erase that result or reopen
authoring. API owns its transaction around ingestion, resource release, public
state, and any later retained-run recovery decision.

## Installed qualification

Run:

```text
astrowoof-terminal-review-qa --output terminal-review-receipt.json
```

Validate the receipt with
`validate_terminal_review_qualification()`. The released expected receipt digest
is:

```text
6289962655c36e4c2cab5828c30499a75155094c0437898c7f68fdf4e0afeb6d
```

The qualification accepts no production workspace, credential, authority document,
or provider endpoint. It performs one local scripted GET and zero POST/create/retry
operations.

## Candidate artifact

- Version: 0.4.28.
- Wheel: `astrowoof_natal_authoring-0.4.28-py3-none-any.whl`.
- Bytes: 1,077,913.
- SHA-256:
  `365ab0bc63a03e2c9c06638631b5e47c78ce494331f014741472a3e59fa58fb4`.
- Source commit: `25e0be9ce670b3643f47f6cdd0a71de7d00ad11e`.

These are the approved immutable release identities. Consumer deployment remains
separately gated on the API-side integration and qualification work.
