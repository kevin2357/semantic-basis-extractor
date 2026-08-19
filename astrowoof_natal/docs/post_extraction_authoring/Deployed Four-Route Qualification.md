# Deployed Four-Route Qualification

SBE exposes a provider-free installed-wheel QA operation for deployment gates:

```console
astrowoof-deployed-qa
```

The command needs no arguments, credentials, network, provider endpoint, native
run workspace, or spend authorization. It writes its closed JSON receipt to
standard output and returns zero only when all assertions pass. A Render QA
one-off may persist that stdout as deployment evidence.

Use `--output PATH` to write the receipt directly or `--schema` to print its
packaged JSON Schema. Python consumers may use:

```python
from astrowoof_natal_authoring import (
    read_deployed_qa_schema,
    run_deployed_qa_qualification,
    validate_deployed_qa_receipt,
)
```

The receipt covers exact interactive, exact Batch, bounded interactive, and
bounded Batch. Interactive cells prove six concurrent scripted creates, serialized
durability, detach, and durable-byte reload/fan-in. Batch cells prove one scripted
provider operation/authority carrying six logical members and a restored round.
The Batch cells invoke SBE's native exact Batch authoring path and native bounded
Batch authoring cycle; they do not construct substitute qualification-only round
records. Shared assertions prove bounded final-QA review precedence and native duplicate
claim refusal before provider work.

`provider_operation_count: 0` refers to real external provider operations. The
receipt separately reports scripted callback counts used by qualification.

This command is qualification-only. Its receipt is not production execution
evidence, native run state, lifecycle inspection, provider custody, spend
settlement, API reservation authority, or publication authority. API must never
use it to advance or repair an individual reading.
