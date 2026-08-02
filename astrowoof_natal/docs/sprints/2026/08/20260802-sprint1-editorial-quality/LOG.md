# Sprint Log: Editorial Quality Beyond Mechanical Acceptance

## 2026-08-02 — Sprint created

### Evidence entering the sprint

- Automated Kevin is the better production baseline.
- Manual Kevin retains stronger peak headlines, metaphors, humor diversity, and summary differentiation.
- Automated Kevin has stronger handler actionability, quality floor, hybrid interaction, and deterministic results.
- Optimized Ella completed for approximately $0.474 with six first-attempt Luna authoring successes, no creative retry, one sparse polish call, validation pass, and zero linter warnings.

### Decisions

- Begin with human-directed, context-naive API polish before production changes.
- Stop for a discovery checkpoint after that experiment.
- Use the complete manual Kevin summaries as the leading pass-6-only gold candidate.
- Test deterministic stratification rather than unseeded shuffling.
- Preserve mechanical polish as a distinct safety layer.
- Explore qualitative diagnosis and bounded qualitative polish separately.
- Compare context-naive polish against a new pass-6 run both without and with proposed qualitative polish.
- Use separate full-card variants to test reordering.

### Next action

Prepare Phase-0 Round 1 through the pre-submission review gate. The fresh API
agent, not the long-context task, will write replacement prose.

## 2026-08-02 — Phase-0 experimental framing corrected

The purpose of Phase 0 is to explore the limits of post-authoring qualitative
polish by a context-naive agent. It is not to prove that a long-context agent
can manually improve Kevin's deck.

Controls:

- No gold examples or old manual Kevin prose enter the request.
- Human work is diagnosis, target selection, prompt/context design, and evaluation.
- The API response is fresh and stateless.
- The complete request is shown to the user before submission.
- Additional rounds require a specific hypothesis supported by a completed round.

## 2026-08-02 — Phase-0 request review

- Keep the experimental purpose in the sprint record, not in model-visible
  instructions; the API agent should receive an ordinary production polish
  assignment.
- Replace the directory-workspace-oriented Guiding Lights copy with a compact
  polish guide explaining the claim deck, voices, astrology-density levels,
  summary authority, sparse targets, and read-only context.
- Add a later sprint review of the full-chart basis transport for token
  efficiency and author comprehension. This does not change the current
  experiment's chart evidence.

## 2026-08-02 — Phase-0 Round 1 submitted

The revised request presented an ordinary targeted polish assignment. Model-
visible instructions contained no experimental framing, gold reference, old
Kevin deck, story-directory workflow, or prior-conversation context. A new
polish-specific guide defined claim decks, evidence boundaries, summaries,
voices, astrology-density levels, sparse targets, and read-only context.

### Service result

- Model: `gpt-5.6-terra`
- Reasoning: `medium`
- Response: fresh background Responses API job
- Response ID: `resp_056b1991508746e3006a6f14127ddc8193ae8b4b25584eed57`
- Wall time: approximately 70 seconds
- Input tokens: 61,918, all uncached by design
- Output tokens: 8,953
- Reasoning tokens: 125
- Estimated cost: $0.28909
- Transport: one create and 27 successful retrieval polls

### Mechanical result

- All 164 required sparse replacements were returned.
- Exactly 164 allowlisted scalar values changed.
- No non-allowlisted value changed.
- The standard validator passed with three advisory warnings.
- The editorial linter passed with zero warnings.
- The three remaining validator warnings appear lexical/heuristic rather than
  actual no-astro leakage; the cited prose contains no astrology.

### Preliminary qualitative signal

- Administrative/corporate humor was replaced by substantially more varied,
  claim-specific dog-life premises without reducing total humor length.
- The six repeated direct-to-dog openings became distinct and lost 71 words in
  aggregate.
- Five over-explained bodies lost 193 words while generally preserving their
  useful behavioral guidance.
- Two sampled compound claims preserved their interacting semantic forces more
  explicitly after revision.
- Summary prose lost 1,166 of 3,428 words (34%). It became clearer and more
  scannable, but several already-strong headlines and images became safer and
  less literary. For example, `Kevin's Day Is a Loop with Paws on It` became
  `Kevin Thrives on Good Loops`.

Round 1 therefore supports a useful boundary hypothesis: targeted polish can
reliably repair identifiable local mechanisms, but requiring replacement of
every field in an entire already-competent summary set may trade away peaks
while raising consistency and concision. Preserve the round unchanged for
matched evaluation before deciding whether Round 2 should add an explicit
`keep` decision or use narrower summary targets.

## 2026-08-02 — Phase-0 Round 2 prepared

Round 2 is an independent rerun from the exact normalized Round-1 baseline and
the same 164-field candidate pool. Round 1 remains immutable.

Hypothesis: bringing the polish agent to information parity with the original
authoring agent, explicitly treating preservation as an editorial success, and
providing descriptive length context will retain existing literary peaks while
still repairing diagnosed local weaknesses.

Model-visible improvements include:

- product and reader-experience orientation;
- miniature-essay and nine-sibling-rendering framing;
- a private structured whole-dog orientation before decisions;
- explicit summary requirements for distinct arguments, examples, advice,
  language, and remembered ideas;
- factual cautions and concrete-advice standards;
- richer original claim evidence and semantic-neighbor context;
- current-deck length measurements described as context rather than quotas;
- one explicit `keep` or `replace` decision per candidate field.

No gold example, old manual Kevin prose, Round-1 output, or conversation history
enters the request. The request builder and submitter compile successfully, and
the submission path has completed a no-network dry run.

## 2026-08-02 — Phase-0 Round 2 submitted

The final Round-2 handoff incorporated a versioned editorial handbook organized
around `Read → Appreciate → Edit`, while concrete card requirements and the
targeted execution contract remained separate. The integration removed
model-visible experimental framing, full-deck claims unsupported by sparse
visibility, documentation-maintenance commentary, and overlapping product
guidance. It added coordinated-set resolution and an explicit counterweight to
excessive preservation.

### Service result

- Model: `gpt-5.6-terra`
- Reasoning: `medium`
- Response ID: `resp_0de029f290978cc9006a6f45d54320819695f3dfef2714cc0f`
- Wall time: approximately 105 seconds
- Input tokens: 157,118, uncached by experimental design
- Output tokens: 15,563
- Reasoning tokens: 792
- Estimated cost: $0.62624
- Handbook: `1.0-round2`
- Handbook SHA-256:
  `2a21a8e0cc66d8e43f9793aa8e168e8b4b3c73119bf33ad0ed5ca63ccd53a1ad`

### Mechanical result

- Exactly 164 decisions were returned: 111 `keep`, 53 `replace`.
- Exactly 53 allowlisted values changed; no non-allowlisted value changed.
- The standard validator passed with the baseline's three apparent lexical
  false-positive advisories.
- The editorial linter passed with zero warnings.

### Preliminary qualitative signal

- All 108 summary fields were kept verbatim. Round 2 therefore preserved every
  summary headline, image, example, and body length that Round 1 had compressed.
- All 24 targeted administrative-humor fields were replaced with more varied
  behavior-specific premises.
- All six repeated openings, ten weak headlines, five over-explained bodies,
  and eight compound-semantic renderings were replaced.
- The three validator-advisory candidates were kept; their prose contains no
  actual astrology and the warnings appear heuristic.
- Replacement rationales generally identify both the repaired mechanism and
  the original asset being protected. Several compound revisions preserve
  strong images while making the contributing semantic forces explicit.

The decision pattern is unusually categorical—every summary candidate was
kept and every substantively diagnosed card candidate was replaced. This may
reflect accurate interpretation of the supplied diagnoses, or it may indicate
that the agent treated diagnosis class as the decision rather than judging all
164 fields independently. Matched human evaluation should test that question.

## 2026-08-02 — Phase-0 discovery checkpoint completed

Round 1 and Round 2 were compared field by field against the same normalized
automated Kevin baseline and against the older manually assembled Kevin deck as
an external quality benchmark. The manual deck was not visible to either API
agent.

The discovery question now has a sufficiently confident answer for sprint
planning: a bounded polish pass can reliably evaluate and repair named local
defects, but it should not be the first stage responsible for conceiving card
theses, whole-dog characterization, creative variety, or summary arguments.

Round 1 changed all 164 authorized fields and reduced targeted prose from
5,376 to 3,880 words. It repaired many local defects but also compressed strong
summary writing and replaced false-positive advisory fields. Round 2 used
`keep|replace`, changed 53 fields, preserved 111 verbatim, and left total target
length essentially unchanged at 5,382 words. It retained all summaries and
advisory fields while repairing all explicitly diagnosed humor, opening,
headline, over-explanation, and compound-semantic targets.

Architectural decision:

- upstream authoring owns conception;
- polish owns preservation-aware evaluation and bounded revision;
- shared quality dimensions must be established upstream before polish inspects
  them;
- the deck should be acceptable even if polish performs no replacements.

The remaining plan now includes a narrow Phase 3.5 for inexpensive polish
hardening without importing the full experimental handbook or adding a critic
call. The larger structured-critic hypothesis remains in Phase 4 for future
design and controlled testing.

Detailed methods, examples, cost data, limitations, and future research are in
`results/PHASE 0 - Targeted Polish Capability Study.md`.

## 2026-08-02 — Phase 1 summary calibration implemented

Pass 6 now receives a complete Markdown rendering of the four manually
assembled Kevin summary cards as a craft-only reference. The handoff explicitly
forbids transferring Kevin's facts, astrology, language, metaphors, jokes,
headlines, sentence structures, and organizing devices. The transfer target is
four-lens differentiation, full-chart synthesis, prose depth, audience purpose,
and astrology-density control.

Pass 6 also receives a writable private thesis plan requiring distinct identity,
daily-life, needs/support, and growth/development arguments plus an explicit
explanation of why needs and growth are not the same thesis. The plan is
returned with the accepted workspace for audit but does not enter the assembled
cards JSON.

Passes 1–5 contain neither artifact. Both summary files are classified in the
pass-local assignment tier, preserving byte-identical shared static and subject
cache prefixes. The pass-6 workspace manifest names both files.

Verification:

- 71 builder and semantic-closure tests pass;
- tests cover pass isolation, gold safeguards, thesis markers, writable-field
  transport, assignment-tier inventory, and cache-manifest behavior;
- a real token-free Bre SBE generation produced all six archives;
- pass 1 contained no summary artifact;
- pass 6 and its ZIP contained the gold reference and thesis plan;
- the pass-6 manifest named both required files.

A token-free prompt-layout report confirmed byte-identical static and subject
prefixes across all six passes. The gold reference contributes an estimated
7,528 tokens and the thesis-plan template 352 tokens to pass 6 only. The
complete pass-6 request is estimated at 50,909 tokens by the repository's
dependency-free UTF-8-bytes/4 planning metric; actual API usage remains the
billing authority.

## 2026-08-02 — Phase 1 isolated Kevin live checkpoint

Only Kevin pass 6 was authored under the Phase-1 configuration. Accepted
historical passes 1–5 were reused, and same-code and summary-isolation decks
were preserved.

### Service result

- Model: `gpt-5.6-terra`, medium reasoning
- Response ID: `resp_09beba8d6c027770006a6f5d4a58b0819a85e2dd67b61044d1`
- One attempt; opaque pass gate accepted
- 42,961 input tokens; 8,277 output tokens; 44 reasoning tokens
- 100 seconds; estimated cost $0.2315575

### Quality result

The private plan formed four distinct arguments and explicitly separated
present support from development over time. Candidate summary bodies totaled
3,244 words, versus 2,675 in the historical automated baseline and 3,367 in the
manual reference. Reader-facing quality, richness, lens separation, and
needs/growth differentiation improved materially over the automated baseline.

The test also revealed substantial same-subject gold leakage. The candidate
shares 30 distinct twelve-word sequences with the manual Kevin reference, with
a maximum same-field run of 18 words, plus conceptually transferred chapter,
spark/return, and four-part-needs structures. No headline is copied exactly,
but explicit anti-copying instructions did not prevent structural imitation.

Decision: retain the thesis plan; keep full prose gold experimental pending a
cross-subject pass-6 test. The Kevin candidate demonstrates the attainable
quality target but is not a clean independent-authorship comparison.

Final whole-deck QA was blocked only by imbalanced newly authored theme groups
(`8, 12, 3, 10`). The historical grouping also fails the current rule. The
pass-local gate/final-validator mismatch is a separate defect. Detailed
analysis is in `results/PHASE 1 - Kevin Summary Calibration Live Test.md`.

## 2026-08-02 — Phase 1 cross-subject Ella live checkpoint

Ella pass 6 was authored with the Kevin gold while accepted Ella passes 1–5
were reused. The request completed on its first accepted attempt after durable
polling resumed the originally submitted response; no duplicate request was
created.

A same-code assembly control differs from the candidate at exactly the 108
summary values and nowhere else; all 50 reader-facing card payloads are
identical. Differences between that control and the optimized historical deck
are preserved separately as prior polish and theme-group drift.

### Service result

- Model: `gpt-5.6-terra`, medium reasoning
- Response ID: `resp_0c7df228968c8380006a6f61b996c0819aa9015072264bfba8`
- 43,398 input tokens; 7,639 output tokens; 53 reasoning tokens
- 188.625 elapsed seconds including detached polling
- Estimated cost: $0.22308

### Leakage result

The candidate shares no eight-, ten-, or twelve-word sequence with the Kevin
gold, no exact headline, and only one generic six-word sequence (`cue and a
familiar resting place`). Its maximum gold-body overlap is six words. Kevin's
facts, astrology, jokes, and four-part needs framework do not transfer.

Chapter, spark, landing, and return language appears in Ella, but the same
devices were already extensive in Ella's prior deck and source-derived prose.
The cross-subject evidence therefore supports same-subject alignment as the
mechanism behind the earlier Kevin leakage.

### Quality result

The thesis plan again produced four distinct arguments and a clean
needs-versus-growth distinction. The candidate is coherent, actionable, and
well voiced, but its 2,830 summary-body words are 34.8% below the existing
optimized Ella set's 4,339. The prior Ella summaries retain stronger literary
peaks and richer development in several lenses. Gold appears safe across
subjects, but its incremental benefit over the thesis plan alone remains
unproven.

Decision: retain the thesis plan; forbid same-subject prose gold; allow Kevin
gold to remain experimental across subjects; do not make always-on gold a
final decision without considering a later thesis-only A/B.

Both newly authored and historical Ella theme plans fail the current
three-or-four-group validation rule. The pass-local acceptance gap is confirmed
as a separate defect. Detailed analysis is in
`results/PHASE 1 - Ella Cross-Subject Gold Test.md`.

The longer optimized and shorter Phase-1 Ella decks were also exposed as
separate artifacts for review in the current website UI. Summary-length
decisions will incorporate desktop/mobile readability, scroll burden,
skimmability, perceived tractability, and completion likelihood rather than
using standalone literary richness as the only criterion.

## 2026-08-02 — Phase 2 deterministic diversified assignment

Implemented the versioned `stratified-v1` assignment policy for card passes
1–5. The policy deterministically balances claim types, categories, behavioral
domains, and canonical priority bands, then orders each pass to reduce adjacent
semantic similarity. It preserves every claim ID and priority ID and leaves
final assembly in canonical priority order. `contiguous` remains available as
the historical control and the backward-compatible default for direct SBE
calls; semantic closure now selects `stratified-v1` by default.

Every split run persists `<subject>.split-assignment.json` and records the
policy, algorithm version, subject-derived replay seed, and exact priority IDs
per pass in the run manifest. Pass-local and root bundle manifests show the
actual assignments rather than implying contiguous ranges.

On the Bre fixture, aggregate claim-type imbalance fell from 12 to 4 and
category imbalance from 14 to 6. The full 74-test suite passed. A token-free
end-to-end Bre generation produced six valid pass directories and six ZIPs;
the exact-once 50-card map was recorded with replay seed
`5a985d114fe6fba4`, and pass 6 remained summary-only.

### Live Kevin A/B

A current-code live A/B authored five contiguous and five stratified card
passes, with one byte-identical control pass 6 reused in treatment. Both decks
were assembled without polish. `stratified-v1` passed whole-deck authoring
acceptance; contiguous failed because of one exact duplicate. Treatment also
removed the control's card-level grammar error and all repeated cross-claim
sequences of ten or more words. Repeated eight-word groups fell from 12 to 4.

The result was not one-sided. Treatment had slightly lower vocabulary breadth,
slightly higher broad body similarity, slightly higher handler/hybrid lexical
overlap, and a seven-card `Kevin, you are` opening family. The policy reduces
literal carryover but does not replace claim-specific rhetorical planning.
Retain it as the semantic-closure default and continue Phase 3.

Service stress exposed three runner defects: polling timeout resubmits a still
durable background response; an omitted reconstructed story file causes a
checker crash instead of a first-class incomplete-delivery result; and resume
can demote an already accepted final attempt when its attempt number equals the
ceiling. The known pass-6 theme-group gate mismatch also reproduced. Full
analysis and examples are in
`results/PHASE 2 - Diversified Assignment Live AB.md`.
