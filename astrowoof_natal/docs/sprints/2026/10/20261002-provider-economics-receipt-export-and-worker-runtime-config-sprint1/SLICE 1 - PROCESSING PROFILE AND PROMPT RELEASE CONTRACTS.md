# Slice 1 — processing-profile and prompt-release contracts

## Result

Slice 1 is complete provider-free. It adds a closed, package-installed
configuration surface; it does **not** yet change any worker command, command
line, run workspace, provider construction, prompt request, environment, or
deployment setting.

The new public module is `processing_profiles.py`. It provides strict catalog
readers and validators for a canonical `processing_profile.v1` and
`prompt_release.v1`, each with a self-identity SHA-256. The two catalogs are
also self-digested. JSON parsing rejects duplicate keys, non-finite values,
trailing non-whitespace, unsupported fields, and digest drift.

## Initial compatibility binding

The one installed profile is deliberately narrow:

| Field | Value |
| --- | --- |
| Profile ID | `astrowoof.exact_natal.live.compat.v1` |
| Profile SHA-256 | `e1affc78ab278d20be990ba8652ee3991a4e672012358ae889cc39f5bc565a2d` |
| Route / execution mode | `exact_natal` / `live` |
| Selection policy | `legacy_atomic.v1` |
| Prompt release | `astrowoof.authoring.compat.v1` |
| Prompt-release SHA-256 | `51e58cb41cf4a317b4fa37e77e18f57567bd4976b56d6e9fa788154b4c1e3d5c` |

The profile makes the currently frozen SBE live settings explicit: OpenAI
interactive service, cost-optimized routing, Luna initial model, Terra retry,
stratified assignment, compact-v2 full-chart basis, six workers, three normal
attempts, two allowed polish attempts, qualitative critic, prompt-cache
settings, and current non-secret transport limits. It also carries the known
deterministic compatibility fragment: exact birth-time mode, Moshier
ephemeris, the four projection contexts, and the current projection contract.

This does not claim bounded or axis-aware support. The resolver proves only
the listed exact/live/legacy tuple; bounded/live, exact/batch, and
axis-aware are all false until separately added, validated, and admitted.

## Prompt asset boundary

`prompt-system-authoring.compat.v1.md` contains the byte-exact current static
system instruction, as canonical UTF-8 with LF termination. Its package digest
is `2ec0738497756b09887e921273371b4f99108378b9197ce9b065beeacd453a71`.
The active prompt release maps its four current exact-route stages—initial,
retry, polish, and critic—to that component. Dynamic workspace evidence and
retry feedback remain outside the asset inventory and remain governed by their
existing private-custody behavior.

The asset is registered but intentionally not read by `closure.py` yet. Moving
ordinary provider construction from the literal to the selected installed
release is Slice 3 work, after the runtime binding path exists. That keeps this
slice a zero-behavior contract addition rather than a stealth prompt change.

## Negative boundaries covered

Focused coverage proves:

- catalog/profile/release digest verification and cross-reference matching;
- unknown profile/release refusal;
- rejection of injected SBE fields such as a synthetic API key, even if the
  enclosing profile digest is recomputed;
- rejection of changed profile content with an unchanged identity digest;
- canonical LF/UTF-8 prompt asset enforcement and asset-digest drift refusal;
- explicit tuple ownership rather than inferred bounded, batch, or axis-aware
  support; and
- test-suite manifest registration for the new focused module.

Focused command: `python -m unittest
astrowoof_natal.tests.test_processing_profiles_slice1
astrowoof_natal.tests.test_test_suite_runner`.

Result: **21 passed** (5 new processing-profile tests plus the manifest-runner
coverage), provider operations: **0**.

A local source wheel was also built solely to inspect package contents. It
contains both catalogs and the prompt asset, whose archived bytes are
LF-terminated and contain no CR byte. That temporary `0.4.66` wheel is
qualification evidence only and is not a release candidate or publishable
artifact.

## Gate B request

API review should confirm the exact catalog schema and initial compatibility
identity, especially the deterministic fragment values and the intended
generation-manifest extension carrying `processing_profile_id` and
`processing_profile_sha256`. The review should also confirm the prompt-release
reference/provenance fields API will preserve without treating prompt text as a
manifest value.

If approved, Slice 2 may wire only the persisted expected ID/digest into the
semantic-closure command boundary and establish its safe durable attestation.
