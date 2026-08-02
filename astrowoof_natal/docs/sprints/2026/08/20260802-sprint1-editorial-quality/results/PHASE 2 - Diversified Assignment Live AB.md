# Phase 2 — Diversified Assignment Live A/B

## Executive result

`stratified-v1` produced a materially cleaner unpolished whole deck than the
historical contiguous assignment in this one-subject controlled test. It
eliminated the control's exact duplicate headline, card-level grammar error,
and all repeated cross-claim sequences of ten or more words. Its whole-deck
acceptance gate passed. The control's did not.

The result is promising rather than universal proof. Stratification did not
improve every proxy: its broad bag-of-words similarity was slightly higher,
its vocabulary breadth slightly lower, and handler/hybrid lexical separation
slightly weaker. It also produced a seven-card `Kevin, you are` opening family.
The policy appears to reduce literal phrase/template carryover; it does not by
itself solve rhetorical-form diversity, vocabulary range, or voice separation.

Recommendation: retain `stratified-v1` as the semantic-closure default and
continue upstream editorial-planning improvements. Do not ask polish to undo
pass-level templating that the assignment policy can prevent, but do not treat
assignment diversity as a substitute for card-level planning either.

## Experimental design

- Subject: Kevin
- Identical projected inputs, selected packet, current code, guidance, model,
  reasoning effort, cache settings, retry ceiling, and opaque pass gate
- Control: priority-contiguous passes
- Treatment: deterministic `stratified-v1` passes
- Model: `gpt-5.6-terra`, medium reasoning
- Polish: disabled
- Initial card calls: five per arm
- Pass 6: authored once in the control and copied byte-for-byte to treatment
- Comparison: complete assembled decks in canonical priority order

The four summaries and theme-group plan are identical. Their shared validation
failures are neutral with respect to the Phase-2 hypothesis.

## Whole-deck QA

| Check | Contiguous | Stratified |
|---|---:|---:|
| Card-level validator errors | 1 | 0 |
| Validator warnings | 3 | 0 |
| Exact cross-card duplicate groups | 1 | 0 |
| Whole-deck authoring acceptance | reject | accept |
| Linter advisories | 1 | 2 |
| Shared pass-6 theme errors | 2 | 2 |

The control's unique failures were invalid second-person grammar on card 4,
an exact repeated hybrid headline (`The Ritual That Says ‘Still Here’`), and
three possible no-astro astrology leaks. Its advisory also found the
`fine-print` humor mechanism three times.

The treatment had no card-level validation error or warning and no exact
duplicate. Its two nonblocking advisories were seven `Kevin, you are`
direct-to-dog body openings and the shared `fine-print` mechanism appearing in
one treatment card, one other treatment card, and the identical summary.

## Deterministic prose metrics

| Metric | Contiguous | Stratified | Direction |
|---|---:|---:|---|
| Total card words | 32,120 | 32,018 | effectively equal |
| Unique words | 3,022 | 2,890 | control wider |
| Type/token ratio | 0.09408 | 0.09026 | control wider |
| Mean body words | 56.74 | 55.62 | effectively equal |
| Repeated 5-word groups | 156 | 144 | stratified better |
| Repeated 6-word groups | 54 | 43 | stratified better |
| Repeated 7-word groups | 22 | 15 | stratified better |
| Repeated 8-word groups | 12 | 4 | stratified better |
| Repeated 9-word groups | 8 | 1 | stratified better |
| Repeated 10–12-word groups | 13 | 0 | stratified better |
| Repeated three-word opening groups (count ≥3) | 25 | 23 | slight stratified edge |
| Body pairs with cosine ≥0.65 | 10 | 14 | control edge |
| Mean top-100 body cosine | 0.6209 | 0.6266 | control edge |
| Mean handler/hybrid body Jaccard | 0.1570 | 0.1618 | control slight edge |

The cosine result does not contradict the n-gram result. Treatment cards often
used the same subject vocabulary—bond, person, game, trust, cue, return—without
repeating the same sentences. For example, its highest-similarity hybrid pair
described two different action/bond syntheses using the shared vocabulary of a
toy, release, return, praise, and partnership. It was conceptually close, not
verbatim templating. This still suggests an improvement opportunity: the
assignment cost balances categories and domains, but its semantic-distance
model could eventually include richer claim motifs.

## Qualitative reading

Both decks contain strong cards. Stratification did not transform weak prose
into a different literary species; it shifted the frequency of certain
failure modes.

The treatment more often found a card-specific organizing image. Examples
include `The Toy Is an RSVP`, `The Two-Member Operations Department`, and
`A Detour With a Return Address`. Its treatment of the core freedom/connection
claim keeps a single memorable thesis: Kevin makes the original opening, then
brings his person the news. The control version is also good, but uses a more
familiar two-act explanatory structure.

The treatment's hybrid prose generally remains genuinely joint rather than a
lightly rewritten handler voice. For the same core claim, Kevin investigates,
the human waits, and the walk becomes a joint expedition; both participants
change the event. Similar reciprocity appears in `The Game Gets Better at the
Check-In` and `The Check-In That Powers the Day`.

The control sometimes wins on compression. `Trust Is Kevin's Main Room` and
`The Look Across the Room` are concise and memorable. Treatment occasionally
adds a second paragraph after the scene to explain what the scene already
showed. That tendency did not increase mean length materially, but it can make
individual cards feel more authored and also slightly more explicit than
necessary.

Headline diversity improved in the hard sense—no exact duplicate—but both
decks retain visible title families. The control favors `Give`, `Make`, and
`When`; treatment favors `Kevin`, `His`, `When`, and `Give`. Likewise,
`Kevin, you are` is a natural direct-to-dog opening and not automatically bad,
but seven uses show that diversified input alone cannot guarantee diverse
sentence architecture.

Overall qualitative judgment: treatment is the preferable unpolished deck,
but by a moderate rather than revolutionary margin. Its clearest win is lower
literal carryover and fewer hard QA defects. Its characterization remains
coherent. Its residual weaknesses belong to editorial planning and surgical
polish, not to reverting the assignment strategy.

## Service and runner behavior

The live test exposed several operational issues that must not be confused
with prose quality:

1. A background response that exceeded the 30-minute polling window was marked
   as an attempt error and immediately resubmitted. The original later ended
   `cancelled` but reported 55,351 input and 10,958 output tokens. Poll timeout
   should preserve a detachable pending response rather than imply a creative
   failure.
2. Control pass 4 attempt 2 completed but omitted Story 031's writing file.
   The checker crashed with `FileNotFoundError`; the runner retried and attempt
   3 passed. Missing reconstructed files should produce a first-class
   incomplete-delivery code rather than “checker emitted no report.”
3. Resuming the already-finalized control later demoted its accepted third
   attempt to `FAILED_REQUIRES_REVIEW` because the attempt count equaled the
   ceiling. Accepted state must dominate attempt-count exhaustion.
4. Treatment pass 5 attempt 1 ended with terminal service status `cancelled`;
   attempt 2 passed. This retry was appropriate.
5. Long service queues exhausted the 30-minute prompt-cache TTL. Initial calls
   recorded no cache hits; only the treatment retry received 30,646 cached
   tokens. Cache efficiency cannot be assumed when queue delay exceeds TTL.
6. The known pass-6 contract gap remains: pass-local acceptance allowed five
   imbalanced theme groups, while final validation requires three or four
   approximately balanced groups.

Locally accounted cost is $1.97829 for control and $1.6704615 for treatment,
but the control total omits the cancelled timed-out response's reported usage.
Those figures therefore must not be interpreted as an assignment-policy cost
comparison. The OpenAI dashboard remains billing authority.

## Artifacts

- `work/phase-002-live-ab/contiguous/final/kevin/natal.kevin.cards.json`
- `work/phase-002-live-ab/stratified-v1/final/kevin/natal.kevin.cards.json`
- `work/phase-002-live-ab/deterministic-quality-metrics.json`
- Both complete run directories, pass attempts, requests, responses, accepted
  workspaces, assignment maps, validators, linters, and accounting records
