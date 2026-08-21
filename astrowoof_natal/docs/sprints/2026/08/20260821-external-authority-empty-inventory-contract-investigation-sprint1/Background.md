# External-Authority Empty-Inventory Contract Investigation

## Purpose

Record the narrow QA finding from recovery of the retained AstroWoof API run
`720f8b3c-aab8-4cbd-a51d-bcc2621305e6` before any implementation is proposed.
This is an SBE lifecycle-contract issue, not an authorization, provider-cost, or
Render configuration decision.

## Context

The retained run had already completed its original six-member initial
interactive authoring wave. The API later resumed it through the normal
provider-pending/reconciliation path. A prior API validation inversion was
fixed, an operator-controlled replay was authorized, and the worker was
redeployed with an exact temporary recovery target.

The replay did not make provider I/O. Its SBE cycle failed when the API tried to
validate SBE's lifecycle inspection with:

```text
SbeProviderContractError: SBE external authority branch evidence is incomplete
```

The API check is deliberately strict. For an
`execution_branch.command == "await_external_authority"`, it requires all of:

- `eligible_now == false`;
- branch reason `spend_authorization_required`;
- capacity disposition `await_external_authority`;
- a nonempty ordered `action_ids` inventory; and
- no `not_before` timestamp.

The observed failure means at least one of those requirements was not true.
The immediate hypothesis was that the QA worker had an older SBE wheel or was
running a different executable from the declared deployment.

## Direct QA Image Evidence

Render reported the QA SBE worker as pinned to:

```text
ghcr.io/kevin2357/astrowoof-sbe-worker@
sha256:318b5fba21d233fd12311027dd868739f24b105162e1e5cdb57a4a821f4af1d8
```

Because Render CLI SSH is interactive-only in the Codex environment, the exact
digest was pulled locally and inspected without changing the service or
workspace. The image contains:

```text
astrowoof-natal-authoring = 0.4.14
astrowoof-api             = 0.1.0
python                     = /usr/local/bin/python
lifecycle module           =
/usr/local/lib/python3.11/site-packages/astrowoof_natal_authoring/lifecycle.py
```

The installed `0.4.14` lifecycle source includes the intended post-build join:

```python
elif execution_branch["command"] == "await_external_authority":
    raw_request = read_external_authority_request(run_dir)
    external_authority_request = build_external_authority_request(
        run_id=str(state.get("run_id") or ""),
        observation=observation,
        actions=raw_request["ordered_actions"],
        initial_wave=raw_request.get("initial_wave"),
    )
    execution_branch["action_ids"] = list(
        external_authority_request["ordered_action_ids"]
    )
```

Therefore this was not a stale-wheel, wrong-image, or missing-executable
deployment problem.

## Supporting Trace Evidence

The retained worker trace exported as `sbe.dog.log` documents the earlier
initial-wave portion of the same broad run lineage under `0.4.13`:

- all six initial creates began concurrently at `2026-08-20T02:32:44Z`;
- all six recorded distinct OpenAI Response IDs by `02:32:51Z`;
- SBE persisted each provider identity;
- `initial_wave_complete` recorded six provider-bound members, zero ambiguity;
  and
- SBE checkpointed state revision 17 and published a
  `provider_pending` native result.

This trace proves that the original fanout and detached provider-pending
handoff were healthy. It is not the raw inspection document from the later
recovery cycle, so it cannot by itself identify which branch field the API saw
as inconsistent.

Render worker events further show that the later recovery acquired a lease and
entered the cycle, then failed during API validation before provider work. The
attempt released its lease as `terminal-failed`; it created no new provider
request and consumed no additional spending authority.

## Diagnosis

The failure is an API-to-SBE lifecycle contract seam:

1. SBE selected `await_external_authority`.
2. The API received a lifecycle inspection that did not meet that branch's
   exact evidence shape.
3. The API correctly failed closed rather than inventing or authorizing a
   next action.

The decisive concern is the action inventory. SBE's lifecycle logic begins the
branch with an empty `action_ids` list, then is expected to replace it with the
ordered identifiers from `external_authority_request`. The public v0.5
validator checks that the two inventories are equal, but equality of two empty
lists can still pass. The API correctly imposes the additional semantic rule:
an external-authority request is meaningless with no action to authorize.

Thus the likely defect is not the API's guard. It is that SBE can emit or expose
an `await_external_authority` inspection with an empty effective request/action
inventory, without converting it into a typed refusal or failing its own
closed-world validation. The exact causal source still needs inspection of the
run-specific lifecycle document or a targeted reproducer: for example, an empty
`ordered_actions` artifact, an incomplete request-building path, or a path that
leaves the preliminary branch shape visible.

## Narrow Remediation Target

Before emitting a lifecycle inspection with
`command == "await_external_authority"`, SBE should guarantee one of two
outcomes:

1. **Valid request:** nonempty ordered action IDs; exact equality between
   `execution_branch.action_ids` and
   `external_authority_request.ordered_action_ids`; and complete bindings for
   those actions.
2. **Typed refusal/review:** no external-authority command, a closed refusal or
   review disposition, and machine-readable evidence explaining why a valid
   ordered inventory could not be constructed.

The SBE-side lifecycle validator should enforce the nonempty-inventory rule,
not rely on the API as the first component able to detect it. Diagnostics for
this boundary should log safe, non-protected structural facts: command,
capacity disposition/reason, action count and identifiers, whether request
construction succeeded, and any typed refusal reason. It must not log prompts,
provider payloads, or protected subject content.

## Non-Goals

- Do not bypass the API check.
- Do not reconstruct an action inventory from logs or infer authority from a
  state name.
- Do not resubmit provider work or mutate the retained run while diagnosing.
- Do not treat the clean initial six-member fanout as evidence that this later
  authority request is valid.

## Coordination Implication

The API should retain its current fail-closed validation. Once SBE provides a
valid request or typed refusal for the retained run, the API can evaluate that
evidence through the ordinary authority path. No API policy relaxation is
justified by this finding.
