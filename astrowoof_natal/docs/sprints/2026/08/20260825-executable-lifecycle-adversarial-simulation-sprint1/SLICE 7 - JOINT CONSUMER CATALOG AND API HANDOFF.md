# Slice 7 — Joint Consumer Catalog and API Handoff

Status: SBE catalog implemented; paused for API fixture-by-fixture review and joined execution

## Public catalog

SBE packages a strict public catalog through:

```python
from astrowoof_natal_authoring import (
    read_adversarial_consumer_catalog,
    validate_adversarial_consumer_catalog,
)
```

Contract identity: `astrowoof.adversarial_consumer_catalog.v1`  
Current catalog SHA-256:
`eea70ce9fed3c1ee986454dbac8e71e5e39b266f895628cd8adb2e53e9eab01e`

The reader validates every packaged fixture's literal bytes against its frozen
SHA-256 before returning the catalog. Qualification-component entries bind public
SBE qualification contracts rather than pretending a static JSON file reproduces a
runtime route. API-owned entries explicitly require API fixtures and contain no
manufactured SBE evidence.

## Case inventory

SBE-owned:

- initial six-member topology;
- provider-pending 4+2 retrieval;
- post-fan-in local retry;
- ordinary v2 external authority;
- ambiguous provider submission;
- optional critic after delivery;
- single/batch providerless denial; and
- operator retirement.

Joint:

- Muffin review/no-action capacity release;
- not-due provider waiting;
- contradictory public evidence; and
- partial Batch usage with unknown distinct from zero.

API-owned:

- expired/lost lease replacement; and
- three-run bounded-capacity starvation.

## Required API behavior

The API must call the SBE public validator before consuming the catalog or a fixture.
It must not inspect `run.json`, private packet/prompt files, logs, provider IDs, or
temporary native workspaces to fill missing facts. Each case's assertion list is the
consumer gate; ownership determines which repository supplies the materializer and
oracle.

The current SBE artifact is a candidate on top of published `0.4.25`. API may build
and use it locally for review, but no production pin/deployment or paid QA is
authorized before Slice 8 release qualification and owner approval.

## SBE evidence

- 15 closed catalog cases.
- All packaged fixture hashes validated through the public reader.
- API-only cases contain no SBE artifact digest or implied native assertion.
- Provider/network calls: 0; spend: USD 0; retained QA access: 0.

