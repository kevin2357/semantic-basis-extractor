# Slice 0 — Frozen Fixture and Command Contract

Status: candidate contract; API review required before Slice 1

## Historical shape represented

The sanitized fixture recipe represents one exact-Natal, interactive, six-pass
initial wave created under the lifecycle-v0.5 provider-pending boundary:

- native status `WAITING_FOR_RESPONSE`;
- run contract `astrowoof.semantic_closure_run.v0.9`;
- six canonical paid action IDs and six distinct provider Response IDs;
- complete public spend bindings, authorizations, and consumption evidence;
- reconciliation policy v0.2 timing with no prior retrieval attempt;
- stored initial-wave state `DETACHED` so the lineage is not orphaned;
- no reported cost, provider response body, completed evidence, external-authority
  request/grant, protected subject data, or create-capable payload.

The recipe deliberately excludes `workspace_contract.logical_root` and snapshot
bytes. The qualification materializer binds each disposable workspace to its own
stable logical absolute path and then creates the complete snapshot through SBE's
supported snapshot writer. This avoids pretending a snapshot is safely relocatable.

## Supported command under qualification

The compatibility operation belongs to the semantic-closure command:

```text
astrowoof-semantic-closure --run-dir RUN \
  --resume --provider openai \
  --provider-reconciliation-cycle \
  --observed-at <canonical UTC instant>
```

`astrowoof-authoring-lifecycle` does not own provider reconciliation. The current
CLI also defaults to `provider=fake`, so `--provider openai` is an explicit part of
the qualified invocation.

No `--spend-authorization`, `--spend-reconciliation`,
`--initial-wave-authorization`, `--external-authority-request`, or
`--external-authority-grant` argument is compatible with this command.

## Expected outcomes

### Not due

Before `resume_not_before`, SBE returns `not_due`, performs no provider retrieval,
and leaves every authoritative workspace byte unchanged. It does not publish a new
native result because there is no new checkpoint to attest.

### Due and still pending

At or after `resume_not_before`, SBE chooses at most four actions, performs GET-only
retrieval, records each attempt and new backoff, writes one strict reconciliation
cycle artifact, updates the complete snapshot, and publishes a sealed native
provider-reconciliation result. No create method is available to the cycle.

### Completed

A completed scripted response is first persisted under its exact native action and
provider identity. Route-local deterministic fan-in may then run under a
reconciliation-only spend controller. Any later paid continuation must stop at its
ordinary authority boundary; reconciliation does not grant it.

### Refusal/review

Incomplete snapshot, missing timing, missing or conflicting provider identity,
binding inconsistency, unsupported route/mechanism, or provider identity mismatch
must fail closed or retain for review. Historical ambiguity is not recovery
authority.

## API bridge rule

The API may grant one audited worker claim for the run-level command only. It must
not select action IDs, infer v0.6 from the old checkpoint, or release provider/spend
authority from a `not_due` result. A v0.6 temporal observation is admitted only
after validating the supported command's resulting checkpoint.

