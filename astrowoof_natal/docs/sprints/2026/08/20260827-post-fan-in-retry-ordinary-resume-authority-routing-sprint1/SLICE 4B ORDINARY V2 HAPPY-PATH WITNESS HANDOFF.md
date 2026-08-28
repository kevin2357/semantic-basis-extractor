# Slice 4B Ordinary-v2 Happy-path Witness Handoff

Status: implemented and provider-free source qualification complete; API review
required before release qualification resumes.

## Public surface

SBE now publishes two representative real-engine witnesses through:

- Python readers/runners/validators exported from `astrowoof_natal_authoring`;
- `astrowoof-ordinary-v2-happy-path-qa`;
- `astrowoof.ordinary_v2_happy_path_qualification.v1`;
- `astrowoof.ordinary_v2_happy_path_bundle.v1`; and
- the packaged `astrowoof.ordinary_v2_happy_path_fixture.v1` fixture.

The CLI defaults to the closed qualification receipt. `--bundle`, `--fixture`,
`--schema`, and `--bundle-schema` expose the other closed public artifacts.
`--output` refuses a destination inside a native SBE workspace.

## Witness 1 — out-of-order ordinary retries

The first witness starts with two provider-bound creative retries. The later
submitted action completes first. SBE retrieves the due actions, advertises and
consumes only the completed action's exact local operation, and keeps the earlier
action in provider custody. Its prepared successor therefore remains masked from
authority. After the earlier retry completes and its local operation is consumed,
both co-ready successors appear as one lexical aggregate `ordinary_action_set`.

The aggregate request/grant is one admission envelope, not one paid action. Each
member retains its distinct binding, authorization document, SBE paid action, and
API reservation authority. Dispatch creates both scripted operations and exact
replay performs no additional create or local consumption.

## Witness 2 — retry to qualitative critic

The second witness retrieves and consumes one creative retry, then invokes the
production `SpendController` callback to prepare an enabled
`qualitative_critic` action. The distinct ordinary-v2 request is granted and
dispatched through the real constrained executor. The endpoint is truthfully
`detached_provider_pending`; it does not claim API reader delivery.

Qualitative critic was selected instead of polish because it provides an honest,
supported downstream ordinary Response boundary without fabricating a deck QA
failure solely to force polish. The fixture does not imply that critic product
policy is SBE-owned.

## Digests and privacy

Each witness has canonical evidence and receipt digests. The bundle binds the
canonical qualification receipt and packaged fixture. Authority projection
carries semantic request/grant digests, ordered action IDs, and exact per-member
binding/document digests. Raw request/grant digests include native workspace
identity and are intentionally not copied into the reproducible public projection.

The public artifacts contain no workspace paths, raw run state, provider IDs,
prompts, provider payloads, credentials, protected provenance, or retained-QA
data. Provider interactions are local scripted callbacks only. External network
calls and spend are zero.

## Consumer boundary

These artifacts are observational qualification evidence. They do not authorize
the API to choose SBE commands, reconstruct private checkpoint state, create
provider work, or manufacture authorization documents. API must continue to use
the native lifecycle-selected command and exact external-authority contracts.
