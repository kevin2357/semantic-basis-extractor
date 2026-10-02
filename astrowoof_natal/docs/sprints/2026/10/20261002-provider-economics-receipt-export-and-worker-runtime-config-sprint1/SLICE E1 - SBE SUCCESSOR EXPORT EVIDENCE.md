# Slice E1 — SBE successor export evidence

## Decision

SBE's producer-side portion is complete provider-free. No new exporter or
remote publisher is required: the public reader already produces the exact
successor/replay contract that API's immutable economics tape consumes. The
new regression makes that terminal-snapshot behavior explicit for both
supported routes.

## Producer boundary

`read_provider_economics_export()` remains a strict local projection over one
sealed workspace snapshot. Its inputs are the exact workspace, canonical
observation time, and only API-persisted accepted predecessor revisions. Its
output is an `astrowoof.provider_economics_export.v1` object containing the
native run identity, route, snapshot SHA-256, canonical export SHA-256, and
only newly durable revisions.

It does not query API state, find a latest revision, write a workspace file,
post a receipt, or make a provider request. Those are essential custody
properties, not omitted functionality.

## New terminal-successor witness

`test_final_successor_and_exact_replay_are_available_for_both_routes` creates
one complete terminal (`DELIVERY_COMPLETE`) workspace for each supported route:

| Route | First read | Second read with first revision as predecessor |
| --- | --- | --- |
| `exact_natal` | one revision, number `1`, `delivery_complete`, publishable | zero revisions; same run and snapshot identity |
| `bounded_natal` | one revision, number `1`, `delivery_complete`, publishable | zero revisions; same run and snapshot identity |

Both first revisions retain `provider_usage_reported`; neither route converts
known usage into zero or manufactures a second transaction. The second output
is a valid, meaningful replay statement rather than an unavailable export.

Focused provider-free command:

```text
PYTHONPATH=astrowoof_natal/src python -m unittest \
  astrowoof_natal.tests.test_provider_economics_export \
  astrowoof_natal.tests.test_provider_economics_qa \
  astrowoof_natal.tests.test_test_suite_runner
```

Result: **23 passed**, provider operations: **0**.

## Diagnostics ownership correction

API's four safe observation classifications are correctly adapter-owned. Two
of them—sealed-publication join mismatch and immutable predecessor/ingress
failure—cannot be authoritatively classified by SBE because they concern API
custody and an already-sealed API publication. The SBE reader continues to
raise its strict local refusal without exposing an error envelope, exception
prose, paths, request data, workspace contents, or provider payloads. API
maps that bounded failure boundary to its privacy-safe operational event while
retaining nonfatal lifecycle behavior.

## Remaining joint Gate C cell

API should run its real immutable-ingress service against this public SBE
reader using a frozen complete workspace, persist the first returned successor,
and call the reader again with that persisted revision as predecessor. The
second result must be accepted as the explicit zero-revision replay. This is
the remaining economics/provenance gate; it needs no SBE protocol change or
release candidate unless the real consumer test reveals a concrete defect.
