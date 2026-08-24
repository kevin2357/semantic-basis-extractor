# Slice 2 — Replay, Refusal, and Temporal Bridge Matrix

Status: API approved; whole-cycle correction implemented in Slice 4

## Result

The immutable SBE 0.4.16 retrieval bridge is safe for the frozen, internally
consistent historical shape, but Slice 2 found one narrower validation gap that
prevents an unconditional `supported_now` decision.

The bridge correctly:

- limits a due cycle to the SBE-selected four actions;
- persists scripted completed-response evidence and changes the checkpoint basis;
- validates the resulting lifecycle v0.6 projection;
- turns provider-response identity conflict into native review without replacing
  the durable original provider identity;
- refuses an incomplete or changed snapshot before retrieval;
- excludes an action whose reconciliation timing or provider identity is absent;
- performs no create, POST, submit, retry, or authorization operation; and
- preserves the installed-wheel Slice 1 behavior: exact 4+2 GET selection followed
  by a byte-identical, zero-artifact `not_due` replay.

## Concrete 0.4.16 gap

If a historical ledger action's public authorization binding carries a `run_id`
that does not match the native run, 0.4.16 still admits that action to provider GET
reconciliation. The retrieved provider identity is durable and no create authority
is produced, but this contradicts the sprint's frozen requirement that binding
mismatch fail closed before retrieval.

This is not evidence that the retained Aster workspace has a bad binding. It is a
provider-free malformed-fixture result. Aster remains untouched, and its exact
restored bytes must be validated through the corrected public boundary before any
operator bridge is authorized.

## Recommended decision

Enter the conditional patch-design gate. The narrow candidate correction is to
validate every selected reconciliation action's complete binding join—including
native run identity—before issuing any GET. Independently valid actions may remain
eligible only if the public contract explicitly permits member-local exclusion;
the mismatched action itself must never be retrieved.

API selected whole-cycle refusal rather than member-local exclusion. Slice 4 records
and qualifies the resulting narrow runtime correction.

## Evidence

- Focused source qualification: 9 tests passed, 1 installed-wheel opt-in test
  skipped in the ordinary run.
- External OpenAI/network calls: 0.
- Local scripted retrievals: provider-free only.
- Provider create/POST/submit/retry: 0.
- Spend: USD 0.
- Retained QA workspace access: 0.
