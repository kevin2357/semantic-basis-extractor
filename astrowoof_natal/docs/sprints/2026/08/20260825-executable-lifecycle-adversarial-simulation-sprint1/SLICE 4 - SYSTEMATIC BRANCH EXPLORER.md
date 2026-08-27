# Slice 4 — Systematic Branch Explorer

Status: implemented and focused-qualified; paused for API review

## Result

SBE now has a bounded breadth-first explorer with a strict redacted action/member
projection. Every member joins:

- one opaque action reference;
- one complete public binding digest;
- create-entry state and create count;
- optional durable provider-identity digest; and
- retrieval count.

The validator enforces create-at-most-once per exact action/binding, retrieval only
after durable identity, and fail-closed ambiguity. This closes the gap identified in
the Slice 3 review without widening frozen adversarial trace v1.

## Current exploration proof

The provider-free qualification:

1. materializes and inspects the real SBE Muffin review/no-action workspace through
   the production v0.7 boundary and finds the minimal one-step stutter;
2. begins from a six-member partial wave with four durable identities and two
   unentered members;
3. proves a distinct unfinished member can be created;
4. proves a second create for the same action/binding is refused;
5. reaches the same final projection through member 5→6 and 6→5 and deduplicates
   that semantic successor; and
6. proves 300 one-second clock steps and acceleration to the declared five-minute
   boundary yield the same canonical instant.

The Muffin cell invokes a real native lifecycle reader. The partial-wave state is an
explicit abstract model over redacted native authority facts; it does not claim to
have submitted or mutated a production workspace. Later joined fixtures may bind
that projection to the installed runtime adapter without changing its invariant.

## Bounds and safety

- Qualification depth is explicit and limited to 2–8.
- Breadth-first order retains the shortest witness.
- Semantic state deduplication is digest-based and deterministic.
- No network capability, credentials, provider operation, retained QA, or spend is
  accepted or used.

## Focused evidence

- 31 adversarial tests passed.
- One optional `jsonschema` check skipped in the lean interpreter.
- `git diff --check` passed with non-failing Windows line-ending notices only.

