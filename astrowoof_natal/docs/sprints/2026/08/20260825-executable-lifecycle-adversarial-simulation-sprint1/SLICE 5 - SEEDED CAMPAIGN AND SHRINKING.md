# Slice 5 — Seeded Campaign and Shrinking

Status: implemented and focused-qualified

## Result

The campaign runner performs deterministic state-aware walks over the redacted
action/binding projection and closed clock model. At every step it derives the
currently enabled event inventory, selects from that inventory with a frozen seed,
applies the event, and records pre/post semantic identities and classification.

The ordinary CI seed set covers exact and bounded routes. Campaign artifacts retain
the seed, requested/executed step counts, ordered transitions, transition-kind
coverage, final state identity, and whole-walk digest. Replaying the declared seed,
route, and bound must reproduce the complete artifact exactly.

The initial shrinker targets the historical no-op checkpoint-republish stutter. It
removes irrelevant time/retrieval events while repeatedly preserving the semantic
violation, yielding the one-event causal witness.

## Safety boundary

- No arbitrary native-byte mutation is exposed.
- Random selection is limited to enabled semantic events.
- Deliberately adversarial injections are named separately.
- The campaign is qualification-only, network-incapable, credential-free, and USD 0.

## Focused evidence

- Fixed seeds: 7, 19, and 41.
- Routes: exact Natal and bounded Natal.
- Exact replay and mutation-refusal coverage included.
- Counterexample shrunk to `adversarial:noop_checkpoint_republish`.

