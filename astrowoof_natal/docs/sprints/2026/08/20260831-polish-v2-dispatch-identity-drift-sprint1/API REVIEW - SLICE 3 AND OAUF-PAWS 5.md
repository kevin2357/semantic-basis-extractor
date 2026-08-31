# API review — Slice 3 and Oauf-paws 5

## Decision

**Approved to begin Slice 4 contract shape and runtime-integration design.**
The provider-free witness reproduces the retained stale-slot failure through the
real v2 commit/dispatch boundaries, preserves the no-successor-create result,
and does not overclaim that a fixture-only cleanup is runtime evidence.

## Scope clarification

The new witness establishes the stale-live-intent counterexample. Its manually
materialized terminal predecessor state is appropriate for this pre-fix proof,
but it does not itself prove that the eventual runtime hook is reached by the
real reconciliation/reporting path. Slice 4 must identify that exact writer
path and the first checkpoint where the complete terminal join is durable.

## Required Slice 4 decisions

1. Name the exact native reconciliation/reporting transition that will validate
   and retire the completed live intent. The implementation must not depend on
   a later generic resume or successor admission in normal new workspaces.
2. Specify the retired record's closed fields and digest inputs: predecessor
   request/grant, ordered actions/provider IDs, terminal-evidence digest,
   retirement revision, and post-checkpoint identity. Do not include prompts,
   response payloads, or other protected subject material.
3. Define the lookup precedence for exact replay versus a fresh successor:
   historical retired record is audit/replay evidence only; a fresh request
   needs a fresh current inspection and cannot borrow predecessor authority.
4. Keep compatibility repair for historical stranded workspaces explicitly
   separate, typed, and fail-closed. It is not a reason to weaken normal
   reconciliation retirement conditions.
5. Retain existing pending/partial/ambiguous/conflicting intent behavior unless
   a separate closed contract establishes a lawful terminal join.

No API contract change is yet indicated. SBE should first determine whether
existing native journal/snapshot structures can express the retired record and
replay proof without inventing a public artifact.
