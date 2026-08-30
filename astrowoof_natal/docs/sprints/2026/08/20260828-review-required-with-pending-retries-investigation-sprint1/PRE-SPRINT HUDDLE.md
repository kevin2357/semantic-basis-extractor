# Pre-sprint huddle — review-required with pending retries

## Working interpretation

This sprint is an investigation, not a presumed bug fix. The preceding terminal
handoff sprint established that the retained Pippin and Duchess checkpoints are
hash-valid and that neither contains the unsealed `review_required` transition.
SBE 0.4.28 now fixes that publication boundary for exact interactive runs, but it
does not answer whether the original editorial decision was correct.

The remaining question is narrower and more semantic: why did each run reach
`native.review.requires_review` while the API still held creative-retry actions
in reported, provider-bound, and providerless-authorized custody states?

## Guiding distinctions

- Attempt count is not pass lineage. Three creative-retry rows may belong to
  different passes.
- Editorial terminality is not custody finality. A valid review decision can
  coexist with retrieval or providerless-denial cleanup, but cannot authorize
  more creative work.
- API ledger state is not native authoring truth. Both must be joined by exact
  run/action/binding/provider identities.
- A trace is diagnostic evidence, not authority. Snapshot-declared native files,
  sealed public artifacts, and API-owned persisted facts remain authoritative in
  their respective domains.
- Missing terminal bytes must remain missing. The investigation may reconstruct
  a conclusion with a stated confidence level, but must not fabricate or repair
  historical native evidence.

## Current leading explanations

The investigation should remain neutral among at least these explanations:

1. **Valid editorial review with residual custody.** A pass exhausted its allowed
   attempts or final QA found an independently terminal defect. Other retry rows
   remained relevant only to custody cleanup.
2. **Premature final QA or incomplete fan-in.** Review ran while a required retry
   response was still provider-bound or before its durable evidence was joined.
3. **Retry-lineage or successor-selection defect.** A later authorized retry was
   stale, duplicated, attached to the wrong pass/attempt, or prepared after an
   already-terminal editorial decision.
4. **Projection disagreement.** Native state correctly fenced editorial work but
   projected zero provider dependencies while the API still held a durable
   provider identity that native evidence should have recognized.
5. **Evidence loss at the historical failure boundary.** The decisive QA report
   existed only after the retained checkpoint and was never durably published.
   In that case the exact historical cause may remain unknowable, while a
   provider-free reproduction can still validate or refute reachable behaviors.

## Evidence posture

A controlled read-only R2 inspection is justified and likely necessary. It may
read the two exact retained checkpoint archives and their snapshot-declared
authoritative members. It must not resume, reconcile, repair, execute, rewrite,
delete, or submit provider work.

Any extracted report must be sanitized. It may retain hashes, native/action/pass
identities, closed reason codes, attempt numbers, structural counts, and bounded
diagnostic excerpts only where essential. Prompts, authored prose, protected
subject data, credentials, and provider payloads must not enter sprint artifacts.

## Decision posture

The plan deliberately freezes only the investigation slices. Later implementation,
contract, release, or recovery slices are conditional and must be written after
the causal evidence is reviewed. Finding a valid editorial outcome is a successful
sprint result and does not require inventing a patch.
