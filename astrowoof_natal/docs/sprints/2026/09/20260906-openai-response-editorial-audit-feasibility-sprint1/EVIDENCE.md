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

## Exact checkpoint and replay result

API supplied and authorized one exact conditional read of checkpoint generation
11. The object matched all frozen coordinates:

- object ETag: `"6148734c493e27681c6ae0987d3f2be3"`;
- archive bytes: `5,002,462`;
- archive SHA-256:
  `b9a916e15daf33c6dbc54958a3e6f6d9c4eea37d043ecebcff42ca490cff6de3`;
- inventory SHA-256:
  `b2afa16f27a8d80066a74900bc47dfc5e40ac0a343a9b20d7dedde1de2421bf8`;
  and
- all 949 declared members matched their exact paths, byte sizes, and hashes.

The provider-free replay used the six downloaded initial outputs with the
retained source archives and selected packet, followed by the two downloaded
polish outputs in lineage order. Results:

- every downloaded authored output equals its retained native authored output;
- all six reconstructed pass workspaces are text-equivalent to their retained
  accepted workspaces (raw byte hashes differ only because the Windows replay
  writes CRLF while the Linux artifact retained LF);
- the initial assembly contains 50 cards, passes structural validation, and has
  five total lint/acceptance findings;
- polish 1 applies 20 edits across 37 eligible targets, reproduces the retained
  candidate exactly, reduces five findings to one, and is accepted;
- polish 2 applies two edits across seven eligible targets, reproduces the
  retained candidate exactly, leaves the finding count at one, and is rejected;
  and
- the replay-selected final deck equals the retained final deck exactly as a
  parsed JSON document.

The surviving warning becomes slightly less severe in polish 2: the repeated
opening `frisbee fandango may` falls from seven occurrences to six. The current
acceptance rule compares finding counts, so that within-finding reduction does
not qualify as improvement. This is a calibration observation, not a replay or
pipeline defect.

Private derived replay artifacts, including the full decks and reports, are at:

`C:\tmp\astrowoof-frisbee-openai-audit-20260906\production-replay`

The sanitized replay receipt SHA-256 is
`deabf7c850647c24e463140093a2c244b7366fb67dde9d01a5c76b7b865b4a85`.
