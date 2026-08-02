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
