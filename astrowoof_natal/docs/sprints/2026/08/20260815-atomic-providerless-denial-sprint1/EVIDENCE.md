# Atomic Providerless-Denial Batch Lifecycle Sprint 1 Evidence

Status: in progress; Slice 0 complete and pending review.

## Planning baseline reviewed

- `docs/sprints/README.md`
- `docs/sprints/2026/08/20260813-log-authoring-lifecycle-sprint1/PLAN.md`
- `docs/sprints/2026/08/20260813-log-authoring-lifecycle-sprint1/LOG.md`
- `docs/sprints/2026/08/20260813-log-authoring-lifecycle-sprint1/SLICE 3 NEGATIVE AUTHORIZATION.md`
- `docs/sprints/2026/08/20260813-log-authoring-lifecycle-sprint1/SLICE 6 CONSUMER.md`
- `src/astrowoof_natal_authoring/lifecycle.py`
- `src/astrowoof_natal_authoring/lifecycle_contracts.py`
- `src/astrowoof_natal_authoring/cli/lifecycle.py`
- `docs/post_extraction_authoring/Authoring Lifecycle Consumer Handoff.md`
- focused lifecycle/negative-authorization test inventory

## Provider and spend evidence

- Provider operations: 0
- Paid spend: $0
- API key used: no
- Release artifact produced: no

Commands, counts, fixture hashes, mutation-boundary results, wheel hashes, and
consumer acceptance will be added only as the corresponding slices execute.

## Slice 0: Baseline and fixture reproduction

Planning commit pushed before execution:

```text
92cebbc docs: plan atomic providerless denial sprint
```

Focused command:

```text
python -m unittest astrowoof_natal.tests.test_negative_authorization -v
Ran 12 tests in 0.999s
OK
```

Full-suite command:

```text
python -m unittest discover -s astrowoof_natal/tests -p "test_*.py"
Ran 275 tests in 114.487s
OK
```

The new terminal two-action baseline proves:

- `inspect_lifecycle()` reports `delivery_complete` while both authorized,
  unconsumed creative-retry actions are independently providerless-denial eligible;
- the first single-action denial returns `applied`;
- exact replay of that first request returns `idempotent_replay`;
- denial of the second action using the same original observation returns
  `stale_observation`;
- the stale refusal does not change authoritative workspace hashes;
- the first action remains `DENIED_PROVIDERLESS` and the second remains
  `AUTHORIZED`; and
- accepted deck and delivery SHA-256 identities are unchanged throughout.

Provider operations: 0. Paid spend: $0. API key used: no.
