# Treatment of Angles (Expanded Design Notes)

## Purpose

This document proposes refinements to the Semantic Basis Extractor (SBE)
while preserving the existing architecture described in *Semantic Basis
Extractor Pipeline and Scoring Metrics*.

The review of the implementation changed an important conclusion: SBE is
already a portfolio optimizer with dependency closure and bundle-aware
scoring, not a simple ranking algorithm. The recommendations below
therefore fit naturally into the existing candidate-generation,
utility-vector, and optimization framework rather than replacing it.

## Existing strengths

The current design correctly separates:

-   exhaustive canonical graph
-   deterministic candidate generation
-   portfolio optimization
-   constrained LLM authoring

This separation should remain unchanged.

## Graph vs. claim layer

The canonical graph should continue to preserve every angle relationship
for auditability.

However, the **claim layer** should reason at the level of angular
configurations rather than individual implied edges.

## Structural vs individualized geometry

Structural geometry:

-   ASC opposite DSC
-   MC opposite IC
-   ASC square MC
-   ASC square IC
-   DSC square MC
-   DSC square IC

These define the angular frame of every chart.

Individualized geometry:

-   Moon conjunct ASC
-   Sun conjunct IC
-   Jupiter trine ASC
-   Venus sextile ASC
-   Pluto conjunct DSC etc.

The latter should dominate scarce claim budget.

## Proposed candidate generator: Axis Relationship

Generate deterministic candidates such as:

Moon on ASC--DSC axis - conjunct ASC - opposite DSC

Sun on IC--MC axis - conjunct IC - opposite MC

Retain both underlying relationships as evidence while emitting one
higher-value candidate.

## Structural inevitability

Add a distinctiveness refinement reducing the marginal value of
relationships implied by chart construction.

These relationships remain useful evidence but should rarely consume
multiple competitive claim slots.

## Bre case study

The reviewed Bre packet devoted numerous slots to angle-angle geometry
while omitting:

-   Moon conjunct ASC
-   Sun conjunct IC
-   Moon opposite Pluto
-   Moon quincunx North Node
-   Venus square North Node

Those omitted relationships better personalize the chart than the
structural angular frame.

## Suggested implementation

Candidate generation: - new AxisRelationshipGenerator

Scoring: - structural inevitability penalty - axis compression bonus

Optimizer: - suppress redundant component candidates once axis candidate
selected.

## Future work

Generalize beyond angles into polarity-chain candidates and other
configuration-level generators already anticipated by SBE.
