# Slice 5 — packaged consumer qualification

## Public surface

The installed package now exposes:

```text
astrowoof-final-qa-mixed-custody-qa
```

It emits the closed receipt
`astrowoof.final_qa_mixed_custody_qualification.v1`. The command is
qualification-only: it accepts no production workspace, provider credential,
authority, or subject input.

## Qualified paths

The command exercises three real public boundaries:

1. ordinary-v2 polish dispatch from a final-QA warning, proving durable custody
   publishes nonterminal reconciliation truth;
2. a post-intent terminal contradiction, proving typed v4/v3 refusal before
   payload resolution or provider call-entry; and
3. the established terminal-review qualification, proving a legitimate sealed
   v0.2 result/receipt and its custody-only successors remain immutable.

The third path caught and closed an adjacent continuity regression. Once a v0.2
review result is sealed, later reconciliation may retrieve and settle its
already-durable provider custody, but it must not feed that response back into
authoring or treat an unused providerless authorization as permission to reopen
the run. The reconciliation coordinator now recognizes the strictly validated
sealed review predecessor and preserves its review posture while publishing the
custody-only successor.

## Evidence

- Source focused matrix: 131 passed, 6 expected optional-schema skips.
- Candidate installed wheel SHA-256:
  `6690df42a4d35c99b93bb4118ed62f1f2dad56c9c07f05209f4439bb2ebc0fa6`.
- Qualification receipt SHA-256:
  `99ef5eccde34a370fb918d5cb6361244131b44e007029293c229ae4878704adf`.
- Three qualification runs produced the same receipt digest.
- Installed `pip check`: pass.
- Installed Draft 2020-12 schema plus Python semantic validation: pass.
- Installed existing `astrowoof-terminal-review-qa`: pass.
- External network calls: 0.
- Real provider creates/retrievals: 0.
- Provider spend: 0.
- Retained Glimmer workspace access/mutation: 0.

The installed wheel still identifies as already-published 0.4.34. It is only a
Slice 5 packaging witness. A separately approved release must freeze a fresh
version before expensive release tests and rebuild from committed source.

## Gate

Paused at Voof-paws 6 before release preparation.
