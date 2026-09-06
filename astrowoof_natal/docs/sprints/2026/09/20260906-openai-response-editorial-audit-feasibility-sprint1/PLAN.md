# Plan

Status: Slices 0–3 complete. All eight exact Frisbee Responses were retrieved
read-only and preserved privately. The pinned generation-11 checkpoint passed
archive/inventory verification, and the released production assembly,
validation, lint, and sparse-polish functions reproduced the complete retained
deck lineage exactly. No runtime or release change is proposed.

## Slice 0 — Build the audit manifest from existing evidence

Parse the saved SBE worker trace into a deterministic, closed manifest containing:

- API run, native run, subject, stage, attempt, and native action identity;
- provider response identity and create/retrieval observation times;
- native acceptance/rejection summary and its digest where logged; and
- an explicit stage inventory for initial wave, creative retries, critic,
  candidate, and polish, including `none_observed` where applicable.

The manifest must distinguish absent evidence from a stage that provably did not
occur. It must contain no prompts or response content.

## Slice 1 — Exact read-only OpenAI retrieval experiment

Using the existing project credential and exact logged response IDs, issue only
read-only `GET /v1/responses/{response_id}` calls for the complete observed
inventory: six initial responses and two polish responses. Include all creative
retry responses when that stage exists; Frisbee has none.

Record per identity:

- retrieved or unavailable;
- returned response ID exactly matches the requested ID;
- provider status, model, creation time, structured-output presence, and usage;
- response JSON SHA-256; and
- sanitized local output path.

Do not create, cancel, retry, delete, or mutate any provider object. Preserve raw
response content only in a private ignored working directory; sprint evidence
contains identities, hashes, and bounded summaries only.

## Slice 2 — Reconstruct the editorial comparison packet

Join each retrieved provider response to its exact native action and recorded
editorial disposition. Determine what can be evaluated from provider output
alone and what still requires native assembled-deck/report evidence.

For polish, compare both attempts rather than examining only the rejected final
attempt. If creative retries exist for a sampled run, include every attempt in
lineage order. Never infer that a provider response is identical to the assembled
deck SBE evaluated.

### Existing-code replay path

Use the released `0.4.50` production functions as the semantic oracle. This does
not prohibit audit-specific scripts: the sprint may create purpose-built parsers,
orchestration, comparison, provenance, and reporting tools, and may stage inputs
in an audit-friendly directory. Such tooling must call or faithfully expose the
existing production assembly and QA operations rather than quietly defining a
second set of assembly or acceptance semantics:

1. Extract each Response's JSON output through `response_output_text()`.
2. Apply each initial authored-field map to its exact source pass workspace with
   `apply_authored_fields()` and require completeness.
3. Assemble the six accepted pass workspaces against the exact selected authoring
   packet with `assembly.assemble(..., allow_partial=False)`.
4. Run the existing structural validator and editorial linter on the baseline.
5. Apply polish attempts in lineage order with `apply_sparse_polish()` using the
   exact target paths/baseline reports, rerunning validation and lint after each.

The raw Responses do not carry the exact selected packet, source pass workspaces,
or the top-level request input. Therefore provider-only evidence can inspect what
the model returned, but cannot by itself prove the exact assembled deck or
reproduce the pipeline's editorial decision. Exact replay requires a bounded
native checkpoint/artifact read or an already promoted equivalent.

Audit-specific tools may also provide exploratory views that production code does
not—for example field-level diffs, attempt timelines, warning deltas, and readable
summaries—provided those views remain derived evidence and never replace the
production validation/lint result.

## Slice 3 — Feasibility conclusion

Classify the approach:

- `provider_only_sufficient` for the intended question;
- `provider_plus_public_native_summary_sufficient`;
- `assembled_deck_required`; or
- `evidence_unavailable`.

Recommend the smallest repeatable audit workflow and identify whether separately
persisting a neutral final evaluated deck would materially improve future audits.
No runtime implementation or release follows automatically from this conclusion.

## Pause points

- Pause if credentials are unavailable or any read would require broader access
  than exact response retrieval.
- Pause before retrieving more than the closed manifest inventory.
- Pause before proposing storage, logging, schema, or editorial-policy changes.
