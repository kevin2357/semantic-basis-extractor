# SBE 0.4.15 API Consumer Handoff

Use snapshot-validated lifecycle inspection v0.5 as the sole next-action authority
projection. Select external-authority work only when the exact closed predicates in
the sprint consumer handoff all validate.

- Require branch and capacity reason `spend_authorization_required`.
- Require 1–32 exact ordered action IDs joined to the embedded request.
- Require null branch/capacity timing fields and `local_work_ready_now=false`.
- Require outer run, observation, logical root, request, and ordered IDs to match.
- Treat `command=none` plus a closed refusal as retained native review, never create
  authority.
- Never reconstruct meaning from private `run.json`, logs, provider IDs, packets,
  or product job state.
- Continue using route-specific constrained execution and run-level reconciliation;
  SBE selects any bounded retrieval subset.

Installed provider-free qualification:

```text
astrowoof-external-authority-qa --output receipt.json --fixtures-dir fixtures
```

Require receipt contract `astrowoof.external_authority_qualification.v2`. The
receipt is qualification evidence only, not native authority, an API reservation,
or billing evidence.

Full predicate tables, retained-workspace handling, and compatibility explanation
are in the Sprint 1 `EXTERNAL AUTHORITY LIFECYCLE HARDENING CONSUMER HANDOFF.md`.
