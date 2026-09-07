# Slice 3 — successful control and blinded packet preparation

## Successful-delivery control

The API-provided generation-10 coordinate was consumed under its exact bounded
authorization: one HEAD and one conditional GET. The operation ledger records
one of each and zero listing, write, delete, provider, execution, recovery, or
mutation operations.

The downloaded archive validated before extraction:

- archive SHA-256:
  `f3b26af43b10eb8e9054a1e28433b824b0fd3612486bd0657544b02122af53ca`;
- inventory SHA-256:
  `aab540b3f5e3875e5e305b2b966f3f2c4b5fdcf101be56c81d1e26c88c3649f4`;
- 935 archive members and 911 snapshot-governed workspace members;
- native result `nres_cc899e12b3d7af0a7f2acf23` with declared digest
  `cc899e12b3d7af0a7f2acf2325fd4ab92fcbfc3ee0c72d56c732a7cc8d7eee57`;
- publication receipt `nreceipt_9991a80bdb6ac564701d1706` with declared
  digest `9991a80bdb6ac564701d1706e9f4c73f55f28d09605cb0862be68602fa41e2d7`;
- final native outcome `delivery_complete`; and
- final validation and lint both passing.

This is not a trivial no-polish control. It contains two materialized, accepted
polish transitions. Production assembly equals the reconstructed pre-polish
deck, every sparse edit reapplies exactly, and the final selected deck reaches
ordinary successful delivery.

## Five-run replay

The common replay tool now covers the four review-required/failed lineages and
the successful control. Two executions were byte-identical:

- private file SHA-256:
  `0c003a67229dec4987e08a212d910a1a407fb7456e0eac55f4ba9a25ec5902fb`;
- canonical receipt SHA-256:
  `e30e118f989c78a3a08ed23cf01a5e46fab68ec67088bdbefc5732f34a2b3bb2`;
- cases: 5; materialized candidate transitions: 8.

The private replay remains outside the repository at
`.tmp-editorial-calibration-r2/private-lineage/five-run-polish-replay.json`.

## Blinded packet construction

Eight private reviewer packets were generated with stable evidence-derived IDs.
Reviewer-facing packets contain the before/after target values, prior and
candidate findings, whole-deck acceptance projection, structural validation,
and binding hashes. Run names, subject identities, historical adoption state,
and terminal outcome live only in a separate answer key.

Two variants were measured using canonical UTF-8 JSON:

| Variant | Minimum bytes | Maximum bytes | Purpose |
|---|---:|---:|---|
| finding-local | 6,917 | 74,254 | bounded review of the affected fields and findings |
| complete selected deck | 1,016,507 | 1,081,094 | private whole-deck calibration context |

The complete deck adds between 998,441 and 1,025,277 bytes per packet. This is a
strong practical reason not to make complete-deck text the default routine
Better Stack event. Finding-local evidence is small enough for a bounded routine
packet, while full decks remain useful private research artifacts under a
separate retention decision.

The smallest accepted-control transition is 6,917 bytes finding-local. It proves
that an accepted control does not require inventing a rejected finding merely to
fit the packet schema: a transition can carry prior/candidate acceptance,
validation, exact edited fields, and provenance even when residual findings are
empty.

Private packet root:
`.tmp-editorial-calibration-r2/private-review-packets/`.

## Remaining Slice 3 gate

Packet construction and size evidence are complete. Slice 3 is not complete
until the blinded packets receive:

1. one owner/human judgment; and
2. one independent editorial-model judgment using the frozen rubric.

No routine packet schema, byte ceiling, runtime hook, Better Stack publication,
or editorial-policy change is authorized by this preparation step.
