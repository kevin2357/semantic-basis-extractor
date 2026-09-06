# Release candidate — SBE 0.4.52

## Artifact-source identity

- Commit: `6c151888b35bfe13502abe52a7870e4bfd4fd19c`
- Build epoch: `1788727982`
- Wheel: `astrowoof_natal_authoring-0.4.52-py3-none-any.whl`
- Bytes: `1,247,759`
- Members: `273`
- SHA-256:
  `5048406266195f2ea8988331b2f6c7b7909ba67007676234f1795d703147ef05`
- Forbidden cache/bytecode members: `0`
- SPC compatibility: `0.11.1`

Two independent clean exports of the artifact-source commit produced
byte-identical wheels with the recorded epoch.

## Regression evidence

- Expanded focused reporter/qualification/release matrix before the installed
  correction: 69 tests passed, 5 skips, in 28.584 seconds.
- Full provider-free suite: 1,103 tests passed, 58 skips, in 1,083.232 seconds.
- Clean installed qualification identified one missing Windows package
  dependency: the standard-library `zoneinfo` renderer requires `tzdata` where
  Windows supplies no IANA database.
- Added only the conditional dependency metadata
  `tzdata; platform_system == 'Windows'`; no runtime code, schema, contract, or
  test behavior changed.
- Repeated the exact focused matrix after that correction: 69 tests passed, 5
  skips, in 30.559 seconds.
- The broad suite was deliberately not repeated after this metadata-only
  correction; the chronology and proportional decision are recorded plainly.

## Clean installed qualification

The exact candidate wheel was installed with its declared dependencies into an
isolated Windows Python 3.12 environment outside the source package.

- `pip check`: no broken requirements.
- Installed SBE version: `0.4.52` from `site-packages`.
- Installed SPC version: `0.11.1`.
- `tzdata`: installed from the declared Windows dependency.
- Wheel contains both timeline schemas and no forbidden bytecode/cache members.
- Generic `astrowoof-release-smoke --require-installed`: pass.
- `astrowoof-run-report-qa`: pass; receipt SHA-256
  `9446526c268cd1334f266266ba6ad1cd25cce246e8ca9098b92e426345c0835b`.
- `astrowoof-run-timeline-qa`: pass; receipt SHA-256
  `2d65be16c87eb1a6f104868957bc3b1b16980f6ca556aaa9a8aab98cad4d31f0`.
- Timeline SHA-256:
  `2956a38644893c83428d884b6cec7500b12391eb5fc0f443d548d14b9f441d0a`.
- HTML SHA-256:
  `46a9f92b9cbefa002f44687958c007f2e52feb7a1cdbbe4a3005a833489b8909`.
- `astrowoof-providerless-denial-qa`: pass; receipt SHA-256
  `b9fd7c1bfa400b0cab8ab55883a223e3ee1f6f24171980a4d058cc47795a3135`.

All qualifications were provider-free and performed no R2, Render, QA,
retained-run, or production work.

## Remaining release-lock gate

Commit this record as the release lock, rebuild twice from that exact commit
and its timestamp, require byte-identical wheels, repeat the installed public
qualifications, then pause for API review and explicit owner authorization
before creating `astrowoof-natal-authoring-v0.4.52`.
