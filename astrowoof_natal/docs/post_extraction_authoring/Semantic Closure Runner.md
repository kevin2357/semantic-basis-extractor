# Semantic Closure Runner

`src/author_semantic_closure.py` orchestrates the AstroWoof authoring stage
between projected-chart inputs and final deck assembly.

The runner covers extraction, six independent authoring passes, per-pass
acceptance, deterministic full-deck assembly, whole-deck QA, optional surgical
polish, delivery packaging, retry, resume, and API accounting.

## Live authoring

Place the four projected context files and optional `params.json` in the input
package expected by SBE. Set the API key in the environment rather than passing
it on the command line:

```powershell
$env:OPENAI_API_KEY = "<secret>"

python src/author_semantic_closure.py `
  --input-package C:\path\to\projected-subjects `
  --subject kevin `
  --run-dir C:\path\to\runs\kevin `
  --provider openai `
  --model gpt-5.6-terra `
  --reasoning-effort medium `
  --split-assignment-policy stratified-v1 `
  --max-workers 6 `
  --max-attempts 3
```

The key is read from `OPENAI_API_KEY` by default and is never written to the
run directory. Use `--api-key-env NAME` to select a different environment
variable.

Each of the six passes receives a fresh Responses API request. The model sees
the pass as a directory of Markdown writing assignments. Structured output is
used only as a private field-value transport; Python reconstructs the supplied
Markdown files around their original field markers. The model cannot rename
files, alter source guidance, edit the bundled checker, or omit a required
field without deterministic rejection.

Passes 1–5 contain card assignments only. Pass 6 additionally receives the
versioned four-summary Kevin craft reference and a writable four-thesis plan.
The reference demonstrates coordinated identity, daily-life, needs, and growth
lenses but is not evidence about the current dog. Both files live in the
pass-local assignment tier: card passes incur no gold-reference tokens, while
the shared editorial and subject prefixes remain cache-stable across all six
passes. The completed thesis plan remains in the accepted workspace for audit
and does not alter the assembled deck schema.

By default, semantic closure uses `stratified-v1` to distribute the 50 cards
across passes 1–5. The deterministic assignment balances claim types,
categories, behavioral domains, and canonical priority bands, then orders each
pass to reduce adjacent semantic similarity. It does not change claim IDs,
priority IDs, selection semantics, or final deck order. SBE writes the complete
replay map, subject-derived seed, and algorithm version to
`<subject>.split-assignment.json` and records them in `run-manifest.json`.

Use `--split-assignment-policy contiguous` for the historical control in which
passes receive priority IDs 1–10, 11–20, and so on. Direct SBE invocation keeps
`contiguous` as its backward-compatible default; semantic closure explicitly
selects `stratified-v1` unless overridden.

### Experimental compact full-chart transport

Semantic closure preserves the historical full-chart rendering by default.
Use `--full-chart-basis-format compact-v1` for a controlled experiment with
the deterministic compact authoring map. The compact build contains:

- pass-local `FULL CHART BASIS.md`, a human-readable chart and semantic-claim
  view;
- `<subject>.compact-full-chart-basis.json` in SBE's local subject output, a
  structured sidecar retaining stable source
  references, dependencies, all distinct projection contexts, and explicit
  reconstruction limits.

The JSON sidecar is excluded from authoring ZIPs and API prompts. It exists for
deterministic audit and future consumers without adding authoring load.

Use `--full-chart-basis-format compact-v2` for the smaller author-only map.
It retains every reconstructed placement, angle, aspect, distinct projection
context, structural concentration, and projected term used by the chart, but
removes selected claims, unselected claims, dependencies, source references,
and reconstruction-limit commentary from the LLM-facing Markdown. Those
details remain in the local
`<subject>.compact-v2-full-chart-basis.audit.json` sidecar. The author map uses
a declared compact grammar, orders aspects by orb, collapses contexts only
after deterministic equality comparison, and emits context-qualified variants
when meanings genuinely differ.

`compact-v2` treats the full-chart document as temporary cognitive context,
not as a downstream semantic artifact. Individual card assignments still
receive their complete claim and evidence. The whole-chart map exists only to
help the author construct a coherent shared understanding of the dog.

The compact representation is a downstream reconstruction from projected
evidence, not a canonical natal export. It does not contact SPC or infer exact
source degrees. The legacy mode remains the production default until matched
live comparisons establish equivalent or better whole-dog and summary quality.

GPT-5.6 authoring calls use explicit prompt caching by default. The request is
ordered as a stable editorial-guidance prefix, a subject-specific full-chart
prefix, and finally the pass-local assignment. Explicit breakpoints follow the
first two tiers, and the request uses a deterministic subject cache key with a
30-minute minimum TTL. `run.json` records the static protocol and per-subject
context hashes so an accidental difference between passes fails before any API
request.

Use `--prompt-cache-mode disabled` for a controlled uncached comparison, or
`--prompt-cache-mode implicit` to retain the tiered breakpoints while allowing
OpenAI's additional implicit breakpoint. `--prompt-cache-ttl 30m` is currently
the only supported TTL value exposed by the runner.

## Concurrency and retries

`--max-workers` controls the number of independent passes in flight. The
default is six. Reduce it when an account's token-per-minute limit cannot
support all six requests concurrently.

For a fresh cached run with concurrent workers, the runner first completes the
smallest generated pass as a cache warmer. It then submits the other five in
parallel. This avoids six simultaneous cache writes for the same subject
prefix. Resume never repeats an accepted pass merely to warm the cache.

There are two retry layers:

1. Transport retries handle rate limits, selected server errors, timeouts, and
   network failures with exponential backoff. Configure them with
   `--max-transport-retries` and `--transport-backoff-seconds`. These do not
   consume creative attempts.
2. Creative retries handle malformed structured output and prose rejected by
   the bundled opaque acceptance gate. `--max-attempts` limits these fresh
   authoring attempts per pass.

An editorial retry receives only the original source workspace plus the public
issue codes, affected claim IDs, and broad guidance from the rejected attempt.
It does not continue the rejected model conversation or expose private checker
thresholds.

Pass acceptance also verifies that authored high-level and detail-level
context filters belong to the deck's fixed vocabulary. Invalid labels produce
the opaque `invalid_context_filter` issue code and a fresh pass retry before
the deck reaches assembly. As a defense for legacy workspaces, assembly removes
only unregistered or duplicate labels, records every removal in the assembly
report, and preserves all valid assignments in their original order.

Before the opaque editorial checker runs, the runner verifies that every
expected writable file and field is present and populated. Missing material is
reported as `incomplete_delivery`, with the missing paths retained in the run
ledger for the next creative attempt. Pass 6 additionally enforces the final
deck contract for aspect/synthesis chapters: independent section-scoped
registries with three to five theme groups per section, each containing at
least two cards, with the largest group no more than twice the size of the
smallest. Interdogpendence and Takeaways may not reuse or trivially reorder
chapter titles.

Fatal request problems such as authentication, permission, and invalid-request
errors stop the affected pass immediately rather than repeating an identical
billable request.

## Model routing

Fixed routing remains the default and preserves the established behavior: the
model and reasoning effort selected with `--model` and
`--reasoning-effort` author every pass and perform polish.

Use `--routing-policy cost_optimized` to route by editorial risk:

- first authoring attempts default to `gpt-5.6-luna` at medium reasoning;
- passes rejected by creative QA retry with `gpt-5.6-terra` at medium
  reasoning;
- sparse whole-deck polish uses `gpt-5.6-luna` at low reasoning.

These defaults are independently configurable with `--model`,
`--reasoning-effort`, `--retry-model`, `--retry-reasoning-effort`,
`--polish-model`, and `--polish-reasoning-effort`. For example:

```powershell
python src/author_semantic_closure.py `
  --input-package C:\path\to\projected-subjects `
  --subject ella `
  --run-dir C:\path\to\runs\ella-routed `
  --provider openai `
  --routing-policy cost_optimized `
  --polish
```

The full route configuration is part of the resume contract. Every response
records its route, requested model, and reasoning effort, while aggregate
accounting reports attempts, tokens, and cost by model. A rejected inexpensive
attempt therefore remains visible in expected-cost comparisons rather than
being hidden by the successful escalation.

## Optional Batch service level

Use `--service-level batch` for asynchronous authoring that can tolerate the
Batch API's 24-hour completion window. Interactive Responses remain the
default. Batch mode uploads one JSONL request file for every model-homogeneous
round, submits it to `/v1/responses`, persists the input file ID and Batch ID,
then resolves returned rows by their unique pass-and-attempt `custom_id`.

```powershell
python src/author_semantic_closure.py `
  --input-package C:\path\to\projected-subjects `
  --subject ella `
  --run-dir C:\path\to\runs\ella-batch `
  --provider openai `
  --service-level batch `
  --routing-policy cost_optimized
```

The Batch API requires every request in an input file to use one model.
Consequently, cost-optimized routing creates a Luna initial round and, only
when needed, a later Terra retry round containing rejected or missing passes.
Accepted passes are never resubmitted. Every returned pass still passes
through the same local workspace reconstruction and opaque acceptance checker
used by interactive mode.

Add `--batch-detach` for a web-worker-friendly invocation. The command submits
or refreshes one active round, saves its lifecycle state, and exits. Invoke the
same command with `--resume --batch-detach` to poll without holding a process
open; omit `--batch-detach` on a later resume to wait through remaining rounds.
`--batch-poll-interval-seconds` controls blocking-mode polling.

Batch accounting applies the documented 50% service discount independently
to each returned response. It records cached input only when OpenAI reports
cached tokens; the runner does not assume that prompt-cache and Batch
discounts combine. Explicit cache-control fields are intentionally omitted
from Batch request files. Sparse whole-deck polish remains an interactive
Responses call because it is conditional on assembled-deck QA and already
transports only targeted fields.

## Assembly and final QA

After all six passes for a subject are accepted, the runner copies them into an
isolated assembly directory, reconstructs `natal.<subject>.cards.json` from the
locked SBE packet, runs structural validation, and runs the whole-deck
editorial linter.

Structural validation errors always stop direct delivery. When `--polish` is
enabled, fixable editorial validation errors may enter the same bounded
recovery loop as lint findings. Validator warnings remain advisory and are
preserved in the report; whole-deck linter warnings determine whether polish
must continue. By default, unresolved lint warnings leave the subject in
`FINAL_QA_REQUIRES_REVIEW`; the best valid baseline remains available under
`final/<subject>/`. Use `--allow-lint-warnings` when linter warnings should be
reported but should not block packaging.

The delivery ZIP contains the cards JSON, assembly report, structural
validation report, and whole-deck lint report. Multi-subject runs assemble and
validate each subject independently.

## Optional whole-deck polish

Add `--polish --max-polish-attempts 2` to let an OpenAI run make bounded,
surgical corrections when final validation fails or the whole-deck linter
warns. Polish resolves the structured validation and lint findings to an exact
allowlist of affected reader-facing field paths. The model receives those
editable values, compact claim/source grounding, and narrowly related prose as
read-only context. It returns a sparse list of replacements rather than the
entire deck. A target omitted from the list is an explicit preservation
decision. When structural validation already passes, an empty edit list records
`POLISH_NO_CHANGE`, stops further polish attempts, and leaves the accepted deck
byte-for-byte untouched. This lets a context-aware editor decline to damage
strong prose merely because a lexical heuristic produced an advisory.

For targeted cards, the repair basis includes a compact semantic mechanism
derived from locked evidence: relevant operators, projected modes and domains,
aspect geometry, participating subsystems, interaction modes, and synthesis
supports. Raw projected graphs remain excluded. A replacement must repair the
named finding while retaining the strongest existing image, behavioral insight,
useful guidance, and every supplied semantic contribution. Concision removes
duplicated labor; it does not require automatic shortening.

Unknown paths, duplicate edits, blank replacements, and locked
fields are rejected before validation. Evidence, claim selection, categories,
filters, identity, and all other non-authoring data remain unavailable for
editing. Theme groups remain unavailable unless the validator explicitly
reports invalid balance; that repair exposes only existing theme-group fields.
Summary prose remains locked unless a deterministic finding explicitly adds
that exact summary field to the sparse edit allowlist.

The first attempt targets only fields named or implicated by deterministic
findings. If it does not improve QA, a second attempt may expand to other
reader-facing fields on those same affected cards, never to unrelated cards.
Each attempt records editable-target count, read-only context count, full-deck
field count, estimated full-versus-sparse input/output sizes, edited-field
count, and omitted-target count.

Python applies the returned fields to a copy of the accepted baseline and runs
the validator in polish mode. The first candidate that repairs an invalid
baseline may replace it only when structural validation passes. After a valid
baseline exists, a candidate replaces the current best deck only when its
whole-deck finding count is strictly lower. That count combines ordinary
linter warnings with unresolved deterministic authoring-rejection classes such
as exact cross-card duplication, repeated long passages, editorial insertion
artifacts, and multi-field opening templates. The target resolver reads both
the ordinary warning list and the nested authoring-acceptance report, so a
known collision cannot disappear from polish merely because it is reported in
a different linter section. The original assembly
therefore remains safe when polish fails, and accepted improvements remain safe
when a later attempt fails. Polish stops early at zero linter warnings.

Recovery compares candidates by structural error count before lint-warning
count. A candidate that removes structural errors but does not yet pass the
validator becomes the next working baseline as `POLISH_IMPROVED_PARTIAL`.
Subsequent attempts therefore address the remaining blocker instead of
discarding useful repairs. Theme-group rebalancing never triggers broad prose
expansion across every themed card; only explicit lint targets and theme-group
fields remain editable.

On resume, persisted validation and lint reports define the current best state.
Exhausted polish budgets do not create another response; a valid, zero-lint
persisted deck proceeds directly to delivery packaging.

`--allow-lint-warnings` may be combined with `--polish` to package the best
structurally valid result when the bounded polish budget does not reach zero.

## Background execution and resume

Background Responses are enabled by default. The runner polls queued and
in-progress responses until completion or until the local polling window ends.
Ending the local window does not cancel the OpenAI response and does not consume
a creative attempt. The pass and run enter `WAITING_FOR_RESPONSE`, preserving
the response ID and unfinished attempt for a later resume. Use `--foreground`
only for controlled testing.

The response ID is persisted as soon as OpenAI creates a background job. If
the runner process stops before the response completes, rerun the command with
the same provider configuration and `--resume`:

```powershell
python src/author_semantic_closure.py `
  --run-dir C:\path\to\runs\kevin `
  --provider openai `
  --model gpt-5.6-terra `
  --reasoning-effort medium `
  --max-workers 6 `
  --max-attempts 3 `
  --resume
```

An interrupted attempt resumes polling its existing response ID. It does not
issue a second response-creation request. Accepted passes are also skipped.
Durable acceptance evidence (`accepted_attempt`, its successful QA report, and
the accepted workspace) is normalized back to `PASS_QA_ACCEPTED` if stale run
state ever disagrees, so resume cannot demote an already accepted pass.
Provider, model, reasoning, background, base-URL, output-token, and attempt
settings must match the original run.

## Run artifacts

The run directory contains:

```text
run.json
sbe/
  sbe-invocation.json
  semantic-basis-output/
  llm-handoff-bundle/
passes/
  <subject>_1/
    source/
    attempt-001/
      openai-request.json
      openai-workspace-prompt.txt
      openai-background-response.json
      openai-response.json
      openai-authored-fields.json
      authoring-pass-acceptance.json
      response/
    accepted/
  ...
  <subject>_6/
batches/
  round-001/
    batch-input.jsonl
    batch-object.json
    batch-output.jsonl
    batch-errors.jsonl  # only when request-level errors are returned
final/
  <subject>/
    accepted-passes/
    natal.<subject>.cards.json
    natal.<subject>.assembly-report.json
    natal.<subject>.validation-report.json
    natal.<subject>.lint-report.json
    polish/
      attempt-001/
    astrowoof-<subject>-delivery.zip
```

`run.json` is written atomically and records pass states, subject delivery
states, authoring and polish attempts, response IDs, model settings, token
usage, estimated cost, QA reports, and delivery paths. The estimate uses a
versioned local model-rate table and is useful for run comparison; the OpenAI
usage dashboard remains authoritative.

Accounting is also divided into `authoring_initial`, `creative_retries`, and
`polish` stages. Each stage records request counts, accepted attempts, response
IDs, cache-hit ratio, prompt-size estimates, usage, and estimated cost. A
completed delivery additionally reports estimated cost per card and per deck.
Explicit cache-write tokens are priced separately at 1.25 times ordinary input
in the local GPT-5.6 estimate.

Completed but malformed responses retain their response ID and token usage in
the ledger, so failed creative attempts remain visible in total cost.

## Token-free prompt layout report

Generate the SBE workspaces and measure the exact prompt strings and response
schemas without contacting OpenAI:

```powershell
python src/author_semantic_closure.py `
  --input-package C:\path\to\projected-subjects `
  --subject ella `
  --run-dir C:\path\to\runs\ella-prompt-report `
  --prompt-layout-report C:\path\to\ella-prompt-layout.json
```

The report gives character count, UTF-8 byte count, stable SHA-256, and a
dependency-free token estimate for the system instructions, user message,
workspace rendering, and strict response schema. It also shows whether each
segment is byte-identical across all six passes. The estimate uses UTF-8 bytes
divided by four and is intended for relative planning only; API response usage
is the billing measurement.

The file inventory lists every Markdown source by prompt tier and reports exact
cross-pass duplication. SBE compacts the authoring surface before this report:
the full-chart basis retains every selected and unselected claim, source
reference, dependency, score, and the complete projected-term registry without
repeating each claim's full evidence record. Claim-specific evidence remains in
its story directory. When multiple voice contexts render the same projected
evidence, one visible record names every context that uses it; genuinely
different voice projections remain separate. The registered filter vocabulary
lives once in the shared authoring brief instead of once per story.

## Compare run cost

Compare any two completed or partial run ledgers without creating a run or
making an API request:

```powershell
python src/author_semantic_closure.py `
  --compare-cost-runs C:\baseline\run.json C:\candidate\run.json `
  --cost-report-output C:\reports\cost-comparison.json
```

The comparison includes stage accounting, token deltas, estimated dollar
savings, and savings ratio. This is the acceptance report used for prompt-cache
and sparse-polish optimization work.

## Token-free workflow test

The deterministic fake provider exercises the same SBE, concurrency, workspace
reconstruction, acceptance, retry, assembly, final QA, delivery, and resume
machinery without contacting OpenAI:

```powershell
python src/author_semantic_closure.py `
  --input-package C:\path\to\projected-subjects `
  --subject kevin `
  --run-dir C:\path\to\runs\kevin-dry-run `
  --provider fake `
  --max-workers 6
```

Use `--fake-reject kevin_2:1` or `--fake-error kevin_4:2` to exercise
editorial-rejection and provider-error retry paths.
