# AstroWoof LLM Handoff Bundle

This bundle contains reusable static instructions plus one subject-specific request packet.

## Run order

1. Read `manifest.json`.
2. Read every file under `static/`.
3. Read `request/bre.selection-qa.json`.
4. Read `request/bre.selected-authoring-packet.json`.
5. Follow `static/Proposed LLM Handoff Prompt.md`.
6. Produce `natal.bre.cards.json`.

The selected packet contains exactly fifty dependency-closed claims. Do not add, remove, reorder, or reselect claims.

Only prose fields described in the editing-permissions document may be changed.
