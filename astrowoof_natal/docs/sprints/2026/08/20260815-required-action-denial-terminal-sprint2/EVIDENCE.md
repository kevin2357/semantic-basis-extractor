# Required-Action Denial Terminalization Sprint 2 Evidence

Status: in progress; Slice 0 complete and pending review.

## Planning inspection

Reviewed:

- the supplied API handoff retained in `SOURCE REQUEST.md`;
- the completed atomic providerless-denial Sprint 1 plan/evidence;
- `astrowoof_natal_authoring.lifecycle` action projection, local dependencies,
  inspection, single/batch denial, recovery, and closeout;
- lifecycle schemas, fixtures, CLI, installed smoke, and consumer handoff; and
- denial, batch denial, bounded lifecycle, and closeout test inventories.

Preliminary finding: `DENIED_PROVIDERLESS` removes action necessity, while the
parent `AUTHORING` status independently synthesizes blocking retry preparation.
This is a hypothesis to reproduce in Slice 0, not yet a completed diagnosis.

The complete consumer requirement additionally freezes the expected semantic
shape: terminal true, zero provider/local dependencies, no local continuation,
and either budget exhaustion or an explicit policy-stop outcome. The leading plan
proposal is `BUDGET_EXHAUSTED` with a separate external-authority reason; this is
pending contract review rather than implemented evidence.

Provider operations: 0. Paid spend: `$0`. API key used: no.
Tests run: none. Release artifact produced: none.

## Slice 0: exact reproduction

Planning commit:

```text
f8d4851 docs: plan required-action denial terminalization sprint
```

Focused command:

```text
python -m unittest \
  astrowoof_natal.tests.test_negative_authorization \
  astrowoof_natal.tests.test_batch_negative_authorization \
  astrowoof_natal.tests.test_bounded_lifecycle -v
Ran 38 tests in 23.233s
OK
```

Full-suite command:

```text
python -m unittest discover -s astrowoof_natal/tests -p "test_*.py"
Ran 296 tests in 137.913s
OK
```

Reproduced state after valid required-action denial:

```text
action state: DENIED_PROVIDERLESS
run status: AUTHORING (exact fixture) / AWAITING_SPEND_AUTHORIZATION (bounded)
provider continuation: false
local continuation: true
local dependency: retry_preparation / authoring_continuation or authorization pause
terminal outcome: nonterminal
closeout disposition: continuation_required
unresolved action IDs: []
exact replay: idempotent_replay
provider submissions: 0
```

The exact single and batch fixtures use authorized, unconsumed creative-retry
actions with `external_authority_denied`. Both prove native requiredness before the
mutation and non-necessity afterward. The real bounded fixture uses a paid provider
double, freezes the generation/spend profile, prepares its required initial action,
denies it providerlessly, validates the complete snapshot, and then calls ordinary
resume. Resume raises `AwaitingSpendAuthorization` without invoking the provider.

Action denial, positive authorization history, exact replay, and snapshot safety
all behave correctly. The gap is the absence of a run-level terminal consequence,
which leaves both runner and lifecycle projections treating work as resumable.

Provider operations: 0. Paid spend: `$0`. API key used: no. Release artifact: none.

## Slice 2: atomic new-denial terminalization

Committed Slice 1 contract baseline:

```text
984d3fc feat: define required-denial terminal transition contract
```

Final focused command:

```text
python -m unittest \
  astrowoof_natal.tests.test_lifecycle_consumer \
  astrowoof_natal.tests.test_negative_authorization \
  astrowoof_natal.tests.test_batch_negative_authorization \
  astrowoof_natal.tests.test_bounded_lifecycle \
  astrowoof_natal.tests.test_lifecycle_closeout \
  astrowoof_natal.tests.test_lifecycle_contracts -v
Ran 70 tests in 19.637s
OK
```

Full-suite command:

```text
python -m unittest discover -s astrowoof_natal/tests -p "test_*.py"
Ran 301 tests in 121.713s
OK
```

Proven behaviors:

- one required spend denial -> v0.2 result, one `BUDGET_EXHAUSTED` transition;
- one required product denial -> `POLICY_STOPPED`;
- mixed required batch -> one policy-stop transition with exact causal members;
- optional bounded polish denial -> skip and delivery, no resubmission;
- accepted delivery cleanup -> delivery status preserved;
- cleanup after prior terminalization -> first terminal authority preserved;
- public state -> bounded outcome/cause/revision only;
- inspection/closeout -> terminal, quiescent, no dependencies/actions, closed;
- exact replay -> stable checkpoint and no second transition;
- provider identity/consumption/report/ambiguity refusals -> unchanged; and
- installed lifecycle smoke/CLI consumer expectations -> v0.2 and one terminal
  observation.

Provider operations: 0. Paid spend: `$0`. API key used: no. Release artifact: none.

## Slice 1: proposed terminal contract

The reviewed proposal is recorded in `results/SLICE 1 CONTRACT.md`. It freezes:

- required/optional/delivery precedence;
- external-spend versus product-policy/cancellation status and cause mapping;
- final semantics of an accepted denial request;
- single/batch v0.2 result-transition evidence;
- terminal inspection, quiescence, and closed non-delivery closeout shape;
- runner short-circuit requirements;
- event ordering/redaction; and
- a narrowly verified retained-0.4.1 reconciliation seam.

The API accepted all seven questions and requested dual batch provenance lists.
The approved contract now packages:

- `astrowoof.provider_negative_authorization_result.v0.2`;
- `astrowoof.provider_negative_authorization_batch_result.v0.2`;
- required `run_transition` on successful v0.2 results;
- ordered `denied_action_ids` plus causal `required_action_ids`;
- closed transition outcome, trigger, and terminal-reason vocabularies; and
- sanitized required-single and mixed required/optional batch fixtures.

Historical v0.1 schemas remain readable and requests remain v0.1. The runtime does
not emit v0.2 until Slice 2 implements the matching atomic mutation.

Focused command:

```text
python -m unittest astrowoof_natal.tests.test_lifecycle_contracts -v
Ran 16 tests in 0.015s
OK
```

Full-suite command:

```text
python -m unittest discover -s astrowoof_natal/tests -p "test_*.py"
Ran 298 tests in 129.648s
OK
```

Provider operations: 0. Paid spend: `$0`. API key used: no. Release artifact: none.
