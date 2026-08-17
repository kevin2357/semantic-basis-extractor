# Slice 1 Contract Freeze

Date: 2026-08-16  
Status: proposed; awaiting Kevin and API-agent review  
Provider operations: 0  
Paid spend: `$0`

## Outcome

The complete proposed contract is published in
[`ROUTE PARITY CONTRACT PROPOSAL.md`](../ROUTE%20PARITY%20CONTRACT%20PROPOSAL.md).
No runtime or packaged schema has changed.

The proposal resolves the planning questions as follows:

- lifecycle inspection advances to v0.3 with strict native route identity,
  per-action provider mechanism/operation binding, and a separate
  consumer-authority projection;
- policy and cycle result advance to v0.2 with route/mechanism summaries;
- one Batch round is one paid action with several non-reservable request members;
- exact Batch polls at most one round with a 40-second provider-I/O bound;
- bounded interactive retains the Responses timing policy;
- route identity includes bounded `route_contract`, fixing the Slice 0 discovery;
- Batch output membership is preflighted atomically before any ingestion;
- bounded continuation consumes cached raw evidence through all actual stages;
- bounded delivery semantics remain ordered rather than inventing a nonblocking
  critic state;
- timing-free 0.4.3 Batch workspaces fail closed without automatic repair;
- bounded Batch stays rejected; and
- unavailable terminal Batch usage is never recorded as zero; it receives a
  billing-reconciliation-pending cost disposition and retains API financial
  authority after provider retrieval custody ends;
- a neutral public dispatcher/CLI name replaces the confusing exact-only flag,
  with a compatibility alias during the patch series.

## Review boundary

This slice intentionally stops before strict packaged schema and fixture mutation.
The approved plan originally listed validation of proposed examples in Slice 1,
but also required API approval before schemas or code. The Slice 0 route-identity
discovery materially affects those shapes, so the safer interpretation is to
freeze prose and exact JSON examples first. After approval, Slice 2 will encode the
accepted examples in strict schemas/fixtures and make them executable contract
tests before runtime dispatch changes.

Current 0.4.3 contract and route-guard regressions passed all 58 tests in 17.575
seconds. The complete repository suite passed all 339 tests in 142.210 seconds.

## Required reviewers

- Kevin: scope, compatibility, bounded route semantics, and timing posture.
- AstroWoof API agent: reservation mapping, worker-claim bounds, result mapping,
  legacy posture, and neutral public seam.

Implementation remains paused until both reviews are reconciled.

## API review reconciliation

The API approved the route matrix, Batch round/member model, timing, bounded-Batch
deferral, and route adapters, subject to two required changes. Both are now
incorporated:

1. inspection v0.3 carries strict native route and per-action mechanism/round
   identity; and
2. terminal Batch usage absence is distinct from real zero usage through an exact
   cost disposition and separate consumer-authority retention projection.

The revised contract awaits Kevin's acceptance and API confirmation before Slice
2 schema/runtime work.

The API subsequently approved all seven review questions. Its final wording
refinement is incorporated: output/member review after terminal provider files are
durable retains consumer authority without falsely retaining provider retrieval
custody or scheduling endless polling.
