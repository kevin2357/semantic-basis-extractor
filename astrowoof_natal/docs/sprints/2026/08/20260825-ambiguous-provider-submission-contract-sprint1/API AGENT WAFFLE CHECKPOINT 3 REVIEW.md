# API Agent Waffle Checkpoint 3 Review

Status: approved in direction; one narrow consumer-CLI correction requested before
Waypoint 4 release qualification.

## What is now ready

Waypoint 3 exposes the correct public consumer boundary:

- closed dispatch result v3 and command result v2 validators are root-level
  package exports;
- `astrowoof-provider-dispatch-result` is a genuinely provider-free
  validation/export command, with no workspace, grant, credential, provider,
  URL, response, or submission option;
- the consumer handoff correctly distinguishes pre-provider refusal, recognized
  ambiguity, detached provider-pending custody, exact replay, and malformed
  evidence;
- the aggregate-refusal handoff correctly describes a provider-bound prefix, a
  causal refusal, and provably unentered suffix members; and
- the consumer manifest binds the v3 schema, command-result v2 schema, and
  sanitized fixture bundle with hashes.

The API disposition table is adoptable as written. In particular, the API must
not turn `pre_provider_refusal` into an implicit retry; it releases only the
exact proven-unspent reservation(s), preserves grant audit evidence, and waits
for a fresh inspection/authority decision. `ambiguous_submission` remains a
review-custody outcome, while `detached_provider_pending` remains
reconciliation-only.

Focused independent replay passed:

```text
17 tests passed, 1 optional-jsonschema skip
```

and `git diff --check` passed.

## Required narrow correction

The CLI's `--input` route recognizes the fixture-bundle schema but manually
loops over `cases` rather than calling
`read_ambiguous_provider_submission_fixture_v1()`'s strict fixture-bundle
validator (or an equivalent shared value validator).

As written, a caller-supplied bundle with an empty `cases` list, extra root
keys, malformed case envelope, or duplicate case names can be accepted by the
CLI even though the advertised packaged reader correctly rejects it. That is a
small but real mismatch with the stated **strict validation/export** consumer
surface.

Please factor/use one strict fixture-bundle validator for both packaged reading
and CLI `--input` validation, and add a CLI regression covering at least an
empty bundle and one malformed/extra-key bundle. The CLI should fail before it
writes an output file.

This is not a request to expand the contract or revisit Waypoint 2 behavior.
After that correction, Waypoint 3 is approved for the planned installed-wheel
and release qualification.
