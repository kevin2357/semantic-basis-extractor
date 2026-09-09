# API review — Slice 3G pre-optional assembled-deck retention

## Decision

Approved:

1. preserve an immutable initial assembled-deck artifact and its canonical
   content digest before **any** optional whole-deck stage can run;
2. return typed `incomplete_native_evidence` with no packet for historical
   optional-stage workspaces that lack that retained evidence; and
3. keep deterministic historical reconstruction outside this contract unless a
   later, explicit contract models reconstruction provenance and verification.

The retained artifact should be named/documented as *initial assembled deck* or
*pre-optional assembled deck*, rather than `pre-polish`, because polish,
qualitative critic, and qualitative candidate are all optional whole-deck
stages. Its role is to prove the input to the first such stage, regardless of
which stage appears first.

## Required retention semantics

- Create the artifact immediately after successful assembly and before an
  optional-stage intent/candidate can be materialized.
- Persist an exact normalized relative path and canonical digest in the native
  subject/assembly relation. Recompute the digest from the retained artifact
  during read-only packet construction and fail closed on any mismatch,
  absence, non-file path, traversal, or duplicate/conflicting declaration.
- Treat the artifact as immutable: later candidate adoption may update the
  ordinary `subject.deck` pointer, but must never overwrite or retarget this
  assembly-input evidence.
- Keep it inside the workspace/checkpoint inventory so ordinary checkpoint,
  restore, and resume preserve it. Add a provider-free proof that the artifact
  and digest survive a checkpoint/restore boundary and that an adopted polish
  candidate cannot alter them.
- The packet uses the verified artifact for both `initial_assembly` output and
  the first optional-stage input. Later candidate/output transitions remain
  their existing exact attempt artifacts.

## API implications

No API lifecycle, provider, custody, spend, or delivery contract change is
needed if this remains native workspace evidence carried transparently by the
existing archive/checkpoint mechanism. API need not manufacture, interpret, or
backfill the artifact. SBE should nevertheless version and test the native
retention surface normally; API's opaque checkpoint archive must continue to
retain the complete workspace/inventory unchanged.

The completed assembly-terminal and creative-retry branches remain valid. Do
not weaken them or emit partial optional-stage packets merely to increase
historical coverage. No API/R2/Better Stack/database/provider mutation or
release work is authorized by this review.
