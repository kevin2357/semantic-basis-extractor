# SBE 0.4.9 API Consumer Handoff

After deploying the exact SBE 0.4.9 worker image, invoke this as a provider-free
Render QA one-off:

```console
astrowoof-deployed-qa
```

The command writes one closed
`astrowoof.deployed_qa_four_route_qualification.v1` receipt to stdout and exits
zero only when all assertions pass. It requires no credentials or network.

API should validate and retain the receipt as deployed-runtime QA evidence. It
must not use the receipt to advance a reading, release provider or spend authority,
publish delivery, infer native run state, or repair a workspace.

For direct Python use:

```python
from astrowoof_natal_authoring import (
    read_deployed_qa_schema,
    run_deployed_qa_qualification,
    validate_deployed_qa_receipt,
)
```

Detailed semantics are documented in
[Deployed Four-Route Qualification](../../docs/post_extraction_authoring/Deployed%20Four-Route%20Qualification.md).
