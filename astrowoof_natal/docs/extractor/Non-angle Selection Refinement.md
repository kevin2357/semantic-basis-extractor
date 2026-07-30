# Non-angle Selection Refinement (Expanded Design Notes)

## Context

These notes assume the existing SBE architecture, including:

-   whole-graph analysis
-   dependency closure
-   bundle optimization
-   marginal utility selection

The goal is not architectural replacement but richer candidate
generation and portfolio scoring.

## What the current system already does well

The Bre packet preserved several excellent motifs:

-   Mercury square Pluto
-   Mercury trine Uranus
-   Venus square Saturn
-   Moon trine Jupiter
-   Venus sextile Jupiter
-   Saturn conjunct North Node

The resulting syntheses around curiosity, confidence, and practice were
among the strongest parts of the deck.

## Primary observation

The remaining weakness is less about individual scoring and more about
**topological preservation**.

The optimizer preserves many excellent local truths while occasionally
losing the larger geometric configuration they belong to.

## Configuration completion

Example:

Selected: - Moon quincunx Saturn - Saturn conjunct North Node

Missing: - Moon quincunx North Node

The missing edge prevents the developmental triangle from appearing as
one coherent pattern.

Recommendation: Add a configuration-completion bonus whenever a
candidate closes an identifiable motif.

## Hub preservation

The Bre chart retained no Sun relationships despite several meaningful
Sun connections in the full graph.

Future scoring should discourage disconnecting major primitives from
their relationship neighborhoods.

## Luminary privilege

Traditional synthesis gives additional interpretive weight to Sun and
Moon relationships.

This need not become a hard rule, but could become a small portfolio
preference when utility scores are close.

## Integration hubs

Bre's Jupiter network illustrates an integration hub:

-   Moon trine Jupiter
-   Venus sextile Jupiter
-   ASC trine Jupiter
-   DSC sextile Jupiter

The packet captured only part of this integration structure.

Future whole-graph analysis could explicitly detect regulatory hubs.

## Information-processing community

The complete Mercury community consisted of:

-   Mercury trine Uranus
-   Mercury square Pluto
-   Mercury quincunx Neptune

The selected packet retained the first two, producing an excellent
investigator narrative, but lost the atmospheric/ambiguous processing
represented by Mercury-Neptune.

Community-aware scoring could recognize these as one semantic
neighborhood.

## Configuration generators

The existing design already anticipates:

-   graph communities
-   bridge motifs
-   polarity chains
-   configuration structures

These should likely become the next major deterministic candidate
generators.

## Suggested new scoring terms

-   configuration completion
-   hub preservation
-   structural inevitability
-   topology preservation
-   luminary connectivity

## Suggested optimizer research

The current greedy bundle optimizer is appropriate for v0.1.

Future research could compare:

-   beam search
-   mixed-integer optimization
-   graph coverage objectives

without changing the candidate contract.

## Overall assessment

After reviewing the implementation documentation, the architecture
appears stronger than initially inferred.

The recommended evolution is incremental:

1.  richer deterministic candidate generators;
2.  slightly richer utility vector;
3.  topology-aware portfolio objectives.

The overall philosophy should remain unchanged.
