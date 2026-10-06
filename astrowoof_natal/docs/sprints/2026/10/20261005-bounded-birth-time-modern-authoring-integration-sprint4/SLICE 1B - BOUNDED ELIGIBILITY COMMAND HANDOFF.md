# Slice 1B — Bounded Eligibility Command Handoff

**Status:** implemented provider-free; ready for API receiver and installed-wheel joined qualification.

## Decision implemented

For a valid admitted family with fewer than fifty invariant authored claims,
`astrowoof-run-bounded-natal` emits exactly one `sbe.command_result.v1` JSONL
stdout envelope. Its result uses
`astrowoof.bounded_eligibility_command_result.v1` with the closed public
disposition `ineligible`, `insufficient_invariant_basis`, non-retryable, and
`provider_activity: not_attempted`.

The path returns success after reporting a product decision. It creates no
workspace, native execution result, publication receipt, spend authorization,
or provider client. It is not a delivery or editorial-review terminal result.

`result_id` (`belig_<24 lowercase hex>`) and `result_sha256` are deterministic
canonical functions of closed content. No timestamp, candidate count or ID,
prompt, evidence text, provider setting, or diagnostic prose enters them.

## API-to-SBE invocation additions

For every new profile-bound bounded command, API must pass this all-or-none
handoff in addition to the existing processing-profile references:

```text
--native-run-id <64 lowercase hex>
--native-invocation-id <ninv_ + 24 lowercase hex>
--canonical-semantic-identity-sha256 <64 lowercase hex>
--projection-set-evidence-sha256 <64 lowercase hex>
```

The native run ID is also persisted in `run.json` when the source is eligible
and a workspace is created. Thus both branches bind the same API-persisted
native-run identity. Missing/partial values are refused before processing, and
these values are invalid on resume.

SBE validates digest syntax, the installed processing-profile binding, route
family, worker role, and invocation-ID shape. API remains the source of truth
for matching the two source-binding digests to its accepted projection set. The
current materialized SBE input has four projected graph bytes, but not API's
projection-result manifest and its member/receipt evidence. SBE therefore
does not invent a substitute projection-set digest or falsely claim to
recompute it.

## Provider-free checks

`test_bounded_eligibility.py`, registered in `test_suite_manifest.json`, proves
deterministic result identity, strict refusal of a tampered disposition, and a
single CLI envelope while provider construction and workspace creation are
prohibited.

The next joint gate needs API's positive and negative receiver fixtures:
wrong run/invocation/source/binding/result identity and a forged nonzero
provider-activity result must all fail closed without terminal state mutation.
