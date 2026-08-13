# Slice 2 Read-only Lifecycle Inspection

Status: complete, 2026-08-13

`astrowoof_natal_authoring.lifecycle.inspect_lifecycle()` projects one exact
semantic-closure workspace into the approved
`astrowoof.authoring_lifecycle_inspection.v0.1` contract.

The operation reads `run.json`, the declared workspace contract, the complete
workspace inventory, and the spend ledger. It does not write run state, public
state, spend documents, snapshots, locks, or inspection artifacts. Callers may
declare native exclusivity conditions, but SBE does not infer API lease validity.

The projection includes:

- the exact operator revision, snapshot-file SHA-256, logical root, inventory
  validity, observation time, and writer-race/exclusivity facts;
- deterministic presentation-only action inventory;
- exact immutable action binding and ledger state;
- durable provider operation identity and explicit provider identity, provider
  evidence, and consumption-evidence facts;
- action necessity, relationship, and provider-less denial eligibility/reason;
- typed local dependencies;
- separate deck, QA, assembly/lint/validation, delivery, publishability, provider
  continuation, and local continuation facts;
- machine-distinct success, review, budget, ambiguity, and nonterminal outcomes;
  and
- explicit typed quiescence.

`observed_at` is the only documented volatile field. Supplying an exact observation
time produces byte-stable equivalent projections for unchanged native evidence.

If snapshot validation fails, inspection still returns a typed fail-closed result:
inventory validity is false, quiescence is `unknown_review_required`, review reasons
identify the invalid snapshot, and no action is provider-less-denial eligible. It
does not repair, refresh, or bless the workspace.

Reported provider actions remain evidence but no longer count as outstanding
provider work. Prepared, authorized, submitting, identity-recorded, waiting, and
ambiguous actions remain necessary until native evidence advances them.

CLI packaging and the final installed-consumer interface remain Slice 6 scope.
