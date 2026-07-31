# Semantic Closure Runner

`src/author_semantic_closure.py` orchestrates the AstroWoof authoring stage
between projected-chart inputs and final deck assembly.

Phase 2 covers extraction, six independent authoring passes, per-pass
acceptance, retry, resume, and API accounting. Full-deck assembly, whole-deck
QA, and the optional surgical polish pass belong to Phase 3.

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
```

`run.json` is written atomically and records pass states, attempt history,
response IDs, model settings, token usage, and estimated cost. The estimate
uses a versioned local model-rate table and is useful for run comparison; the
OpenAI usage dashboard remains authoritative.

Completed but malformed responses retain their response ID and token usage in
the ledger, so failed creative attempts remain visible in total cost.

## Token-free workflow test

The deterministic fake provider exercises the same SBE, concurrency, workspace
reconstruction, acceptance, retry, and resume machinery without contacting
OpenAI:

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
