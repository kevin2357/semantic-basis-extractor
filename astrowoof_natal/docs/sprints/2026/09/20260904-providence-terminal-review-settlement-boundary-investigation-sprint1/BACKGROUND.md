# Providence terminal-review settlement-boundary investigation

## Purpose

Determine the exact native terminal-review custody result emitted for
**Providence Poptart**, why it was selected after a fully reconciled
six-action initial wave plus one creative retry, and whether it is a correct
SBE result that API has not implemented or an SBE contract defect.

This is bounded read-only investigation only. No listing, writes, provider
access, reconciliation, resume, repair, retained-run mutation, deployment, or
release is authorized by this scaffold.

## Frozen coordinates

- API run: `5dda2560-1d6c-4a8c-b393-363da3c81212`
- API reading: `ff37a4c5-d905-4b49-9931-df28ca024679`
- Native run: `d7017c0ce261b1536ed005e45b2f94ccde056d83c62e789c7f484d361840612f`
- SBE: `0.4.47`; SPC: `0.11.1`
- Exact failure time: `2026-09-04T20:32:19Z`
- Worker error relayed by API:
  `SBE terminal review custody requires an unsupported settlement boundary`

Trace sequence established by API/worker evidence:

1. Six initial provider actions completed and were reconciled.
2. One creative retry completed and was reconciled.
3. Native local resume reported `terminal_closed` with
   `provider_local_dependency_count=0`.
4. The terminal-publication ingress rejected the result as a non-retryable
   provider-lifecycle contract error; its lease was released.

## Required answers

1. Supply/identify the exact sealed terminal-review result, receipt, action
   inventory, `custody_finality`, reconciliation IDs, providerless-denial IDs,
   and relevant terminal projection fields.
2. Derive the expected finality from the native action custody facts and
   explain every non-final action, if any.
3. State whether the result is valid SBE v0.2 terminal-review evidence.
4. If API needs a new disposition, specify its exact no-I/O semantics and
   constraints. Do not propose inferring or fabricating a settlement.

## Diagnostic log export

Unfiltered Render SBE worker logs, local copies only:

- `C:\tmp\providence-terminal-custody-20260904\sbe-worker-01.log`
  (19:38–19:53 UTC)
- `C:\tmp\providence-terminal-custody-20260904\sbe-worker-02.log`
  (19:53–20:08 UTC)
- `C:\tmp\providence-terminal-custody-20260904\sbe-worker-03.log`
  (20:08–20:23 UTC)
- `C:\tmp\providence-terminal-custody-20260904\sbe-worker-04.log`
  (20:23–20:38 UTC; primary evidence window)

## API boundary context

API currently recognizes terminal-review `final` and the retained-provider
`provider_reconciliation_required` form. It rejects any other finality rather
than assuming a settlement action. The investigation must determine whether
that strict refusal correctly caught invalid native evidence or reveals a
missing general disposition.
