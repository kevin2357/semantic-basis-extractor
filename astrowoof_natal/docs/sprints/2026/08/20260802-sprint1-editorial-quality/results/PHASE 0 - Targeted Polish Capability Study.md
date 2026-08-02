# Phase 0: Targeted Polish Capability Study

## Executive finding

Phase 0 asked:

> After independent authoring has produced a complete AstroWoof deck, how much
> writing-quality improvement can a context-naive LLM polish pass reasonably be
> expected to provide?

The answer is stable enough to guide implementation:

> A polish pass is a capable selective editor, but it is not a reliable
> substitute for strong upstream conception.

Polish can repair clearly diagnosed local mechanisms, reject false-positive
warnings, restore supplied semantic contributions, and preserve strong prose
when explicitly authorized to do so. It should not be expected to invent the
deck's missing creative architecture, turn 50 templated completions into 50
independently conceived essays, discover every subtle weakness unaided, or
rescue summaries whose four arguments were never properly differentiated.

The production principle is:

> Upstream authoring owns conception. Polishing owns evaluation and revision.

A deck should be acceptable if polish returns no changes. Polish should raise
the floor, correct bounded defects, and protect existing peaks.

## Why this study was needed

The semantic-closure pipeline could already produce structurally valid,
grounded, complete decks at low cost. Deterministic QA could detect missing
fields, schema violations, placeholders, certain repeated openings, and other
measurable editorial pathologies. It could not fully answer:

- Does this read like a miniature essay or a filled template?
- Is the headline memorable rather than merely correct?
- Do several jokes use the same comic machinery with different nouns?
- Did a compound claim retain all interacting semantic forces?
- Are the four summaries genuinely different arguments?
- Did concision improve the writing, or remove its most distinctive material?

The older manually assembled Kevin deck was an external benchmark because it
contained higher literary peaks in headlines, metaphor, comic variety, and
summary differentiation. The newer automated Kevin deck had the stronger
production floor, grounding discipline, actionability, hybrid interaction, and
reproducibility. Phase 0 explored whether downstream polish could recover the
missing strengths well enough that upstream authoring would not need to own
them.

## Experimental design and controls

Both rounds began from the exact same normalized automated Kevin deck. The
older manually assembled Kevin deck was withheld from both API agents and used
only after generation as an external quality benchmark.

Both agents were context-naive:

- fresh stateless Responses API jobs;
- no previous response ID or conversation history;
- no manual Kevin prose or gold examples;
- no Round-1 output supplied to Round 2;
- only production-reproducible dog, chart, claim, and deck context;
- strict sparse allowlists and locked non-target values;
- exact prompts, payloads, responses, usage, and evaluations preserved.

The shared candidate pool contained 164 scalar fields:

- 108 fields across four summary cards;
- 24 administrative/corporate humor fields;
- 6 repeated direct-to-dog openings;
- 5 over-explained handler bodies;
- 10 weak or administrative headlines;
- 8 compound-semantic renderings;
- 3 validator advisories suspected of being false positives.

The experiment was not required to produce a better deck. A neutral or
damaging result would still identify responsibilities that should remain
upstream.

## Round 1: mandatory replacement

Round 1 described the product, voice modes, astrology-density modes, evidence
boundaries, and diagnosed defects. It required a replacement for every target.

### Result

- Model: `gpt-5.6-terra`, medium reasoning
- Input: 61,918 tokens
- Output: 8,953 tokens
- Estimated cost: $0.28909
- Approximate wall time: 70 seconds
- 164 of 164 target fields changed
- No non-allowlisted value changed
- Validator passed with three advisories
- Editorial linter passed with zero warnings

Round 1 behaved like re-authoring plus compression. Targeted prose fell from
5,376 to 3,880 words, a reduction of approximately 28%. Summaries alone fell
from 3,428 to 2,262 words, a 34% reduction.

It removed obvious defects, but mandatory replacement made preservation
impossible. Strong fields and false-positive advisories were rewritten along
with actual weaknesses.

For example:

> Kevin's Day Is a Loop with Paws on It

became:

> Kevin Thrives on Good Loops

The result is clear and concise, but less memorable. Round 1 established that
a pass can raise consistency while lowering literary peaks.

## Round 2: information parity and `keep|replace`

Round 2 independently restarted from the original baseline. It tested whether
a preservation-aware editor with better context could repair actual defects
without rewriting successful prose.

It added clearer product orientation, a `Read -> Appreciate -> Edit` handbook,
explicit preservation authority, one `keep` or `replace` decision per field,
richer localized evidence, descriptive length context rather than quotas, and
stronger summary and voice guidance. It still received no gold, manual Kevin
prose, Round-1 result, or conversation history.

### Result

- Model: `gpt-5.6-terra`, medium reasoning
- Input: 157,118 tokens
- Output: 15,563 tokens
- Estimated cost: $0.62624
- Approximate wall time: 105 seconds
- 111 `keep` and 53 `replace` decisions
- Exactly 53 allowlisted values changed
- No non-allowlisted value changed
- Validator passed with the baseline's three apparent false positives
- Editorial linter passed with zero warnings

### Decision distribution

| Diagnosis | Fields | Action |
|---|---:|---:|
| Administrative humor | 24 | Replace all |
| Compound semantic flattening | 8 | Replace all |
| Generic/administrative headlines | 10 | Replace all |
| Over-explained bodies | 5 | Replace all |
| Repeated openings | 6 | Replace all |
| Summary coherence | 108 | Keep all |
| Validator prose advisories | 3 | Keep all |

Total targeted prose ended at 5,382 words, six words longer than baseline.
Round 2 behaved as an editor rather than a compressor.

The categorical decisions are encouraging but not conclusive evidence of
independent diagnosis. Explicit diagnosis classes may have strongly determined
the actions. A future critic experiment should test diagnosis separately from
editing.

## Three-way qualitative comparison

### Summary cards

Round 1 changed all 108 fields, making them shorter and more regular while
removing several strong images and headlines. Round 2 kept every summary field
exactly.

Round 2 demonstrated protection, not summary improvement. Neither round proved
that naive polish can turn adequate summaries into excellent four-lens
synthesis. Compared with the manual benchmark, the experiment did not reliably
manufacture missing peak phrasing or differentiation from scratch.

Therefore summary arguments belong upstream in pass 6. Later summary polish
should respond to specific overlap or execution diagnoses, not require
wholesale rewriting.

### Repeated openings

The six baseline fields shared a `Kevin, you do not...` architecture.

- Baseline: 335 words
- Round 1: 264
- Round 2: 330

For the bond-versus-investigation card:

- Baseline: `Kevin, you do not have to choose between being your own
  investigator and being close to your person.`
- Round 1: `The mystery can have your nose, and your person can still have your
  trust.`
- Round 2: `Look back, Kevin. Take the offered touch. Then go see what that
  strange sound was from a safe distance.`

Round 1 produced the most lyrical isolated sentence. Round 2 made the more
reliable editorial intervention: it fixed the doorway without discarding the
rest of the essay.

### Over-explained bodies

- Baseline: 495 words
- Round 1: 302
- Round 2: 399

Round 1 cut approximately 39%; Round 2 approximately 19%. In Kevin's opening
relationship card, the versions were 94, 53, and 72 words. Round 2 retained the
important two-act mechanism: Kevin's unconventional entrance is followed by a
check for connection. Round 1 conveyed the point but reduced its texture.

The lesson is not that longer is better. Polish should remove duplicated labor,
not richness still doing semantic or emotional work.

### Compound semantics

- Baseline: 520 words
- Round 1: 494
- Round 2: 573

This was Round 2's strongest category. For Neptune in Sagittarius in Doghouse
10, it retained Neptune's atmospheric sensitivity, Sagittarius's outward
orientation, Doghouse 10's visible pack function, their synthesized social
effect, and a practical navigation cue. Its no-astrology hybrid version kept
the memorable `sidewalk briefly ceremonial` image while making the shared
interaction clearer.

For Part of Fortune in Cancer in Doghouse 5, it preserved the easy reward
channel, emotional security, play/performance, and their interaction.

Downstream polish can repair flattened meaning when the defect and source
contributions are supplied, existing assets are protected, and replacement is
sparse. It cannot recover evidence the pipeline no longer provides.

### Humor

- Baseline: 336 words
- Round 1: 339
- Round 2: 384

Round 1 was generally punchier. Round 2 was more claim-specific and behavioral.

- Baseline: `Kevin does not say hello; he submits a proposal for a more
  interesting version of hello...`
- Round 1: `Kevin treats every hello like a new game he invented halfway
  through the first bounce.`
- Round 2: `Kevin does not say hello; he arrives sideways, adds a surprise
  flourish, and waits to see whether anyone appreciates the choreography.`

Round 2 preserves the claim mechanism; Round 1 lands faster. Some Round-2 jokes
became affectionate poetic lines rather than jokes. Humor should be conceived
upstream, then inspected for mechanism diversity and whether it is funny.

### Headlines

Round 2 was more reliably precise; Round 1 sometimes produced the sharper
headline:

- Baseline: `The Toy Is a Relationship Proposal`
- Round 1: `Kevin Brings Toys as Invitations`
- Round 2: `When Kevin Brings a Toy, He Brings Connection`

Round 2 explains the claim well; Round 1 reads more naturally as a headline.
Round 2 also introduced a small `Kevin + verb` cluster. Later polish should
evaluate the edited set together, not merely compare each field to its source.

### Validator advisories

Round 2 correctly kept all three fields. The advisories were lexical heuristic
matches, not actual astrology leakage. Round 1 rewrote them and removed useful
detail without solving a real problem. Deterministic findings should initiate
review, not compel mutation.

## Comparison with the manual Kevin reference

The manual deck was excluded from generation, so this comparison concerns
outcomes rather than imitation.

The automated baseline and both candidates retain the automated pipeline's
consistent grounding, handler actionability, shared-scene hybrid prose,
deterministic completeness, and dependable floor.

The manual reference still demonstrates qualities neither polish round
reliably manufactured from scratch:

- higher peak headline memorability;
- more surprising metaphors;
- less predictable comic forms;
- stronger four-summary differentiation;
- the sense that each card began from its own creative thesis.

Round 1 occasionally approached those qualities but also destroyed peaks.
Round 2 protected peaks and made stronger semantic repairs, but did not supply
missing deck-level creative architecture. That is why conception remains an
upstream responsibility.

## Responsibility boundary

### Upstream owns

- the whole-dog portrait;
- each card's remembered idea, thesis, and lived doorway;
- differentiation from neighboring claims;
- audience purpose and astrology-density conception;
- initial comic premise and headline;
- complete source interpretation;
- four distinct summary arguments.

### Polish can own

- repeated openings and architectures;
- reused joke mechanisms;
- isolated generic headlines;
- duplicated explanation;
- flattened but supplied compound semantics;
- bounded voice execution and deck-level cleanup;
- deciding that a warning merits no change.

### Shared responsibilities

Humor, headlines, voice distinction, summary coherence, semantic precision,
and deck diversity must begin upstream and may be inspected downstream.

Use this routing test:

> Can an editor repair the defect from finished prose plus localized evidence
> without deciding anew what the card fundamentally is?

If not, move the intervention upstream.

## Future structured-critic hypothesis

Both the Codex review and an independent discussion with the agent that helped
produce the strongest Bre deck converged on separating diagnosis from rewriting.

A possible future architecture is:

1. assemble the independently authored deck;
2. run deterministic validation and lint;
3. give the read-only deck to a qualitative critic LLM;
4. receive strict structured findings, not revised prose;
5. select or cap eligible findings;
6. send only those paths, diagnoses, evidence, and necessary context to a
   preservation-aware editor;
7. apply sparse edits and rerun deterministic/value-level QA.

A critic finding might contain:

- quality dimension and priority;
- exact target and comparison paths;
- concrete diagnosis and rewrite objective without proposed prose;
- confidence;
- required claim or whole-chart evidence;
- summary, card, or deck-level scope;
- local-repair versus upstream-reconception classification.

Potential advantages include independent diagnosis, detection of semantic
repetition beyond lexical lint, smaller rewrite contexts, capped cost and
mutation, separate critic/editor evaluation, and feedback that can inform
future upstream improvements.

Risks include added cost and latency, invented problems, checkbox criticism,
shared critic/editor biases, whole-deck token load, and misclassifying upstream
conception failures as editable symptoms.

This sprint should preserve the hypothesis without detouring into its full
implementation. Phase 3.5 applies inexpensive lessons to the existing polish
path; Phase 4 retains the critic as a separate controlled investigation.

## Cost conclusions

Round 2 cost approximately 2.17 times Round 1 and used roughly 2.54 times as
many input tokens. The context and decision machinery improved editorial
behavior, but the complete experiment handoff is not a suitable default
production payload.

Near-term production work should retain principles rather than copy the package:

- compact `keep` or no-op authority;
- sparse targets;
- localized evidence only when required;
- preservation guidance in a stable cacheable prefix;
- no elaborate rationale for obvious keeps;
- no full handbook unless later tests justify it;
- measured token and cost deltas on live QA.

## Confidence and limitations

Confidence is high in the architectural boundary and moderate in the outer
limit of specialized polish. Round 2 changed several variables at once, so it
identifies a successful bundle of principles rather than each component's
isolated causal effect.

Only one subject and source deck were tested. Targets were human-diagnosed
rather than independently discovered by the model. Summary improvement,
specialized humor editing, and rescue of deeply templated decks remain
incompletely tested. These limitations do not block the sprint: they do not
undermine the conclusion that localized repair is viable while missing
conception must be prevented upstream.

## Durable decisions

1. Require acceptable pre-polish decks.
2. Preserve strong prose as a first-class success condition.
3. Do not compel edits solely because deterministic QA emitted an advisory.
4. Supply semantic evidence when asking polish to repair semantic loss.
5. Do not equate shorter prose with better prose.
6. Keep summary conception in pass 6 and test it separately.
7. Treat humor, headlines, voices, and diversity as shared responsibilities.
8. Add only narrow, inexpensive polish hardening in this sprint.
9. Preserve the structured critic as the leading future qualitative-diagnosis
   hypothesis.
10. Evaluate exact diffs, examples, cost, and human judgment alongside QA.

## Preserved artifacts

Exact inputs, request builders, prompts, API payloads, responses, metadata,
candidate decks, validator/linter reports, and value-level audits are under:

- `work/round-001/`
- `work/round-002/`

Immutable Kevin reference decks and the authoring packet are under:

- `astrowoof_natal/qa/reference_decks/kevin/`

Together these provide the starting point for a later full polish and
structured-critic design effort.
