# Postscript — 0.4.58 and 0.4.59 Alloy impact assessment

Date: 2026-09-10

## Decision

No Alloy model change or rerun is required for the SBE 0.4.58 and 0.4.59
pipeline corrections. Both changes preserve the editorial decision, deck, and
ownership relationships represented by `editorial_review_contract_v3.als`.

This is the retrospective impact assessment required by the Native Worker
Change Playbook. The assessment should have been recorded in each sprint before
implementation; executable tests alone were not a substitute for it.

## SBE 0.4.58 — first-polish authority selection

The Ada/Aldus correction changed lifecycle precedence before a polish decision
exists. When immutable state proves one exact eligible prepared first-polish
request, `FINAL_QA_FAILED` no longer prematurely forces terminal-review posture.
The request remains available for API authorization.

The correction did not alter:

- the number or order of editorial decisions;
- initial-pass, creative-retry, or polish predecessor relationships;
- candidate materialization or adoption;
- assembled-deck or sequential deck continuity;
- terminal selected/delivered deck relationships;
- action, binding, or provider Response ownership after execution; or
- finding, validation, projection, artifact, or packet ownership.

The Alloy model begins with materialized editorial decisions and their
relational consequences. It does not model the API authorization wait that
precedes an eligible polish decision. Extending the model solely to mirror that
lifecycle control state would add no check over the adopted packet relations.

Executable authority-selection, duplicate-attempt, lifecycle, terminal, and
providerless-denial regressions are therefore the faithful qualification
boundary for 0.4.58.

## SBE 0.4.59 — detached terminal command handoff

The Gutenberg/Hypatia correction changed how an already-determined terminal
review or delivery publication is carried to API:

- the same invocation now emits the exact command-result envelope derived from
  its newly published result and receipt; and
- detached terminal review uses native result v0.2 so the existing closed
  terminal-review command can validate its custody fields.

The correction did not change the editorial decision lineage, selected deck,
delivery equality, terminal outcome, or any modeled ownership relation. It
changed publication versioning, serialization, transport, and immutable
result/receipt handoff identity. Those concerns are explicitly outside the
Alloy model and are assigned by the playbook to contract, CLI/JSONL,
installed-wheel, and API-consumer qualification.

## Other same-day changes

The capture-status identity correction, packaged-fixture LF canonicalization,
relocated operator assessment, and operator-assessment diagnostics concern
concrete identity proofs, canonical bytes, packaging, read-only observation, or
logging. They do not change the relational editorial contract and likewise
have no Alloy impact.

## Model status

`editorial_review_contract_v3.als` and its existing recorded bounded evidence
remain unchanged. This assessment makes no new SAT/UNSAT claim and does not
reinterpret prior stopped checks as evidence.

Future work must reassess Alloy impact if it changes decision chronology,
attempt/retry/predecessor structure, assembly winners, materialization,
adoption, deck continuity, terminal selection/delivery, action/Response
ownership, finding/validation/projection ownership, artifact identity/absence,
or the non-authoritative API-observation boundary.
