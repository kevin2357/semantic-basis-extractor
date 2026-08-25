# AstroWoof Natal Authoring 0.4.18

Status: published and independently digest-verified

SBE 0.4.18 is a narrow temporal-lifecycle compatibility patch over 0.4.17.

Lifecycle v0.5 can legitimately classify a resolved action relationship as
`independent`. The v0.6 temporal projection previously rejected that valid v0.5
value because its closed vocabulary still expected the obsolete `nonblocking`
spelling. This release accepts the three lifecycle-defined values:
`blocking`, `independent`, and `superseded`.

The correction is deliberately validation-only. It does not alter provider
submission, provider retrieval, spend authority, state mutation, prompt
construction, delivery, or the public lifecycle contract. It allows retained
workspaces whose ordinary actions have resolved independently to be inspected
and continued through their already-authorized native path.

## Qualification

- Artifact source commit: `d29d923fe6bcf4d62c4714d20e51d693ad972a82`.
- Fixed build epoch: `1787603106`.
- Two byte-identical wheel builds.
- Complete source suite: 594 passed; 3 environment/opt-in skips.
- Focused temporal/provider-pending regression suite: 33 passed; 3 skips.
- Installed release smoke: pass.
- External provider/network calls: 0.
- Provider POST/create/submit/retry calls: 0.
- Spend: USD 0.

The immutable tag is `astrowoof-natal-authoring-v0.4.18`. GitHub reports the
published wheel at 893881 bytes with SHA-256
`23322ab8fae2301c1266c526853df8b4fdecbf8eed96b60d6746eec42c81f08e`,
exactly matching the qualified local artifact.
