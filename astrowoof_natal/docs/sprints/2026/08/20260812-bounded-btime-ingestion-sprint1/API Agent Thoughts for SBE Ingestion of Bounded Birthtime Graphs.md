# API Agent Thoughts for SBE Ingestion of Bounded Birthtime Graphs

```yaml
status: advisory-input-for-sprint-planning
author: astrowoof-api-agent
date: 2026-08-12
target: semantic-basis-extractor
sprint: 20260812-bounded-btime-ingestion-sprint1
source_context: AGF bounded-natal Sprints 1-3 and AstroWoof orchestration planning
```

## Purpose and limits

These are API-consumer observations after reviewing AGF's coordinate-derived and
time-frame-derived bounded natal work and its subsequent AGF/SPC decoupling. They
are not a substitute for the AGF handoff, the bounded graph schemas, or a joint
SPC/SBE design review. They highlight properties that seem especially important to
preserve when SBE turns four bounded projected graphs into a bounded semantic basis.

The central product value is not merely that a time is unknown. It is that every
promoted conclusion has a declared domain over which it is true, while variation,
transition, prerequisites, and counterexamples remain first-class evidence rather
than being hidden behind a representative timestamp.

## Keep bounded ingestion a distinct contract

The bounded graph is not an exact canonical graph with nullable fields, confidence
scores, or a warning attached. Its structure answers a different question. SBE
should therefore accept it through an explicit bounded input schema and emit an
explicit bounded claim-deck schema/version.

Avoid normalizing bounded evidence into the existing exact projected-chart shape.
That would invite downstream code to treat an invariant, a conditional alternative,
and an unavailable conclusion as three slightly different values of the same fact.
They are different epistemic kinds and need different validation and authoring rules.

Exact and bounded decks may share claim vocabulary, ranking machinery, synthesis
infrastructure, and much of the authoring system, but schema identity should make it
impossible to mistake one authority class for the other.

## Preserve the quantified domain of truth

An invariant claim means that the claim holds across the entire admitted birth-time
domain under the declared evaluation contract. SBE should not weaken that into
`likely`, `usually`, or `probably`, nor strengthen a merely sampled observation when
the AGF evidence does not authorize continuous-domain certainty.

Conversely, absence from the invariant canonical portion is not evidence that a
placement or relationship is false. It may vary, become undefined, depend on a
prerequisite, cross a boundary, or lack sufficient evidence. Extraction should use
the bounded evidence's explicit status/reason rather than infer one from omission.

Useful claim-level provenance would retain at least:

- the bounded source-chart identity and schema/resource identities;
- the projected context and source evidence identifiers;
- the admitted local-time interval and timezone basis by reference or digest;
- whether authority is invariant, conditional, alternative, transitional, or
  unavailable;
- the root evidence family that owns the conclusion; and
- any prerequisites or counterexample/transition witnesses needed to explain its
  limits.

The final reader need not see all of that machinery, but the claim deck and delivery
provenance should make every authored statement traceable back to it.

## Do not recreate the noon-reference model indirectly

No ranking shortcut should select one sampled minute as a representative chart and
then run ordinary natal extraction against it. Likewise, a majority-duration value
is not invariant merely because it dominates the interval. Frequency may be useful
descriptive evidence in a future product design, but it is not permission to present
that value as the dog's natal fact.

The same warning applies to synthesis. Two individually supported alternatives must
not be combined into one definite personality conclusion unless their joint truth is
actually supported over the required domain. Synthesis needs to preserve the
quantifier and prerequisites of every input, not just their prose-friendly content.

## Treat root-owner evidence as a deduplication invariant

AGF's root-owner evidence families appear important for preventing a single changing
placement from multiplying into many apparently independent relationship changes.
SBE ranking should respect that ownership. Otherwise semantic-maximality scoring may
overweight one volatile root because it produces many derived aspects, rulerships,
or house-dependent consequences.

A bounded selector could measure coverage over independent semantic/evidence
families rather than raw claim count. That aligns nicely with SBE's original
`semantic basis` idea: select a compact set that spans the most defensible meaning,
without allowing a dense dependent family to crowd out unrelated invariant facts.

This also suggests recording why an eligible claim was not selected: redundant root
family, lower incremental semantic coverage, conditional conflict, prerequisite not
selected, or capacity limit. Such reasons would be valuable when tuning quick versus
complete decks later.

## Separate stable portrait from uncertainty narrative

The most useful bounded reading may have two coordinated semantic layers:

1. a stable portrait composed only of facts valid over the entire interval; and
2. a restrained uncertainty layer explaining genuinely meaningful alternatives or
   transitions without pretending the dog has several simultaneous exact charts.

The stable portrait should remain rich enough to be a real reading, not merely a
list of caveats. Conditional material should earn inclusion because it adds material
meaning, not because the source graph happens to enumerate it. This is another place
where marginal semantic coverage is likely more useful than a fixed quota per
evidence class.

Authoring instructions should distinguish:

- `always supported across the supplied interval`;
- `one of these alternatives applies, depending on the unknown time`;
- `this feature changes within the interval`;
- `this conclusion is unavailable because its prerequisite is not invariant`; and
- `not evaluated or unsupported`.

Those distinctions should survive all audience and astrology-density variants. A
low-terminology version may omit technical mechanics, but it must not erase the
epistemic boundary.

## Houses, angles, sect, lots, and dependent claims

It is particularly encouraging that bounded AGF can promote terrestrial-frame facts
when they truly remain invariant. SBE should not suppress houses, angles, sect, lots,
or derived relationships merely because birth time is bounded. It should consume
them under the same evidence rule as every other fact: promote what is invariant,
qualify what is conditional, and omit what cannot be defended.

Dependent facts need explicit prerequisite handling. A relationship that stays
numerically stable but depends on a non-invariant angle, house, ruler, or sect state
should not become an unconditional claim. Prefer validation against declared
prerequisite links over re-deriving dependency semantics inside SBE.

## Four projections must describe one bounded source

The four WoofMap projections should all bind to the same bounded source-chart
identity, time-domain identity, AGF graph identity, projection release/resource
tuple, and subject. SBE should fail closed if the packet mixes intervals, subjects,
source graphs, bounded-schema revisions, or exact and bounded projection kinds.

The API will eventually enforce the packet at its orchestration boundary as well,
but SBE remains the authority for whether the four inputs form one semantically
coherent extraction packet. A compact machine-readable admission summary would help
the API distinguish incompatible input from extraction failure.

## Identity and future multi-subject work

Keep source-chart identity opaque. Do not derive it from dog name, coordinates,
timestamps, or filenames. The API needs to associate multiple natal charts with one
dog and will later support chart types concerning multiple subjects. A bounded deck
should therefore carry subject/chart references supplied by the caller without
assuming one permanent chart per subject or one subject per future chart kind.

This is also a good reason to avoid baking `natal:<subject>` strings into semantic
identity. Natal is the current workflow, not the universal identity model.

## Validation and fixture ideas

Useful acceptance fixtures would include:

- a narrow interval whose bounded deck nearly matches an exact chart;
- a sign or house cusp crossing with a clear transition witness;
- a stable aspect whose dependent context changes;
- invariant houses/angles over a short interval;
- an unavailable terrestrial-frame family with an explicit reason;
- multiple derived claims sharing one volatile root owner;
- mixed-source, mixed-interval, mixed-subject, and mixed exact/bounded packets that
  must fail admission;
- equivalent bounded inputs in different serialization order producing the same
  semantic identity and selection; and
- a deck where invariant facts alone exceed capacity, proving conditional material
  cannot displace stronger authority merely to satisfy a category quota.

Golden tests should assert evidence class, prerequisites, root ownership, exclusion
reason, and provenance—not only authored wording or final claim count.

## Observability hooks worth adding during ingestion

The companion logging request proposes a structured non-authoritative event stream.
Bounded ingestion would benefit from aggregate events for:

- packet admission and shared-identity validation;
- counts by evidence class, projected context, and root-owner family;
- invariant versus conditional eligibility;
- exclusions by closed reason code;
- synthesis attempts rejected for incompatible domains or prerequisites;
- selected incremental-coverage contribution; and
- final deck counts and digests by epistemic class.

These events must never substitute for claim-deck provenance or native run state.
They exist to reveal systematic thinning, overrepresentation, and failure patterns
across real unknown-time use, which is likely to be common for dogs.

## Closing principle

The bounded pipeline should optimize meaning only after it preserves truth
conditions. A smaller reading made entirely from defensible invariant and clearly
qualified conditional claims is more aligned with AstroWoof than a richer reading
that quietly collapses the interval into an invented exact birth time.
