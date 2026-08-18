# Slice 3 — Exact Interactive Concurrent Submission

Status: complete; awaiting Kevin review before commit.

## Outcome

Fresh exact-Natal interactive authoring now prepares one six-member initial wave at
one native state revision. SBE exposes six exact member actions, requires the API's
one wave envelope plus all six ordered member authorizations, applies that authority
all-or-none, and only then permits provider creation.

The six Responses creates overlap. Each worker crosses its own authorized
submission boundary, while all native ledger, journal, marker, and pass-state writes
remain serialized. A returned Response ID is recorded immediately even while other
creates remain active. After the create tasks unwind, SBE publishes one checkpoint
and detaches; no initial-wave thread polls for completion.

The ordinary short reconciliation cycle remains responsible for retrieval. Its
existing four-due/four-parallel limit is unchanged, so a six-member wave can settle
through two bounded retrieval subwaves. Pass-local creative retries and both Batch
routes are unchanged.

## Safety properties

- Interactive request construction has one canonical builder. A regression compares
  the create-wave payload with the payload sent by the established authoring path.
- Full-response cache warming is absent from the initial wave.
- The complete frozen run/stage ceiling is checked before SBE publishes a wave for
  external authorization.
- A partial, reordered, stale, or binding-mismatched authority set mutates no ledger
  authority and performs no provider create.
- Request payloads are durable private workspace artifacts and are re-hashed before
  submission.
- A durable provider ID is reused and never POSTed again. `SUBMITTING` without an ID
  becomes ambiguous on recovery and fails closed.
- Deterministic local idempotency keys remain correlation hints only; the code does
  not treat them as proof of provider idempotency.
- The six create calls use a 15-second per-call timeout and the coordinator enforces
  the frozen 20-second provider-I/O wave bound.

## Public invocation seam

The first invocation prepares the wave and exits at native external authority. The
authorized resume supplies:

```text
--initial-wave-authorization WAVE.json
--spend-authorization MEMBER-1.json
--spend-authorization MEMBER-2.json
--spend-authorization MEMBER-3.json
--spend-authorization MEMBER-4.json
--spend-authorization MEMBER-5.json
--spend-authorization MEMBER-6.json
```

The member documents must be in canonical pass order and exactly match the wave.

## Verification

- Transport-neutral plus exact integration focus: 12 tests passed in 3.881 seconds.
- Full exact semantic-closure plus coordinator suite: 96 tests passed in 160.701
  seconds (run before the final additional all-or-none regression, which passed in
  the focused run).
- Python compile: pass.
- `git diff --check`: pass (line-ending notices only).
- Provider operations: zero.
- Paid spend: `$0`.

## Scope retained for later slices

- Bounded interactive adoption is Slice 4.
- Batch compatibility proof is Slice 5.
- Failure-matrix and state-machine/oracle qualification is Slice 6.
- Consumer fixture/API review is Slice 7.
