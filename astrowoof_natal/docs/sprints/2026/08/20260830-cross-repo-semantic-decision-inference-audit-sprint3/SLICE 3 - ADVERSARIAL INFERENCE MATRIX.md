# Slice 3 — adversarial inference matrix

## Method

Each row holds a tempting proxy constant while changing one independent fact.
Evidence comes from source inspection and provider-free API tests against the
SBE `0.4.32` source surface. This slice identifies observable decisions and
test gaps; final ownership/severity classification remains Slice 4 work.

The API review correction is incorporated: normal result-availability absence
continues the **ordinary selector**, which may choose initial-wave admission,
legacy recovery, or lifecycle inspection. It does not universally imply one
inspection operation.

## Required mutation matrix

| Case | Proxy held constant | Independent mutation | Expected contract decision | Observed evidence | Slice 3 result |
|---|---|---|---|---|---|
| M-01 sealed + nonterminal | Result is sealed and available | Outcome is `awaiting_external_authority`, provider pending, local work, or refusal rather than terminal | Read exact result, then continue ordinary selector/typed nonterminal ingress | Sprint 60 tests and `test_sealed_nonterminal_result_does_not_preempt_initial_wave` | Contract-backed after Sprint 60 |
| M-02 invocation result vs discovery | Both exact invocation result and another latest/available result exist | IDs conflict | Invocation-returned ID wins; discovery cannot substitute | `test_terminal_review_ingress_uses_invocation_result_not_latest_discovery` | Contract-backed for terminal-review envelope |
| M-03 recovery discovery | No invocation-returned ID | Valid availability names one exact result | Read/validate only that ID, then classify it | `test_sealed_terminal_preflight_outranks_bridge_and_lifecycle_selection` and nonterminal variants | Contract-backed named preflight |
| M-04 sealed predecessor/successor | Both publications are immutable | Later custody-only successor exists | Preserve predecessor; consume successor only through explicit continuity | SBE terminal-review qualification and API native-transition replay/continuity tests | Contract-backed; no recency authority |
| M-05 review + retained custody | Outcome spelling remains `review_required` | Custody finality ranges from final to provider reconciliation/denial/mixed | Ingest exact v0.2 editorial result; handle every action by its custody disposition; never infer release/publication | v0.2 validator/action joins; `completed_without_usage` remains provider-created | Native ingress is strict; outer API close remains a policy question |
| M-06 no local dependencies + fan-in | `local_dependencies=[]` | Completed provider evidence makes deterministic fan-in ready | Upgrade to v0.7/v0.8 and consume local operation, not “no work” | Legacy v0.5 upgrade qualification and local-work tests | Contract-backed narrow upgrade |
| M-07 provider ID + not due | Provider custody and snapshot remain identical | Observation time moves from before to at due time | Not-due releases until SBE time; due invokes only SBE-selected subset | `test_v06_temporal_persistence_accepts_same_basis_later_due_observation` | Contract-backed |
| M-08 provider complete + local ready | Provider identity remains | Observation changes pending to completed evidence | Execute deterministic fan-in before new authority | post-fan-in v0.7/v0.8 qualifications | Contract-backed |
| M-09 terminal + nonpublishable | Native terminal result remains valid | Delivery/publication flags are false | Terminal non-delivery; never publish | terminal-review and denial fixtures; publication is a separate branch | Contract-backed separation |
| M-10 provider terminal + usage unavailable | Provider operation is terminal | Usage is null instead of reported zero | Retain financial authority/unsettled state; do not invent `$0` | `_validate_terminal_review_api_action_joins` and accounting contract | Contract-backed conservative settlement |
| M-11 exit 0 + refusal | Process exit is success | Typed generic provider-dispatch refusal is emitted | Consume refusal and route to fresh selector/authority; never treat as provider success | `_StdoutJsonlCapture` conflict checks and duplicate-submission fence tests | Contract-backed typed refusal |
| M-12 exit 2 + result | Process exit is nonzero | Valid terminal-review command envelope is emitted | Exact envelope/result wins over exit diagnostic | terminal-review ingress tests | Contract-backed |
| M-13 empty action inventory + local operation | Paid-action inventory empty | v0.7 local operation inventory is nonempty | Local operation can be eligible; emptiness is not no-work proof | v0.7 local-work validator/qualification | Contract-backed orthogonal inventories |
| M-14 unchanged status + advanced basis | Human-readable status unchanged | Durable checkpoint/native facts advance | New basis is new authority/evidence; do not compare status strings | temporal/local-work persistence tests | Contract-backed digest authority |
| M-15 changed status + unchanged/contradictory basis | Status text changes | Basis/joins do not advance or contradict | Refuse; status cannot manufacture progress | temporal regression and local-operation consumption validators | Contract-backed refusal |

## Requested focused mutations

### F-01 — generic `read_latest_sealed` fallback

The named availability preflight is now safe, but
`SbeNativeTerminalIngressService.ingest()` retains a separate branch:

```text
no terminal_review_command_result
+ no sealed_terminal_result_id
→ read_latest_sealed(...)
```

`test_reader_discovers_only_to_read_an_explicit_sealed_result` proves what that
reader does, not that the caller had permission to select the latest result.
The fallback can therefore choose a result without invocation identity. Current
ordinary terminal-review and Sprint 60 preflight callers supply exact identity,
but the public ingress method still permits the broader call.

Result: **confirmed cross-artifact join gap / missing negative test**. A
minimized regression should call terminal ingress without either exact identity
and expect a typed `exact_result_identity_required` refusal. Historical recovery
that genuinely needs discovery should resolve availability first and pass the
result ID explicitly.

### F-02 — absent readiness value

`SbeReadingWorker._run_claim()` persists:

```python
result.local_continuation_required
if result.local_continuation_required is not None
else result.disposition != DELIVERY_ACCEPTED
```

Holding a tempting non-delivery disposition constant while removing the
explicit readiness fact therefore writes `local_continuation_required=True`.
Current production lifecycle mappers normally populate the field, so the risk
is latent rather than evidence of a current route failure. The generic worker
contract nevertheless interprets absence as permission to retain local work.

Result: **confirmed absent-evidence fallback / missing negative test**. A
minimized fixture is an otherwise valid `QUIESCENT` result with
`local_continuation_required=None`; expected behavior is typed refusal before
workspace readiness mutation.

### F-03 — due/not-due subset ownership

The v0.6 persistence test holds the checkpoint basis and provider custody
constant while advancing trusted observation time. The first decision is
not-due; the second selects `provider_reconciliation_cycle` with exactly
`provider_custody.next_due_action_ids`. API persists both decisions against one
basis and exact replay at the same time is idempotent.

No API code computes provider age, expands the subset, or selects response IDs.
The runtime invokes the run-level reconciliation command.

Result: **contract-backed SBE subset ownership**. Add a direct runtime-spy test
in a correction sprint only if API wants this invariant tested independently of
the persistence and installed 4+2 qualification layers.

## Six Slice 2 tensions resolved or narrowed

| Tension | Slice 3 determination |
|---|---|
| Three meanings of review | The spelling is not authoritative. Lifecycle review, v0.2 terminal editorial review, and bounded review must remain separate mapper inputs. |
| Both review branches fail API run/reading | Confirmed current API policy. It is not derived from SBE terminality in the lifecycle-review branch. Joint review must decide whether `failed` is the intended product review state, but the local capacity release itself is supported. |
| v0.2 terminal review retains custody | Supported only because action dispositions remain durable and separately joined. Outer API failure cannot be interpreted as reservation, provider-custody, settlement, or publication completion. |
| Latest sealed fallback | Confirmed join gap; exact identity should be mandatory at terminal ingress. |
| Bounded review/unsupported collapse | Confirmed mapper tension. `unsupported` supplies no native-terminal positive permission, and neither branch visibly carries an exact terminal result ID into `_bounded_cycle_result`. |
| Readiness fallback | Confirmed absent-evidence inference; current production mappers usually avoid it, but the worker interface permits it. |

## Additional confirmed mapper hazard

`_bounded_cycle_result()` maps both:

- `review_required` with `retain_for_review`; and
- `unsupported` with `unsupported_retain_capacity`

to `SbeCycleDisposition.TERMINAL_CLOSED`. The worker then invokes terminal
ingress. At this mapping site there is no invocation-bound v0.2 terminal result
ID or terminal-review envelope. Terminal ingress can consequently fall into its
generic latest-result reader.

This composes two independent gaps: a scheduling disposition is treated as
terminal-result permission, and the missing exact identity is replaced by
latest discovery. Existing parametrized tests explicitly expect the
`TERMINAL_CLOSED` mapping, so this is reachable tested behavior rather than a
dead branch.

## Missing-test inventory for follow-up implementation

1. Terminal ingress without either exact invocation result or explicit preflight
   result ID must refuse.
2. `QUIESCENT`/review/terminal cycle results with absent explicit readiness must
   refuse before workspace mutation.
3. Bounded `unsupported_retain_capacity` must never enter terminal ingress,
   fail the API run, or select a latest result.
4. Bounded `retain_for_review` must prove whether it carries a real terminal
   result or must use the nonterminal review path.
5. A v0.2 `review_required` fixture with provider-reconciliation custody must
   prove independently that outer API closure cannot release/erase action
   custody or financial authority.
6. A nonterminal lifecycle-review fixture must assert the intended API product
   status explicitly (`failed`, separate review state, or other closed policy),
   rather than only asserting slot release.
7. A direct runtime spy should prove due reconciliation invokes the run-level
   command without API-selected member IDs, complementing existing v0.6 and 4+2
   qualification evidence.

## Verification

- Focused ingress/preflight set from Slice 2: 10 passed.
- Broader provider-free API lifecycle/worker/ingress/adversarial set: 122 tests
  completed successfully against the SBE `0.4.32` source surface.
- The first broad attempt against API's existing `.venv` failed collection
  because that environment contains a stale pre-0.4.32 SBE installation. No
  test assertion failed; the successful rerun explicitly placed the released
  0.4.32 source surface first on `PYTHONPATH`.
- Provider calls, retained-QA access, deployment, configuration mutation, and
  spend: zero.

## Slice 3 conclusion

Most of the required mutations are already contract-backed. Three concrete API
consumer seams remain for Slice 4 classification:

1. generic latest-result terminal ingress;
2. absent-readiness inference; and
3. bounded review/unsupported terminal collapse.

The review/product-status question is narrower: exact v0.2 terminal editorial
review is valid native evidence, but API outer terminalization, provider custody,
settlement, and delivery remain separate decisions. The joint gate should freeze
the intended API review state before implementation ownership is assigned.
