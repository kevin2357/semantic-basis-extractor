# Slice 1 — v1 schema and semantic contract freeze

## Status

Complete; paused at Voof-paws 2 before the workspace reader/projection.

## Public contract

`astrowoof.operator_disposition_assessment.v1`

Implemented structural schema:

`resources/contracts/operator-disposition-assessment.v1.schema.json`

Implemented strict Python contract module:

`operator_disposition.py`

The Python validator enforces the same primitive safety constraints without the
optional `jsonschema` dependency and additionally enforces semantic joins that
JSON Schema alone cannot express.

## Frozen identity

The assessment digest canonically binds:

- native run ID;
- route family and route contract;
- SBE release and compatibility identity digest;
- state revision, snapshot digest, checkpoint-basis digest, and opaque logical
  workspace root ID;
- lifecycle schema and complete lifecycle-document digest;
- exact terminal result/receipt/discovery identities when present;
- complete custody summary, dominant class, posture, supported actions, reason,
  and evidence categories; and
- explicit diagnostic-only / zero-provider-I/O / zero-mutation assertions.

`logical_workspace_root_id` has the closed `lroot_<24 lowercase hex>` shape.
The public assessment never carries an absolute filesystem path, R2 object key,
URI, or restored-host path.

## Frozen semantic table

| Class | Posture | Actions |
|---|---|---|
| `provider_free_quiescent` | `permitted` | `[]` |
| `provider_pending_known_identity` | `permitted` | `provider_reconciliation_cycle` |
| `completed_unadopted` | `native_prior_action_required` | `ordinary_resume` |
| `native_local_work_ready` | `native_prior_action_required` | `ordinary_resume` |
| `providerless_authority` | `permitted` | exactly one applicable v1/v2 authority, providerless denial, or operator-review operation |
| `submission_ambiguous` | `permitted` | `operator_review`, then `fresh_disposition_assessment` |
| `sealed_terminal` | `permitted` | `terminal_result_ingress` |
| `unsupported_or_inconsistent` | `prohibited` | `[]` |

The ordering in multi-action lists is normative. No-action is only `[]`; no
`none` token exists.

## Precedence enforcement

The Python validator mechanically recomputes dominant evidence precedence:

1. ambiguity;
2. completed but unadopted provider evidence;
3. known provider identity/custody;
4. lineage conflict without higher provider custody;
5. concrete local work;
6. providerless authority;
7. exact terminal evidence; and
8. provider-free quiescence.

An explicitly unsupported/inconsistent assessment must carry at least one
closed evidence category and always has posture `prohibited`.

## Terminal evidence boundary

The self-contained validator proves exact field shape, identity syntax,
assessment binding, discovery-mode consistency, and terminal-summary joins.
It does not pretend that a supplied digest proves bytes it has not read. Slice 2
must construct this block only from `read_native_transition_result`, optionally
preceded by the bounded availability reader in an explicit recovery/preflight
mode. The generic contract builder is not transition authority.

## Fixture and mutation coverage

The focused test module provides one deterministic positive fixture for every
custody class and covers:

- strict closed shape and primitive types without `jsonschema`;
- assessment digest binding;
- unknown/inconsistent posture prohibition;
- canonical empty-list no-action semantics;
- mixed-custody precedence;
- terminal discovery/result/receipt shape and summary joins;
- path-private logical-root rejection;
- sorted/bounded provider-reference semantics;
- zero-I/O/zero-mutation assertions; and
- optional Draft 2020-12 schema validation when `jsonschema` is installed.

## Safety

This slice adds a contract module, schema, and focused tests only. It does not
read a workspace, alter lifecycle selection, perform provider I/O, mutate native
state, or assert any API-owned resource fact.
