# API Agent Slice 7 Review and SBE Response

## Review disposition

The API review rejected the first Slice 7 installed qualification as too narrow.
Its contract fixtures were useful, but its runtime proof built request/grant objects
in memory, invoked the initial-wave coordinator directly, and treated a JSON reload
as fresh-worker restoration. It did not prove the supported workspace, lifecycle,
constrained continuation, or reconciliation boundaries.

The review required a provider-free installed-wheel qualification that:

- prepares a complete sanitized native workspace through SBE runtime code;
- reads lifecycle inspection v0.5 and the public authority request;
- stores API authority outside the native workspace;
- crosses actual fresh-process boundaries;
- invokes the constrained continuation with a scripted production transport;
- proves six durable identities and no seventh create on replay;
- invokes the real provider-reconciliation selection/entry point;
- obtains typed unjoinable-lineage refusal through lifecycle inspection; and
- exercises ordinary actions through the public snapshot-validating reader.

## SBE response

Implemented as requested. `astrowoof-external-authority-qa` now constructs a real
exact-interactive workspace containing six production-shaped pass archives. It
exports the embedded lifecycle request, persists the grant and six member documents
outside the workspace, and uses separate Python processes for constrained create,
retained replay, and reconciliation. Its scripted Responses transport records
exactly six POSTs and the SBE-selected bounded GET subset.

Independent snapshot-valid workspaces exercise the typed lineage refusal and
ordinary-action reader. Stable sanitized contract fixtures remain separate from the
temporary runtime workspace so their published hashes are reproducible.

The stronger test exposed one actual contract join defect: inspection v0.5 binds
the request to inspection `observed_at`, while the constrained executor previously
re-read a request using the native state timestamp. The reader now accepts the
supplied lifecycle observation only after exact equality of every safety-bearing
snapshot field; only the timestamp may differ. Exact and bounded constrained
execution use that checked observation, and changed snapshot identity fails as
`stale_observation` before provider I/O.

## Qualification evidence

- Combined authority/lineage/lifecycle/event gate: 80 passed, five optional schema
  skips on the lean host.
- Exact constrained execution: 11 passed.
- Bounded constrained fence regressions: 4 passed.
- Fresh installed Python 3.11 wheel command and public receipt validator: passed.
- Candidate wheel SHA-256:
  `32f6572ae26af19ebd687548a87dbd8bfc4ac8d1a81ee1408c1377440a52057b`.
- Provider/network calls: scripted only. Spend: USD 0.
- Retained Aster workspace accessed or mutated: no.

Status: ready for renewed API Slice 7 review; not committed or released.
