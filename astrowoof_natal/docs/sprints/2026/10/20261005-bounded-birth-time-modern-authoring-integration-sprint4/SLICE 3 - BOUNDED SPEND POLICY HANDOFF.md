# Slice 3 — bounded paid-initialization spend-policy handoff

## Finding

The published `0.4.70` bounded route had a correct paid lifecycle but an
incomplete profile-bound command adapter: it resolved an OpenAI profile and
then constructed native generation settings without `spend_policy`. The
lifecycle therefore correctly raised before it created a ledger or workspace.

## 0.4.71 correction

`astrowoof-run-bounded-natal` now accepts `--spend-policy <json-path>` for a
new profile-bound OpenAI run. It loads and validates the policy before source
selection, workspace construction, or provider construction, then includes the
validated policy in the generation settings consumed by `create_bounded_run()`.
The native lifecycle seals that policy in the ordinary paid spend ledger.

The option is fail-closed:

- new profile-bound OpenAI runs require it;
- malformed/invalid policy input refuses before a workspace exists;
- resume refuses replacement policy, preserving the sealed ledger;
- reconciliation cannot use it through resume; and
- `--prepare-only` cannot manufacture a profile-bound OpenAI workspace using
  the fake provider.

No policy default, provider bypass, authorization shortcut, or change to the
provider-free under-floor eligibility result was introduced.

## Immutable profile bundle

The source candidate is versioned `0.4.71` and adds only successor bounded
records:

| Identity | Value |
| --- | --- |
| Processing profile | `astrowoof.bounded_natal.live.stable_facts.v2` |
| Profile digest | `083cec5b4e2631b3835bd1a0eb22c5d40bdbc9139f9a10aff580df6060ef0bf0` |
| Prompt release | `astrowoof.authoring.bounded_stable_facts.v2` |
| Prompt release digest | `f91501af0425ecf71e77ca6d1daacc582780de98f70c9fe01a4c4b1e9b49476b` |
| SBE worker descriptor digest | `89953f31ba9ea5f302bed0e8d14c2ef27a029d8a08d723958985d3f43bbc7b05` |
| Processing-profile catalog digest | `1e1cacec47969d4d19baaf1aecb677c7c6aa818cf3f7bfab998894e66f32ebc7` |
| Prompt-release catalog digest | `880671e257d6480e6957baa1dbd72873330981302c05014e18939dfe1f18473a` |

The older `stable_facts.v1` / `bounded_stable_facts.v1` records remain
unchanged and continue to name their `0.4.70` bundle.

## Provider-free proof

Focused tests passed:

```text
python -m unittest \
  astrowoof_natal.tests.test_bounded_eligibility \
  astrowoof_natal.tests.test_processing_profiles_slice1 \
  astrowoof_natal.tests.test_processing_profile_runtime_slice2

Ran 24 tests — OK
```

The real bounded CLI test uses a full 50-claim compiled fixture with a real
OpenAI-mode provider object, a sentinel API key, and disabled socket creation.
It creates the durable workspace, stores the exact policy, prepares six
`authoring_initial` actions, reaches `AWAITING_SPEND_AUTHORIZATION`, and
records no provider identity or submission.

## Next gate

Build a retained `0.4.71` candidate wheel, install that exact wheel in an
isolated API context, and replay API's real bounded initializer. API must prove
that the sealed profile/prompt bundle and native spend policy are admitted and
that the prepared workspace later resumes only under normal authority. This is
not authorization to tag, publish, deploy, activate a profile, or contact a
provider.
