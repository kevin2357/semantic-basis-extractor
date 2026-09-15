# Slices 3–4 — Shared Digest Correction and Focused Qualification

## Implementation

Added `terminal_action_binding_sha256()` beside the existing canonical closed
terminal binding projection and used it at all v0.2 identity boundaries:

- terminal action-disposition production;
- terminal result/API-action validation;
- editorial capture's initial-pass disposition membership; and
- editorial capture's optional-stage disposition membership.

Editorial packet decisions continue to carry SHA-256 of the complete ledger
binding. The change does not substitute the smaller terminal projection digest
into packet content, alter delivery capture, accept multiple digest domains, or
change the sealed projection.

## Regression coverage

The new manifest-registered
`test_terminal_review_capture_binding_join.py` uses realistic complete bindings
with the four live extra fields. It proves:

- no-polish and two-polish producer-generated v0.2 review captures succeed;
- packets, projections, and artifacts validate;
- provider-response artifact expectations derive from the fixture's action
  inventory;
- assembled-deck artifact expectations derive from its distinct deck digests;
- packet decisions retain complete-binding digests;
- every sealed projection-field mutation fails closed;
- missing, duplicate, wrong-action, and conflicting dispositions fail closed;
  and
- a changed non-contract `model` field does not redefine terminal identity.

The older reduced-binding review fixture was upgraded to a realistic
producer-generated disposition rather than weakening the shared helper.

## Qualification

- Python 3.12 focused editorial/terminal/manifest matrix: 82 passed.
- Python 3.11 focused runtime/terminal matrix: 36 passed, 4 expected skips.
- `git diff --check`: passed.
- New test module: present in `test_suite_manifest.json`.

## Exact retained-workspace confirmation

The corrected public capture was rerun offline against both previously
verified archives in network-disabled, read-only Python 3.11 containers at
their original logical roots.

| Witness | Branch | Decisions | Projections | Provider responses | Distinct decks | Artifacts | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| A | `editorial_review` | 7 | 9 | 7 | 2 | 9 | valid |
| B | `editorial_review` | 8 | 13 | 8 | 3 | 11 | valid |

This confirms the correction restores the packet, projections, and complete
inventory-derived longitudinal artifact bundle for both original failures.
No additional R2 operation or retained mutation occurred.

## Gate D

Slices 3–4 are complete and paused for joint review. No version bump, broad or
package qualification, release, deployment, or live witness has occurred.

