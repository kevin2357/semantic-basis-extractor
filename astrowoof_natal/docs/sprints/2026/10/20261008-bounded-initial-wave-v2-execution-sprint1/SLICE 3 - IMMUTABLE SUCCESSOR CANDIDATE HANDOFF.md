# Slice 3 — Immutable successor candidate handoff

## Disposition

Gate C approved the bounded initial-wave v2 command.  The temporary `0.4.71`
wheel used to prove that command is not a candidate for API admission: it was
built before the Gate C fixes were committed and cannot carry a new immutable
profile identity.

This slice therefore prepares a distinct `0.4.72` candidate.  It does not
rewrite either historical bounded bundle:

| Record | Disposition |
| --- | --- |
| `astrowoof.bounded_natal.live.stable_facts.v1` | retained historical `0.4.70` profile |
| `astrowoof.bounded_natal.live.stable_facts.v2` | retained historical `0.4.71` profile |
| `astrowoof.bounded_natal.live.stable_facts.v3` | new initial-wave-v2 candidate profile |

The prompt assets themselves are unchanged.  A separate prompt-release v3 is
nevertheless required because a prompt release's profile allowlist is part of
its sealed identity; v2 must not be mutated to point at v3.

## Successor static identities

| Surface | Immutable value |
| --- | --- |
| SBE package version | `0.4.72` |
| Bounded profile | `astrowoof.bounded_natal.live.stable_facts.v3` |
| Profile version | `3.0.0` |
| Profile SHA-256 | `5ccdbac1d8b81b9099fa7689f08460c30a2563192b4c766587ea190bfb05caed` |
| Prompt release | `astrowoof.authoring.bounded_stable_facts.v3` |
| Prompt release version | `3.0.0` |
| Prompt release SHA-256 | `737bb2cb64e426b281a12a88578b7831473b228d2b40a7fdb2c8c7ad5fa1b0e6` |
| SBE worker descriptor SHA-256 | `440d4475d4b746833f45bc9a4efc53d220fca636476ca6f8d626f4259b201cf8` |
| Processing-profile catalog SHA-256 | `039fd08ea77f105cb52ae9376e7e3907b3ff130d258f6afccafc375f609d1982` |
| Prompt-release catalog SHA-256 | `d827e2d7cc1aa7fbc4c4f62b3624dda0d30b7afce6bd709bac71523d6006851e` |
| Required SPC distribution | `semantic-projection-core==0.11.1` |

The v3 profile retains the bounded route contract
`astrowoof.bounded_natal.authoring_run.v2`, stable-facts-only policy, four
projection contexts, and the exact v2 stage-prompt/workspace-component
inventory.  Its only semantic successor change is binding that immutable
configuration to the package that contains the approved v2 initial-wave
command.

## Candidate qualification

| Field | Value |
| --- | --- |
| Artifact-source commit | `0b814260d8dcec5e3daa246374b047a8c7c4fe9c` |
| `SOURCE_DATE_EPOCH` | `1791471128` |
| Filename | `astrowoof_natal_authoring-0.4.72-py3-none-any.whl` |
| Retained wheel | `C:\tmp\sbe-0.4.72-bounded-initial-wave-v2-candidate\wheel-a\astrowoof_natal_authoring-0.4.72-py3-none-any.whl` |
| Duplicate build | sibling `wheel-b` directory |
| SHA-256 | `dadd3969f83f834e4c0dee7d61a2ef6b4be6592ad2505e31e1384c36999cb29b` |
| Byte size | `1,446,113` |
| Wheel members | `330` |
| Raw command fixture | `C:\tmp\sbe-0.4.72-bounded-initial-wave-v2-candidate\installed-command-fixture.json` |
| Fixture SHA-256 | `d55e1f484307d6d527d423fe2244e31bea95b9f023a2a6a7e320a3d3e800e3e2` |

Two clean canonical-LF Git archives from `0b814260` built with that epoch into
independent directories. Filename, member inventory, byte size, and
whole-wheel SHA-256 are byte-identical. The inventory contains the public
bounded command schema and no cache, build, bytecode, or other generated
members.

The exact wheel was installed only in the isolated candidate venv. It resolved
from `site-packages` as `0.4.72`, and `pip check` passed after installing SPC's
declared `jsonschema` dependency in that disposable environment. Its public
`astrowoof-external-authority-v2` command, using `--provider fake`, produced:

| Cell | Exit | Typed outcome | Safety result |
| --- | --- | --- | --- |
| First six-member dispatch | `0` | `detached_provider_pending` | exactly one durable intent and six fake provider bindings |
| Exact replay | `0` | `exact_replay` | no new mutation, publication, or provider I/O |
| Altered grant | `3` | `pre_provider_refusal` | no mutation or provider I/O |

The raw success, replay, and refusal envelopes are retained in the fixture
named above. The fixture is produced by an API-shaped request/grant whose
native run ID is generated before the command call; the installed candidate
echoes that same ID in all three outputs. It uses no network or real provider
credentials.

## API Gate D request

Install only the SHA-bound wheel above into an isolated API context. Admit the
v3 profile/release/catalog identities as a new immutable bundle; do not alter
v1 or v2. Exercise the raw success envelope, exact replay, and altered-grant
refusal fixture through API's bounded initial-wave ingress and idempotency
boundary, while retaining ordinary-v2 coverage unchanged.

No package publication, tag, deployment, profile activation, workspace
mutation, or provider operation is part of this candidate handoff.
