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

### API consumer review

Approved without blocking revisions. The API explicitly accepted:

- the fixed 32-action maximum;
- release only from exact matching successful/replay members with
  `release_eligible: true`;
- zero release for every refused batch, including `eligible` members;
- exact replay binding to the original observation timestamp;
- provider-bound evidence precedence over generic staleness;
- `eligible`/`not_evaluated` refusal semantics; and
- ordered per-action then batch events on first application, with batch-only event
  observation on exact replay.

The optional batch refusal event is diagnostic only and may contain only bounded,
redacted category information.

## Slice 2: Locked all-or-none preflight

Implemented and evidenced:

- strict runtime request validation before workspace access;
- one acquisition of the existing lifecycle/spend cross-process lock;
- one locked state/snapshot/inspection decision basis;
- ordered all-member resolution and eligibility evaluation;
- provider-safety evidence precedence over generic staleness;
- typed batch and per-member refusals; and
- authoritative workspace byte equality across all normal refusal cases and the
  successful preflight.

Focused command:

```text
python -m unittest astrowoof_natal.tests.test_batch_negative_authorization \
  astrowoof_natal.tests.test_lifecycle_contracts -v
Ran 21 tests in 0.874s
OK
```

Full-suite command:

```text
python -m unittest discover -s astrowoof_natal/tests -p "test_*.py"
Ran 285 tests in 119.423s
OK
```

Provider operations: 0. Paid spend: $0. API key used: no.

## Slice 1: Versioned batch contract

Added package-resource contracts:

- `astrowoof.provider_negative_authorization_batch_request.v0.1`;
- `astrowoof.provider_negative_authorization_batch_result.v0.1`;
- `authorization.denied_providerless_batch` under `sbe.execution_event.v1`;
- four sanitized request/applied/replay/refusal fixtures; and
- contract/payload catalog entries.

Contract properties evidenced by tests:

- strict object shapes and closed vocabularies;
- 1 through 32 ordered members;
- canonical digest stability across JSON formatting/key order;
- digest difference after member reordering;
- fixture result digest exactly matches its request;
- rejection of empty/oversized requests, unknown fields, and multiline external
  authority references;
- explicit semantic ownership of duplicate-ID refusal by locked preflight;
- distinct applied, replay, and all-or-none refusal results; and
- packaged resource discovery through the supported resource accessor.

Focused command after catalog synchronization:

```text
python -m unittest astrowoof_natal.tests.test_lifecycle_contracts \
  astrowoof_natal.tests.test_execution_events -v
Ran 21 tests in 0.153s
OK
```

The first full-suite attempt correctly failed one catalog-consistency test because
the code-owned required-payload map lacked the newly declared batch event. After
adding the exact required fields, the final full-suite command passed:

```text
python -m unittest discover -s astrowoof_natal/tests -p "test_*.py"
Ran 278 tests in 108.805s
OK
```

Provider operations: 0. Paid spend: $0. API key used: no.
