# Slice 0 — Payload Representation Characterization

Status: complete; API selected the closed deterministic rebuild rule

## Confirmed exact-route defect

The provider-free production adapter reproducer confirms:

1. `build_interactive_authoring_request()` produces a complete payload whose user
   content is an ordered array of three `input_text` blocks:
   `static_prefix`, `subject_prefix`, and `pass_assignment`.
2. The first two blocks carry prompt-cache breakpoint metadata.
3. The spend action binds the canonical SHA-256 of that complete object.
4. `OpenAIResponsesProvider.author()` persists `openai-request.json` after replacing
   the complete user-content array with one string placeholder.
5. It persists `openai-workspace-prompt.txt` as the three segment strings flattened
   with `\n\n` separators.
6. The pre-patch v2 resolver hashes the redacted JSON, finds no binding match, and
   returns `request_payload_digest_mismatch`.

This is the production mechanism behind the QA refusal.

## Historical reconstruction limit

The redacted JSON plus prompt text do not, by themselves, preserve the exact
original JSON field value. They omit:

- the fact that user content contained three blocks rather than one;
- the exact three block boundaries; and
- the prompt-cache breakpoint metadata attached to the first two blocks.

The complete payload can be reproduced when the original segment map is still
available from the production builder, and that reproduced object matches the
binding digest exactly. But claiming that the persisted two-file pair alone is a
lossless representation would be false.

API selected the first of these two honest compatibility rules:

1. **Snapshot-bound deterministic rebuild:** rerun the exact versioned authoring
   request builder from the complete retained source workspace, feedback, route,
   attempt, profile, and packaged resource identities; require the rebuilt flattened
   text to equal the persisted prompt and the complete payload digest to equal the
   action binding. This is SBE-native reconstruction, not API inference, but must be
   version/profile/resource bound and fail closed when any input is unavailable.
2. **No historical reconstruction:** fix future persistence only and provide a
   separate narrowly reviewed repair artifact/procedure for the two retained runs.

The simpler proposed reattachment of the text file as one JSON field is invalid and
must not be implemented.

## Bounded applicability

Bounded ordinary interactive work does not use the lossy authoring-pass artifact
shape:

- initial bounded interactive preparation writes the complete body directly to
  `openai-request.json` and validates its digest before create;
- later bounded ordinary interactive stages use `OpenAIResponsesProvider.complete_json`,
  which also writes the complete request body directly.

No bounded runtime change is justified by this incident. Shared canonical digest
helpers may be reused only where they preserve these stronger existing rules.

## Post-refusal posture clarification

SBE 0.4.23 currently does not erase refusal history. It:

- appends an immutable run-level refused-invocation record;
- appends the same evidence to each unentered action;
- removes the refused aggregate grant/intent from active custody; and
- marks unentered providerless actions operationally `PREPARED`, with authorization
  and consumption removed, so a later inspection can create a fresh request.

Thus `PREPARED` describes current providerless eligibility while the embedded
history proves the earlier refusal. API accepted this posture: the refused
invocation and grant remain immutable and unusable, and any later create requires
a fresh inspection, request, grant, and authorization decision.

## Evidence

- Focused production-path characterization: 1 test passed.
- Provider transport: scripted local object only; external calls 0.
- Provider creates relevant to the resolver: 0.
- Credentials/network/spend: 0.
- Retained QA access/mutation: 0.
- Runtime source changes: 0.
