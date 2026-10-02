# Slices P1-P3 — editorial v2 and axis-aware profile

## Scope and outcome

These provider-free slices add one new exact-Natal/live profile without
altering the installed compatibility fallback:

| Binding | Compatibility fallback | New editorial/axis-aware candidate |
|---|---|---|
| Processing profile | `astrowoof.exact_natal.live.compat.v1` | `astrowoof.exact_natal.live.axisawaresbe.v1` |
| Selection policy | `legacy_atomic.v1` | `axis_aware.v1` |
| Prompt release | `astrowoof.authoring.compat.v1` | `astrowoof.authoring.editorial.v2` |
| Workspace guidance | original resources | copied v2 resources |

The compatibility profile and source assets retain their prior bytes and
identities. The new profile is not API-admitted, deployed, or activated.

## P1 — actual static workspace inventory

The live semantic-closure create path runs the installed extractor subprocess
with `--handoff-profile authoring-workspace` and split layout. The only static
instruction resources copied directly into each pass workspace are:

1. `authoring/AstroWoof Story Workspace Authoring Brief.md` ->
   `AUTHORING BRIEF.md`
2. `authoring/AstroWoof Authoring Guiding Lights.md` ->
   `GUIDING LIGHTS.md`

The provider system message is a third static component, selected by the
existing stage resolver. `START HERE.md`, dog details, chart basis, claim and
summary writing files, whole-dog templates, and optional summary-gold material
are generated or selected per run. Their exact bytes remain covered by the
existing workspace snapshot/archive and generation-manifest custody, rather
than being misrepresented as a universal prompt-release component.

The extractor now receives only the already-validated profile ID and digest
from semantic closure. It independently verifies the installed profile before
workspace assembly; a mismatched digest refuses. The profile replaces any
caller-selected exact-Natal policy at that extraction boundary.

## P2 — editorial release v2

`astrowoof.authoring.editorial.v2` is a v2 prompt-release record because it
adds a closed `workspace_components` inventory alongside ordinary provider
stage components. It contains copied versions of the two static workspace
guidance files and a copied, byte-identical system message.

The only prose change is the direct-to-dog audience/density clarification:

> Audience changes address and tone, never astrology density: direct-to-dog
> `full_astro` prose must still name and explain the relevant retained
> astrological factors in warm, readable second-person prose.

No chart claim, dynamic assignment, provider payload, subject data, endpoint,
credential, response, or workspace path is in the release record.

## P3 — closed identities

| Item | SHA-256 |
|---|---|
| Editorial prompt release | `089942e352e92fa2ad2e80ad8a3a705ef7976aa2c64e9001f2b068c84bffa94f` |
| Editorial authoring brief | `8097cc2639212f82a0ff2b916baacd3d4f7bdaeca3cce22c0ada4d10db659bbc` |
| Editorial guiding lights | `ac1625fed0e6791b7c39c79610e104ba9a99ea720f4ecbe5cba55a8a070e7d08` |
| Prompt-release catalog | `e48a2b1c474d31cb82295cefa40b2b32f338f29b3a1241eb2f6f941c828cf4cc` |
| Axis-aware profile | `55914fd51e2c39169e81cc32f8d85b61ba3d97f3610358a7735e935cc5d5854a` |
| Processing-profile catalog | `7a4ac541478ca4cb2982f9bfb8816c41bfac95470ba470664f3157dd446c7394` |

## Provider-free evidence

- 15 focused source tests passed: profile/release validation, legacy and v2
  prompt-stage resolution, workspace asset selection, axis-policy override,
  and semantic-closure-to-extractor profile-reference threading.
- A locally built `0.4.66a0` wheel contained all three new editorial assets and
  the prompt-release catalog.
- A no-dependency install of that wheel resolved the axis-aware profile and
  its two v2 workspace assets successfully.

The wheel is source qualification evidence only. Its version is the existing
alpha descriptor and it is not a release candidate or publishable artifact.

## Gate D remaining work

API must admit the final profile ID/SHA, and the deterministic-runtime and SBE
release artifacts must carry matching final catalogs and package descriptors.
The joined provider-free replay must prove old-profile original-byte assembly,
new-profile v2-only assembly, exact profile handoff across both actual worker
boundaries, and pre-provider refusal for mismatched profile/release/image
identities. A new versioned SBE candidate will be required before that gate.
