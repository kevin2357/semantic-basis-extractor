# SBE LLM Prompt Versioning — Slice 0 Findings

## Scope and conclusion

This is an investigation of the current SBE authoring path only. No prompt,
provider request, model configuration, checkpoint, package, or deployment was
changed.

Prompt versioning is worth doing, but the right abstraction is a **prompt
release binding**, not a loose ``--prompt-version`` string. The binding must
identify the exact approved prompt assets and their canonical digests before
the first provider action, then persist that identity with the action/run so a
retry or resume cannot silently select newer wording.

## Current path

`OpenAIResponsesProvider._prompt()` in `closure.py` builds the request from:

- a literal system instruction embedded in Python;
- workspace material partitioned into static guidance, subject context, and
  pass-specific assignment documents; and
- optional retry feedback serialized into the pass assignment portion.

The provider then combines this geometry with the response schema. The
workspace content is deliberately authoritative for the individual assignment,
so prompt versioning cannot mean hashing one system string and declaring the
whole request frozen. It must distinguish reusable prompt assets from
job-specific workspace evidence and from retry feedback.

The production-relevant provider-construction inventory is:

| Route/path | Current selection source | Binding implication |
| --- | --- | --- |
| exact ordinary authoring | `closure.py` creates initial and, under cost-optimized routing, retry/polish/critic providers | One release maps every applicable stage; model routing is not prompt provenance. |
| exact external-authority v2 | The CLI rebuilds a provider from an exact sealed action binding and persisted request material | Resumed/authorized work must use persisted binding, never a current default. |
| bounded authoring | `bounded_run` creates `OpenAIBoundedLifecycleProvider`, delegating to `OpenAIResponsesProvider` | Bounded releases require explicit route compatibility; they cannot inherit exact assets by implication. |
| qualification/recovery helpers | Provider-free utilities construct synthetic providers | They validate registry behavior but never define production defaults. |

Current request metadata already records token-free layout information and a
rendered workspace-prompt SHA-256. That is useful evidence but not reusable
asset provenance. The release binding should extend, not replace, those request
digests.

There is useful existing custody behavior: request payloads and the full
workspace prompt are written to private attempt files
(`openai-request-payload.private.json` and `openai-workspace-prompt.txt`),
while public metadata uses a placeholder. The external-authority-v2 recovery
path also knows how to re-open that persisted full prompt. This supports exact
historical recovery, but it is not a release-selection mechanism.

The editorial-review contract already models the target provenance shape:
`prompt_template_id`, `prompt_template_version`,
`prompt_template_sha256`, and `rendered_request_sha256`. In this repository
those fields are currently exercised by synthetic editorial fixtures and their
schema/QA validators. Slice 0 found no corresponding ordinary runtime producer
that stamps those four values onto every live authoring action. Treat the
fixture contract as a useful consumer target, not proof that live prompts are
already versioned.

## Recommended prompt-release contract

Create a canonical non-secret registry whose release entry contains:

- a stable release ID and semantic version;
- the canonical SHA-256 of each prompt asset and a digest of the release map;
- stage mapping (initial, retry, polish, and any other provider-writing stage);
- allowed routes, processing-profile IDs, model/routing constraints, and
  allowed environments;
- active/deprecated status; and
- asset location within a qualified immutable package/release bundle.

The parent processing profile should select one prompt release. The release may
map a stage to several components (system guidance, shared editorial guidance,
and a stage wrapper) rather than pretending dynamic workspace evidence is a
template file. At request construction SBE should compute and retain:

1. prompt release ID/version/digest;
2. the component asset digests actually selected for the stage; and
3. a digest of the fully rendered provider request.

The first two are safe provenance. The last verifies the concrete request
without placing prompt text, dog data, feedback, provider output, or secrets in
normal logs. Existing private attempt custody can continue to hold the full
rendered request under its established access boundary.

## Selection and precedence rules

For a new job, API admission should bind the profile and thereby its prompt
release before any provider action is prepared. SBE may expose a CLI selector
for local/qualification use, but it must resolve through the same registry and
cannot bypass route/profile/environment compatibility checks.

For a resumed or reconciled run, the persisted release ID and digest win. A
conflicting CLI value, an unavailable asset, a changed asset under the same
version, or a release/profile incompatibility must fail closed before a new
provider request. There must be no “use current default” fallback. A creative
retry or polish attempt may use a stage-specific asset from the *already bound*
release, but it must record its own exact component and rendered-request
digests.

This preserves the historical recovery path: existing workspaces with their
already-persisted private prompt material remain recoverable under the legacy
rules. The new release binding applies at new action creation; it must not
rewrite old workspace evidence or infer a new release for it.

## Asset and packaging considerations

Prompt assets should be ordinary package resources or equally immutable release
assets, read as canonical UTF-8/LF bytes before hashing. The project has
already encountered line-ending packaging drift in fixture assets; prompt
provenance must therefore validate the bytes installed in the candidate wheel,
not merely bytes in a source checkout. A mutable remote prompt document or a
``latest`` alias would defeat the point of the binding.

No prompt text belongs in structured normal logs. Useful safe event fields are
release ID/version, release digest, component digest inventory, rendered
request digest, model identifier, route, stage, and action identity. Do not
include field text, feedback, subject names, workspace paths, raw exception
prose, API keys, or provider response text.

## Gate A test matrix for a later slice

Provider-free tests should prove all of the following before a live prompt
experiment:

- current behavior is reproduced by an explicit compatibility release;
- a selected valid release reaches each applicable stage with the expected
  provenance and rendered-request digest;
- unknown, deprecated, wrong-environment, wrong-route, and wrong-profile
  releases are refused before provider request creation;
- an altered installed asset fails digest verification;
- retry/polish preserve the bound release but retain stage-specific provenance;
- resume/reconciliation refuses a missing or mismatched bound release; and
- existing legacy workspaces recover through their persisted historical
  request path without synthetic backfill.

## Slice 0 decision

Prompt wording changes—such as improving direct-to-dog/full-astrology density—
should wait until this provenance boundary is designed and qualified. The
immediate next discovery question is which durable action/run records can carry
the release binding without weakening existing spend-authority and replay
semantics.
