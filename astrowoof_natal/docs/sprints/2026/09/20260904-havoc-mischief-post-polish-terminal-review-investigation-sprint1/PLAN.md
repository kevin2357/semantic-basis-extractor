# Plan

## Slice 0 — Freeze and classify the visible terminal timeline — complete

Read the supplied report/log artifacts, map all initial and polish action
boundaries, and produce one compact timeline per run. Record the exact known
terminal claim and the evidence ceiling.

Finding: Havoc's supplied trace independently shows the first polish result
joining the exact optional-stage attempt, followed by `FINAL_QA_FAILED` and a
validation exit of 1 (with lint exit 0). It does not expose the individual
validation issue codes. Mischief's supplied filtered/cohort trace ends while
initial provider custody remains live; it contains no polish/adoption or final
validation record. The API-provided terminal claim remains the current
authority for Mischief, but cannot be independently explained from this trace
export. Neither trace supports a provider, transport, or custody conclusion.

## Slice 1 — Bounded final-artifact inspection — complete

Request exact API-issued coordinates for each final accepted checkpoint plus
the named validation/acceptance artifacts, then inspect only those objects
read-only. Compare status, issue codes, advisory codes, report exit behavior,
and polish input/output identity. In particular, use the authoritative final
artifact to fill the known issue-code gap for Havoc and the absent timeline
segment for Mischief; do not infer either from the log window.

Finding: both pinned archives and signed inventories verified. Every initial
authoring acceptance record is an `accept` with no editorial or advisory code;
both post-polish lint reports pass with no warnings; and both post-polish
validation reports fail with the identical one-item deterministic category
`theme_group_cardinality`. The error is the obsolete three-or-four theme-group
requirement with observed count zero. This is a shared dormant-feature
validation policy, not an optional-stage adoption, provider, custody, or
terminal-projection defect.

## Slice 2 — Product and contract conclusion — complete

The evidence supports a narrowly scoped removal of theme-group cardinality and
balance checks from the final polish validator and its packaged handoff bundle.
The dormant feature fields may remain tolerated, but no retained or new deck
should be rejected because theme-group data is absent, incomplete, or
imbalanced. Confirm that product decision and the intended compatibility scope
with API before opening an implementation/release follow-up. No provider or
live-run recovery is implied by this sprint.

## Slice 3 — Remove the final-validator dormant feature — complete

Remove theme-group registry, member, cardinality, balance, and polish-edit
enforcement from the actual `astrowoof_natal_authoring.validation` source that
is copied into each handoff bundle. Retain `--allow-theme-group-edits` only as
a deprecated parser-compatible no-op. Prove missing, malformed, and legacy
theme representations no longer influence validation, while live context-filter
and ordinary editorial constraints still fail normally.

## Slice 4 — Fresh packaged-boundary qualification — complete, release preparation

Build a fresh handoff bundle from the changed source and invoke its copied
validator, rather than importing the source validator directly. Qualify both a
theme-free otherwise-valid deck and a deck with a genuine non-theme validation
failure. Confirm no provider, API, R2, or retained-workspace access. Pause for
release scope review before versioning or publication.

Release-review correction: `--allow-theme-group-edits` remains accepted as a
deprecated no-op in both authoring and polish invocations. It no longer trips
the authoring-only guard reserved for live context-filter and summary edits.

Release target: `astrowoof-natal-authoring 0.4.44`. The gate is intentionally
lean: the source and copied-validator qualification are package-local, with a
fresh wheel build, isolated install, and the same copied-validator exercise
required before publication.
