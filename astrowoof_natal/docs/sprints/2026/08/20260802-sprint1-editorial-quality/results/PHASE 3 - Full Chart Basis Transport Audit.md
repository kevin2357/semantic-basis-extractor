# Phase 3: Full-Chart Basis Transport Audit

## Executive conclusion

The current `FULL CHART BASIS.md` is semantically useful but inefficient as an
authoring transport. Across Ashley, Brandi, Bre, Ella, and Kevin it costs an
estimated 18,335–19,041 tokens. The complete projected-term registry accounts
for 55.7–58.5% of that total even though much of its nested metadata is not
needed for whole-dog synthesis.

A deterministic author-oriented prototype retained the complete selected and
unselected claim inventory, all recoverable projected objects, all recoverable
relationships, their source references, and a compact projected decoder while
reducing estimated tokens by 49.7–51.8%. This demonstrates that the present
representation can be made materially smaller and easier to scan without
discarding the semantic basis available to SBE.

The audit also found a real ownership boundary. SBE can reconstruct a useful
projected chart map, but it cannot reconstruct a guaranteed lossless canonical
natal chart. The recommended long-term contract is therefore hybrid:

1. Semantic Projection Core (SPC) owns a compact, projection-neutral canonical
   source-chart capsule in projected-artifact metadata.
2. SBE owns the compact author-facing projected interpretation derived from
   the projected graph, claim basis, and projected-term registry.
3. The authoring LLM receives both layers, clearly labeled, rather than either
   an original chart alone or the current structural dump alone.

No production handoff was changed during this audit. A controlled live A/B is
required before replacing the current basis.

## Experimental implementation checkpoint

The subsequent `compact-v1` implementation deliberately tightened the audit
prototype before live use. The measurement prototype selected one context per
object or relationship; production-candidate code preserves every distinct
general, handler, direct-to-dog, and hybrid projection available in retained
evidence. This is a stronger semantic contract and a less aggressive size
reduction.

The implemented author-facing Markdown reduces the five reference subjects by
35.8–39.0% rather than the prototype's 49.7–51.8%. Ella falls from 18,804 to
11,526 estimated basis tokens. Stable source references and dependencies remain
in a structured local sidecar rather than being repeated throughout Markdown.
The sidecar is excluded from authoring ZIPs and API input.

A matched no-service semantic-closure layout report for Ella measured:

- shared subject prefix: 19,416 → 12,138 estimated tokens (37.5% reduction);
- six-request aggregate input: 381,673 → 338,005 estimated tokens (11.4%
  reduction before cache-price effects);
- identical pass assignments and response schemas between treatments;
- one stable subject-prefix hash within each six-pass treatment.

The experimental path is available as
`--full-chart-basis-format compact-v1`; `legacy` remains the default. All 84
tests and matched six-ZIP smoke builds passed. These figures supersede the
prototype's token estimate for planning the live A/B, while the prototype
remains useful evidence about the maximum compression available if context
semantics are intentionally narrowed later.

## Question examined

The audit began with a practical concern: agents can use the current full-chart
basis, but a human author would not naturally choose to receive chart material
in that form. The review asked:

- How expensive is the current representation?
- Which portions carry authoring value?
- Can SBE produce a cleaner chart map from the evidence already retained?
- What is lost in downstream reconstruction?
- If upstream metadata is warranted, should it represent the original natal
  chart, the projected chart, or both?

## Current transport

`render_full_chart_basis()` currently emits three large sections:

1. **Selected Chart Material** — all 50 selected claim summaries plus type,
   priority, source references, and dependencies.
2. **Additional Chart Material** — every unselected candidate retained for
   whole-chart understanding.
3. **Complete Projected-Term Registry** — a recursive Markdown rendering of
   the artifact registry, excluding template keys.

This is better understood as a semantic claim inventory plus a decoder dump
than as a chart. Individual story packets already receive richer local evidence
and only their relevant projected terms, so the whole-chart file primarily
serves characterization, summary synthesis, and deck-level continuity.

## Method

The audit used the preserved selected-authoring packets for five subjects:
Ashley, Brandi, Bre, Ella, and Kevin. For each subject it:

1. regenerated the production `FULL CHART BASIS.md`;
2. measured bytes, lines, and a conservative four-bytes-per-token estimate;
3. traversed every selected and unselected claim's projected evidence;
4. joined projected relationship endpoints to projected object records;
5. constructed a deterministic chart map containing recoverable source and
   projected semantics;
6. rendered a compact author-facing prototype;
7. retained explicit reconstruction limits rather than presenting inferred
   data as canonical truth.

The reproducible audit script and generated fixtures are under
`work/phase-003-full-chart-basis-audit/`.

## Measurements

| Subject | Current est. tokens | Registry share | Prototype est. tokens | Reduction | Objects | Relationships |
|---|---:|---:|---:|---:|---:|---:|
| Ashley | 18,704 | 57.0% | 9,185 | 50.9% | 17 | 37 |
| Brandi | 19,041 | 57.2% | 9,388 | 50.7% | 17 | 43 |
| Bre | 18,598 | 58.5% | 8,958 | 51.8% | 17 | 37 |
| Ella | 18,804 | 57.9% | 9,123 | 51.5% | 17 | 37 |
| Kevin | 18,335 | 55.7% | 9,219 | 49.7% | 17 | 41 |

The current transport is strikingly stable at roughly 18–19k estimated tokens
per dog. Selected and additional claims together cost roughly 7.7–8.1k. The
registry alone costs roughly 10.2–10.9k.

All 47–50 registry terms were referenced somewhere in each complete claim
basis. Whole-file filtering to “referenced terms only” therefore does not solve
the problem. The useful reduction comes from flattening the chart map and
preserving the author-relevant meaning of each term without recursively
serializing all registry metadata.

## What SBE can recover reliably

Across all five packets the prototype recovered 17 chart objects. A typical
object line can carry:

- canonical object or angle name;
- canonical sign;
- canonical house when present;
- projected subsystem/operator;
- projected mode;
- projected Doghouse/domain;
- stable source reference.

For relationships it can carry:

- canonical aspect type;
- orb;
- canonical endpoints when the projected IDs can be joined to object evidence;
- projected source and target subsystems;
- projected relationship operator;
- projected interaction mode;
- stable source relationship reference.

This is far more legible than asking the author to infer the same structure
from repeated evidence blocks and a thousand-line registry.

## What downstream reconstruction cannot guarantee

Three limitations prevent the SBE reconstruction from being treated as the
canonical natal chart:

1. **Exact positions are absent.** The retained projected object evidence
   preserves sign and house but not canonical longitude or degree.
2. **Relationship endpoints require a join.** The relationship record contains
   projected endpoint IDs. Canonical names are recovered only when matching
   object records survive in the available material.
3. **Completeness is unknowable downstream.** SBE can report everything present
   in the projected artifacts and candidate pool, but absence cannot be
   distinguished from an upstream omission or filtering decision.

The prototype labels itself a deterministic downstream reconstruction for this
reason. It must not silently acquire canonical authority.

## Original chart, projected chart, or both?

### Original chart alone

A compact canonical natal summary would give exact placements, angles, points,
aspects, orbs, source identity, and completeness. That is valuable for
traceability and orthodox astrological orientation, but it does not contain the
canine semantic interpretation that makes AstroWoof authoring possible. Giving
the LLM only the original chart would force it to recreate or bypass the
projection.

### Projected chart alone

A compact projected chart map gives the author the meaning it actually needs:
canine subsystems, modes, Doghouses, and interaction dynamics. It is the most
direct input for characterization and summary writing. On its own, however, it
can obscure canonical provenance and cannot repair source details discarded
before SBE.

### Hybrid representation

The two layers solve different problems and should remain distinct:

- the **canonical capsule** answers “what was calculated?”;
- the **projected authoring map** answers “what does this projected semantic
  system say about this dog?”

This is not redundant duplication. It is a provenance layer paired with an
interpretation layer.

## Recommended ownership and schema direction

If SPC adds only one upstream feature, it should add a projection-neutral
`source_chart_summary` to projected-artifact metadata. A conceptual shape is:

```json
{
  "source_chart_summary": {
    "schema_version": "...",
    "source_identity": {
      "chart_id": "...",
      "generator_version": "...",
      "source_hash": "..."
    },
    "objects": [
      {
        "id": "Sun",
        "longitude": 153.0,
        "sign": "Virgo",
        "house": 10
      }
    ],
    "aspects": [
      {
        "source_id": "Sun",
        "target_id": "Jupiter",
        "aspect": "conjunction",
        "orb": 0.126
      }
    ]
  }
}
```

The exact schema belongs in an SPC design pass. It should include relevant
angles, nodes, calculated points, cusp/house-system metadata where applicable,
and explicit provenance. It should be stable across projection domains and
must not contain AstroWoof editorial prose.

SBE should then construct a separate compact authoring view, conceptually:

```text
Canonical chart capsule
  exact source placements, geometry, provenance

Projected chart map
  canonical ref -> projected subsystem / mode / Doghouse
  canonical relationship ref -> projected dynamic / interaction mode

Whole-chart semantic basis
  selected claims
  additional claims
  concise projected decoder
```

SPC may eventually expose a generic compact projected-graph summary if other
consumers need one. Even then, SBE should continue to own selection,
author-oriented ordering, Markdown rendering, and any AstroWoof-specific
explanation. SPC should not author a whole-dog portrait or summary-card thesis.

## Evidence traceability

Compression must not mean removing identity. The production candidate should
retain machine-stable references beside compact lines even if the prose view
de-emphasizes them. An author or validator must be able to trace:

- a recovered object to its canonical object reference and projected record;
- a relationship to its source relationship reference and projected edge;
- a semantic claim to its claim ID and dependencies;
- a decoder entry to its registry key.

The prototype demonstrates the readable form but is not yet the final schema.
The production implementation should preferably build a structured compact
object first and render Markdown from it, avoiding a second lossy prose-only
artifact.

## Whole-dog comprehension

The prototype improves scanability in several concrete ways:

- the chart's object pattern is visible in seventeen lines;
- tight aspects and repeated systems can be inspected as a relationship list;
- canonical and canine vocabularies appear side by side;
- selected and additional claims remain available for higher-order motifs;
- projected definitions are concise enough to consult without dominating the
  document.

These are strong reasons to expect equal or better comprehension, but this
audit does not claim that token count and human readability prove LLM outcome
quality. The existing representation has already produced usable profiles.
Replacement requires a live controlled comparison of whole-dog portrait and
summary quality, grounding, and omission behavior.

## Production recommendation

Proceed in two bounded stages:

1. **SBE prototype and A/B:** implement the compact structured authoring map
   behind an experimental flag, generate matched current/compact pass-6 inputs,
   and compare portraits and four summaries on at least Ella plus one other
   subject. Measure actual API cached/uncached tokens and output quality.
2. **SPC contract design:** separately specify and add the canonical
   `source_chart_summary`; then let SBE consume it when present while preserving
   a clearly labeled reconstruction fallback for older artifacts.

Do not block the SBE experiment on SPC. The present evidence is sufficient to
test whether compact projected transport improves authoring. Do not declare
the downstream reconstruction canonical or remove the current path until the
live comparison passes.

## Acceptance criteria for a future replacement

- materially lower actual input tokens;
- all selected and additional claims remain available to summary authoring;
- every projected object and relationship present in the current basis remains
  represented or intentionally summarized;
- evidence/source references remain traceable;
- whole-dog portraits preserve the same major tensions and motifs;
- four summaries remain distinct and fully grounded;
- no increase in unsupported canonical astrology claims;
- deterministic tests cover old artifacts without upstream capsules and new
  artifacts with them;
- the current rendering remains available until migration fixtures pass.

## Audit artifacts

The work directory contains:

- `audit_full_chart_basis.py`;
- `audit-metrics.json`;
- five regenerated current bases;
- five compact prototypes;
- five structured reconstructed chart maps.

These are research artifacts, not production contracts.
