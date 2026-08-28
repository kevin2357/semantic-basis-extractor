# Slice 5 — Installed Terminal Review Qualification and API Handoff

## Status

Implementation and isolated-wheel qualification complete. API fixture/consumer
review is pending before broad release preparation.

## Supported consumer surface

The installed wheel exports:

- `run_terminal_review_qualification()`;
- `validate_terminal_review_qualification()`;
- `read_terminal_review_qualification_schema()`; and
- `astrowoof-terminal-review-qa`.

The command accepts no run workspace, provider credential, authority document, or
production input. It constructs a private sanitized workspace, uses a scripted GET
transport, deletes the workspace on return, and emits the closed
`astrowoof.terminal_review_qualification.v1` receipt.

## What the receipt proves

The installed public path proves that an exact-interactive run:

1. publishes a validated v0.2 review result, canonical v0.1 publication receipt,
   and invocation-bound terminal command-result envelope before exit 2;
2. preserves separate reported, provider-reconciliation-only, and
   providerless-denial-only action dispositions;
3. forbids new provider creation after the editorial review decision;
4. reconciles the exact durable provider identity using one scripted GET;
5. denies the exact unused authorized action through the existing public denial
   operation;
6. reaches terminal closeout with no provider or local continuation;
7. preserves the original v0.2 review result bytes while publishing a contiguous
   custody-only successor; and
8. keeps historical v0.1 evidence readable without allowing it to masquerade as
   the richer v0.2 contract.

The receipt intentionally carries stable assertions and action identities, not
temporary workspace paths or minted result/receipt identifiers. This makes it
reproducible across fresh workspaces while the qualification internally validates
all exact result, receipt, invocation, snapshot, and journal joins.

## API ingestion order

For a production invocation, API should ingest and validate the command-result
envelope against the referenced result and receipt before interpreting process
exit 2. `latest` discovery is diagnostic only and is not invocation correlation.

The v0.2 result's ordered action dispositions then drive separate actions:

- `terminally_accounted`: ingest immutable evidence; no provider custody remains;
- `provider_reconciliation_only`: retain custody and invoke only SBE's supported
  run-level reconciliation command when SBE says it is due;
- `providerless_denial_only`: retain API authority until the supported denial
  result proves denial; and
- ambiguity or contradiction: retain for review and perform no provider create.

Reconciliation or denial creates successor native evidence. It never mutates the
original editorial review receipt, never reopens authoring, and never changes the
historical fact that the invocation exited review-required.

## Qualification identities

- Candidate version: `0.4.28` (unreleased working candidate).
- Candidate wheel SHA-256:
  `c71dcc6ed6ba9d5af7defb1125f3515ff9fa95729f7c29cf0ba6086d142eacd2`.
- Qualification receipt SHA-256:
  `6289962655c36e4c2cab5828c30499a75155094c0437898c7f68fdf4e0afeb6d`.
- External provider/network calls: 0.
- Provider POST/create/retry: 0.
- Scripted local retrieval GETs: 1.
- Spend: USD 0.
- Retained Pippin/Duchess access or mutation: 0.

These candidate identities are review evidence, not final release identities.
Slice 6 must rebuild from committed source and publish fresh final hashes.
