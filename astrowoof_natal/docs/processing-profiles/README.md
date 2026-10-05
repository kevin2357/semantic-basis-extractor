# Processing profiles

A processing profile is the immutable semantic recipe for one AstroWoof run
family. It says what kind of natal input is being processed, which deterministic
and authoring behaviour applies, which prompt release is allowed, and which
package descriptors must be present for each worker role.

The machine-readable source of truth is installed with the SBE package:

- `astrowoof_natal_authoring/resources/contracts/processing-profile-catalog.v1.json`
- `astrowoof_natal_authoring/resources/contracts/prompt-release-catalog.v1.json`

Human-facing catalog: [CATALOG.md](CATALOG.md).

## The identity chain

```text
persisted run
  -> processing profile ID + SHA-256
       -> prompt release ID + SHA-256
       -> authoring and workspace component inventory + SHA-256 values
       -> deterministic-runtime and SBE-authoring package descriptors
  -> API-selected worker-release context
```

The first branch is package-owned semantic provenance. The final branch is
deployment-owned routing: it identifies the worker context able to execute the
already selected immutable profile. It is not part of a profile digest, because
an image rollout is not automatically a semantic-profile change.

## Invariants

- A profile ID and its SHA-256 identify one closed JSON object. Never modify a
  released profile in place.
- A prompt release is likewise immutable. Its digest covers every declared
  system-prompt and workspace-guidance component, not only the system message.
- A run persists its exact profile identity at admission. Continuation and
  recovery route to its compatible worker-release context; they do not consult
  a currently active selector as a substitute.
- The API may select only an admitted profile/context pair. SBE independently
  verifies that the incoming identity exists in its installed catalog and that
  the installed package satisfies the profile's SBE descriptor.
- A profile may be installed and valid without being selected as the default in
  QA or production. Selection/activation is an API control-plane decision.

## What changes require a new identity?

Create a new profile when any semantic input changes: route family or execution
mode, selection policy, deterministic flags, SBE flags, prompt-release binding,
or required package descriptor. Create a new prompt release when any prompt or
workspace-guidance component changes. A routine rebuild or deployment of the
same qualified descriptor does not itself require either.

Use the runbooks in [../operations](../operations/) for the creation and
selection workflow.
