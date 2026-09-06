# Evidence

## Initial source

- Trace export: `C:\Users\kevin\Downloads\sbe logs.txt`
- SHA-256: `7b3729c2801da39fa27eae56e0dc3c2023e998729618df84236dde0147f493f1`
- SBE release observed: `0.4.50`
- SPC release observed: `0.11.1`

## Initial findings

- Provider response identities are logged after a successful POST returns and
  again during retrieval; native action identity exists before call entry.
- Frisbee has two logged polish provider identities.
- Its terminal inventory contains six `authoring_initial` and two `polish`
  actions. No creative-retry, critic, or candidate action is observed.
- The final polish response was adopted and reported before the editorial
  rejection; this is suitable for an audit, not a recovery operation.

## Exact retrieval result

On 2026-09-06, eight exact `GET /v1/responses/{response_id}` requests succeeded
with HTTP 200. No provider object was created, cancelled, retried, deleted, or
modified. Each returned object had `status=completed`, `store=true`,
`background=true`, and `model=gpt-5.6-luna`.

The raw response bodies were saved byte-for-byte under:

`C:\tmp\astrowoof-frisbee-openai-audit-20260906\raw`

They contain generated content and are intentionally outside the repository.
Their exact hashes and joins are recorded in `AUDIT MANIFEST.md`.

The retrieval confirms that the response objects remain available and contain
the complete model output plus usage and response metadata. They do not contain
the original input as a top-level `input` field. Reasoning output items exist,
but these responses expose no plaintext reasoning-summary text.

## Source feasibility findings

No implementation change is needed to replay production assembly or editorial
QA. The current source already exposes the complete deterministic chain:

- `response_output_text()` extracts the structured model result;
- `apply_authored_fields()` reconstructs each pass workspace from its source;
- `assembly.assemble()` combines six accepted pass workspaces with the selected
  authoring packet;
- `validation.py` and `editorial_lint.py` evaluate the assembled or polished
  deck; and
- `apply_sparse_polish()` applies only the validator-selected edit paths.

The downloaded OpenAI objects do not include the original request input, selected
authoring packet, source pass archives/workspaces, assembled baseline, or its
exact validation/lint reports. These are required inputs, not missing code. Thus:

- provider-only review is sufficient to inspect the six authored maps and both
  proposed polish edit sets;
- exact baseline reconstruction and exact editorial replay require the retained
  native workspace/checkpoint or equivalent promoted artifacts; and
- after those inputs are obtained, replay is local, deterministic,
  provider-free, and uses existing released code.
