# API review — Slices 0–2

## Decision

Approved.  The implementation is suitably bounded and preserves capture
semantics.  Proceed to Slice 3 installed-wheel/API-host coexistence
qualification; do not release, deploy, or launch a live witness yet.

## Review findings

- The public builder emits one started event, bounded architectural completion
  records, and one completed-or-failed terminal record.
- The two previously ambiguous escape classes are distinguishable: a collector
  fault retains `pre_assembly_evidence_collection`, while a fallback double
  fault retains `typed_status_construction`.
- The diagnostic wrapper preserves the original exception object and traceback
  with bare `raise`; it does not turn an escaping exception into a typed result
  or otherwise broaden the capture contract.
- Root identity is hashed at the public call boundary.  Failure projection
  excludes raw paths, error prose, workspace values, packets, prompts,
  responses, bindings, credentials, and exception objects.
- Frame selection is restricted to the approved capture modules and safe
  basename/function/positive-line projection.  The fingerprint is derived from
  those safe values plus closed phase/class.
- The new logging-sensitive tests cover pre-assembly escape, typed-status
  double-fault, typed unsupported return, and a failing logger handler.

## Slice 3 requirements

The installed-wheel/API-host qualification must demonstrate with `force=False`:

1. API's existing structured JSONL events remain valid and nonduplicated;
2. SBE capture diagnostics arrive through the same host formatter/catalog;
3. a simulated pre-assembly TypeError and typed-status double-fault retain
   distinct safe phase/frame outputs; and
4. ordinary packet and typed-unsupported behavior is unchanged.

No Better Stack request, provider action, R2 access, queue/workspace mutation,
release, deployment, or live-run action is authorized by this approval.
