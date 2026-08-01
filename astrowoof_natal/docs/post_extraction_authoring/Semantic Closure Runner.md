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

## Concurrency and retries

`--max-workers` controls the number of independent passes in flight. The
default is six. Reduce it when an account's token-per-minute limit cannot
support all six requests concurrently.

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

Fatal request problems such as authentication, permission, and invalid-request
errors stop the affected pass immediately rather than repeating an identical
billable request.

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
warns. Polish receives the validation report, lint report, and an exact map of
reader-facing prose fields. It cannot return edits to evidence, claim
selection, categories, filters, identity, or other locked data. Theme groups
remain unavailable unless the validator explicitly reports that their balance
is invalid; in that case only existing theme-group fields are added to the
strict transport for rebalancing.

Python applies the returned fields to a copy of the accepted baseline and runs
the validator in polish mode. The first candidate that repairs an invalid
baseline may replace it only when structural validation passes. After a valid
baseline exists, a candidate replaces the current best deck only when its
whole-deck linter warning count is strictly lower. The original assembly
therefore remains safe when polish fails, and accepted improvements remain safe
when a later attempt fails. Polish stops early at zero linter warnings.

On resume, persisted validation and lint reports define the current best state.
Exhausted polish budgets do not create another response; a valid, zero-lint
persisted deck proceeds directly to delivery packaging.

`--allow-lint-warnings` may be combined with `--polish` to package the best
structurally valid result when the bounded polish budget does not reach zero.

## Background execution and resume

Background Responses are enabled by default. The runner polls queued and
in-progress responses until completion. Use `--foreground` only for controlled
testing.

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
