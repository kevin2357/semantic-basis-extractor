# Slice 0 — frozen event and phase contract

## Decision

Gate A is approved by API. The diagnostic contract uses the existing SBE
application logger, formatter, event catalog, and host propagation path. It does
not introduce an execution-event authority or a new output transport.

## Event family

| Event | Cardinality | Purpose |
| --- | --- | --- |
| `editorial_runtime_capture_started` | exactly one | bind supplied result identity and root-string digest before native reading |
| `editorial_runtime_capture_phase_completed` | bounded architectural milestones | prove which boundary completed without per-member logging |
| `editorial_runtime_capture_completed` | exactly one on return | classify packet versus typed unsupported return |
| `editorial_runtime_capture_failed` | exactly one on escaping exception | retain safe phase, class, allowlisted frame, and fingerprint |

Exactly one completed or failed terminal event follows one started event. No
pass, artifact, deck member, finding, provider response, or binding produces an
event.

## Closed phases

- `root_normalization`
- `exact_result_reader`
- `eligibility_classification`
- `exact_source_proof`
- `pre_assembly_evidence_collection`
- `guarded_packet_assembly`
- `packet_validation`
- `typed_status_construction`
- `final_return`

The sequence, not merely the terminal phase, preserves the proven distinction:
a collector status-construction double-fault has no completed pre-assembly
milestone; an assembly-refusal double-fault does.

## Safe failure projection

Failure retains only module basename, function name, positive source line,
exception class, closed phase/branch, supplied public result ID, root-string
SHA-256, proven native/subject correlations when available, and a 16-character
fingerprint over module/function/line/class/phase. Frame selection is limited to
the approved SBE capture modules. Exception prose and arbitrary values are
never supplied to logging.

All diagnostic projection and logger calls are fail-silent. The public wrapper
uses bare `raise` after best-effort logging, preserving the original exception
object and active traceback.
