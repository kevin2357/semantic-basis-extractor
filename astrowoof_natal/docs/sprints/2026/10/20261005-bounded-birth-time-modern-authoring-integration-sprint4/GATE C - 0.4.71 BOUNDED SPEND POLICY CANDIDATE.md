# Gate C — 0.4.71 bounded spend-policy candidate

## Scope

This is a retained, unpublished provider-free candidate for API's joined
installed-wheel admission. It is not a tag, public package publication, worker
deployment, profile activation, or authorization to make a provider request.

## Candidate identity

| Field | Value |
| --- | --- |
| Artifact-source commit | `234aa64cffa36ab7ad1f1695f1226304ceb55982` |
| Distribution version | `0.4.71` |
| Wheel path | `C:\tmp\sbe-0.4.71-release-lock-20261008\wheel-a\astrowoof_natal_authoring-0.4.71-py3-none-any.whl` |
| Wheel SHA-256 | `f230893ce5e3b735d9e130c6fbbe92f472dfb20f665daec5eb5fe39cf2af5527` |
| Wheel bytes | `1,434,161` |
| Wheel members | `328` |
| Recorded `SOURCE_DATE_EPOCH` | `1791452810` |
| Build | Two clean canonical-LF Git archives with `pip wheel --no-deps --no-build-isolation` |

## Immutable bounded bundle

| Field | Value |
| --- | --- |
| Profile ID | `astrowoof.bounded_natal.live.stable_facts.v2` |
| Profile SHA-256 | `083cec5b4e2631b3835bd1a0eb22c5d40bdbc9139f9a10aff580df6060ef0bf0` |
| Prompt release ID | `astrowoof.authoring.bounded_stable_facts.v2` |
| Prompt release SHA-256 | `f91501af0425ecf71e77ca6d1daacc582780de98f70c9fe01a4c4b1e9b49476b` |
| SBE descriptor SHA-256 | `89953f31ba9ea5f302bed0e8d14c2ef27a029d8a08d723958985d3f43bbc7b05` |
| Required SBE package | `astrowoof-natal-authoring==0.4.71` |
| Required SPC package | `semantic-projection-core==0.11.1` |
| Profile catalog SHA-256 | `1e1cacec47969d4d19baaf1aecb677c7c6aa818cf3f7bfab998894e66f32ebc7` |
| Prompt catalog SHA-256 | `880671e257d6480e6957baa1dbd72873330981302c05014e18939dfe1f18473a` |

The old bounded `v1` profile/release records are retained unchanged for the
published `0.4.70` bundle. API must admit this `v2` identity independently.

## SBE proof

The focused source gate ran 24 tests successfully across bounded eligibility,
profile catalog/runtime, and immutable binding coverage. Its paid CLI case
uses a full 50-claim fixture, a sentinel OpenAI key, and disabled sockets. A
valid policy creates the durable OpenAI-bound workspace, seals the policy in
the ledger, prepares six `authoring_initial` actions, returns the ordinary
authority-boundary result, and reaches zero provider submission/identity.

Two independent clean archive builds produced the exact filename, member
inventory, byte size, and SHA-256 above. The wheel contains no cache, build,
bytecode, or generated temporary members. A fresh out-of-checkout Windows
environment installed the exact wheel and local SPC `0.11.1` wheel; `pip
check` passed and `astrowoof-release-smoke --require-installed` completed
with a full deterministic delivery, forced retry, manifest-integrity, and
cleanup pass. The installed runtime loaded from `site-packages`, reported
`0.4.71`, and exposed `--spend-policy` on the bounded CLI.

## API Gate C request

Install **only this SHA-bound wheel** into an isolated API context. The earlier
working-tree candidate (`b6683ba1…e954d00`) is superseded and must not be used
for release admission. Use the
`v2` processing-profile handoff and provide the API-owned policy through the
new `--spend-policy <json-path>` argument on a new bounded initialization.
Prove all of the following without network/provider access:

1. the API-provided policy creates a durable OpenAI-bound bounded workspace;
2. the initial wave contains exactly six prepared actions and no provider
   custody or submission;
3. the sealed policy/profile/prompt binding survives the later resume handoff;
4. missing/malformed policy remains a pre-workspace refusal; and
5. the older `v1` identity is neither rewritten nor substituted.

Any release lock, tag, publication, context deployment, profile selection, or
provider-backed QA action remains a separate approval.
