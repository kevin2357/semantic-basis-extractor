# Controlled Kevin Comparison Report

## Executive conclusion

K7 is the strongest current production baseline. It combines the current
upstream authoring architecture with a demonstrably effective, inexpensive
mechanical cleanup layer. K8 proves that qualitative criticism adds important
information, but its candidate should not automatically replace K7: six of its
seven edits are clear improvements while one trades away a stronger joke.

The sprint therefore supports a layered quality architecture:

1. prevent semantic and structural problems upstream;
2. require whole-deck deterministic QA after independent pass authoring;
3. apply sparse mechanical repair to bounded surface findings;
4. use qualitative criticism for diagnosis and selective research candidates;
5. retain human or later policy review before promoting qualitative edits.

No single polish pass substitutes for good upstream conception.

## Matrix integrity

All available decks contain the same fifty claim IDs. Differences among K0,
K1/K2, and K6–K8 are therefore editorial and process differences rather than
claim-selection differences.

- **K0:** manual six-pass final deck.
- **K1:** original automated pre-sprint baseline.
- **K2:** K1 after the Phase-0 context-naive targeted polish experiment.
- **K3:** same-subject summary-gold failure evidence.
- **K4/K5:** intentionally not run after K3 was disqualified.
- **K6:** fresh current upstream authoring, no polish.
- **K7:** K6 plus bounded mechanical polish.
- **K8:** K7 plus qualitative diagnosis and a separate candidate.

K3 is not a candidate. K8 is not promoted production output. Historical
comparisons involving K0–K3 retain process/version confounds; K6→K7 and K7→K8
are the clean controlled deltas.

## Deterministic comparison

| Variant | Mean card-body words | Mean summary-body words | Dominant opening groups | Lint warnings |
|---|---:|---:|---:|---:|
| K0 | 61.82 | 93.53 | 2 | 5 |
| K1 | 60.88 | 73.69 | 2 | 2 |
| K2 | 60.76 | 73.69 | 0 | 0 |
| K3 | 60.88 | 90.11 | 2 | 2 |
| K6 | 53.46 | 130.64 | 2 | 3 |
| K7 | 53.46 | 130.64 | 0 | 0 |
| K8 | 53.35 | 130.64 | 0 | 0 |

Every deck has 150 unique humor fields, so exact uniqueness is not the
problem. Comic mechanisms can repeat while every string remains unique.

The current authoring process produces tighter ordinary card bodies than K0,
but much longer summaries. K7/K8 summaries average about forty percent more
words than K0 and about seventy-seven percent more than K2. This supports the
UI observation that summary depth and summary usability need an explicit
product contract rather than a single assumed ideal length.

## Summary-set review

### K0: strongest architecture and peak writing

K0's summaries remain the best differentiated four-card set:

- `The Friendly Original With a Serious Heart` owns identity and temperament.
- `Kevin's Day Has Acts, Not Just Hours` owns temporal rhythm.
- `Give Him an Anchor, a Gate, a Laboratory, and a Stage` owns support needs.
- `Do Not Train Out the Spark; Train the Landing` owns development.

Each lens has a memorable organizing device and a distinct reader purpose.
The prose is deep without requiring every card to restate the whole chart.

### K2: strongest concise set

K2 is the most immediately scannable set. `Kevin's Day Is a Loop with Paws on
It` and `Kevin's Best Growth Is Organized Curiosity` are clear and product-
friendly. The tradeoff is reduced dimensionality: the needs and growth cards
are effective but less piercing than K0.

### K7: richer current synthesis, weaker lens separation

K7's summaries are polished and coherent. `A Day Built From Checkpoints` and
`Let the Odd Idea Become a Skill` contain strong prose. As a set, however, they
repeatedly return to curiosity, clear transitions, bounded outlets, trust, and
safe return. Identity, daily life, needs, and growth become four routes to the
same conclusion rather than four non-substitutable lenses.

The critic's summary-overlap finding is accurate. Local rewriting is the wrong
repair because the theses themselves require stronger separation before prose.
K8 correctly leaves them unchanged.

## Ordinary-card review

### K0 versus current automation

K0 retains a higher creative ceiling: more memorable metaphors, sharper comic
premises, and more willingness to let individual cards choose unusual forms.
Current automation has a higher floor: clearer handling advice, more stable
audience distinctions, better schema discipline, and fewer weak filler cards.

K6 ordinary bodies are also tighter than K0 without collapsing into the terse
K2 polish style. The semantic-contribution and audience-posture planning added
upstream are doing real work.

### K6 to K7: clean mechanical value

K7 changes exactly four reader-facing fields. Two body edits eliminate the
six-card `Kevin, you are/can` opening families; two headline edits reduce the
fine-print comic mechanism below threshold. No unrelated field changes.

Both sparse calls improved the deterministic finding count, and thirteen of
seventeen offered target instances were preserved. This is strong evidence for
default bounded mechanical polish when whole-deck lint identifies a repairable
surface problem.

### K7 to K8: valuable diagnosis, mixed candidate authority

The critic sees problems the linter cannot:

- conceptual convergence among four independence/reconnection cards;
- convergence among all four summary theses;
- investigation/bureaucracy humor concentration;
- repeated corrective-defense posture in handler prose;
- exchangeable headlines;
- over-explained full-astrology cluster cards.

Its upstream/local classification is sound. The candidate's handler edits and
three of four joke edits are improvements. The remaining quote removes a
repeated mechanism but also removes some comic snap. Thus K8 validates the
critic and bounded-candidate architecture while arguing against automatic
candidate promotion.

## Audience and astrology-density assessment

The current deck keeps Handler, Direct-to-Dog, and Hybrid purposes more stable
than the early automated decks. Handler prose teaches and guides; Direct-to-Dog
generally reassures or encourages; Hybrid more often describes coordination
rather than lightly rephrasing Handler.

Astrology-density escalation is also clearer. No-astro prose is behavior-led,
light astrology adds accessible interpretive language, and full astrology
usually identifies the actual placement/aspect mechanism. Five no-astro
validator advisories remain in K7/K8. They are visible but nonblocking; the
current system correctly does not authorize edits from advisory heuristics
alone.

## Cost interpretation

- K6 authoring: approximately `$1.12486975`.
- K7 mechanical polish: approximately `$0.024424`.
- K8 critic: approximately `$0.106461`.
- K8 candidate editor: approximately `$0.009893`.

K6 is an upper-bound authoring cost because four complete Terra retries were
caused only by invalid context-filter metadata. A metadata-only recovery path
should materially reduce expected cost. K7's value per dollar is excellent.
K8 criticism costs more than sparse editing because it reads the whole deck,
but its upstream diagnoses are materially useful.

## Decisions supported by the matrix

1. **Keep `stratified-v1` as the default assignment policy.** It improves pass
   composition without changing claim priority or deck structure.
2. **Keep summary prose gold cross-subject only.** Same-subject gold is
   prohibited; K3 remains failure evidence.
3. **Keep four-thesis summary planning, but strengthen thesis independence.**
   The current plan prevents collapse better than no plan, but K7 shows that
   shared full-chart motifs can still dominate every lens.
4. **Use sparse mechanical polish by default when blocking lint findings are
   present.** It is cheap, bounded, and effective.
5. **Keep qualitative criticism read-only and nonblocking initially.** Use it
   in QA, sampled production review, or research rather than making every deck
   pay the whole-deck critic cost immediately.
6. **Never auto-promote qualitative candidate edits yet.** Preserve candidates
   separately until review or a stronger acceptance policy exists.
7. **Add failure-aware metadata recovery.** Invalid context filters should not
   trigger complete creative reauthoring or Terra escalation.
8. **Preserve validator warnings as advisory.** Study warning precision before
   allowing them to mutate prose.
9. **Treat summary length as a product-mode question.** Complete and Quick
   WoofMaps may need distinct content contracts rather than one compromise.

## Upstream work exposed by K8

The next authoring improvements should not be framed as more prohibitions. They
should improve pre-prose conception:

- require each summary thesis to name its unique reader question, memorable
  answer, and information it deliberately leaves to another lens;
- make aspects that share placements identify different observable situations,
  stakes, and causal contributions before drafting;
- include a pass-level comic-mechanism and rhetorical-posture plan that favors
  positive diversity without turning forms into quotas;
- eventually feed structured critic findings back into research planning,
  while keeping critic prose out of the production deck unless separately
  accepted.

## Preferred artifacts

- **Production comparison baseline:** K7.
- **Qualitative research candidate:** K8.
- **Summary architecture reference:** K0, with cross-subject-only use.
- **Concise summary reference for product exploration:** K2.
- **Same-subject leakage evidence:** K3.

The deterministic source matrix is `kevin-comparison-matrix.json`.
