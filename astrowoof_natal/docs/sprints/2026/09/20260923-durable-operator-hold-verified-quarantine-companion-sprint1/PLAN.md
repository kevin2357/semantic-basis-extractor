# Plan — durable operator hold and verified quarantine companion

## Status

**Closed — SBE discovery complete.** No new SBE command, schema, reader, or
wheel is warranted for the manual operator-hold workflow. The final working
route is API/worker/platform owned:

```text
API durable hold
  -> final API-parent held-run refusal before child launch
  -> operator-authorized worker redeploy to contain pre-existing work
  -> new boot/readiness + child-ledger + API admission + platform retirement proof
  -> API operator_quarantined finalization and capacity release
```

The SBE wheel remains eligible to emit cooperative same-invocation evidence,
but cannot certify worker-wide child absence or old-container retirement.

## Completed discovery

- Confirmed the SBE wheel does not own a worker-wide process inventory, API
  queue/admission state, or Render service lifecycle.
- Confirmed a cold SBE command cannot prove that an earlier worker container
  has no live child; `not_found` in that context would be ambiguous, not a
  capacity-release proof.
- Identified the required API correction: enforce the durable hold in the
  mandatory parent child-admission seam immediately before `Popen`, including
  all launch kinds, and record a typed local refusal rather than starting a
  held target from pre-existing authority.
- Classified worker replacement, new-boot health, child-ledger emptiness,
  admission/queue state, and old-boot no-overlap as API/worker/platform facts.

## Out of scope and handoff

No SBE source change is requested. The API sprint owns the final launch guard,
the operator break-glass/redeploy receipt, finalization, and live qualification.
Any future request for SBE service-wide process assertions requires a new
companion sprint and a concrete host-owned capability design.
