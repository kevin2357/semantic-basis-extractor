# Gate B — 0.4.70 bounded candidate wheel

## Scope and status

This is a retained, local, provider-free candidate for the API/SBE joined
bounded eligibility replay. It is **not** a tag, public release, deployment,
activation, or provider authorization.

The candidate is versioned `0.4.70` because the installed bounded profile
requires its SBE package descriptor to identify the wheel that contains the
new command/result contract. `0.4.69` is already published and cannot
truthfully describe these changed bytes.

## Candidate identity

| Field | Value |
| --- | --- |
| Wheel | `astrowoof_natal_authoring-0.4.70-py3-none-any.whl` |
| Retained path | `C:\tmp\sbe-0.4.70-bounded-gate-b-candidate\astrowoof_natal_authoring-0.4.70-py3-none-any.whl` |
| SHA-256 | `86d209daf8878a59d3813ed30938e1fd7a572d51fca9756151f5b87ad0872135` |
| Byte size | `1,438,637` |
| Processing-profile catalog SHA-256 | `f6ad1e5a73efcd9fab8e0692e7e03631250e48f3f125585ed73b52fc70dadf8d` |
| Prompt-release catalog SHA-256 | `f9ebcb02503217003d6dbf87867b8a32eed81860c17a46bf9128149a952e3214` |
| Bounded profile | `astrowoof.bounded_natal.live.stable_facts.v1` |
| Bounded profile SHA-256 | `34eeb96a16d2b9f781fde6497cd2e8facc70beb942a7ca4427cda670fb6a65de` |
| Prompt release | `astrowoof.authoring.bounded_stable_facts.v1` |
| Prompt release SHA-256 | `ddf589eee616ef04b411a345d81c1fc635682766593ffed18020a72a329118fe` |

The prompt release explicitly allowlists the bounded profile, and the profile
requires `astrowoof-natal-authoring==0.4.70` plus
`semantic-projection-core==0.11.1` for the authoring role.

## Provider-free qualification performed

- Focused source contract suite: 21 tests passed (`bounded_eligibility`,
  processing-profile catalog, and runtime-profile coverage).
- `git diff --check` passed.
- The wheel contains 328 members, including the bounded eligibility module,
  bounded CLI, both package catalogs, and bounded prompt resources.
- Installed into an isolated target from the wheel with `--no-index --no-deps`.
  The installed package resolved version `0.4.70`, resolved the bounded
  profile/release allowlist, exposed `astrowoof-run-bounded-natal`, and built
  and validated an exact typed eligibility result.

## Joint API replay inputs

API must install only the retained wheel with the recorded SHA-256, supply the
pre-persisted native run/invocation IDs and accepted source digests, and prove
the receiver accepts the exact sealed result while refusing every altered
identity/disposition/provider-activity case. The source binding remains
API-owned evidence: SBE validates only its closed shape and preserves it
exactly; it does not invent a projection-set digest.
