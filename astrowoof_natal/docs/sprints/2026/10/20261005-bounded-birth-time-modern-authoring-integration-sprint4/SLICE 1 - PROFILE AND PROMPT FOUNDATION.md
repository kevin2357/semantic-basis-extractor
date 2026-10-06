# Slice 1 — Profile and Prompt Foundation

**Status:** profile-bound CLI/lifecycle, prompt consumption, and the under-50
typed result are implemented. Installed-wheel qualification remains open.

## Installed immutable identities

The package now carries a bounded-only profile and prompt release. Neither
rewrites an exact profile or makes a bounded profile selectable in API.

| Surface | Identity |
| --- | --- |
| Processing profile | `astrowoof.bounded_natal.live.stable_facts.v1` |
| Profile SHA-256 | `c2a1b87c508d0bbcff3f03541b66175469969be8a1f9dae9a0b7ce713affabbc` |
| Prompt release | `astrowoof.authoring.bounded_stable_facts.v1` |
| Prompt-release SHA-256 | `ddf589eee616ef04b411a345d81c1fc635682766593ffed18020a72a329118fe` |
| Processing-profile catalog SHA-256 | `0140865de5a0149725093cd0dba941265deaf0e7619f6312b672388b7ead8dfb` |
| Prompt-release catalog SHA-256 | `f9ebcb02503217003d6dbf87867b8a32eed81860c17a46bf9128149a952e3214` |

The profile binds `bounded_natal` / live to
`astrowoof.bounded_natal.authoring_run.v2`, AGF `0.8.1`, SPC `0.11.1`,
`woofmapped_bounded_astrology.v0@0.1.0`, and the fixed four-source-context
family. Its rendered product remains the existing three audiences: handler,
direct-to-dog, and hybrid.

The release binds the existing bounded authoring brief and guiding-lights
assets by canonical SHA-256. It also owns four stage-specific bounded system
instructions—initial, retry, polish, and critic. Those instruction bytes are
the historical bounded anti-precision instruction set, now package-resolved
and included in provider requests rather than merely copied beside a workspace.
The change makes the established stable-facts boundary attributable without
changing its creative stance.

## Validation

`processing_profiles.py` now accepts the bounded SPC projection contract only
for `birth_time_mode: bounded`; the exact contract continues to be required
for exact profiles. The bounded CLI consumes the same atomic four-field API
handoff as the exact CLI, verifies the installed profile's distinct bounded
run contract, replaces caller-owned provider/model/stage knobs, freezes the
full binding in `run.json`, and refuses a resume whose binding is absent or
different. It materializes the declared workspace guidance assets, with
digests, and profile-bound provider calls use release-resolved stage prompts
while retaining only safe prompt-release provenance in stage metadata.

On a terminal delivery, the command emits the same-invocation terminal
delivery command envelope generated from the just-sealed native result and
receipt. Non-delivery states retain public run state rather than inventing a
delivery handoff.

Focused qualification:

```text
tests.test_processing_profiles_slice1,
tests.test_processing_profile_runtime_slice2,
tests.test_bounded_provider,
tests.test_bounded_lifecycle: passed
```

## Eligibility completion and remaining qualification

The under-50 command contract is now recorded in
[Slice 1B](SLICE%201B%20-%20BOUNDED%20ELIGIBILITY%20COMMAND%20HANDOFF.md).
The installed-wheel test must exercise the real executable against the API Gate
B sealed artifact, including API receiver refusal cases, resume-binding
mismatch, and ordinary receipt-backed terminal command-envelope behavior.

The retained Gate B family could not be re-admitted with the desktop bundled
Python because that runtime lacks `jsonschema`, a required SPC validator
dependency. API's locked `--network=none` Docker evidence remains the
authoritative successful admission/replay witness; this local missing-module
failure is not an input-contract refusal.
