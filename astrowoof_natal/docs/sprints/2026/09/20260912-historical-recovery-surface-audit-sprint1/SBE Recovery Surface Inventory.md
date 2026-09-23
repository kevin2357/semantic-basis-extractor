# SBE Recovery Surface Inventory

## Scope and method

This is the combined Slice 0alpha incident-change reconnaissance and Slice 0
current native-surface inventory for Control Room issue #5. It traces the API
incident set through SBE sprint records, commit history, current public
readers/CLIs/package resources, and test coverage. It makes no removal decision.

## Slice 0alpha — API incident map to SBE work

| API sprint | Matching SBE companion work | Current native conclusion |
| --- | --- | --- |
| 26 native terminal ingestion | `20260817-native-terminal-transition-journal-sprint1` | Generic sealed journal/result/receipt reader and publication boundary. |
| 27 lifecycle-inspection compatibility | `20260819-provider-pending-lifecycle-classification-patch-sprint3` | Generic released v0.5 lifecycle inspection; not a one-off replay. |
| 32 provider-pending reconciliation | `20260823-provider-pending-observation-idempotency-sprint1` and provider-reconciliation follow-ons | Generic custody-preserving reconciliation and temporal projection; API-only recovery commands do not imply native-only bridges. |
| 33 retained initial-wave fence | `20260820-retained-initial-wave-next-action-fence-sprint1` | General no-duplicate/new-initial-wave safety fence. |
| 35 executable-contract qualification | external-authority contract and execution-bridge work, including `20260824-external-authority-v2-execution-bridge-sprint1` | Public command/result boundary used by current execution, not retained-run rescue code. |
| 37 legacy provider-pending/temporal bridge | `20260824-legacy-provider-pending-bridge-compatibility-sprint1` and `20260824-temporal-lifecycle-vocabulary-compatibility-patch-sprint1` | Narrow historical API bridge depended on shared v0.5 reader/projection support; no SBE command is keyed to Aster or a named retained run. |
| 38 stuck-run terminal retirement | `20260824-operator-stuck-run-native-retirement-patch-sprint1` | Generic, exact quiescent/provider-free retirement capability with closed refusals. |

The companion mapping is evidence of origin, not a removability decision. In
particular, Sprint 37 is the strongest historical API candidate but it consumes
the same SBE v0.5 lifecycle evidence used by current public readers.

## Inventory records

### SBE-01 — sealed native transition journal and reader

- **Source / provenance:** `native_transitions.py`, `cli/native_transition.py`,
  package contract resources; Sprint 26 companion; commits `590da05d`,
  `64836b0b`, `8385990c`, and `ea071dba`.
- **Accepted evidence:** sealed native transition journal/result/receipt shapes;
  unsupported or legacy evidence yields typed unavailable/unsupported outcomes,
  not inferred transition truth.
- **Reachability:** public Python exports and CLI; current API worker terminal
  ingress; packaged contract resources; not fixture-only.
- **Authority / failure:** SBE validates native evidence only; API owns durable
  state/capacity mutation. Invalid snapshot/journal evidence fails closed.
- **Tests / posture:** native-transition and consumer-ingestion fixtures plus
  current API worker coverage. **Durable capability.**

### SBE-02 — lifecycle inspection and temporal projection

- **Source / provenance:** `lifecycle.py`, `lifecycle_contracts.py`,
  `temporal_lifecycle.py`, `cli/lifecycle.py`; Sprint 27/32/37 companion work;
  commits `d29d923f` and `9591385f` among the temporal-vocabulary releases.
- **Accepted evidence:** released lifecycle inspection v0.5 and explicit
  temporal projections/contracts v1-v3. The v0.5 reader is production runtime
  behavior, not merely a fixture adapter.
- **Reachability:** public Python exports, lifecycle CLI, external-authority-v2
  execution, operator disposition, retry/post-fan-in readers, API lifecycle
  consumer, and packaged schema resources.
- **Authority / failure:** produces read-only lifecycle classification; malformed
  or contradictory provider/authority evidence fails closed and never grants
  execution from status alone.
- **Tests / posture:** lifecycle, pending-lifecycle, external-authority,
  temporal, retry, and operator-disposition qualifications. **Durable supported
  migration/reader; not removable with API Sprint 37 alone.**

### SBE-03 — retained initial-wave next-action fence

- **Source / provenance:** `initial_wave.py`, `initial_wave_contract.py`, and
  closure/external-authority launch validation; Sprint 33 companion.
- **Accepted evidence:** exact released wave authorization and next-action
  binding bundles; no named historical run or pre-v1 workspace predicate.
- **Reachability:** ordinary current closure and external-authority execution,
  public resources/contracts, and API orchestration.
- **Authority / failure:** refuses duplicate or incompatible initial-wave work
  before provider creation; it does not recover a retained run.
- **Tests / posture:** initial-wave contract fixtures and current orchestration
  coverage. **Durable preventative capability.**

### SBE-04 — external-authority execution and reconciliation readers

- **Source / provenance:** `external_authority_v2.py`,
  `external_authority_v2_execution.py`, `reconciliation.py`, and public CLI;
  Sprint 35 companion and later execution-bridge work.
- **Accepted evidence:** released external-authority request/grant/command
  contracts and lifecycle inspection evidence. Legacy or masked custody is
  refused rather than converted into a fresh provider create.
- **Reachability:** ordinary current API worker subprocess routes and public
  CLI/package schemas; not operator-only.
- **Authority / failure:** API supplies authority; SBE validates/uses exact
  input and preserves provider-custody ambiguity. Invalid joins fail closed.
- **Tests / posture:** external-authority and reconciliation qualifications,
  including installed-wheel API gates. **Durable capability.**

### SBE-05 — legacy provider-pending and temporal evidence support

- **Source / provenance:** shared SBE-02 reader/projection family plus
  `20260824-legacy-provider-pending-bridge-compatibility-sprint1` fixtures and
  `legacy_local_work_upgrade_qa.py` resources.
- **Accepted evidence:** pre-v1/v0.5 provider-pending/lifecycle shapes only
  where the released reader can validate exact custody and action inventory.
  The named legacy-upgrade bundle/fixture is qualification evidence; it is not
  an operator runtime command.
- **Reachability:** current API historical bridge commands may invoke the
  shared reader; public Python exports and package schemas are also reachable
  by current lifecycle/assessment paths.
- **Authority / failure:** no generic historical continuation is created.
  Unsupported/malformed evidence yields a typed refusal/unsupported result;
  no provider work is synthesized.
- **Tests / posture:** legacy-local-work qualification, lifecycle fixtures, and
  API release-pair tests. **Needs joint version-support decision.** The API
  bridge command may be removable while this native reader remains supported.

### SBE-06 — operator retirement

- **Source / provenance:** `operator_retirement.py`,
  `cli/operator_retirement.py`, operator-retirement contracts/fixtures; Sprint
  38 companion; commit `3151c4fc`.
- **Accepted evidence:** exact quiescent, provider-free native state and
  immutable retirement request/assessment contracts v1.
- **Reachability:** public CLI/Python surface, installed qualification, and
  current API operator-runner integration; not fixture-only.
- **Authority / failure:** SBE proves only native retirement eligibility;
  provider-pending, active, contradictory, or ambiguous cases refuse closed.
  API owns capacity release.
- **Tests / posture:** operator-retirement qualification and API operator-runner
  coverage. **Durable capability.**

## Slice 0 conclusion

The incident-era review found no current SBE production branch keyed to Aster,
Bramble, or a named historical run. The primary native dependency of API's
possible historical-only commands is the shared, released v0.5 lifecycle and
temporal reader family. Future removal work must therefore prove a narrower
version-support decision; it may not delete those readers merely because the
API bridge commands become unsupported history.
