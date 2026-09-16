# Final Release Candidate Result — SBE 0.4.66

## Verdict

Technical qualification, reviewer approval, immutable publication, and
fresh-download verification are complete for SBE `0.4.66`.

## Immutable coordinates

| Evidence | Exact value |
| --- | --- |
| Release-lock/tag target | `a9cb1745da5604869591efd9120e1bd8de76c2f7` |
| Version | `0.4.66` |
| Proposed tag | `astrowoof-natal-authoring-v0.4.66` |
| `SOURCE_DATE_EPOCH` | `1789534964` |
| Wheel | `astrowoof_natal_authoring-0.4.66-py3-none-any.whl` |
| Wheel bytes | `1,406,483` |
| Wheel SHA-256 | `ec30e79780b7a4ffc47510ec25f5b6cb3b09639a8b6a2ec6b2def0661f871daf` |
| Wheel members | `316` identical members; no cache/bytecode members |
| API joined revision | `613c0e01a7d473bf1aa0009e7902c23c98f6e093` |

Both clean exports of the exact release-lock commit reproduced the previously
qualified wheel byte-for-byte. The wheel selected for publication is the
`wheel-a` artifact from that final lock build; no later rebuild may replace it.

## Regression evidence

- Focused suspension/v2/manifest matrix: **74 passed**.
- Broad/full checked-in manifest, supported one-worker profile: **1,229 tests,
  3 expected skips, 0 failures**, 1,308.851010 seconds.
- Full inventory SHA-256:
  `ae272ce3009640bad4259db697e1c00bb92bfcdbf2ac754a59b87f1cc60591f0`.
- API candidate-overlay focused matrix: **68 passed**.

## Installed evidence

- Exact final wheel reinstalled into the isolated environment.
- `pip check`: no broken requirements.
- Imported version: `0.4.66`; module resolved from `site-packages`.
- Installed release smoke: pass; file SHA-256
  `14282cfe06fdd56cb18a7c441b5a5efe13e659e44a2514aa6f359e4ade920b6a`.
- Installed adversarial lifecycle qualification: pass; file SHA-256
  `86bd36e984b91d988bbcd1983a36192918f157f07c1fdac207b5a753c746367e`.
- Installed native-suspension qualification: pass; semantic SHA-256
  `5b19552a05ea43221a258ef039ef00f1737915c262c5f74ec5b638094c927b3c`;
  file SHA-256
  `e6b4ed8b794ba5a1483afd9f300f15e7905b13cc6b0f08db14c6d778fed4176f`.
- Joined API/SBE capability → fence → request → suspension → child-restart
  replay: pass; file SHA-256
  `cafff210c8b25e5a1ff949fa53d67067937376b9946418cda7ecc522f3aa320b`.

## Safety and scope

The qualification performed zero provider calls, spend, R2 access, live
process termination, or API resource release. The exact force fence remained
unresolved and run allocation/custody remained held.

Supported scope is exact interactive ordinary-v2 dispatch/reconciliation.
Initial-wave fan-out, Batch, and bounded routes remain excluded. Parent crash,
PID/exact-exit proof, worker-execution capacity reclamation, and later operator
assessment remain API-owned work. A native suspension result is evidence, not
complete custody-release authority.

## Publication result

- Release URL:
  <https://github.com/kevin2357/semantic-basis-extractor/releases/tag/astrowoof-natal-authoring-v0.4.66>
- Release ID: `RE_kwDOToQdE84XOpFI`.
- Published: `2026-09-16T07:31:24Z`.
- Wheel asset ID: `RA_kwDOToQdE84h0nHy`; GitHub and fresh-download SHA-256
  both match the qualified wheel.
- Checksum asset ID: `RA_kwDOToQdE84h0nHx`; SHA-256
  `5c1b08b7343515639f0ac55dd189988ba288c6dcfe54013248551bd203b27e94`.
- Local and remote peeled tag target:
  `a9cb1745da5604869591efd9120e1bd8de76c2f7`.

This document is committed after publication. It records evidence only and
does not move or replace the immutable tag.
