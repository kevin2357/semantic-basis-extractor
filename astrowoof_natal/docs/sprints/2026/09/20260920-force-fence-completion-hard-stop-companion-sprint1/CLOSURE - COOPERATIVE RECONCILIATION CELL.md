# Closure — cooperative reconciliation hard-stop companion

## Outcome

**Complete.** The first active `provider_reconciliation_cycle` hard-stop path
now has a fully qualified cross-repository boundary:

`exact API launch → later force fence → exact SBE v1 suspension handoff →
API direct-child exit proof → exact fenced allocation completion`.

SBE contributes only the existing safe-point producer and public closed-reader
contract. It neither claims process exit, releases capacity, cancels provider
work, nor changes retained custody.

## Final provider-free evidence

- API's R1 test captures the actual `Popen` argv and verifies its canonical
  digest against the persisted supervision envelope.
- API's R2 completion evidence is explicitly scoped to `direct_child_exit`;
  it retains PID, permitted return code, UTC observation, command digest, the
  two distinct invocation identities, and the exact named SBE handoff.
- The only wheel used in the joint replay was published SBE `0.4.66`:
  `astrowoof_natal_authoring-0.4.66-py3-none-any.whl`, SHA-256
  `ec30e79780b7a4ffc47510ec25f5b6cb3b09639a8b6a2ec6b2def0661f871daf`.
- The installed-wheel joined harness passed exact publication and replay with
  zero provider operations/spend, R2 access, live termination, and
  pre-completion capacity release.
- API's corresponding cooperative matrix passed 164 provider-free tests using
  that isolated installed wheel.

## Deliberate non-claims

This closure does not qualify an unsupported SBE route, worker replacement,
collateral-child handling, or live QA operation. Those are API/operator
concerns under their later gates. They should reopen SBE work only if they
surface a concrete missing native evidence or reader behavior.
