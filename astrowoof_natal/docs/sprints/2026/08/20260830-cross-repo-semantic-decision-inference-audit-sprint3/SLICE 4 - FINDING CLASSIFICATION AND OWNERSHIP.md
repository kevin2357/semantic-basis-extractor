# Slice 4 — finding classification and ownership

## Classification freeze

The joint audit found three production consumer defects. All three belong to
AstroWoof API. SBE `0.4.32` already publishes the exact facts and public readers
needed to correct them; no SBE schema or runtime release is justified.

The classification deliberately distinguishes a defect from an explicit API
product policy. API currently uses outer `failed` for review outcomes. That
policy may later be redesigned, but the audit found no basis to treat the policy
choice itself as an accidental inference so long as custody, settlement, and
delivery remain separately governed.

## Confirmed defects

| ID | Finding | Class | Priority | Potential impact | Why existing SBE evidence is sufficient | Correction owner |
|---|---|---|---|---|---|---|
| D-01 | Generic `read_latest_sealed` fallback in terminal ingress | API mapper defect + missing negative test | High | A live worker can substitute generic latest discovery for exact invocation/preflight identity, risking wrong-result adoption or premature outer terminalization | Availability v0.1 supplies an exact ID for named recovery; command envelopes supply exact invocation result IDs; `read_exact_sealed` validates the full join | API |
| D-02 | Absent explicit readiness becomes `local_continuation_required=True` | API mapper/interface defect | High | Retained slot/retry loop, starvation, or incorrect scheduling when evidence is absent | Current v0.5/v0.6/v0.7/v0.8 consumers expose explicit branch/readiness facts; absence can remain unknown/refused | API |
| D-03 | Bounded `retain_for_review` and `unsupported_retain_capacity` map to `TERMINAL_CLOSED` | API mapper defect | Highest of this set | Fabricated terminal-ingress attempt, generic latest-result selection, incorrect job/run/reading failure, and possible custody mishandling | Validated bounded result and embedded lifecycle inspection already distinguish terminal, review, and unsupported dispositions; real terminal ingress separately requires exact sealed terminal evidence | API |

### Severity rationale

D-03 is first because it composes the other dangerous behavior: a nonterminal or
unsupported scheduling conclusion becomes terminal processing, then the absence
of an exact terminal identity can activate D-01. D-01 follows because identity
substitution threatens authoritative result selection. D-02 is still high
because the project has repeatedly observed retry/slot churn from readiness
misclassification, but current production mappers usually populate the field,
making it less immediately reachable.

## Explicit API policy, not defect classification

| Decision | Classification | Required guardrail |
|---|---|---|
| Outer API job/run/reading becomes `failed` after exact v0.2 terminal editorial `review_required` | API product policy | Must follow exact terminal-result ingestion; must not release provider custody, reservations, unsettled billing, or publish delivery merely because outer state is failed |
| Outer API job/run/reading becomes `failed` for lifecycle `retain_for_review` with no runnable local action | API product policy | Must use the nonterminal review branch, retain the inspectable workspace/evidence, release only local capacity, and never fabricate native terminal evidence |

The two policies share an outer status but not native meaning. Operational and
diagnostic projections must retain that distinction through failure
classification, native receipt presence, custody facts, and reason code.

## Contract-backed decisions

The following Slice 3 families are classified as safe, contract-backed
consumption under the pinned SBE `0.4.32` contract:

1. sealed nonterminal result discrimination;
2. invocation-returned result precedence;
3. named availability preflight with exact read;
4. immutable predecessor/successor continuity;
5. v0.2 per-action custody joins;
6. legacy v0.5 completed-evidence upgrade to v0.7/v0.8;
7. provider-pending not-due/due temporal progression;
8. completed-provider-evidence fan-in precedence;
9. terminal/nonpublishable delivery separation;
10. missing usage remaining unsettled rather than zero;
11. exit-0 typed generic refusal;
12. exit-2 invocation-bound terminal review;
13. action inventory and local-operation inventory independence;
14. checkpoint-basis progress outranking status text; and
15. contradictory basis/status refusal.

The due/not-due runtime-spy cell remains useful missing coverage, but it tests an
already supported decision rather than filling an SBE contract gap.

## Non-findings and limitations

| Item | Classification | Disposition |
|---|---|---|
| SBE needs a universal API disposition field | Rejected design direction | Orthogonal SBE facts already support the decisions; keep API policy in API |
| SBE `review_required` string is inherently terminal/nonterminal | Naming ambiguity only | Require exact schema, fields, custody finality, and result identity |
| Stale SBE package in local API `.venv` | Environment/diagnostic mismatch | Do not treat its collection errors as product behavior; release-pair tooling remains the deployment authority |
| Historical version reinterpretation | Historical compatibility limitation | Continue using named, closed operator recovery services; unknown versions fail closed |

## Correction ordering

One API implementation sprint should correct these together because D-03 can
currently fall into D-01:

1. require exact result identity at normal terminal ingress;
2. route bounded terminal, review, and unsupported outcomes through three
   distinct worker dispositions;
3. require explicit readiness before workspace mutation;
4. add due/not-due runtime-spy coverage;
5. add exact review/custody assertions showing outer failed status does not
   erase action-level authority; and
6. run the existing adversarial and installed SBE `0.4.32` consumer matrix.

No SBE implementation sprint or SBE release is recommended from the current
evidence.

## Slice 4 gate decision

Classification and ownership are frozen subject to API/owner review:

- API mapper defects: 3;
- SBE public-contract gaps: 0;
- cross-artifact gaps requiring SBE work: 0;
- explicit API policy decisions preserved: 2;
- contract-backed mutation families: 15;
- historical/environment limitations: 2.

Slice 5 should turn this classification into bounded API implementation and
joint qualification handoffs, plus process-document updates. It should not
change production source in either repository.
