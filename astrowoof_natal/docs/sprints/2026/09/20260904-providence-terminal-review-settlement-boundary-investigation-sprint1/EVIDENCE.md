# Evidence

## Current status

Slices 0–2 are complete and Voof-paws 3 passed. The public architectural gap and Providence's exact
sealed artifact are both proven. The separately authorized generation-12 read
validated the complete v0.2 result, canonical v0.1 receipt, eight-action ledger
projection, archive inventory, snapshot, checkpoint basis, and journal range.
The result correctly requires denial settlement for exactly one providerless
prepared polish action. A packaged provider-free qualification now proves the
exact precursor/denial/final-successor chain and refusal/replay fences.
Candidate `0.4.48` is frozen before release-bound testing. Slice 3 installed-
wheel and release preparation is active; runtime changes and live settlement
remain unapproved.

## Inputs used

- Four owner-supplied local SBE worker-log exports under
  `C:\tmp\providence-terminal-custody-20260904`.
- Released SBE `0.4.47` terminal-review contracts and validators.
- Current API terminal reader, transition validator, disposition mapper, and
  worker routing source.
- API Sprint 67's previously frozen retained-custody disposition table.
- API pre-Slice 0 review in this sprint.
- API generation-12 coordinate packet, SHA sidecar, and handoff note.
- One exact conditional R2 read of the frozen generation-12 checkpoint.
- Released/current SBE v0.2 result, v0.1 receipt, checkpoint-basis, journal,
  and terminal-action-disposition validators/builders.
- New providerless-denial qualification v1/v2 schemas, public reader/validator,
  CLI, packaged fixture, and focused regressions.

## Core result

Providence emitted an invocation-bound v0.1 command envelope referring to a
sealed v0.2 review result whose aggregate finality was
`providerless_denial_required`. The trace describes seven reported actions and
one providerless prepared polish action, which is exactly the public shape that
derives that finality. API validates the five-value finality contract but its
later disposition mapper implements only final closeout and retained provider
reconciliation.

The retained checkpoint now proves the exact result is valid. Seven ordered
actions are terminally accounted; only `paid_f5a73dc0325db8a8aedafe05` is
providerless-denial-only. The denial inventory contains exactly that action,
the reconciliation inventory is empty, and provider create is forbidden. This
certifies the missing API settlement boundary; it does not authorize settlement
of Providence.

## Safety receipt

- R2/storage operations: 1 HEAD, 1 conditional GET, 0 list/write/delete
- Provider create/retrieval/transport operations: 0
- Retained-run reads: 1 exact checkpoint; retained-run writes: 0
- API database reads or writes: 0
- Runtime changes: 0; additive schemas/package qualification surface: yes
- Deployments/releases: 0

## Next gate

Voof-paws 4 will ask API to review the exact installed `0.4.48` wheel,
qualification receipt, release-lock identity, and focused-gate evidence. No
live settlement or runtime implementation is authorized.

## Candidate 0.4.48 qualification

- Artifact-source commit: `96dd0ef539e1972ce694f75b60eac7bc3491caa8`
- Recorded `SOURCE_DATE_EPOCH`: `1788559932`
- Focused source matrix: 104 passed, 6 expected optional-schema skips
- Full/broad suite: deliberately not run; this is additive qualification-only
  package surface with no production lifecycle mutation, and API accepted the
  focused-gate scope at Voof-paws 3
- Two committed-source wheel builds: byte-identical
- Wheel: `astrowoof_natal_authoring-0.4.48-py3-none-any.whl`
- Wheel bytes: `1,209,061`
- Wheel SHA-256:
  `d1e84055183e2c45eb687aed61c247425008edec53e33f424c57cc89bf89a8e0`
- Wheel inventory: 262 members; canonical inventory SHA-256
  `1c089e706022ab302a9b9c0c13f6e15e81a9d246b335447eb3e17952c898d669`
- Expected qualification module, v1/v2 schemas, packaged fixture, and entry
  point present; no cache, bytecode, private, temporary, or Git members found
- Isolated install: SBE `0.4.48`, SPC `0.11.1`, imports from `site-packages`
- `pip check`: pass
- Installed v1 semantic output: deterministic, packaged-fixture exact match,
  receipt SHA-256
  `bc163221266b024296b6faf49f5669f50fba5831c19d64175ace09e9d0554c5e`
- Installed v2 outputs: strict validation pass; identity-rich receipts are
  invocation-specific while embedding the identical v1 semantic receipt
- Installed v1/v2 schema CLI and Python readers: exact match
- Generic installed `astrowoof-release-smoke --require-installed`: pass;
  receipt-file SHA-256
  `b166f60e376321a8830410a3686add4875d8d610b4cde9957630f01b8d3fc3d9`
- Provider create/retrieval/transport, spend, R2, retained QA, API mutation,
  deployment, recovery, and live settlement during qualification: zero
