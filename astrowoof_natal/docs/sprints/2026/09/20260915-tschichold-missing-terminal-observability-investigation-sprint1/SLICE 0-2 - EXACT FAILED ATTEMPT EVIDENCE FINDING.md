# Slice 0–2 — Exact Failed-Attempt Evidence Finding

## Finding

Tschichold's missing Better Stack packet is not a terminal handoff, API
authority, transport, or repository-delivery defect. The observer selected the
exact terminal-review result and entered SBE capture, then failed closed while
collecting initial-pass evidence.

The exact live and replayed failure is:

```text
ValueError: Pass attempt evidence is incomplete
editorial_review_runtime.py:428
phase=pre_assembly_evidence_collection
```

## Retained-workspace proof

The owner-authorized checkpoint read matched its pinned byte count and archive
digest. Its pass-3 history is valid:

1. Attempt 1 reached `ATTEMPT_ERROR` because the provider-authored workspace
   omitted one required field.
2. That attempt retains `openai-authored-fields.json`, but correctly has no
   `authoring-pass-acceptance.json`; acceptance QA never ran.
3. Attempt 2 was reconciled, evaluated, and accepted. It retains both files.

The runtime collector currently requires both artifacts from every recorded
pass attempt. Tschichold is therefore refused before packet assembly. This
explains why no editorial packet or longitudinal artifact POST exists.

## Why no patch is proposed

Skipping attempt 1 would erase a paid, failed attempt and make attempt 2 appear
to be initial materialization despite its creative-retry identity. Including
attempt 1 faithfully would require the editorial lineage contract to represent
a pre-QA failed attempt without a QA-report digest. That is a semantic contract
decision, not a harmless missing-file tolerance.

Editorial observability delivery is explicitly best-effort. With eleven of the
twelve post-release runs publishing successfully, the owner chose to retain the
current fail-closed behavior rather than broaden the lineage/checkpoint seam for
this uncommon but valid workspace history.

## Closure

- No SBE or API implementation change.
- No schema, fixture, or Alloy-model change.
- No package or deployment work.
- No retry or mutation of Tschichold.
- Preserve this witness as a known limitation if future product requirements
  call for complete failed-attempt longitudinal history.
