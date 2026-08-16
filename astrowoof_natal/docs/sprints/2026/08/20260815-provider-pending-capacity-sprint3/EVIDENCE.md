# Provider-Pending Capacity Release Sprint 3 Evidence

## Planning baseline

```text
SBE release baseline: 0.4.2
latest immutable tag: astrowoof-natal-authoring-v0.4.2
implementation started: false
provider operations: 0
paid spend: $0
API key used: no
```

Initial code inspection established:

- public inspection computes provider continuation from necessary native actions;
- `WAITING_FOR_RESPONSE` also creates blocking local dependency
  `provider_result_reconciliation / provider_result_pending`;
- public quiescence is therefore `not_quiescent` while provider work remains;
- interactive Responses persist provider ID and waiting state, then can resume
  polling from a fresh process;
- the main coordinator publishes a complete snapshot after worker threads unwind;
- Batch already supports detach, but interactive Responses use a local polling
  timeout rather than a supported poll-once cycle; and
- no public durable `resume_not_before` currently exists.

No runtime test or mutation has been performed during planning.

## API review disposition

Accepted before implementation:

```text
resume_not_before: durable SBE lower-bound recommendation
early bounded resume: typed not_due, no provider poll
financial authority: API-owned; SBE emits custody-retention action evidence only
bounded cycle: small frozen wall-clock ceiling includes HTTP retrieval timeout
SBE cohort: native fresh-worker/bounded-resume proof
API cohort: actual capacity release and third-reading admission proof
required route: full exact interactive pipeline across every enabled stage
secondary routes: explicit parity-supported or fail-closed/deferred classification
```

## Slice 0: exact baseline

Committed planning baseline:

```text
1b47808 docs: plan provider pending capacity release
```

Provider-free fixture:

```text
run status: WAITING_FOR_RESPONSE
paid actions: 3
action state: WAITING x3
durable provider IDs: resp_provider_pending_1..3
snapshot valid: true
fresh-process inspection: pass, no mutation
provider continuation: true
local continuation: true
quiescence: not_quiescent
closeout: continuation_required
unresolved action IDs: 3
public capacity-release conclusion: absent
public next due time: absent
```

Focused command:

```text
python -m unittest \
  astrowoof_natal.tests.test_semantic_closure.TestSemanticClosure.test_background_timeout_preserves_response_for_same_attempt_resume \
  astrowoof_natal.tests.test_semantic_closure.TestSemanticClosure.test_pending_background_response_does_not_consume_a_retry \
  astrowoof_natal.tests.test_provider_pending_capacity -v
Ran 5 tests in 3.883s
OK
```

Complete suite:

```text
python -m unittest discover -s astrowoof_natal/tests -p "test_*.py"
Ran 313 tests in 160.785s
OK
```

Provider operations: 0. Paid spend: `$0`. API key used: no. Runtime release remains
0.4.2.

## Slice 3: bounded interactive reconciliation

Committed Slice 2 implementation:

```text
150d396 feat: persist provider reconciliation timing
```

Native assertions:

```text
early cycle: not_due, zero retrievals, zero mutation, no checkpoint
due wave: maximum 4 actions, parallel GET-only retrieval
HTTP retrieval: timeout <= 15 seconds, transport retries = 0
pending: backoff advances once, provider custody retained
transport warning: distinct timing outcome, authority unchanged
completed: immutable response evidence, immediate local continuation
local QA: cached response consumed, exactly one GET total, zero POST
mixed: completed local work plus pending-provider detach
identity mismatch: review_required, never ordinary retry
snapshot failure: checkpoint release false, retain_for_review
six due actions: four retrieved, two attempt counters unchanged
```

Focused command:

```text
python -m unittest \
  astrowoof_natal.tests.test_provider_pending_capacity \
  astrowoof_natal.tests.test_semantic_closure.TestSemanticClosure.test_bounded_cycle_consumes_completed_response_without_second_get_or_post -v
Ran 17 tests in 3.920s
OK
```

Initial complete suite before the final two focused guards:

```text
Ran 328 tests in 155.167s
OK
```

Final complete suite:

```text
python -m unittest discover -s astrowoof_natal/tests -p "test_*.py"
Ran 330 tests in 156.238s
OK
```

Provider operations: 0. Paid spend: `$0`. API key used: no. No action commitment,
authorization, consumption, or reported-cost record was created by a poll-only
cycle.

## Slice 4: exact-stage completeness and secondary routes

Committed Slice 3 implementation:

```text
d994a4a feat: add bounded provider reconciliation cycle
```

Route/stage assertions:

```text
exact interactive initial authoring: supported
exact interactive creative retry: supported
exact interactive polish: supported when frozen profile enables polish
exact interactive qualitative critic: supported when enabled
exact interactive qualitative candidate: supported when enabled
disabled optional stage: unsupported, zero retrieval
Batch: unsupported, zero retrieval
bounded Natal: unsupported, zero retrieval
unsupported/review/authority/terminal classification: nonmutating
delivery plus nonblocking critic: publishable + release_until_due
pending critic action: retain_consumer_authority = true
optional completed evidence: consumed with zero second GET and zero POST
```

Focused command:

```text
python -m unittest \
  astrowoof_natal.tests.test_provider_pending_capacity \
  astrowoof_natal.tests.test_semantic_closure.TestSemanticClosure.test_optional_complete_json_stages_consume_reconciled_evidence_without_get \
  astrowoof_natal.tests.test_semantic_closure.TestSemanticClosure.test_bounded_cycle_consumes_completed_response_without_second_get_or_post
Ran 22 tests in 5.164s
OK
```

Complete suite:

```text
python -m unittest discover -s astrowoof_natal/tests -p "test_*.py"
Ran 335 tests in 158.131s
OK
```

Provider operations: 0. Paid spend: `$0`. API key used: no. No build, version bump,
tag, or publication occurred. Runtime release remains 0.4.2.

## Slice 5: public interfaces, events, and consumer handoff

Committed Slice 4 implementation:

```text
d2c51de feat: complete bounded reconciliation stages
```

Installed/public assertions:

```text
CLI flag: --bounded-provider-reconciliation
CLI boundary: --resume + --provider openai + interactive only
spend authorization/reconciliation mutation in bounded mode: rejected
Python: reconciliation.run_bounded_authoring_reconciliation
result schema: astrowoof.provider_reconciliation_cycle_result.v0.1
progress evidence: strict local_continuation object
checkpoint events: run.detached, checkpoint.committed
not_due: no mutation, no result checkpoint, no checkpoint event
installed smoke resources: catalog + inspection v0.2 + policy + not_due fixture
HTTP status authority: API-persisted state only
```

Focused command:

```text
python -m unittest \
  astrowoof_natal.tests.test_lifecycle_consumer \
  astrowoof_natal.tests.test_lifecycle_contracts \
  astrowoof_natal.tests.test_provider_pending_capacity \
  astrowoof_natal.tests.test_execution_events
Ran 53 tests in 5.344s
OK
```

Complete suite:

```text
python -m unittest discover -s astrowoof_natal/tests -p "test_*.py"
Ran 338 tests in 158.531s
OK
```

Provider operations: 0. Paid spend: `$0`. API key used: no. No wheel, version bump,
tag, or publication occurred. Runtime release remains 0.4.2.

## Slice 6: native parallel and cross-platform qualification

Committed Slice 5 implementation:

```text
b21f333 feat: expose bounded reconciliation interfaces
```

Parallel native cohort:

```text
workspaces: aster, bramble, clover
aster + bramble: concurrent bounded cycles
outcome: detached_provider_pending
capacity: release_until_due
provider IDs and consumer-authority references: preserved
clover: independently inspectable, continue_local_cycle
focused cohort test: 1 passed in 0.292s
```

Candidate build/content:

```text
filename: astrowoof_natal_authoring-0.4.2-py3-none-any.whl
fixed SOURCE_DATE_EPOCH reproducible build A:
  2db4602132531c5842aca649ce2bdc453cb0923e821ee6a4d08f98da770ab1c5
fixed SOURCE_DATE_EPOCH reproducible build B:
  2db4602132531c5842aca649ce2bdc453cb0923e821ee6a4d08f98da770ab1c5
wheel members: 88
py.typed: present
lifecycle contract schema: present
reconciliation not_due fixture: present
```

Cross-platform installed checks:

```text
Windows Python 3.11.9:
  exact local SBE 0.4.2 + SPC 0.11.0 wheels installed
  pip check: no broken requirements
  astrowoof-lifecycle-smoke --require-installed: pass
  --bounded-provider-reconciliation installed CLI flag: present

Linux python:3.11-slim:
  exact local SBE 0.4.2 + SPC 0.11.0 wheels installed
  pip check: no broken requirements
  astrowoof-lifecycle-smoke --require-installed: pass
  --bounded-provider-reconciliation installed CLI flag: present
```

Complete suite:

```text
python -m unittest discover -s astrowoof_natal/tests -p "test_*.py"
Ran 339 tests in 158.959s
OK
```

Provider operations: 0. Paid spend: `$0`. API key used: no. The dedicated external
qualification tree was removed after compact hashes/results were retained here. No
version bump, tag, publication, or API capacity-allocation assertion occurred.

## Slice 7: closeout

Committed Slice 6 qualification:

```text
5793403 test: qualify provider pending capacity release
```

Final artifacts:

```text
FINAL API RESPONSE.md
API COMPANION ADOPTION CHECKLIST.md
results/SLICE 7 CLOSEOUT.md
Authoring Lifecycle Consumer Handoff.md
```

Release recommendation: pinnable patch 0.4.3 after final API review and separate
authorization. Provider operations: 0. Paid spend: `$0`. API key used: no. Version
bump, tag, publication, and API companion capacity-slot qualification remain
unperformed.

## Slice 1: proposed public contract

Committed Slice 0 baseline:

```text
aa65f77 test: reproduce provider pending capacity seam
```

Proposed contract identities:

```text
astrowoof.authoring_lifecycle_inspection.v0.2
astrowoof.provider_reconciliation_policy.v0.1
astrowoof.provider_reconciliation_cycle_result.v0.1
```

The contract freezes capacity/custody vocabulary, checkpoint-release safety,
durable lower-bound timing, early nonmutating `not_due`, bounded cycle/transport
limits, exact-interactive stage coverage, secondary-route fail-closed behavior,
events, compatibility, and API ownership. Values remain pending API review; no
runtime emits them yet. Lifecycle v0.1 remains the current runtime output during
this gate.

Provider operations: 0. Paid spend: `$0`. API key used: no.

API review accepted with one required timing correction:

```text
maximum_due_actions_per_cycle: 4
maximum_parallel_retrievals: 4
provider_retrieval_timeout_seconds: 15
maximum_cycle_wall_clock_seconds: 20
excess due action deferral: cycle finish + 15 seconds, no provider-attempt increment
custody projection stage: required immutable context
delivery with nonblocking critic pending: publishable + release_until_due
```

Packaged contract resources added:

```text
inspection v0.2 strict schema and sanitized fixture
reconciliation policy v0.1 strict schema and sanitized fixture
reconciliation cycle result v0.1 strict applied/not_due variants
not_due sanitized fixture with no result_checkpoint
contract catalog: v0.2 current; v0.1 historical
```

Focused command:

```text
python -m unittest astrowoof_natal.tests.test_lifecycle_contracts
Ran 19 tests in 0.089s
OK
```

Complete suite:

```text
python -m unittest discover -s astrowoof_natal/tests -p "test_*.py"
Ran 316 tests in 156.752s
OK
```

Provider operations: 0. Paid spend: `$0`. API key used: no. Runtime release remains
0.4.2 and still emits lifecycle inspection v0.1 pending Slice 2.

## Slice 2: durable timing and checkpoint projection

Committed Slice 1 contract:

```text
513614f feat: define provider reconciliation lifecycle contract
```

Implemented evidence:

```text
new provider identity: durable timing, initial due +15 seconds
backoff: 15, 30, 60, 120, 240, 300, 300... seconds
multiple actions: stable due-time/action-ID fan-in, maximum four next actions
future due: release_until_due only with complete safe checkpoint
due now: continue_local_cycle, provider authority retained
legacy missing timing: unsupported_retain_capacity, authority retained
state persisted before snapshot: retain_for_review, checkpoint release false
inspection current: astrowoof.authoring_lifecycle_inspection.v0.2
inspection historical: astrowoof.authoring_lifecycle_inspection.v0.1
```

Focused command after correcting historical consumer assertions:

```text
python -m unittest \
  astrowoof_natal.tests.test_lifecycle_consumer \
  astrowoof_natal.tests.test_provider_pending_capacity \
  astrowoof_natal.tests.test_lifecycle_contracts -v
Ran 30 tests in 2.776s
OK
```

First complete-suite diagnostic:

```text
Ran 320 tests in 159.594s
FAILED (failures=2)
both failures: consumer tests expected lifecycle inspection v0.1
resolution: update assertions to approved current v0.2 contract
```

Corrected complete suite:

```text
python -m unittest discover -s astrowoof_natal/tests -p "test_*.py"
Ran 320 tests in 154.782s
OK
```

Final gate after explicit Batch fail-closed coverage:

```text
focused lifecycle/capacity/consumer contracts: 31 tests, OK
complete repository suite: 321 tests in 148.808s, OK
```

Provider operations: 0. Paid spend: `$0`. API key used: no. Runtime release remains
0.4.2.
