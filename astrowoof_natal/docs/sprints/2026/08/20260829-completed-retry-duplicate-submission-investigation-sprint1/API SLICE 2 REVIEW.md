# API Slice 2 Review

## Decision

Approved to proceed to Slice 3. This review covers the provider-free native
fence implementation only; it does not authorize a release, retained-QA
recovery, provider access, or a new provider create.

The focused working-source test suite passed:

```text
test_completed_retry_duplicate_submission_slice2.py
Ran 3 tests — OK
```

`git diff --check` also passes. The first attempted test invocation used the
installed 0.4.29 wheel and correctly failed to import this uninstalled Slice 2
module; the passing result above is against the working source tree.

## Findings

### 1. Typed generic refusal is the correct SBE-side fence

The refusal is closed, digest-bound, has no provider I/O, returns exit zero,
and leaves the workspace byte-for-byte unchanged in the focused test. Its exact
identity is sufficient for API audit and routing:

- native run;
- checkpoint basis and snapshot digests;
- lifecycle state revision; and
- canonical action inventory.

It is deliberately not a v2 grant/result pair. API must treat it as a request
to obtain a *fresh* lifecycle inspection, never as a grant or as an authority
to retry generic resume.

### 2. The generic-refusal API consumption remains a required downstream seam

Current API `ProcessSbeProviderRuntime.resume()` treats any exit-zero command
as `None`; its stdout capture currently recognizes only the terminal-review
command envelope. Consequently, API cannot yet consume
`astrowoof.generic_provider_dispatch_refusal.v1` as a typed disposition. If a
legacy generic caller reaches this defensive fence today, it could otherwise
return successfully, re-inspect unchanged state, and eventually schedule the
same generic invocation again.

This is not a reason to weaken the SBE fence. It is a specific Slice 3/API
integration requirement:

1. publish an API-shaped fixture for this refusal;
2. add a strict API reader/capture path for this exact schema;
3. map it to fresh lifecycle inspection and the selected v2 dispatch path;
4. prove the generic command is not requeued as an ordinary successful resume;
   and
5. prove an ordinary v0.8 external-authority selection reaches that v2 path
   without relying on this defensive fallback.

The release notes should state that the new SBE public schema requires its API
consumer before live legacy-generic invocation is enabled.

### 3. Local-work contradiction is compatible with the existing terminal path

The terminal-review command result exits with code 2 only after the v0.2 native
result and immutable receipt are sealed. This is compatible with the current
heartbeating API runtime: it captures the terminal-review command envelope and
accepts exit 2 only when that exact envelope is present. The API native-result
validator already accepts the new `local_work_progress_contradiction`
cause code through the released v0.2 result shape and retains exact
provider/reservation custody for terminal ingress.

Slice 3 should nevertheless include an API-shaped end-to-end fixture proving
that the result is ingested as `review_required`, rather than being reduced to
`sbe.dependency.command_failed`, with the provider-bearing action retained for
the proper follow-up path.

## Requested Slice 3 fixtures

Please publish provider-free, installed-wheel-fixture-ready JSON for both
outcomes:

1. one exact generic provider-dispatch refusal with the stable reason code and
   no mutation/publication; and
2. one `local_work_progress_contradiction` v0.2 terminal-review publication
   plus command envelope, including a provider-bearing action disposition.

No protected workspace, prompt, provider payload, secret, or retained-QA data
is needed in either fixture.
