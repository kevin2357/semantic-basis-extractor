# Slice 6 — Failure Atomicity and Lifecycle

## Result

The exact- and bounded-Natal interactive initial waves now publish one complete
pre-POST checkpoint after all six actions have durably entered `SUBMITTING`, but
before any provider request begins. Returned provider identities are then committed
one at a time under the native mutation lock, and each identity commit refreshes the
complete workspace snapshot before it is considered recoverably durable.

This preserves six-way provider I/O overlap without requiring six serial full-
workspace scans before submission. It also gives every interruption one of three
honest classifications:

- the create was definitely not attempted;
- the exact provider identity is present in the validated native checkpoint and
  only reconciliation may follow; or
- provider acceptance may have occurred without a durable identity, so the action
  is ambiguous, retains consumer authority, and cannot be resubmitted.

## Failure atomicity

The qualification interrupts an initial wave immediately after the first returned
identity receives its complete snapshot checkpoint. Although all six simulated
provider creates have returned by then, only the checkpointed identity is native
truth. On fresh execution SBE reuses that exact identity, classifies the other five
`SUBMITTING` actions as ambiguous, performs no additional provider POST, and
publishes another valid complete checkpoint. The same proof passes for exact and
bounded interactive routes.

The provider atomicity gap is irreducible: OpenAI does not provide a transactional
operation that atomically accepts a Response create and writes its provider ID into
SBE's workspace. If the process is lost after provider acceptance but before ID
durability, SBE fails closed. A deterministic local request key is correlation
material, not proof of provider idempotency.

## Lifecycle and authority

Validated lifecycle inspection of a six-ID detached wave reports:

- `execution_capacity.disposition = release_until_due`;
- six provider-custody actions;
- six retained consumer-authority actions; and
- no implication that worker-slot release releases API reservations or financial
  authority.

The zero-through-six known-ID matrix preserves every known provider-bound action in
the aggregate custody list. Zero known IDs remains an external-authority/local-
continuation outcome; one through six known IDs detach provider-pending; mixed
unstarted members remain explicit local continuation. Ambiguous members are never
flattened into an unstarted/retryable state.

No public lifecycle state or transition-oracle vocabulary was added. The existing
inspection v0.3, cycle-result v0.2, journal/result/receipt publication, capacity,
custody, authority, ambiguity, and terminal vocabularies remain sufficient and are
revalidated by the Slice 6 suite.

The broad exact regression also exposed one overly strong form of the Slice 4 QA
precedence rule: a run already marked for review could not advance after every
subject acquired concrete delivery evidence. The corrected ordering still prevents
weak pass-derived persistence from erasing final QA, while allowing valid all-
subject delivery evidence to close the run.

## Tests

- Zero-through-six known provider IDs with exact custody preservation.
- Exact interactive interruption after the first identity checkpoint, validated
  snapshot, fresh execution, five ambiguities, and zero duplicate creates.
- Bounded interactive equivalent of the same interruption and recovery.
- Six-ID exact and bounded detached lifecycle inspection with capacity release and
  retained custody/consumer authority.
- Existing single-writer, stale-observation, not-due, reconciliation, native
  result/receipt, and route-parity contract suites.

All tests use scripted/provider-free transports. Provider operations and paid spend:
zero.
