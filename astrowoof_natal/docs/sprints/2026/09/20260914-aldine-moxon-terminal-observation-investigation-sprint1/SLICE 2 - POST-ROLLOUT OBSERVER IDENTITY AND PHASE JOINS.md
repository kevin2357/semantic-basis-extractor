# Slice 2 — Post-Rollout Observer Identity and Phase Joins

## Decision

Slice 2 proves exact terminal-result carry-forward and excludes native root
drift, release-pair skew, and any attempted Better Stack delivery. It cannot
honestly distinguish exact-read, evidence collection, packet construction, or
request-preflight failure from the retained telemetry. The remaining failure
is inside API's locally caught `capture_or_preflight` region and requires the
gated exact-workspace reproduction (or equivalent phase-safe diagnostics).

## Exact terminal joins

| Pup | Producer contract | Exact result | Terminal observer attempt | Outcome |
| --- | --- | --- | --- | --- |
| Aldine | native result v0.2 `review_required`, final custody | `nres_d0568048c5fc2d9cfd68d7c7` | final generation-9 closeout attempt | `unavailable / capture_or_preflight` |
| Moxon | native result v0.1 `delivery_complete` | `nres_5a90fadd039f369c7303ecd3` | generation-9 delivery/publication retry | `unavailable / capture_or_preflight` |

The observer completion rows carry those exact IDs. Neither route uses a
run-wide or latest-result selector. The two producer contracts remain distinct
even though API reports the same flattened local failure kind.

## Release and root findings

- Every target-bound SBE fingerprint reports SBE `0.4.61` and SPC `0.11.1`.
- The worker instance is the post-Sprint-97 instance for both pups. API `main`
  contains root correction `6411cf5` and rollout evidence commit `fe217d1`.
- Aldine's native logical-root digest is stable as
  `2efa0c6ebb7f71d77b5bffb607f1de67c3ca65d1f3312747038f68062a007d5e`
  through its final revision.
- Moxon's native logical-root digest is stable as
  `a242cabd6f407a38970d248265aa3c65410bfb1a02c7a0597be21a6e6701918a`
  through delivery revision 61.
- All target fingerprint validations are `valid`; neither trace shows native
  root drift or snapshot invalidation before terminal publication.
- API source prepares one registered job workspace, passes its `sbe` child
  directly to `observe_terminal()`, and the corrected checkpoint writers
  persist the resolved physical workspace rather than an API-run-derived root.

The four-root equality cannot be promoted from source invariant to exact live
fact from these logs alone. `worker.checkpoint.accepted` omits
`logical_restore_path`; registration and observer events omit their safe root
digest. Reconstructing path strings from run IDs would violate the approved
evidence method and would not prove what the live process actually carried.

## First failing phase

The strongest supported localization is:

1. exact result handoff reached `EditorialReviewObserver.observe_terminal()`;
2. the call returned before any `EditorialReviewPostOutcome` existed;
3. API's single `try` region covers native exact read, evidence collection,
   capture-status construction, packet/projection/artifact construction,
   envelope construction, and request preparation;
4. its exception handler collapses transport-domain, filesystem, value,
   key, and type exceptions to `capture_or_preflight` without a phase or safe
   exception fingerprint.

Therefore no HTTP request or Better Stack failure is established, but no
specific earlier subphase is established either. The shared branch is not
evidence that Aldine v0.2 and Moxon v0.1 failed for the same internal reason.

## Next gate

Request joint review before Slice 3. If approved, obtain immutable coordinates
for exactly the terminal checkpoint of each named job and separately obtain
owner authorization for one conditional HEAD and one bounded GET per object.
Run the exact public capture at the contract-bound root inside the established
read-only, network-disabled container. No provider, retry, reconciliation,
workspace mutation, or live QA action is needed.
