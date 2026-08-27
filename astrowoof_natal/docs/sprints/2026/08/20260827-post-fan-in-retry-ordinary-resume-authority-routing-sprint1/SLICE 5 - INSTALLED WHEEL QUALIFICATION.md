# Slice 5 — Installed-Wheel Qualification

Status: SBE candidate qualification complete; API/Linux review pending.

> Supersession note: the original candidate below remains valid pre-4A evidence,
> but is not the joined-campaign artifact. Corrective Slice 4A produced replacement
> source `9205235` and deterministic wheel SHA-256
> `db5ff09afce53b063dea1b29d8fcb94af581bcf383f7cab5da1d65cc0d4e48ed`.
> Its installed receipt/bundle, adversarial qualification, and generic release
> smoke passed. API must use that exact replacement wheel.

## Candidate identity

- Source commit: `e1a22ab`
- Version: `0.4.27`
- Fixed build epoch: `1787844361`
- Wheel filename: `astrowoof_natal_authoring-0.4.27-py3-none-any.whl`
- Wheel size: 1,048,593 bytes
- Wheel SHA-256:
  `ae8da7a7ce64cd83e1a4444fb8a77587eafb1c1f5a7ff1cc3ac615dfb51e611a`
- Exact SPC dependency: `semantic-projection-core==0.11.1`

Two sequential builds from the same source and fixed epoch produced identical
wheel bytes.

## Package inventory

Direct wheel inspection confirmed the package contains:

- `py.typed`;
- the closed `post-fan-in-retry-qualification.v1` receipt schema;
- the stable `post-fan-in-retry-routing.v1` scenario fixture; and
- the `astrowoof-post-fan-in-retry-qa` console entry point.

## Installed qualification

The candidate and exact SPC dependency were installed outside the checkout in a
literal `site-packages` tree. The following installed commands passed:

- `astrowoof-release-smoke --require-installed`;
- `astrowoof-adversarial-qa`; and
- `astrowoof-post-fan-in-retry-qa` twice in fresh disposable workspaces.

The two post-fan-in receipts were byte-identical. Their SHA-256 is
`0db488713ad4711f52431d0a65187d6103f7784e41cd9a2c1d192c5af7eee074`.

## Broad regression

The full source suite completed with 829 passing tests and 40 expected
environment/opt-in skips in 825.722 seconds.

## Safety boundary

- External provider/network calls: 0
- Provider creates: 0 external; scripted local qualification only
- Spend: USD 0
- Retained QA cohort access or mutation: none

This evidence qualifies the SBE candidate on Windows. It does not substitute for
the planned API/Linux joined campaign. API must run that campaign against the exact
wheel digest above before the sprint advances to the final release decision.
