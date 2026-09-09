# API review — Slice 3D native-result version provenance

## Decision

**Approved.** The correction is provenance-only and matches the native
publication surface:

- ordinary accepted delivery: `astrowoof.native_execution_result.v0.1`;
- ordinary interactive editorial closeout:
  `astrowoof.native_execution_result.v0.2`; and
- both branches: `astrowoof.native_publication_receipt.v0.1`.

SBE may implement the two explicit, exact-reader runtime branches.

## Required branch fence

The builder must first use the explicit-ID reader and validate the returned
result/receipt pair, then dispatch on the validated result schema and outcome.
Admit only the exact v0.1 delivery and v0.2 ordinary editorial-review branches
described above. A reader-recognized v0.3 zero-action terminal result—or any
other version/outcome/receipt pairing—must return a typed ineligible or
unsupported result with no partial packet. Reader support is not packet
eligibility.

## Evidence accepted

- The packet already carries explicit result and receipt schema identities, so
  this corrects fixture truth without widening packet structure or version
  inference.
- The accepted fixture now states v0.1; the editorial-closeout fixture states
  v0.2; both state the canonical receipt v0.1 identity.
- I independently reran the focused contract suite in the supported source
  layout: **23 passed, 1 expected optional `jsonschema` skip**. The scoped
  fixture diff hygiene check is clean.

## Retained boundaries

No latest-result discovery, workspace mutation, provider/storage/API/database/
network work, lifecycle/custody/spend/retry change, transport, release, or
deployment is authorized. The two branches remain a read-only construction path
whose failure cannot alter the terminal run.
