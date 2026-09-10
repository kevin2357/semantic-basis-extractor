# Slice 3 — 0.4.56 package qualification

Status: exact release-lock qualification passed; final pre-tag review pending.

## Candidate identity

- distribution: `astrowoof-natal-authoring`
- version: `0.4.56`
- fixed pre-lock `SOURCE_DATE_EPOCH`: `1789030800`
- wheel filename: `astrowoof_natal_authoring-0.4.56-py3-none-any.whl`
- wheel size: 1,376,426 bytes
- wheel SHA-256:
  `56be2706c792014468081fdf0fab8d101bf250141e97f349ba4e921d9d0abe82`
- two independent builds: byte-identical

This pre-lock digest is qualification evidence, not the final release digest.
The release artifact must be rebuilt reproducibly from the release-lock commit.

## Clean installed environment

- SBE: exact candidate wheel `0.4.56`
- SPC: locally built sibling package `0.11.1`
- jsonschema: `4.26.0`
- tzdata: `2026.3`
- `pip check`: no broken requirements
- SBE import origin: isolated environment `site-packages`
- new public runtime constructor: present
- new exact-source validator: present

## Installed tests

- focused fixture/runtime/qualification matrix: 27 passed, no skips;
- API functional consumer cells: 4 passed;
- independent API candidate-version assertion: `0.4.56` passed; and
- API source-overlay compatibility guard before packaging: 5 passed unchanged.

API's checked-in package-identity test still names released baseline `0.4.55`;
it was not edited by SBE. The candidate version was verified independently while
all four functional cells ran directly against the installed `0.4.56` wheel.

## Boundaries

No API sender, Better Stack, provider, database, retained-run, lifecycle,
workspace mutation, tag, or GitHub release operation occurred. Publication
remains gated after exact-commit qualification and final API/owner review.
