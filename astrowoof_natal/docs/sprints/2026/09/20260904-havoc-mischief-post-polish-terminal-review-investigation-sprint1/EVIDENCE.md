# Evidence index

| Evidence | Scope | Authority |
| --- | --- | --- |
| `BACKGROUND.md` frozen identity table | two QA runs | API-provided identifiers |
| SBE worker export in `C:\tmp\qa-havoc-mischief-run-report-20260904` | observed native timeline | non-authoritative diagnostic evidence |
| run-evolution `report.json`, `.html`, `.md`, `.mmd` | deterministic projection of exported logs | non-authoritative diagnostic evidence |
| future API checkpoint coordinate packet | named final artifacts only | API/R2 read authority |

## Slice 0 local diagnostic evidence

| Artifact | SHA-256 | Observed scope / limit |
| --- | --- | --- |
| `sbe-worker-havoc.log` | `6cdcdfda03390876a4023decfbf420c087bc80e23625be07e9ad7c09287b2827` | Shows Havoc through first-polish adoption and terminal publication, but not the structured validation issue list. |
| `havoc-report/report.json` | `8e7cd10b5f31fba6d9b7b823c7946c5c1b669133609670e3cfaba6a9433bf02e` | Deterministic diagnostic projection of the Havoc export. |
| `sbe-worker-mischief.log` | `adec82371f1927ebfea46efd3993546bea4a269b09e7a48bcd731b8fe8746d7d` | Stops at a provider-pending checkpoint; no optional-stage or terminal evidence. |
| `mischief-report/report.json` | `fc79c09013ad004775ee99f23748825338bd50e14bfffb0e6ba3774abeb3d07e` | Deterministic diagnostic projection of the incomplete Mischief export. |

These are non-authoritative, sanitized operational diagnostics. They support
the stated evidence ceiling only and do not substitute for a snapshot-valid
checkpoint or sealed native result.

## Slice 1 bounded checkpoint evidence

| Subject | Checkpoint | Verified archive SHA-256 | Verified inventory SHA-256 | Selective finding |
| --- | --- | --- | --- | --- |
| Havoc | generation 10 / `14efd1f6-fbfb-48cb-b647-127203fc57bf` | `c202b11cbf5c9c1e8c72bc8b6c7369fdece37c5d6262cf6839fe696bd4dcbf22` | `3c0a144c6cb4febd943133e8c20acaa3aa85d8615e6d3d9ffb329d4d9feab4d9` | Six acceptance records accepted; post-polish validation fails only `theme_group_cardinality`; lint passes. |
| Mischief | generation 8 / `cbfb0d16-f255-4f97-b64e-982c84b8ffea` | `c94e166cb88b4e44b734335226393fc9df30864d86e82d0613d128c1e3132ece` | `b0e05d0adc7d9e10209a3411d1c5d69ffecd3bf9d684be2f907eeb3a5b751343` | Six acceptance records accepted; identical post-polish validation failure; lint passes. |

The two conditional archive reads emitted local receipts with the closed
operation count `{head: 1, get: 1, list: 0, write: 0, delete: 0}` per archive.
Selective inspection read only the packet-named snapshot, final polish
validation/lint reports, and six acceptance records per archive. It did not
restore or execute either workspace.

## Slice 3 source evidence

| Check | Result |
| --- | --- |
| theme-free final validation | passes when all live editorial rules pass |
| malformed/legacy theme registry | tolerated; no final validation effect |
| non-theme context-filter violation | still fails final validation |
| focused source/package suite | 54 passed (`test_sbe_v03`, `test_theme_group_qa_dormant_slice4`) |
| copied handoff validator subprocess | theme-free/legacy-shaped deck passes; invalid context filter fails |
| deprecated flag compatibility | copied validator accepts `--allow-theme-group-edits` in authoring and polish without changing validation semantics |

The next gate is release-scope review. This correction has no provider, API,
lifecycle, or retained-run behavior change.

## Slice 4 release evidence

- Released version: `astrowoof-natal-authoring 0.4.44`.
- Immutable source commit and tag: `a19e5529e0b933d01ce33d9e7bebb53a21a15647` /
  `astrowoof-natal-authoring-v0.4.44`.
- Two wheels rebuilt from that exact source are byte-identical:
  `76696ec947f02c03a1334225a3c7eaa3384a22860be25e833501db0292c9a89d`.
- The final focused source suite ran after the version bump: `54` passing.
- A disposable environment installed the released wheel with
  `semantic-projection-core 0.11.1`; its provider-free theme-policy
  qualification passed, the installed validator guard excludes the deprecated
  theme flag, and `pip check` reported no broken requirements after installing
  declared dependencies.
- The published GitHub release asset was downloaded once and hash-checked; its
  SHA-256 exactly matches the qualified wheel. GitHub reports the same digest.
