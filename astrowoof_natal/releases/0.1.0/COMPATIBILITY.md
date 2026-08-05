# AstroWoof Natal Authoring v0.1 Compatibility

## Supported boundary

`astrowoof-natal-authoring 0.1.0` is a dependency-free, pure-Python wheel for
Python 3.11 or newer. The release was built and fully verified with CPython
3.12.13 on Windows. Its wheel tag is `py3-none-any`; however, a Linux worker
image must still run `astrowoof-release-smoke --require-installed` before being
promoted because this sprint did not execute a Linux container smoke test.

The supported executable interfaces are:

- `astrowoof-semantic-closure` — durable six-pass authoring orchestration;
- `astrowoof-build-natal-basis` — deterministic extraction/handoff generation;
- `astrowoof-release-smoke` — installed-runtime deterministic acceptance.

The internal Python module layout is not a public API in v0.1. API workers
should invoke the CLI and consume the versioned JSON contracts.

## Input compatibility

Preferred input uses `astrowoof.projected_natal_input.v0.1`. The release also
accepts the legacy four-file projected directory and normalizes it internally.
Unversioned historical `params.json` files normalize to
`astrowoof.subject_params.v0.1`.

The controlled live baseline used four SPC 0.10.0 projections carrying AGF
graph version 1.3.0. These versions are recorded provenance evidence, not a
claim that every future upstream version is automatically compatible. New
upstream releases should run deterministic fixture QA and a controlled live
sample before promotion.

## Run and delivery compatibility

- New operator state: `astrowoof.semantic_closure_run.v0.7`.
- Historical operator states v0.2–v0.6 remain resumable through documented
  in-memory migration.
- Public polling: `astrowoof.semantic_closure_public_run.v0.1`.
- Delivery: `astrowoof.natal_delivery_manifest.v0.1` with deck, assembly,
  validation, lint, and manifest artifacts.
- Existing source-tree scripts remain compatibility shims in v0.1.

Readers may ignore additive optional fields within a contract version. Any
required-field, naming, or meaning change requires a new contract version.

## Known boundaries

- AGF and SPC are not bundled or executed by this wheel.
- The worker must provide four completed projected contexts and subject params.
- The OpenAI key is supplied through `OPENAI_API_KEY`; credentials are never
  part of inputs, run state, public state, or delivery artifacts.
- Distributed leases, queues, object storage, authentication, quotas, and HTTP
  endpoints belong to the future AstroWoof API service.
- Only one worker may mutate a run directory at a time.
