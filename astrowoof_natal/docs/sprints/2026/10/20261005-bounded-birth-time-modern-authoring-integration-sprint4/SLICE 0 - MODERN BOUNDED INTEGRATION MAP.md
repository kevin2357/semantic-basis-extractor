# Slice 0 — Modern bounded integration map

**Status:** design/inventory complete. No source, catalog, prompt, wheel, or provider mutation occurred.

## Decision

Bounded authoring is not a catalog-only addition. The conservative bounded core is mature and reusable, but it predates the profile-bound runtime and terminal handoff used by the current exact route. The required work is a narrow adapter around that core, not a rewrite of bounded admission or selection.

## Reusable foundation

| Surface | Existing bounded behavior | Required posture |
| --- | --- | --- |
| Intake | `bounded_admission.py` accepts exactly the four SPC bounded contexts and refuses exact/mixed families. | Retain; invoke after sealed API/deterministic handoff validation. |
| Stable selection | `bounded_basis.py` / `bounded_selection.py` admit invariant dependency-closed claims only and require exactly 50. | Retain; make under-50 an explicit deterministic eligibility outcome. |
| Provider privacy | `bounded_authoring.py` removes time/interval, location, source graph, and raw evidence from prompts. | Retain and regression-test it from the integrated command. |
| Native publication | `native_transitions.py` recognizes bounded v1/v2 routes for result sealing. | Reuse, but return its same-invocation result/receipt through a current command envelope. |
| Lifecycle | `bounded_lifecycle.py` supplies six-pass work, spend, reconciliation, and fake-provider machinery. | Retain state mechanics; source behavior settings from the installed profile. |

## Why profile and prompt records alone are insufficient

The installed profile/prompt catalogs contain only `exact_natal` entries. A bounded record needs its own route family, deterministic descriptor, SBE command contract, selection policy, and immutable prompt release.

More importantly, `cli/bounded_run.py` accepts caller-selected `--input-package`, `--subject`, `--generation-profile`, provider/model/reasoning, and service-level flags. It merely copies the arbitrary generation-profile JSON into `run.json`; it neither resolves an installed processing profile nor binds profile/prompt digests or workspace-component inventory. A new catalog record would therefore be inert.

The reusable model is exact `closure.py`: validate API profile handoff against the installed catalog; derive knobs from that profile; resolve prompt components by profile/stage; materialize and hash workspace components; and require binding equality on resume. Bounded needs a specialized version of this model.

## Material integration gaps

### General projection: deferred product decision

The bounded source projection family includes `general`, but the rendered
WoofMap product currently exposes only `handler`, `direct_to_dog`, and `hybrid`.
Legacy bounded `VOICE_KEYS` already matches those three rendered audiences. Do
not add a fourth bounded audience in this migration solely because a general
semantic projection exists. Preserve the source contract as needed for
validation/provenance, and record a future cross-route product investigation
for whether `general` should ever become a rendered audience.

### Command/result/receipt handoff

The bounded CLI calls `publish_native_execution_result()` but prints only `public_run_state(state)`. It does not emit the current exact route's command envelope containing the just-sealed result/receipt identities, nor current terminal-review behavior. The integrated route needs exact result/receipt handoff, bounded delivery/claim/deck/disposition descriptors, and no latest-result discovery.

### Prompt provenance

Legacy bounded provider instructions correctly prohibit representative time and exact geometry, but do not use installed prompt-release workspace components. Create a bounded prompt release with versioned bounded guidance assets and hashes. Reusing exact guidance without bounded prohibitions is unsafe; using old bounded resources without immutable inventory is unprovable.

### Eligibility outcome

Insufficient invariant material currently fails selection. A valid sealed source below the 50-card floor needs a typed, non-provider, non-retryable bounded eligibility result so API can distinguish product eligibility from authoring failure.

## Proposed first bounded profile shape

| Field | Required rule |
| --- | --- |
| Profile | New immutable `astrowoof.bounded_natal.live.<policy>.v1`; never reuse an exact ID. |
| Route | `family: bounded_natal`, `execution_mode: live`, and a bounded command-contract ID. |
| Deterministic descriptor | AGF 0.8.1 + SPC 0.11.1, bounded birth mode, four contexts, and `woofmapped_bounded_astrology.v0@0.1.0`. |
| SBE settings | Profile-owned provider/authoring values; integrated calls do not accept arbitrary behavior overrides. |
| Prompt release | New immutable `bounded_natal` release with bounded prompt and hashed workspace components for every stage. |
| Selection policy | Explicit stable-facts-only / 50-card / no-representative-time identity. |
| Binding | API passes ID/SHA/manifest SHA/route/environment; SBE verifies installed values and resume equality. |

Bounded-vs-exact and axis-aware-vs-non-axis-aware remain independent axes.

## Slice 1 boundary

1. Add bounded profile/prompt catalog entries, resolution, and workspace inventory.
2. Add a profile-bound integrated bounded command or mode. Preserve the free-form CLI as legacy tooling rather than redefining it silently.
3. Preserve the current three rendered audiences; do not introduce a fourth
   `general` audience in this bounded migration.
4. Add result/receipt/terminal-review command envelopes and typed under-50 eligibility output.
5. Qualify real-source behavior only when API Gate B provides sealed AGF/SPC four-context evidence.

## Gate A recommendation

Approve this direction for implementation design, but not a bounded release. API Sprint 128 Gate A freezes stored bounded birth-data semantics; its Gate B still supplies the real deterministic family needed for installed integration qualification.

## Sources inspected

- `processing_profiles.py`, the installed profile/prompt catalogs, and exact profile binding in `closure.py`.
- `cli/bounded_run.py`, `bounded_admission.py`, `bounded_basis.py`, `bounded_selection.py`, `bounded_authoring.py`, `bounded_lifecycle.py`, and `bounded_provider.py`.
- `native_transitions.py` and the bounded test suite.
