# Plan — Waffle/Scone Post-Provider Finalization Boundary

Status: Complete; immutable SBE `0.4.40` tagged, published, and independently
verified.

## Goal

Correctly carry advisory-only theme-group findings through final assembly and
make post-provider local-finalization progress truthful and non-spinning. Keep
Waffle's native failure distinct from Scone's independently typed
review-with-custody result unless evidence proves a shared invariant.

## Slice 0 — Production-path characterization

- Freeze the exact Waffle trace interval from pass-6 acceptance through the
  repeated subprocess failure, including release, run, revision, action-state,
  provider-custody, local-work, and exception evidence.
- Trace every theme-group distribution enforcement site across pass acceptance,
  assembly, validation, and finalization. Prove whether `0.4.39` softened all
  intended consumers or left assembly as a contradictory hard gate.
- Reproduce provider-free through the real `closure.main()`/ordinary-resume
  boundary:
  - an advisory-only, production-shaped pass-6 artifact is accepted;
  - lifecycle advertises completed-provider fan-in/adoption work;
  - final assembly raises the observed balance `ValueError`; and
  - the public command produces the same untyped failure/re-entry posture.
- Capture the ordering between selected local work, consumed-operation history,
  `finalize_subjects`, snapshot publication, and command-result publication.
  Determine which semantic operation is consumed and whether that operation
  actually changed native truth before consumption.
- Add controls for a balanced advisory-free artifact and for genuinely malformed
  theme-group structure. Do not weaken structural rejection while reproducing
  the distribution-policy gap.
- Compare Scone only at its public result/custody boundary. Do not infer shared
  cause from `review_required`, `terminal_closed`, or an exit code.
- Use the exact retained checkpoint only if source characterization cannot prove
  the consumed-key/checkpoint join; obtain a complete object coordinate before
  any exact HEAD/GET.

### Voof-paws 1 — causal and invariant review

Pause after the production-path reproducer. Review the two candidate findings
separately:

1. advisory policy contradicted by final assembly; and
2. whether local-work consumption was false or instead belonged to the
   preceding completed-provider fan-in operation.

Slice 0 resolved item 2 in favor of the latter: the consumed operation is the
completed-provider fan-in/adoption operation, which does durably change native
truth before finalization begins. Freeze the assembly-policy correction and the
typed deterministic-failure posture before implementation.

## Slice 1 — Cross-layer advisory-policy correction

Status: complete.

- Centralize or share the hard/advisory classification sufficiently that pass
  acceptance, assembly, validation, and finalization cannot drift again.
- Remove only distribution-policy rejection authority from final assembly:
  `theme_group_coverage`, `theme_group_balance`, and
  `cross_section_theme_mirroring` remain persisted advisories.
- Preserve exact hard failures for malformed registries, invalid or duplicate
  identity/metadata, unknown assignments, competing assignment artifacts, and
  invalid structural joins.
- Add a production-shaped Waffle regression proving:
  `advisory accepted -> assembly succeeds -> no creative retry -> finalization
  remains eligible`.
- Add mutation tests proving structural failures cannot be relabeled as
  advisories and unknown issue codes fail closed.

## Slice 2 — Local-work completion and failure contract

Status: complete.

- Define the durable completion point for finalization local work. Consumption
  must be committed only after the operation changes native truth and its
  successor checkpoint/publication can be validated.
- On a deterministic pre-completion failure, preserve the prior semantic
  operation as unconsumed unless a sealed typed result explicitly establishes a
  different non-replayable disposition.
- Classify failure categories without conflating them:
  - genuine retryable operational dependency failure;
  - deterministic native input/assembly contradiction requiring review;
  - successful finalization/terminal publication; and
  - provider custody or ambiguity, which retains its existing precedence.
- Prefer existing native-result v0.2 and command-result surfaces if they can
  state the outcome truthfully. Add a new version only if the closed current
  shape cannot express the necessary fact.
- Ensure a sealed typed result returned by the invocation outranks process exit
  code. Do not require API to parse stderr, exception text, or run.json.
- Add interruption and exact-replay tests around the durable completion point.

### Voof-paws 2 — public failure/disposition freeze

Pause before runtime mutation if Slice 2 changes a public result schema or API
mapping. Review exact absent/contradictory/unknown-version behavior and the
retry-versus-review disposition.

## Slice 3 — Runtime integration and realistic matrix

Status: complete.

- Apply the agreed consumption ordering under the native writer/snapshot fence.
- Exercise the real public command for:
  - Waffle-shaped advisory-only successful finalization;
  - injected deterministic assembly failure with no false consumption and a
    closed non-spinning outcome;
  - transient dependency failure with truthful retryability;
  - structural theme-group failure;
  - exact replay/interruption recovery; and
  - Scone-shaped retained provider custody, proving no accidental terminal or
    local-finalization authority.
- Prove provider custody and ambiguity continue to outrank unrelated local
  finalization. No new provider creation, recovery, or retained-QA mutation is
  authorized.
- Capture the new `✨🐶` workspace, state, decision, mutation, publication, and
  exit summaries as diagnostic evidence without treating logs as authority.

## Slice 4 — Installed qualification and API handoff

Status: complete; API review pending at Voof-paws 3.

- Package a provider-free qualification using supported public boundaries, not
  test-only state writers.
- Validate the Waffle success and deterministic-failure receipts from a clean
  installed wheel, including consumed-operation continuity and exact result
  identity.
- Retain a packaged Scone comparator proving custody-aware review semantics are
  unchanged.
- Document the exact API intake rule for typed results versus retryable command
  failure; identify any API-only mapper work separately.
- Confirm zero provider/network/R2/retained-QA access and no paid authority.

### Voof-paws 3 — installed consumer review

Pause for cross-repository review of the installed receipts and API handoff
before version bump or release preparation.

## Slice 5 — Release preparation, if runtime changes warrant it

Status: complete; immutable release published and verified.

- Bump to a fresh immutable patch version before release-bound tests and hashes.
- Run the narrow finalization/assembly/local-work suites, installed qualification,
  and release smoke. Select broader depth proportionate to the actual diff and
  record omissions honestly.
- Build twice from the committed source identity and require byte-identical
  wheels, clean install/`pip check`, exact hashes, `git diff --check`, and
  explicit final release approval before tagging or publication.
