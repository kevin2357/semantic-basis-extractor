# Slice 1β — qualified worker compatibility descriptors

## Result

Slice 1β is complete provider-free. The canonical profile now carries a
closed `worker_compatibility` map with the two actual process-boundary roles:
`deterministic_runtime` and `sbe_authoring`.

Each entry is an `astrowoof.worker_compatibility.v1` object containing a
closed, sorted list of exact required distributions and a SHA-256 over its
canonical JSON representation excluding the self digest. This makes the value
derived qualification evidence rather than a caller-created label.

| Role | Required distributions | Compatibility SHA-256 |
| --- | --- | --- |
| `deterministic_runtime` | `astrology-graph-foundry==0.8.1`, `semantic-projection-core==0.11.1` | `df053cefa0e436d784c6b49cc3b74d1fe9b33d0f6c5a18576a408934cafa1fbb` |
| `sbe_authoring` | `astrowoof-natal-authoring==0.4.66`, `semantic-projection-core==0.11.1` | `ed51592f2d32ec803054ec0353c7ac5dfac336475c43c6992404a9449559e581` |

The republished profile remains
`astrowoof.exact_natal.live.compat.v1`; its new SHA-256 is
`28a92d24dbbc10597c11c5bca0309ee9ea7aad5168069138f5e76dd90e32bf7a`.
The profile-catalog SHA-256 is now
`3c90d1a570ada01caefec7f830bc5c17bf3995fa96365953b7ec8aaff4f7c74c`.

## Important two-layer distinction

The profile's compatibility descriptors are immutable *package requirements*.
They are intentionally different from the API control plane's
environment-specific deployed-worker `compatibility_identity`, which varies by
QA/production rollout and continues to fence the actual selected image. Putting
that environment state into a package-installed cross-environment profile
would make every normal rollout require a new SBE release and would turn a
deployment selector into processing semantics.

Later worker validation must therefore establish both facts:

1. its installed package set matches the profile-owned role descriptor; and
2. API's existing control-plane deployment identity matches the admitted
   generation-manifest binding.

Neither fact can substitute for the other.

## Coverage

The focused processing-profile module now proves that both descriptors are
present, role-bound, digest-validated, and included in the parent profile
digest. A changed required version yields a new child digest and a new parent
profile digest; a role/key mismatch refuses even if both digests are recomputed.

Focused result: **22 passed** (`test_processing_profiles_slice1` plus manifest
runner), with zero provider operations.

## Gate B closure request

API should review the replacement profile digest and the two descriptor field
names. If accepted, API may use the profile reference above in its immutable
generation-manifest design and both repositories may begin their next
provider-free consumer slices. A release candidate will update the SBE package
version requirement atomically with any future SBE version bump and obtain a
new profile digest; it must never silently reuse this digest.
