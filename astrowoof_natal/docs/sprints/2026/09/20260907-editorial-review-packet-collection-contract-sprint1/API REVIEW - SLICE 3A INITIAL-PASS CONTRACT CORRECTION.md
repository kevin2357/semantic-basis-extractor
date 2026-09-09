# API review — Slice 3A initial-pass contract correction

## Decision

**Approved.** The v2 correction faithfully implements the jointly frozen
stage-discriminated model and removes the synthetic initial-pass deck fiction.
SBE may proceed to the narrow, read-only Slice 3 runtime builder under the
existing ordinary-live-exact fences.

## Evidence accepted

- `initial_pass_materialization` is closed and stage-specific: it retains
  released-pass, source-basis, accepted-workspace, authored-claim-set, and
  exact action/binding/Response evidence without calling either side a deck.
- The one assembly-owned bridge is the right missing relation. It binds exactly
  the complete six-pass population and establishes the first real whole deck
  consumed by the first post-initial decision. It is neither a seventh decision
  nor a hidden provider/lifecycle event.
- Later creative-retry and optional-stage decisions retain the prior
  whole-deck algebra. Versioning packet, decision, projection, transport, and
  semantic-contract resources together prevents a v1 reader from silently
  accepting the altered meaning.
- The five additional rehashed counterexamples cover the critical new lies:
  false whole-deck initial pass, duplicate/reordered materialization, incorrect
  pass identity, incomplete bridge membership, and a mismatched first input.
- The bounded Alloy v2 world is useful additional design evidence, with an
  inhabited world and no bounded counterexamples for its three stated
  assertions. It remains optional design tooling, not release or runtime
  authority.
- I independently ran the focused contract modules in the supported source
  layout: **23 passed, 1 expected optional `jsonschema` skip**. The scoped diff
  hygiene check is clean.

## Runtime fences retained

The builder may use only the explicit invocation-returned result and the
validated read-only exact-result reader. It must not discover a latest result,
mutate a workspace, access provider/storage/network/API/database authority, or
cause a lifecycle, custody, retry, spend, or terminal-state change. Every
excluded, incomplete, contradictory, unknown-version, record-overflow, or
byte-overflow case still returns a typed status with no partial packet or
projection set.

Artifact policy is unchanged: direct initial-pass digest identities are
sufficient; this approval does not introduce workspace/claim-set artifact
payload delivery.

## Next boundary

After the builder has provider-free qualification and exact no-side-effect
evidence, pause for the existing package/installed-wheel review. Neither a
runtime integration nor this approval authorizes Better Stack transport,
release, deployment, or live retained-workspace access.
