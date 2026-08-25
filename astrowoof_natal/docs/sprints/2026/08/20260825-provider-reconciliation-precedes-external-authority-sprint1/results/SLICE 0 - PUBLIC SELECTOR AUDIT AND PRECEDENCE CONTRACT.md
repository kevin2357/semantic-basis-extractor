# Slice 0 — Public Selector Audit and Precedence Contract

Date: 2026-08-25  
Status: complete; awaiting API review before runtime changes

## Reproduction

The provider-free reproducer constructs complete snapshot-valid exact- and
bounded-Natal workspaces with six retained provider Response identities and one
later ordinary `PREPARED` action. It invokes the public lifecycle v0.5 and temporal
v0.6 readers at canonical times and hashes every authoritative workspace file
before and after inspection.

No retained QA workspace, provider transport, authorization consumption, or
provider create/retrieve operation is used.

## Exact defect

`_capacity_and_custody()` currently evaluates these predicates in this order:

1. invalid/ambiguous/integrity/unsupported;
2. due provider retrieval;
3. **any `PREPARED` action**;
4. completed provider evidence;
5. scheduled/not-due provider custody; and
6. other local continuation.

Consequently, a later prepared action masks both future-scheduled retained custody
and completed provider evidence requiring deterministic fan-in. The public result
becomes `await_external_authority`, even though existing provider custody must be
settled first. Due retrieval happens to be correct because its predicate appears
before `PREPARED`.

The defect also leaks into temporal v0.6 basis identity. At the not-due observation,
the basis contains an external-authority request inventory; at the due observation,
the basis contains no authority request because reconciliation wins. The immutable
workspace is byte-identical, but the projected checkpoint-basis digest changes due
to this incorrect branch-dependent authority projection.

## Frozen precedence table

| Native facts | Current v0.4.21 selection | Required selection |
|---|---|---|
| Snapshot/binding/inventory contradiction + prepared | review/refusal | review/refusal |
| Ambiguous provider submission + prepared | review/refusal | review/refusal |
| Unsupported retained provider timing/mechanism + prepared | unsupported/review | unsupported/review |
| Due retained provider custody + prepared | reconciliation, up to four | unchanged |
| Completed provider evidence requiring fan-in + prepared | **authority (defect)** | ordinary local fan-in |
| Retained provider custody not due + prepared | **authority (defect)** | reconciliation command, ineligible until native `not_before` |
| Causal local work that determines the next paid inventory + prepared | authority can mask local work | ordinary local continuation |
| Prepared only | external authority | unchanged |
| Provider custody not due only | release until due | unchanged |
| Completed provider evidence only | local continuation | unchanged |
| Terminal/no work | terminal/none | unchanged |

“Causal local work” is deliberately narrow: it is local work whose result can
determine, alter, or refuse the exact next paid-action inventory. Unrelated optional
work does not receive a general starvation priority.

## Contract impact

No new public command or lifecycle state is needed. Existing v0.5 fields can express
the corrected branches, and v0.6 can project them without reinterpretation:

- due custody: `provider_reconciliation_cycle`, `eligible_now=true`, native subset;
- not-due custody: `provider_reconciliation_cycle`, `eligible_now=false`, native
  `not_before`;
- completed evidence: `ordinary_resume`, `eligible_now=true`; and
- authority: only after higher-priority custody/fan-in facts are exhausted.

Slice 1 should tighten the semantic validators in place. Under one unchanged basis,
trusted time may alter only reconciliation eligibility/due subset. The authority
inventory/digest must remain stable until provider retrieval/fan-in records a new
checkpoint basis.

## Test evidence

`test_provider_reconciliation_precedes_authority_slice0.py` proves:

- exact and bounded due custody already selects four-action reconciliation;
- exact and bounded not-due custody is currently masked by prepared authority;
- completed provider evidence is currently masked by prepared authority;
- the public readers are nonmutating; and
- current time-only inspection changes the authority-bearing basis, freezing the
  second observable symptom for the patch regression.

