# Slice 0 — Contract, Lineage, and Applicability Audit

Date: 2026-08-24
Status: implementation evidence complete; API review requested before Slice 1

## Confirmed gap

The supported v0.6 lifecycle reader can produce a strict, stable
`astrowoof.external_authority_request.v2` for a real snapshot-valid workspace with
ordinary `PREPARED` actions. The observed request is:

- `request_kind: ordinary_action_set`;
- lexical `action_id` order;
- reference-only identity bound to the checkpoint-basis digest; and
- joined to complete public bindings in the v0.6 inspection inventory.

The current provider-capable external-authority CLI is not its executor. It accepts
the v1 request/grant model, requires exactly six authorization documents, requires
exact interactive OpenAI resume, and dispatches only the stored initial wave. A
two-member v2 ordinary request is refused by argument validation before state
mutation or provider construction. Therefore the API cannot safely invoke the
released command, synthesize v1 material, or use generic resume.

## Existing authority surfaces

| Surface | Request | Authority | Native execution | Status |
|---|---|---|---|---|
| Exact interactive initial wave | v1 `initial_wave_admission` with six complete bindings | v1 aggregate grant + six ordinary documents | `execute_exact_initial_wave_with_external_authority` | Supported; preserve |
| Bounded interactive initial wave | v1 `initial_wave_admission` with six complete bindings | v1 aggregate grant + six ordinary documents | bounded constrained initial-wave path | Supported; preserve |
| Temporal lifecycle inspection | v2 reference bound to checkpoint basis and ordered IDs | none | none | Supported read-only half |
| Ordinary prepared actions | v2 `ordinary_action_set`; complete bindings live in strict inspection | missing v2 grant | missing | This sprint |
| Provider-bound actions | no create authority | existing provider identity | reconciliation only | Supported; preserve |

## Route/stage applicability matrix

The matrix distinguishes semantic stage from provider transport. Slice 1 must not
promise support by inference; Slice 4 must prove each supported cell through its
real adapter.

| Native route/stage | Response | Batch | v2 disposition |
|---|---|---|---|
| Exact initial six-pass wave | Existing v1 wave command | One ordinary Batch-round action | Response not applicable to v2; Batch parity candidate |
| Bounded initial six-pass wave | Existing v1 wave command | One ordinary Batch-round action | Response not applicable to v2; Batch parity candidate |
| Exact pass-local creative retry | Ordinary action | Ordinary Batch-round action | Parity candidate where native adapter prepares it |
| Bounded pass-local creative retry | Ordinary action | Ordinary Batch-round action | Parity candidate where native adapter prepares it |
| Exact polish | Ordinary Response action | No independent Batch adapter identified | Response parity candidate; Batch fail closed/deferred |
| Bounded polish | Ordinary Response action | Bounded optional Batch remains unsupported | Response parity candidate; Batch fail closed/deferred |
| Exact qualitative critic | Ordinary Response action | No independent Batch adapter identified | Response parity candidate; Batch fail closed/deferred |
| Bounded qualitative critic | Ordinary Response action | Bounded optional Batch remains unsupported | Response parity candidate; Batch fail closed/deferred |
| Exact qualitative candidate | Ordinary Response action | No independent Batch adapter identified | Response parity candidate; Batch fail closed/deferred |
| Bounded qualitative candidate | Ordinary Response action | Bounded optional Batch remains unsupported | Response parity candidate; Batch fail closed/deferred |
| Any action with durable provider ID | Existing mechanism | Existing mechanism | Reconciliation-only; v2 create must refuse |
| `SUBMITTING` without durable ID / ambiguous action | Any | Any | Review/ambiguity refusal; no I/O |

Slice 1 should freeze one route-neutral v2 grant and executor contract with
route-specific dispatch adapters. Slice 2/3 should initially implement only cells
for which the current native route can prove a prepared, providerless, unconsumed
action and can checkpoint intent before entering its established provider adapter.
Every other cell remains typed fail-closed.

## Complete binding source

The v2 request remains compact. Its current inspection contains each selected
action's complete public binding. The normative authorization documents also carry
that complete binding. The v2 grant will contain ordered document references and
digests, not another binding copy. SBE must:

1. validate the request against a fresh strict inspection;
2. resolve each ordered inspection action;
3. validate each complete authorization document;
4. rederive each binding digest; and
5. require request order, inspection order, grant member order, document action,
   complete binding, digest, and reference to agree exactly.

## Writer and publication unit

The durable atomic publication unit is one complete native checkpoint containing:

- the exact v2 grant identity/digest;
- exact selected ordered inventory;
- all authorization applications/consumption evidence; and
- submission intent for every selected member.

A valid checkpoint represents either none of that unit or all of it. Provider I/O
begins only after the complete snapshot is published and the writer is released.

## Waiting semantics

Current v0.6 projection already establishes the necessary native/local facts for
the reproduced ordinary request:

- `selected_command = await_external_authority`;
- `reason_code = spend_authorization_required`;
- `eligible_now = false`;
- `local_work_ready_now = false`;
- `due_action_ids = []`; and
- `not_before = null`.

Repeated inspection is byte/read-only with respect to the workspace. The new
command's no-grant result must use only these native/local facts and must not claim
API consumer authority, reservations, capacity, leases, or admission state. API
maps the decision to blocked/non-retryable behavior.

## Refusal precedence

Slice 1 should preserve this ordering:

1. provider identity/evidence, consumption, or ambiguity appeared;
2. incomplete/invalid snapshot or writer ownership;
3. stale basis/run/root/route/mechanism/inventory/binding;
4. partial/invalid/mismatched grant or documents;
5. unsupported/deferred adapter; and
6. generic resume / compatible v2 grant required.

This ensures an operationally meaningful provider-safety contradiction is not
flattened into generic staleness.

## Slice 0 executable evidence

`test_external_authority_v2_execution_gap.py` proves through public readers that:

- a snapshot-valid ordinary workspace projects the expected quiescent v0.6 branch;
- the v2 request joins its strict inspection and is lexically ordered;
- inspection and request construction do not mutate the workspace; and
- the released generic/external-authority resume parser has no ordinary v2
  execution boundary, refuses before provider work, and leaves workspace bytes
  unchanged.

No provider credentials, network, retained workspace, submission, retrieval, or
spend are used.

## Slice 1 API decisions requested

1. Approve `ordinary_action_set` as the first executable v2 request kind; keep
   `initial_wave_admission` on its existing v1 constrained command.
2. Approve authorization documents as the only complete-binding carrier and grant
   members as ordered document digest/reference records.
3. Approve the route/stage matrix, especially optional Batch deferral.
4. Approve the complete grant+inventory+authorization+intent checkpoint unit.
5. Approve the refusal precedence and native-only quiescence vocabulary.
