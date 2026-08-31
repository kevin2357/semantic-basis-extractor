# API review — Slice 0 classification freeze

## Decision

Approved in substance. Slice 0 has the right conservative shape and identifies
the important omitted case: concrete executable local work must be represented
as `native_local_work_ready`, not mislabeled quiescent or inconsistent.

The precedence table, opaque logical-root identifier, explicit empty-list
no-action rule, reader-bound terminal rule, and native-only posture wording all
align with API Sprint 66.

## Correct before Slice 1 schema freeze

1. **Make Background.md match the frozen eight-class vocabulary.** It still
   lists the former seven classes and omits `native_local_work_ready`. The plan
   and Slice 0 table are now the intended vocabulary, so Background should be
   amended to avoid a future consumer/reviewer treating the older list as
   authoritative.

2. **Resolve the unknown/inconsistent wording.** Background currently says
   unknown/inconsistent evidence “may justify local quarantine,” while the
   frozen table correctly assigns `unsupported_or_inconsistent` posture
   `prohibited`. Those can coexist only if “local quarantine” in the background
   means an API-visible request/refusal/audit with **no** SBE assessment-based
   local capacity release. If the intended meaning is that the assessment
   authorizes the real `quarantine_run` operation, then `prohibited` must win:
   API cannot release a slot or fence into the completed quarantine state from
   evidence SBE cannot safely classify. Please state that distinction directly.

No other changes are needed before Slice 1.

## API mapping note

`submission_ambiguous`/`provider_pending_known_identity` may be
`permitted` because their native posture says no ordinary local authoring worker
needs to remain scheduled; API still separately refuses to revoke a live job
lease and releases only exact target-owned local resources under its writer
lock. The assessment does not make that API proof redundant.

After the two documentation corrections, SBE is approved to begin Slice 1.

No provider activity, retained-workspace access, mutation, deployment, tag, or
release is authorized by this review.
